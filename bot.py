import speech_recognition as sr
import pyttsx3
import json,time
from datetime import datetime
from programmi_appoggio import amazon_scraping as am
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline





def inizializza_bot():
    engine = pyttsx3.init()
    voce_bot = engine.getProperty("voices")
    engine.setProperty("voice", voce_bot[0].id) #lingua italiana
    rate_parole = engine.getProperty('rate')
    engine.setProperty('rate',150)
    return engine


def load_memory_bot(path: str) -> dict:
    "carica il file json con tutte le domande e risposte del bot"
    with open(path,"r") as f:
        data = json.load(f)
    return data



def save_new_questions(data: str, path: str):
    "salva nel file json le nuove domande con le corrispettive risposte"
    with open (path,"w") as f:
        json.dump(data, f, indent=3)



def presentazione(testo: str):
    "stampa lettera per lettera con un ritardo di 5 millisecondi, pura estetica"
    for lettera in testo:
        print(lettera,end="",flush=True)
        time.sleep(0.03) 
   

# sezione preparazione dati machine learning
def prepara_dati(memoria):
    domande = [item["domanda"] for item in memoria["domande"]]
    risposte = [item["risposta"] for item in memoria["domande"]]
    return domande, risposte

def addestramento(domande,risposte):
    model = make_pipeline(TfidfVectorizer(),MultinomialNB())
    model.fit(domande,risposte)
    return model

def predict_risposta(model,nuova_domanda):
    probabilita = model.predict_proba([nuova_domanda])
    risposta = model.predict([nuova_domanda])
    
    probabilita_predict = probabilita[0][model.classes_ == risposta[0]]
    soglia = 0.05
    if probabilita_predict >= soglia:
        return risposta[0]
    else:
        return ""





def bot():
    
    riconoscimento_vocale = sr.Recognizer()
    
        
    #carico memoria
    memory = load_memory_bot("botVocale/memoria/memoria.json")
    domande, risposte = prepara_dati(memory)
    model = addestramento(domande,risposte)
    
    #inizializzo bot
    engine = inizializza_bot()
    engine.say("Ciao sono Jarvis,un ChatBot, come posso aiutarti? Se vuoi uscire di' esci\n")
    print("Ciao sono Jarvis, come posso aiutarti? Se vuoi uscire di' esci")
    engine.runAndWait()
    
    
    
    while True:
        
        with sr.Microphone() as source:
            print("Parla: ")
            audio = riconoscimento_vocale.listen(source, phrase_time_limit=2)
        
        try:
            testo = riconoscimento_vocale.recognize_google(audio, language="it-IT")
            print(f"\nTu: {testo}")
        except sr.UnknownValueError:
            engine.say("Non riesco a capire l'audio")
            engine.runAndWait()
            continue
        except sr.RequestError:
            engine.say("Errore nella richiesta al servizio di riconoscimento vocale")
            engine.runAndWait()
            continue
            
        #uscita
        if testo.lower() == "esci":
            break
        
        # comandi personalizzati, es ore, ricerca su amazon, ecc
        if testo.lower() == "che ore sono":
            ora = datetime.now().strftime("%H:%M:%S")
            engine.say(f"Sono le {ora}")
            print(f"\nJarvis: Sono le {ora}")
            engine.runAndWait()
            continue
        #ricerca amazon
        elif testo.lower() in ["fai una ricerca su amazon","cerca su amazon"]:
            engine.say("Cosa vuoi che ti cerchi?")
            print("Jarvis: Cosa vuoi che ti cerchi?")
            engine.runAndWait()
            
            with sr.Microphone() as source:
                print("\nParla: ")
                audio = riconoscimento_vocale.listen(source)
            
            try:
                testo = riconoscimento_vocale.recognize_google(audio, language = "it-IT")
                print(f"\nTu: {testo}")
                risultato = am.cerca_oggetto(testo)
                engine.say(f"Ho trovato {risultato} risultati, per il prodotto {testo}, controlla il file nella cartella risultato")
                print(f"Jarvis: Ho trovato {risultato} risultati, per il prodotto {testo}, controlla il file nella cartella risultato")
                engine.runAndWait
                continue
            except sr.UnknownValueError:
                engine.say("Non riesco a capire l'audio")
                engine.runAndWait()
                continue
            except sr.RequestError:
                engine.say("Errore nella richiesta al servizio di riconoscimento vocale")
                engine.runAndWait()
                continue

        
        #risposta tramite predict e json
        risposta = predict_risposta(model,testo.lower())
        # bot risponde
        if risposta:
            engine.say(f"{risposta}")
            print(f"Jarvis: {risposta}\n")
            engine.runAndWait()
               
        else: #nel caso non sa come rispondere gli andiamo a "dire" la risposta
            engine.say("Scusa ma non so la risposta, se me la dicessi  potrei aiutarti in futuro, dimmi la risposta o dimmi 'no'")
            print("\nJarvis: Scusa ma non so la risposta, se me la dicessi  potrei aiutarti in futuro, dimmi la risposta o dimmi 'no'\n")
            engine.runAndWait()
            print("Parla: ")
            
            with sr.Microphone() as source:
                audio = riconoscimento_vocale.listen(source,phrase_time_limit=2)
            try:
                nuova_risposta = riconoscimento_vocale.recognize_google(audio)
                print(f"\nTu: {nuova_risposta}")
            except sr.UnknownValueError:
                engine.say("Non riesco a capire l'audio")
                engine.runAndWait()
                continue
            except sr.RequestError:
                engine.say("Errore nella richiesta al servizio di riconoscimento vocale")
                engine.runAndWait()
                continue
            
                
            if nuova_risposta.lower() != "no":
                #aggiorniamo le domande/risposte
                memory["domande"].append({"domanda": testo, "risposta" : nuova_risposta})
                #salviamo
                save_new_questions(memory, "botVocale/memoria/memoria.json")
                engine.say("Grazie! Ho imparato una nuova cosa")
                print("Jarvis: Grazie! Ho imparato una nuova cosa")
                engine.runAndWait()
                
                #riaddestra modello
                domande, risposte = prepara_dati(memory)
                model = addestramento(domande,risposte)

    
    engine.say("Ciao alla prossima!")
    engine.runAndWait()
     
            
        

        
if __name__ == "__main__":
    bot()
