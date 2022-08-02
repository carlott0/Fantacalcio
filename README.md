# Fantacalcio
Assistente guida per l'asta iniziale del fantacalcio. 

![image](https://user-images.githubusercontent.com/49305804/181594220-3f284deb-dfa2-4e1f-b953-54d10f2afd32.png)


AGGIORNAMENTO:
Puoi scaricare lo zip con l'eseguibile .exe direttamente da qui:
https://www.mediafire.com/file/a7zi477oxqflxn5/Fantacalcio.zip/file

Requirements:

Python3

Install requirements:

pip3 install -r requirements.txt

Per far sì che l'applicazione funzioni, è necessario avere a disposizione gli excel nella cartella "excel". Ovvero: "calendario.xlsx", "classifica.xlsx", "giocatori.xlsx, "Quotazioni_Fantacalcio.xlsx".

In pratica per funzionare bisogna sapere il calendario, la classifica dell'anno precedente (le neopromosse dalla B alla A dovranno essere sostituite con le retrocesse in B), i giocatori con le rispettive quotazioni. Tutti questi dati solitamente sono ottenibili online a inizio campionato.

Nel momento in cui sto testando il programma ottiene tali file autonomamente, ma al momento del nuovo anno di fanta potrebbe esserci qualche problema, in caso importare a mano gli excel. 
#EDIT Il download del calendario dà problemi, usare quello già a disposizione o inserire a mano.

![test3](https://user-images.githubusercontent.com/49305804/181827179-36659d72-d16b-407a-be15-bcfd9db3bf7b.png)

Ottimizzato per budget 500 crediti. Se si vogliono cambiare bisogna modificare il valore nel file crediti.txt, e inserire una diversa funzione prezzo all'interno dei file xlsx della cartella '/Funzione Prezzo/', poiché la previsione del prezzo sulla base della quotazione iniziale si basa su 500 crediti (esempio: immobile quotazione 40 il prezzo reale sarà sui 180 circa su 500, 250 sui 800 (?) e 350 sui 1000 (??)).

Nei file nella cartella src verranno salvati i giocatori comprati, nel file crediti.txt è possibile modificare i pesi di ogni ruolo, cioè i prezzi massimi che si vuole spendere per un reparto.
A default i portieri su 500 crediti costano il 3%, ovvero 15 crediti, i difensori 35 su 500 (7%), i centrocampisti 100 su 500(20%), e gli attaccanti 350 su 500 (70%).

Per avviare il programma eseguire il comando python3 fantacalcio.py e seguire le istruzioni che seguono di volta in volta. Il progamma ogni volta che viene chiamato un giocatore crea un possibile reparto e dice il prezzo probabile di quel giocatore, oltre a altri dati come i gol fatti l'anno precedente, l'indice di titolarietà e se si tratta di un rigorista.
![test5](https://user-images.githubusercontent.com/49305804/181827213-6a3eaca4-9647-476b-ad72-240170dd948b.png)

La cartella 'old lega' contiene gli excel con i valori del mio fanta della scorsa asta, per ogni reparto contiene il prezzo di partenza e il prezzo a cui è andato ogni giocatore. Viene poi usato per migliorare la stima del prezzo dei giocatori di quest'anno. Se non si vuole usare questa funzione cancellare semplicemente la cartella 'old lega'. 
![test4](https://user-images.githubusercontent.com/49305804/181827204-32548b52-117e-4143-bc03-4f73b1781512.png)


Per ogni giocatore che viene chiamato si consiglia di inserire il prezzo a cui viene venduto, anche se non lo abbiamo comprato, poiché i valori vengono usati per determinare meglio il prezzo probabile dei prossimi giocatori (es. se durante l'asta i giocatori vanno via a poco, il sistema abbassa i prezzi probabili).  

La cartella indice viene caricata dinamicamente all'inizio e contiene l'indice di titolarietà dei giocatori.

La cartella categorie contiene le fasce in cui ogni giocatore si trova (manca da aggiornare gli attaccanti).
La cartella infortunii contiene due file, in cui vi sono gli infortunati e gli squalificati (quest'ultimi viene indicato anche quante giornate).

Ho vinto 2 fantacalci di fila con questo metodo, il primo era un fanta a 12 il secondo fanta a 10.

In realtà nell'ultimo fanta avevo speso 400 crediti su 500 (80%), ma la squadra non era equilibrata.

Se sono presenti bug o desideri dei chiarimenti, scrivimi.

@author: carlotto
