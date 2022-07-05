# Fantacalcio
Assistente guida per l'asta iniziale del fantacalcio 

Per far sì che l'applicazione funzioni, è necessario avere a disposizione gli excel nella cartella "excel". Ovvero: "calendario.xlsx", "classifica.xlsx", "giocatori.xlsx, "Quotazioni_Fantacalcio.xlsx".

In pratica per funzionare bisogna sapere il calendario, la classifica dell'anno precedente, i giocatori con le rispettive quotazioni. Tutti questi dati solitamente sono ottenibili online a inizio campionato.

Nel momento in cui sto testando il programma ottiene tali file autonomamente, ma al momento del nuovo anno di fanta potrebbe esserci qualche problema, in caso importare a mano gli excel.

Ottimizzato per budget 500 crediti. Se si vogliono cambiare bisogna modificare il valore nel file crediti.txt, e inserire una diversa funzione prezzo all'interno del codice fantacalcio.py, poiché la previsione del prezzo sulla base della quotazione iniziale si basa su 500 crediti (esempio: immobile quotazione 40 il prezzo reale sarà sui 180 circa su 500, 250 sui 800 (?) e 350 sui 1000 (??)).

Nei file nella cartella src verranno salvati i giocatori comprati, nel file crediti.txt è possibile modificare i pesi di ogni ruolo, cioè i prezzi massimi che si vuole spendere per un reparto.
A default i portieri su 500 crediti costano il 3%, ovvero 15 crediti, i difensori 35 su 500 (7%), i centrocampisti 100 su 500(20%), e gli attaccanti 350 su 500 (70%).

Per avviare il programma eseguire il comando python3 fantacalcio.py e seguire le istruzioni che seguono di volta in volta. Il progamma ogni volta che viene chiamato un giocatore crea un possibile reparto e dice il prezzo probabile di quel giocatore.


Ho vinto 2 fantacalci di fila con questo metodo, il primo era un fanta a 12 il secondo fanta a 10.

In realtà nell'ultimo fanta avevo speso 400 crediti su 500 (80%), ma la squadra non era equilibrata.


Se sono presenti bug o desideri dei chiarimenti, scrivimi.

A breve aggiungerò anche i rigoristi.

@author: carlotto
