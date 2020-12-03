# Explanations Food RecSys

Il sistema è costituito dal servizio Recommender, dal servizio Explanations e dalla web application.
La cartella "foodWebApp" contiene i servizi Recommender ed Explanations.
La cartella "foodrecsys2.1" contiene la web application "Rec Sys".
La cartella "foodRecExp" contiene la web application "Rec Exp".


## Installazione

Prima di avviare i servizi assicurati di utilizzare Python 3 e installa il microframework flask con il seguente comando

```bash
    pip install flask flask-restful pandas
```

## Servizio Recommender

Per avviare il Recommender esegui il comando

```bash
    ./start_server.sh 
```

Per arrestare il Recommender esegui il comando

```bash
    ./stop_server.sh 
```

Per ulteriori informazioni sul servizio, leggi la documentazione del repo [FoodRecSys2020](https://github.com/swapUniba/FoodRecSys2020).


##Servizio Explanations

Per avviare il Explanations esegui il comando

```bash
    ./start_expl_server.sh 
```

Per arrestare il Recommender esegui il comando

```bash
    ./stop_expl_server.sh 
```

All'interno del codice, potrai notare (nel main) alcuni array di stringhe contenenti i nomi delgli stili di spiegazione.
Ci sono gli array con tutti i nomi identificativi degli stili implementati, e quelli utilizzati per la configurazione attuale del sistema. 
Il servizio gira sulla porta 5003. Il servizio costruisce un JSON contenente nome dello stile e relativa spiegazione, per ciascuno stile. Il JSON è mandato alla web application tramite il protocollo HTTP.


## Web Application "Rec Exp"

I linguaggi utilizzati per il suo sviluppo sono stati PHP, HTML5 e CSS.

Essa è articolata in 5 pagine principali:

    1)index.html, pagina di presentazione del sistema e del suo funzionamento;
    2)form.html, pagina di inserimento delle informazioni dell’utente, che saranno utilizzate dal recommender e dall'explanations service;
    3)recipes.php, pagina  che ha il compito di creare il profilo utente elaborando le informazioni ottenute, di richiedere i servizi del food recommender system ed explanations e di visualizzare i risultati all’utente con o senza spiegazione. Per una questione di organizzazione e migliore modularità del sistema si è previsto un modulo PHP esterno da includere e da cui richiamare le funzioni più complesse che eseguono i compiti appena descritti (/php/requestFunctions.php).
    4)bye.php, pagina  che ha il compito di memorizzare i risultati dell’esperimento nel log dei risultati (/results/explResults.csv) e di comunicare all’utente la conclusione dell’esperimento senza errori.


In questa configurazione la web app mostra sempre la spiegazione.
Gli stili utilizzati sono quelli presenti nel codice e sono tutti di livello doppio, ossia spiegazioni con confronto tra due ricette.


## Web Application "Rec Sys"

La web application "Rec Sys" si differenzia dalla precedente in quanto per ogni utilizzo è generato random un valore (variabile ShowExpl in form.php).
Tale valore stabilisce se la configurazione è senza spiegazione, con spiegazione di livello singolo, oppure con spiegazione di livello doppio.