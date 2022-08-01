##################################
#### Author Carlo Maria Conti ####
##################################
import pandas as pd
import numpy as np
import random
import os.path
from os import path
from bs4 import BeautifulSoup
import os
import urllib.request
from requests_html import HTMLSession
import os, errno
from tabulate import tabulate
from termcolor import colored
import requests
#from pyfiglet import Figlet
import json



def getInfortunati():
    session = HTMLSession()
    session.headers.update({
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
                "Connection":"close"
    })
    l="https://sosfanta.calciomercato.com/tabella-indisponibili-tutti-gli-infortunati-e-i-tempi-di-recupero-verso-lasta-da-chiesa-a-lovato/"
    r=session.get(l)
    soup= BeautifulSoup(r.content, "html.parser")
    infortunati=[]
    squalificati=[]
    for el in soup.find("div",{"class":"entry-content"}).find_all("strong"):
        if el.text.isupper():
            continue
        if str(el).count("<")>2:
            continue
        if '"' in str(el):
            continue
        for c in el.text:
            if c.strip().isupper() :
                if "("  in el.text:
                    squalificati.append(el.text.upper())
                else:
                    infortunati.append(el.text.upper())
    if not path.exists("./infortunii/"):
        os.makedirs("./infortunii/")
    with open("./infortunii/infortunati.txt","w") as w:
        for el in infortunati:
            w.write(el)
            w.write("\n")
    w.close()
    with open("./infortunii/squalificati.txt","w") as w:
        for el in squalificati:
            w.write(el)
            w.write("\n")
    w.close()    

def pertit():
    session = HTMLSession()
    session.headers.update({
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
                'Connection':'close'
    })
    l="https://www.fantacalcio.it/probabili-formazioni-serie-a"
    r=session.get(l)
    soup= BeautifulSoup(r.content, "html.parser")  
    session.close()
    
    l=soup.find_all("ul",{"class":"player-list starters"})
    titolari={}
    for el in l:
        giocatori=el.find_all("a",{"class":"player-name player-link"})
        progress=el.find_all("div",{"class":"progress-value"})
        gtemp=[]
        ptemp=[]
        for g in giocatori:
            gtemp.append(g.text.strip().upper())
        for p in progress:
            ptemp.append(p.text.strip().upper())
        i=0
        for i in range(0,len(gtemp)):
            titolari[gtemp[i]]=ptemp[i]
    l2=soup.find_all("ul",{"class":"player-list reserves"})
    riserve={}
    for el in l2:
        giocatori=el.find_all("a",{"class":"player-name player-link"})
        progress=el.find_all("div",{"class":"progress-value"})
        gtemp=[]
        ptemp=[]
        for g in giocatori:
            gtemp.append(g.text.strip().upper())
        for p in progress:
            ptemp.append(p.text.strip().upper())
        i=0
        for i in range(0,len(gtemp)):
            riserve[gtemp[i]]=ptemp[i]
        
    if not path.exists("./indice/"):
        os.makedirs("./indice/")
    with open("./indice/titolari.txt","w") as w:
        for el in titolari.keys():
            b=el+":"+titolari[el]
            w.write(b)
            w.write("\n")
    w.close()
    with open("./indice/riserve.txt","w") as w:
        for el in riserve.keys():
            b=el+":"+riserve[el]
            w.write(b)
            w.write("\n")
    w.close()

def lista_portieri():
    try:
        session = HTMLSession()
        session.headers.update({
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
                    'Connection':'close'
        })
        l="https://sosfanta.calciomercato.com/portieri-ecco-la-guida-allasta-fascia-per-fascia-su-chi-puntare-dai-top-fino-ai-low-cost/"
        r=session.get(l)
        soup= BeautifulSoup(r.content, "html.parser")  
        session.close()
        cat={}
        g=""
        l=soup.find("div",{"class":"entry-content"}).find_all("p")
        for el in l:
            if "–" in el.text:
                try:
                    c=el.text.split("–")[0]

                    g=el.text.split("–")[1].split("\n")[0]
                    cat[c]=g
                except:
                    continue
        fin=[]
        dael=[]
        for c in cat:
            g=cat[c]
            if not c.isupper():
                dael.append(c)
                continue
            if "," not in g:
                fin.append(g)
                cat[c]=list(np.unique(fin))
                fin=[]
                continue
            gx=g.split(",")
            for el in gx:
                if len(gx)<2:
                    continue
                for e in gx:
                    fin.append(e)
            cat[c]=list(np.unique(fin))
            fin=[]
        for el in dael:
            del cat[el]

        return cat
    except:
        return {}
def lista_difensori():
    try:
        session = HTMLSession()
        session.headers.update({
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
                    'Connection':'close'
        })
        l="https://sosfanta.calciomercato.com/difensori-ecco-la-guida-allasta-chi-prendere-al-fantacalcio-la-divisione-in-fasce/"
        r=session.get(l)
        soup= BeautifulSoup(r.content, "html.parser")  
        session.close()
        cat={}
        g=""
        l=soup.find("div",{"class":"entry-content"}).find_all("p")
        for el in l:
            if "–" in el.text:
                try:
                    c=el.text.split("–")[0]

                    g=el.text.split("–")[1].split("\n")[0]
                    cat[c]=g
                except:
                    continue
        fin=[]
        dael=[]
        for c in cat:
            g=cat[c]
            if not c.isupper():
                dael.append(c)
                continue
            if "," not in g:
                fin.append(g)
                cat[c]=list(np.unique(fin))
                fin=[]
                continue
            gx=g.split(",")
            for el in gx:
                if len(gx)<2:
                    continue
                for e in gx:
                    fin.append(e)
            cat[c]=list(np.unique(fin))
            fin=[]
        for el in dael:
            del cat[el]
        return cat
    except:
        return {}
def lista_centrocampisti():
    try:
        session = HTMLSession()
        session.headers.update({
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
                    'Connection':'close'
        })
        l="https://sosfanta.calciomercato.com/centrocampisti-ecco-la-guida-allasta-dai-top-fino-ai-low-cost-su-chi-puntare-al-fanta/"
        r=session.get(l)
        soup= BeautifulSoup(r.content, "html.parser")  
        session.close()
        cat={}
        g=""
        l=soup.find("div",{"class":"entry-content"}).find_all("p")
        for el in l:
            if "–" in el.text:
                try:
                    c=el.text.split("–")[0]

                    g=el.text.split("–")[1].split("\n")[0]
                    cat[c]=g
                except:
                    continue
        fin=[]
        dael=[]
        for c in cat:
            g=cat[c]
            if not c.isupper():
                dael.append(c)
                continue
            if "," not in g:
                fin.append(g)
                cat[c]=list(np.unique(fin))
                fin=[]
                continue
            gx=g.split(",")
            for el in gx:
                if len(gx)<2:
                    continue
                for e in gx:
                    fin.append(e)
            cat[c]=list(np.unique(fin))
            fin=[]
        for el in dael:
            del cat[el]
        return cat
    except:
        return {}
def lista_attaccanti():

    try:
        session = HTMLSession()
        session.headers.update({
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
                    'Connection':'close'
        })
        l="https://sosfanta.calciomercato.com/attaccanti-ecco-la-guida-allasta-chi-prendere-dai-top-player-fino-agli-ultimi-slot/"
        r=session.get(l)
        soup= BeautifulSoup(r.content, "html.parser")  
        session.close()
        cat={}
        g=""
        l=soup.find("div",{"class":"entry-content"}).find_all("p")
        for el in l:
            if "–" in el.text:
                try:
                    c=el.text.split("–")[0]

                    g=el.text.split("–")[1].split("\n")[0]
                    cat[c]=g
                except:
                    continue
        fin=[]
        dael=[]
        for c in cat:
            g=cat[c]
            if not c.isupper():
                dael.append(c)
                continue
            if "," not in g:
                fin.append(g)
                cat[c]=list(np.unique(fin))
                fin=[]
                continue
            gx=g.split(",")
            for el in gx:
                if len(gx)<2:
                    continue
                for e in gx:
                    fin.append(e)
            cat[c]=list(np.unique(fin))
            fin=[]
        for el in dael:
            del cat[el]
        return cat
    except:
        return {}
def rigoristi():
    try:
        link="https://www.fantamaster.it/rigoristi-tiratori-seriea-2022-2023-consigli-fantacalcio/"
        session = HTMLSession()
        session.headers.update({
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
                    'Connection':'close'
        })
        r=session.get(link)
        soup= BeautifulSoup(r.content, "html.parser")
        buff=""
        for el in soup.find("div",{"class":"td-post-content tagdiv-type"}).find_all("ul"):
            if "RIGORISTI" in el.text and "PUNIZIONI" in el.text:
                buff+=(el.text.split("RIGORISTI: ")[1].split("PUNIZIONI:")[0])+", "
        lista=[]
        for el in buff.split(","):
            if el.strip()=='':
                continue    
            lista.append(el.strip().upper())
        #return lista
        link="https://sosfanta.calciomercato.com/ecco-tutti-i-rigoristi-squadra-per-squadra-gerarchie-e-novita-per-la-stagione-2022-23/"
        session = HTMLSession()
        session.headers.update({
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
                    'Connection':'close'
        })        
        r=session.get(link)
        soup= BeautifulSoup(r.content, "html.parser")
        lista2=[]
        for el in soup.find("div",{"class","entry-content"}).find_all("strong"):
            if el.text.strip().isupper() or not el.text.strip()[0].isupper() or el.text.strip()=="Condividi su":
                continue
            lista2.append(el.text.strip().upper())
        listafin=list(np.unique(lista+lista2))
        return listafin     
        
    except:
        return []
       

def calcola_calendario():
    #hanno disabilitato il sito, usare l'excel fornito da me o inserire a mano
    try:
        link="https://www.fantacalcio.it/Servizi/Excel.ashx?type=3&t=1657102506000"
        data = pd.read_excel(link, header=1)
        giornate_dispari=data['Unnamed: 0']
        giornate_pari=data['Unnamed: 3']
        g_sinistra=[]
        for i in np.arange(1,len(giornate_dispari),1):
            if type(giornate_dispari[i]) != float:
                if "Giornata" not in giornate_dispari[i]:
                    g_sinistra.append(giornate_dispari[i])
        g_destra=[]
        for i in np.arange(1,len(giornate_pari),1):
            if type(giornate_pari[i]) != float:
                if "Giornata" not in giornate_pari[i]:
                    g_destra.append(giornate_pari[i])
        new_calendario=pd.DataFrame()
        g=g_sinistra + g_destra
        i_giornata=0
        new_g=np.array_split(g, 380)
        new_calendario=pd.DataFrame()
        g=g_sinistra + g_destra
        i_giornata=1
        new_g=np.array_split(g, 38)
        for el in new_g:
            new_calendario['Giornata '+str(i_giornata)]=el
            i_giornata+=1
        new_calendario.to_excel('./excel/calendario.xlsx')
        return 0
    except:
        return 1
def calcola_classifica():
    try:    
        session = HTMLSession()
        session.headers.update({
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
        })
        link="https://www.repubblica.it/sport/dirette/calcio/serie-a-2021/classifica/"
        r=session.get(link)
        soup= BeautifulSoup(r.content, "html.parser")
        numeri="1 2 3 4 5 6 7 8 9 0".split(" ")
        squadre=[]
        for div in soup.find_all("tr",{"class":"as21-classifica-table-tr"}):
            s=str(div.text).replace(" ","").replace("\n","")
            squadra=""
            for c in s:
                if c not in numeri:
                    squadra+=c
            squadre.append(squadra.upper())

        
        link="https://www.repubblica.it/sport/dirette/calcio/serie-a-2022/classifica/"
        r=session.get(link)
        soup= BeautifulSoup(r.content, "html.parser")
        numeri="1 2 3 4 5 6 7 8 9 0".split(" ")
        squadre2=[]
        for div in soup.find_all("tr",{"class":"as21-classifica-table-tr"}):
            s=str(div.text).replace(" ","").replace("\n","")
            squadra=""
            for c in s:
                if c not in numeri:
                    squadra+=c
            squadre2.append(squadra.upper())

        retrocesse=list(set(squadre) - set(squadre2))
        nuove=list(set(squadre2) - set(squadre))
        i=0
        for el in squadre:
            if el in retrocesse:
                squadre=[item.replace(el, nuove[i]) for item in squadre]
                i+=1
                
        df=pd.DataFrame(squadre, columns=["SQUADRE"])
        df.to_excel('./excel/classifica.xlsx')
        
        return 0
    except:
        return 1
        
        
def ottieniVal(ruoli,qa):

    i=0
    try:
        w=pd.read_excel("./Funzioni Prezzo/difensori.txt", names=['Valore Nominale','Prezzo Asta'])
        d1=w['Valore Nominale']
        d2=w['Prezzo Asta']
    except:
        d1 = [1,5,10,15,20,25,30]
        d2 = [1,10,15,20,30,40,50]
    
    
    
    
    
    try:
        w=pd.read_excel("./Funzioni Prezzo/centrocampisti.txt", names=['Valore Nominale','Prezzo Asta'])
        c1=w['Valore Nominale']
        c2=w['Prezzo Asta']
    except:
        c1 = [1,5,10,15,20,25,30,35]
        c2 = [1,10,20,30,35,40,50,60]
        
    
    
    
    try:
        w=pd.read_excel("./Funzioni Prezzo/attaccanti.txt", names=['Valore Nominale','Prezzo Asta'])
        a1=w['Valore Nominale']
        a2=w['Prezzo Asta']
    except:
        a1 = [1,5,10,15,20,25,30,35,40,45]
        a2 = [1,10,30,40,50,70,110,140,160,200]
    

    
    
    ris=[]
    for el in ruoli:
        p=int(qa[i])
        if el=="D":
            a,b,c = np.polyfit(d1, d2, 2)
            prezzo_probabile=int(a*p*p+b*p+c)
        elif el=="C":
            a,b,c = np.polyfit(c1, c2, 2)
            prezzo_probabile=int(a*p*p+b*p+c)
        elif el=="A":
            a,b,c = np.polyfit(a1, a2, 2)
            prezzo_probabile=int(a*p*p+b*p+c)
        else:
            prezzo_probabile=p
        ris.append(prezzo_probabile)
        i+=1
    return ris

        
def calcola_quotazioni():
    try:
        link="https://www.fantacalcio.it/api/v1/Excel/prices/17/1"
        
        
        headers={
        "authority": "www.fantacalcio.it",
        "method": "GET",
        "path": "/api/v1/Excel/prices/17/1",
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "it,en-US;q=0.9,en;q=0.8,it-IT;q=0.7",
        "cookie": "addtl_consent=1~39.4.3.9.6.9.13.6.4.15.9.5.2.7.4.1.7.1.3.2.10.3.5.4.21.4.6.9.7.10.2.9.2.18.7.6.14.5.20.6.5.1.3.1.11.29.4.14.4.5.3.10.6.2.9.6.6.4.5.4.4.29.4.5.3.1.6.2.2.17.1.17.10.9.1.8.6.2.8.3.4.142.4.8.42.15.1.14.3.1.8.10.25.3.7.25.5.18.9.7.41.2.4.18.21.3.4.2.1.6.6.5.2.14.18.7.3.2.2.8.20.8.8.6.3.10.4.20.2.13.4.6.4.11.1.3.22.16.2.6.8.2.4.11.6.5.33.11.8.1.10.28.12.1.3.21.2.7.6.1.9.30.17.4.9.15.8.7.3.6.6.7.2.4.1.7.12.13.22.13.2.12.2.10.5.15.2.4.9.4.5.4.7.13.5.15.4.13.4.14.8.2.15.2.5.5.1.2.2.1.2.14.7.4.8.2.9.10.18.12.13.2.18.1.1.3.1.1.9.25.4.1.19.8.4.5.3.5.4.8.4.2.2.2.14.2.13.4.2.6.9.6.3.4.3.5.2.3.6.10.11.6.3.16.3.11.3.1.2.3.9.19.11.15.3.10.7.6.4.3.4.6.3.3.3.3.1.1.1.6.11.3.1.1.11.6.1.10.5.2.6.3.2.2.4.3.2.2.7.15.7.12.2.1.3.3.4.5.4.3.2.2.4.1.3.1.1.1.2.9.1.6.9.1.5.2.1.7.2.8.11.1.3.1.1.2.1.3.2.6.1.12.5.3.1.3.1.1.2.2.7.7.1.4.1.2.6.1.2.1.1.3.1.1.4.1.1.2.1.8.1.7.4.3.2.1.3.5.3.9.6.1.15.10.28.1.2.2.12.3.4.1.6.3.4.7.1.3.1.1.3.1.5.3.1.3.2.2.1.1.4.2.1.2.1.2.2.2.4.2.1.2.2.2.4.1.1.1.2.2.1.1.1.1.2.1.1.1.2.2.1.1.2.1.2.1.7.1.2.1.1.1.2.1.1.1.1.2.1.1.3.2.1.1.8.1.1.1.5.2.1.6.5.1.1.1.1.1.2.2.3.1.1.4.1.1.2.2.1.1.4.3.1.2.2.1.2.1.2.3.1.1.2.4.1.1.1.5.1.3.6.3.1.5.2.3.4.1.2.3.1.4.2.1.2.2.2.1.1.1.1.1.1.11.1.3.1.1.2.2.5.2.3.3.5.1.1.1.4.2.1.1.2.5.1.9.4.1.1.3.1.7.1.4.5.1.7.2.1.1.1.2.1.1.1.4.2.1.12.1.1.3.1.2.2.3.1.2.1.1.1.2.1.1.2.1.1.1.1.2.1.3.1.5.1.2.4.3.8.2.2.9.7.2.3.2.1.4.6.1.1.6.1.1; euconsent-v2=CPb8hAAPb8hAAAKAqAITCXCsAP_AAH_AABCYI4Nd_X__bX9j-_5_6ft0eY1f9_r37uQzDhfNs-8F3L_W_LwX32E7NF36pq4KmR4Eu3LBIQNlHMHUTUmwaokVrzHsak2cpyNKJ7JEknMZe2dYGF9Pn9lD-YKY7_5_9_b52T-9_9_-39T3_8ff__dp_2__-vDfV599jfn9fV_789KP___9v__8__________38EbwCDARAIACDBABAAAACEAAEAAkAIAAAAQAAUASADgoAAhYBAACEAAgESEIAAIAQEAMAAAEEACQAIAQAsEAgAAgEAAIAAQAAABAQAAwAkBAAAAACQgQAgABAgIAgAAOQgACgAggBCAQAACiQwAgDrOAAAQQIVAACSQEAgAAQsDAcACAlYkABSAAoAAhBCgFEAkJBZAAQAAuACgAKgAZAA5AB4AIAAYQA0ADUAHkAQwBFACYAE8AKoAbwA5gB6AD8AISAQwBEgCOAEsAJoAUoAtwBhgDIAGWANUAbIA74B7AHxAPsA_YB_gIGARSAi4CMQEaARwAlIBQQCngFXALmAYoA0QBrADaQG4AbwA4gB6AD5AIdARCAkQBMQCZQE2AJ2AUOApEBTQCxQFoALYAXIAu8BeYDBgGGwMjAyQBk4DLgGcgM-AaQA06BrAGsgNvAbqA4KByYHKAOXAdYA8cB7QEIQIXgQ9Ah-BEMCKRKCAAAgABYAFAAMgAcAA_ADAAMQAeABEACYAFUALgAYgAzABtgEMARIAjgBRgClAFuAMIAZQA1QBsgDvAH4ARgAjgBJwCngFXgLQAtIBdQDFAG4AOoAfIBDoCKgEXgJEATYAsUBbAC7QF5gMjAZOAywBnIDPAGfANIAawA28BwADrAHtAQPAgkBC8CGoEPQIsjoNwAC4AKAAqABkADkAHwAgABdADAAMYAaABqADwAH0AQwBFACYAE8AKsAXABdADEAGYAN4AcwA9AB-gEMARIAjoBLAEwAJoAUYApQBYgC3gGEAYcAyADKAGiANkAd4A9oB9gH6AP8AgcBFAEYgI4AjsBKQEqAKCAU8Aq4BYoC0ALTAXMBdYC8gL0AYoA2gBuADiAHUAPQAh0BEICKgEXwJBAkQBKgCZAE2AJ2AUOApoBVgCxQFoALYAXAAuQBdoC7wF5gL6AYMAw0BjADHoGRgZIAycBlUDLAMuAZmAzkBnwDRIGkAaSA0sBpwDVQGsANvAbqA4uByYHKAOXAdYA8cB6QD2gH1gQBAgkBBoCDwELwIdAQ9AikQghAALAAoABkAFwAMQAagBDACYAFMAKoAXAAxABmADeAHoARwApQBYgDCAGUAO8AfYA_wCKAEYAI4ASmAoIChgFPAKvAWgBaQC5gGKANoAdQA9ACIYEggSIAk4BKgCbAFNALFAWiAtgBcAC5AF2gMjAZOAzkBngDPgGiANJAaWA1UBwADlAHWAPHAgkBCgCF4EOgIelIKYAC4AKAAqABkADkAHwAggBgAGMANAA1AB5AEMARQAmABPACkAFUAMQAZgA5gB-gEMARIAowBSgCxAFuAMIAZQA0QBqgDZAHfAPsA_QCLAEYgI4AjoBKYCggKGAVcArYBcwC8gGKANoAbgA9ACHQEXgJEAScAmwBOwChwFigLQAWwAuABcgC7QF5gL6AYaAxiBkYGSAMngZYBlwDOQGeAM-gaQBpMDWANZAbeA3UBwUDkwOUAcuA6wB4oDxwHtAQhAheBDMCHQEPQIgARSFQGQAKABDACYAFwARwAywCMAEcAKvAWgBaQDeAJBATEAmwBTYC2AFyALzAZGAzkBngDPgG5AOUAheMgLABDACYAI4AZYA-wCMAEcAKuAVsA3gCTgExAJsAWiAtgBeYDIwGcgM8AZ8A5QCF4aA-AFwAQwAyABlgDZAH4AQAAgoBGACngFXgLQAtIBrADeAHVAPkAh0BFQCRAE2AJ2AUiAuQBjADIwGTgM5AZ4Az4BygDrBEBgAQwAyABlgDZAH4AQAAjABTwCrgGsAOqAfIBDoCRAE2AJ2AUiAuQBkYDJwGcgM-AcoA6wA.f_gAAAAAAAAA; fanta_web_sign=value; fantacalcio.it=Ccazmp6ks930QjnK3WWkcia4Co99jgjt%2BqRLsOyS4QF71Y5H4byIRx63kVyztFKqOkEijfDQY0nC%2FeayQVh3Gd6CVndjnD3TDxADNyxFTRjUfQCyQ6yJq3Z713OLOAMRF0HBJlp3WQPg%2Fwp2Dr%2BdSiVJw%2FDlE9clGjVqNDzWOjpdLezQBslXTBse85hfujGPD9Qiq52fUTzplMzdgyGag8qYlPa%2FXbJHSB0fqQJpZpvbFqGHqmcomRj4kWSCz8cvr%2F6yDSCo1Yd9kR4mv5V0p32WCbRtnS0N5sfpxVBLG1czgUJXpezNauQF3CT2a2Og84uinzAWqeSRaH8XK%2Bv81SaGqp8GnmFQQ1CScVdoinKLR4Br9EudzjwaFJi0Y5D3%2FqOgJJ2CZ98WyB2Y7HovnI%2BCnr7r7HWH%2F%2BagHEBd%2BU3BXQelfEQCvH44Qg6owRdb8mavIik8G1vY%2BeHMz17CDA%3D%3D;",
        "dnt": "1",
        "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "service-worker-navigation-preload": "true",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        'Connection':'close'}
        
        
        
        
        r=requests.get(link, headers=headers)
        output = open('./excel/q.xlsx', 'wb')
        output.write(r.content)
        output.close()

        
        
        
        data = pd.read_excel("./excel/q.xlsx", header=1)
        new=pd.DataFrame()
        new['Id']=data['Id']
        new['R']=data['R']
        new['Nome']=data['Nome']
        new['Squadra']=data['Squadra']
        new['Qt. A']=data['Qt.A']
        new['Qt. I']=data['Qt.I']
        lista=ottieniVal(data['R'],data['Qt.A'])
        new['VAL']= pd.Series(lista)
        new.to_excel('./excel/Quotazioni_Fantacalcio.xlsx')
        os.remove('./excel/q.xlsx')
        
            
        return 0
    except:
        return 1

def calcola_giocatori():
    try:
        link="https://www.fantacalcio.it/api/v1/Excel/stats/16/1"

        
        headers={
        "authority": "www.fantacalcio.it",
        "method": "GET",
        "path": "/api/v1/Excel/prices/17/1",
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "it,en-US;q=0.9,en;q=0.8,it-IT;q=0.7",
        "cookie": "addtl_consent=1~39.4.3.9.6.9.13.6.4.15.9.5.2.7.4.1.7.1.3.2.10.3.5.4.21.4.6.9.7.10.2.9.2.18.7.6.14.5.20.6.5.1.3.1.11.29.4.14.4.5.3.10.6.2.9.6.6.4.5.4.4.29.4.5.3.1.6.2.2.17.1.17.10.9.1.8.6.2.8.3.4.142.4.8.42.15.1.14.3.1.8.10.25.3.7.25.5.18.9.7.41.2.4.18.21.3.4.2.1.6.6.5.2.14.18.7.3.2.2.8.20.8.8.6.3.10.4.20.2.13.4.6.4.11.1.3.22.16.2.6.8.2.4.11.6.5.33.11.8.1.10.28.12.1.3.21.2.7.6.1.9.30.17.4.9.15.8.7.3.6.6.7.2.4.1.7.12.13.22.13.2.12.2.10.5.15.2.4.9.4.5.4.7.13.5.15.4.13.4.14.8.2.15.2.5.5.1.2.2.1.2.14.7.4.8.2.9.10.18.12.13.2.18.1.1.3.1.1.9.25.4.1.19.8.4.5.3.5.4.8.4.2.2.2.14.2.13.4.2.6.9.6.3.4.3.5.2.3.6.10.11.6.3.16.3.11.3.1.2.3.9.19.11.15.3.10.7.6.4.3.4.6.3.3.3.3.1.1.1.6.11.3.1.1.11.6.1.10.5.2.6.3.2.2.4.3.2.2.7.15.7.12.2.1.3.3.4.5.4.3.2.2.4.1.3.1.1.1.2.9.1.6.9.1.5.2.1.7.2.8.11.1.3.1.1.2.1.3.2.6.1.12.5.3.1.3.1.1.2.2.7.7.1.4.1.2.6.1.2.1.1.3.1.1.4.1.1.2.1.8.1.7.4.3.2.1.3.5.3.9.6.1.15.10.28.1.2.2.12.3.4.1.6.3.4.7.1.3.1.1.3.1.5.3.1.3.2.2.1.1.4.2.1.2.1.2.2.2.4.2.1.2.2.2.4.1.1.1.2.2.1.1.1.1.2.1.1.1.2.2.1.1.2.1.2.1.7.1.2.1.1.1.2.1.1.1.1.2.1.1.3.2.1.1.8.1.1.1.5.2.1.6.5.1.1.1.1.1.2.2.3.1.1.4.1.1.2.2.1.1.4.3.1.2.2.1.2.1.2.3.1.1.2.4.1.1.1.5.1.3.6.3.1.5.2.3.4.1.2.3.1.4.2.1.2.2.2.1.1.1.1.1.1.11.1.3.1.1.2.2.5.2.3.3.5.1.1.1.4.2.1.1.2.5.1.9.4.1.1.3.1.7.1.4.5.1.7.2.1.1.1.2.1.1.1.4.2.1.12.1.1.3.1.2.2.3.1.2.1.1.1.2.1.1.2.1.1.1.1.2.1.3.1.5.1.2.4.3.8.2.2.9.7.2.3.2.1.4.6.1.1.6.1.1; euconsent-v2=CPb8hAAPb8hAAAKAqAITCXCsAP_AAH_AABCYI4Nd_X__bX9j-_5_6ft0eY1f9_r37uQzDhfNs-8F3L_W_LwX32E7NF36pq4KmR4Eu3LBIQNlHMHUTUmwaokVrzHsak2cpyNKJ7JEknMZe2dYGF9Pn9lD-YKY7_5_9_b52T-9_9_-39T3_8ff__dp_2__-vDfV599jfn9fV_789KP___9v__8__________38EbwCDARAIACDBABAAAACEAAEAAkAIAAAAQAAUASADgoAAhYBAACEAAgESEIAAIAQEAMAAAEEACQAIAQAsEAgAAgEAAIAAQAAABAQAAwAkBAAAAACQgQAgABAgIAgAAOQgACgAggBCAQAACiQwAgDrOAAAQQIVAACSQEAgAAQsDAcACAlYkABSAAoAAhBCgFEAkJBZAAQAAuACgAKgAZAA5AB4AIAAYQA0ADUAHkAQwBFACYAE8AKoAbwA5gB6AD8AISAQwBEgCOAEsAJoAUoAtwBhgDIAGWANUAbIA74B7AHxAPsA_YB_gIGARSAi4CMQEaARwAlIBQQCngFXALmAYoA0QBrADaQG4AbwA4gB6AD5AIdARCAkQBMQCZQE2AJ2AUOApEBTQCxQFoALYAXIAu8BeYDBgGGwMjAyQBk4DLgGcgM-AaQA06BrAGsgNvAbqA4KByYHKAOXAdYA8cB7QEIQIXgQ9Ah-BEMCKRKCAAAgABYAFAAMgAcAA_ADAAMQAeABEACYAFUALgAYgAzABtgEMARIAjgBRgClAFuAMIAZQA1QBsgDvAH4ARgAjgBJwCngFXgLQAtIBdQDFAG4AOoAfIBDoCKgEXgJEATYAsUBbAC7QF5gMjAZOAywBnIDPAGfANIAawA28BwADrAHtAQPAgkBC8CGoEPQIsjoNwAC4AKAAqABkADkAHwAgABdADAAMYAaABqADwAH0AQwBFACYAE8AKsAXABdADEAGYAN4AcwA9AB-gEMARIAjoBLAEwAJoAUYApQBYgC3gGEAYcAyADKAGiANkAd4A9oB9gH6AP8AgcBFAEYgI4AjsBKQEqAKCAU8Aq4BYoC0ALTAXMBdYC8gL0AYoA2gBuADiAHUAPQAh0BEICKgEXwJBAkQBKgCZAE2AJ2AUOApoBVgCxQFoALYAXAAuQBdoC7wF5gL6AYMAw0BjADHoGRgZIAycBlUDLAMuAZmAzkBnwDRIGkAaSA0sBpwDVQGsANvAbqA4uByYHKAOXAdYA8cB6QD2gH1gQBAgkBBoCDwELwIdAQ9AikQghAALAAoABkAFwAMQAagBDACYAFMAKoAXAAxABmADeAHoARwApQBYgDCAGUAO8AfYA_wCKAEYAI4ASmAoIChgFPAKvAWgBaQC5gGKANoAdQA9ACIYEggSIAk4BKgCbAFNALFAWiAtgBcAC5AF2gMjAZOAzkBngDPgGiANJAaWA1UBwADlAHWAPHAgkBCgCF4EOgIelIKYAC4AKAAqABkADkAHwAggBgAGMANAA1AB5AEMARQAmABPACkAFUAMQAZgA5gB-gEMARIAowBSgCxAFuAMIAZQA0QBqgDZAHfAPsA_QCLAEYgI4AjoBKYCggKGAVcArYBcwC8gGKANoAbgA9ACHQEXgJEAScAmwBOwChwFigLQAWwAuABcgC7QF5gL6AYaAxiBkYGSAMngZYBlwDOQGeAM-gaQBpMDWANZAbeA3UBwUDkwOUAcuA6wB4oDxwHtAQhAheBDMCHQEPQIgARSFQGQAKABDACYAFwARwAywCMAEcAKvAWgBaQDeAJBATEAmwBTYC2AFyALzAZGAzkBngDPgG5AOUAheMgLABDACYAI4AZYA-wCMAEcAKuAVsA3gCTgExAJsAWiAtgBeYDIwGcgM8AZ8A5QCF4aA-AFwAQwAyABlgDZAH4AQAAgoBGACngFXgLQAtIBrADeAHVAPkAh0BFQCRAE2AJ2AUiAuQBjADIwGTgM5AZ4Az4BygDrBEBgAQwAyABlgDZAH4AQAAjABTwCrgGsAOqAfIBDoCRAE2AJ2AUiAuQBkYDJwGcgM-AcoA6wA.f_gAAAAAAAAA; fanta_web_sign=value; fantacalcio.it=Ccazmp6ks930QjnK3WWkcia4Co99jgjt%2BqRLsOyS4QF71Y5H4byIRx63kVyztFKqOkEijfDQY0nC%2FeayQVh3Gd6CVndjnD3TDxADNyxFTRjUfQCyQ6yJq3Z713OLOAMRF0HBJlp3WQPg%2Fwp2Dr%2BdSiVJw%2FDlE9clGjVqNDzWOjpdLezQBslXTBse85hfujGPD9Qiq52fUTzplMzdgyGag8qYlPa%2FXbJHSB0fqQJpZpvbFqGHqmcomRj4kWSCz8cvr%2F6yDSCo1Yd9kR4mv5V0p32WCbRtnS0N5sfpxVBLG1czgUJXpezNauQF3CT2a2Og84uinzAWqeSRaH8XK%2Bv81SaGqp8GnmFQQ1CScVdoinKLR4Br9EudzjwaFJi0Y5D3%2FqOgJJ2CZ98WyB2Y7HovnI%2BCnr7r7HWH%2F%2BagHEBd%2BU3BXQelfEQCvH44Qg6owRdb8mavIik8G1vY%2BeHMz17CDA%3D%3D;",
        "dnt": "1",
        "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "service-worker-navigation-preload": "true",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        'Connection':'close'}
        
        
        
        r=requests.get(link, headers=headers)
        output = open('./excel/g.xlsx', 'wb')
        output.write(r.content)
        output.close()
        #	Id	R	Nome	Squadra	Pg	Mv	Mf	Gf	Gs	Rp	Rc	R+	R-	Ass	Amm	Esp	Au
        data = pd.read_excel("./excel/g.xlsx", header=1)
        new=pd.DataFrame()
        new['Id']=data['Id']
        new['R']=data['R']
        new['Nome']=data['Nome']
        new['Squadra']=data['Squadra']
        new['Pg']=data['Pg']



        new.to_excel('./excel/giocatori.xlsx')
        os.remove('./excel/g.xlsx')
        
        
        return 0
    except:
        return 1
def calc(g,el):
    i=0
    res=0
    for c in g:
        if i>len(c):
            break
        if c==el[i]:
            res+=1
        i+=1
        
    return res

def calcola_giocatore_simile(g,q):
    migliore=0
    
    m=""
    for el in q['Nome']:
        t=calc(g.upper().strip(),el.upper().strip())

        if t>migliore:
            m=el
            migliore=t
    return m

def genera_excel():
    try:
        os.makedirs("./excel/")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
                
    ris=0
    if not path.exists("./excel/calendario.xlsx"):
        ris+=calcola_calendario()
    if not path.exists("./excel/classifica.xlsx"):
        ris+=calcola_classifica()
    if not path.exists("./excel/Quotazioni_Fantacalcio.xlsx"):
        ris+=calcola_quotazioni()
    if not path.exists("./excel/giocatori.xlsx"):
        ris+=calcola_giocatori()
    if ris==0:
        return "OK"
    return
def por(g1,g2, classifica, d_giocatori, d_calendario):
    if len(d_giocatori[d_giocatori['Nome'].str.contains(g1.upper())]['Squadra']) !=1:
        return
    squadra_1=d_giocatori[d_giocatori['Nome'].str.contains(g1.upper())]['Squadra'].item()
    if len(d_giocatori[d_giocatori['Nome'].str.contains(g2.upper())]['Squadra']) !=1:
        return
    squadra_2=d_giocatori[d_giocatori['Nome'].str.contains(g2.upper())]['Squadra'].item()
    sq1=0
    sq2=0
    tot=0
    diff=[]
    casa=0
    for c in d_calendario:
        giornata=d_calendario[c]
        for g in giornata:
            if squadra_1.upper() in str(g).upper():
                if str(g).upper().split("-")[0]==squadra_1.upper():
                    casa=1
                avv_1=g.replace(squadra_1,"").replace("-","")
                sq1=1
            if squadra_2.upper() in str(g).upper():
                if str(g).upper().split("-")[0]==squadra_2.upper():
                    casa=1
                avv_2=g.replace(squadra_2,"").replace("-","")
                sq2=1
            if sq1==1 and sq2==1:
                i=classifica.index(avv_1.upper())
                k=classifica.index(avv_2.upper())
                value=i+k
                if  casa==1 and value > 15:
                    tot+=1
                sq1=0
                casa=0
                sq2=0
                break
    ris=d_giocatori[d_giocatori['Nome'].str.contains(g1.upper())]['Mv'].item()+d_giocatori[d_giocatori['Nome'].str.contains(g2.upper())]['Mv'].item()
    return str(tot)+";"+str(ris)
def genera_portieri(scelta):
    diz={}
    classifica=list(pd.read_excel("./excel/classifica.xlsx")['SQUADRE'])
    d_giocatori=pd.read_excel("./excel/giocatori.xlsx")
    d_giocatori['Nome'] = d_giocatori['Nome'].apply(lambda nome : nome.upper())

    d_calendario=pd.read_excel("./excel/calendario.xlsx")
    p=list(d_giocatori.loc[(d_giocatori['R'] == 'P')]['Nome'].values)#&(d_giocatori['Pg'] > 1)
    portieri=[]
    for el in p:
        portieri.append(el.upper())
    voti={}
    for i in np.arange(len(portieri)):
        x= portieri[i]
        for j in np.arange(i+1,len(portieri)):
            y = portieri[j]
            a=por(y,x, classifica, d_giocatori, d_calendario)
            if a is not None:
                diz[x+"-"+y]=a.split(";")[0]
                voti[x+"-"+y]=a.split(";")[1]
    #rispetto voti
    marks={k: v for k, v in voti.items() if v}
    ret_marks={k: v for k, v in sorted(marks.items(), key=lambda item: item[1],reverse=True)}
    #rispetto casa e diff partita
    new_diz={k: v for k, v in diz.items() if v}
    ret_diz={k: v for k, v in sorted(new_diz.items(), key=lambda item: int(item[1]),reverse=True)}
    d_5 = [v for v in list(ret_diz.keys())[:20]]
    m_5 = [v for v in list(new_diz.keys())[:20]]
    if scelta==1:
        return d_5
    elif scelta==2:
        return m_5
    return
def dif(giocatore_chiamato,acquistati,budget_rimasto, giachiamati):
    tit_risultato=[]
    quotazioni=pd.read_excel("./excel/Quotazioni_Fantacalcio.xlsx", names=['Id','R','Nome','Squadra','Qt. A','Qt. I','VAL'])
    quotazioni['Nome'] = quotazioni['Nome'].apply(lambda nome : nome.upper())
    da_comprare=8-len(acquistati)   
    x=pd.read_excel("./excel/giocatori.xlsx")
    x['Nome'] = x['Nome'].apply(lambda nome : nome.upper())
    t=x.loc[(x['R']=='D')]       
    
    try:
        p=int(quotazioni[quotazioni['Nome'].str.contains(giocatore_chiamato.upper())]['VAL'].values[0])
    except:
        return 1,0,[]
    prezzo_probabile=p
    if prezzo_probabile <=0:
        prezzo_probabile=1    
    try:
        gf=(t[t['Nome'].str.contains(giocatore_chiamato.upper())]['Gf'].values[0])
    except:
        gf=0        
    print("Gol scorsa stagione:",gf)
    #print("Prezzo di valore:",p)
    #print("Prezzo probabile d'asta:",int(prezzo_probabile))
    difensori=quotazioni.loc[(quotazioni['R'] == 'D')]
    ds=list(quotazioni.loc[(quotazioni['R'] == 'D')].sort_values(by='VAL')['Nome'].values)
    squadre=[]
    valore_reparto=0
    valore=0
    if len(acquistati)!=0:
        for g in acquistati:
            squadre.append(difensori[difensori['Nome'].str.contains(g.upper())]['Squadra'].values[0])
            valore_reparto+=int(quotazioni[quotazioni['Nome'].str.contains(g.upper())]['Qt. A'].values[0])
        valore=round(valore_reparto/len(acquistati),0)
   #print("Valore Reparto attuale:",valore)
    if  budget_rimasto -da_comprare <= 0:# or budget_rimasto -da_comprare<=int(prezzo_probabile):
        ds=list(quotazioni.loc[(quotazioni['R'] == 'D') & (quotazioni['Qt. A'] < 5)]['Nome'].values)
        for k in range(0,da_comprare):
            d=random.choice(ds)
            if d.upper() not in acquistati and d.upper() not in giachiamati:
                acquistati.append(d)
                trovato=0
                try:
                    with open("./indice/titolari.txt","r") as r:
                        l=r.readlines()
                    r.close()
                    for el in l:
                        if d in el:
                            tit=el.split(":")[1].replace("%","")
                            trovato=1
                            break
                    if trovato==0:
                        with open("./indice/riserve.txt","r") as r:
                            l=r.readlines()
                        r.close()
                        for el in l:
                            if d in el:
                                tit=el.split(":")[1].replace("%","")
                                trovato=1
                                break
                    if trovato==0:
                        tit=(t[t['Nome'].str.contains(d.upper())]['Pg'].values[0])
                        tit=round(round(int(tit)/38,2)*100,2)
                except:
                    tit=1  
                try:
                    v=int(quotazioni[quotazioni['Nome'].str.contains(d.upper())]['VAL'].values[0])
                except:
                    v=1
                budget_rimasto=budget_rimasto-v
                titolarieta=int(tit)
                tit_risultato.append(titolarieta)
                k+=1
        return 0,p,tit_risultato
    while(len(acquistati)!=8):
        d=random.choice(ds)
        if d.upper() in acquistati or d.upper() in giachiamati:
            continue
        try:
            with open("./indice/titolari.txt","r") as r:
                l=r.readlines()
            r.close()
            for el in l:
                if d in el:
                    tit=el.split(":")[1].replace("%","")
                    trovato=1
                    break
            if trovato==0:
                with open("./indice/riserve.txt","r") as r:
                    l=r.readlines()
                r.close()
                for el in l:
                    if d in el:
                        tit=el.split(":")[1].replace("%","")
                        trovato=1
                        break
            if trovato==0:
                tit=(t[t['Nome'].str.contains(d.upper())]['Pg'].values[0]) 
                tit=round(round(int(tit)/38,2)*100,2)
        except:
            tit=0

        try:
            v=int(quotazioni[quotazioni['Nome'].str.contains(d.upper())]['VAL'].values[0])
        except:
            v=1
        if int(tit)==0 and v<10:#evito che giocatori nuovi e forti non vengano considerati
            continue
        titolarieta=int(tit)
        try:
            gf=(t[t['Nome'].str.contains(d.upper())]['Gf'].values[0])
        except:
            gf=0        
        if titolarieta>10 or gf>3:
            prezzo_previsto=int(v)
            new_budg=budget_rimasto-prezzo_previsto
            if new_budg > da_comprare:
                acquistati.append(d)
                da_comprare-=1
                prezzo=budget_rimasto-new_budg
                budget_rimasto=new_budg
                tit_risultato.append(titolarieta)                
                ds=list(quotazioni.loc[(quotazioni['R'] == 'D')]['Nome'].values)
                if d in ds:
                    ds.remove(d)
            if new_budg <= da_comprare:
                ds=list(quotazioni.loc[(quotazioni['R'] == 'D') & (quotazioni['Qt. A'] < 5)]['Nome'].values)
                k=0
                while(k<da_comprare):
                    d=random.choice(ds)
                    if d.upper() not in acquistati and d.upper() not in giachiamati:
                        acquistati.append(d)
                        prezzo=1
                        budget_rimasto=budget_rimasto-1
                        try:
                            with open("./indice/titolari.txt","r") as r:
                                l=r.readlines()
                            r.close()
                            for el in l:
                                if d in el:
                                    tit=el.split(":")[1].replace("%","")
                                    trovato=1
                                    break
                            if trovato==0:
                                with open("./indice/riserve.txt","r") as r:
                                    l=r.readlines()
                                r.close()
                                for el in l:
                                    if d in el:
                                        tit=el.split(":")[1].replace("%","")
                                        trovato=1
                                        break
                            if trovato==0:
                                tit=(t[t['Nome'].str.contains(d.upper())]['Pg'].values[0])
                                tit=round(round(int(tit)/38,2)*100,2)
                        except:
                            tit=1
                        titolarieta=int(tit)
                        tit_risultato.append(titolarieta)
                        k+=1
                return 0,p,tit_risultato
            else:
                continue
        else:
            continue
    return 0,p,tit_risultato
def difensori(u,budget):
    i=1
    acquistati=[]
    reparto_finale={}
    new_acquisti=[]
    valore_prima=0
    valori=[]
    giachiamati=[]
    valore_reparto=0

    
    quotazioni=pd.read_excel("./excel/Quotazioni_Fantacalcio.xlsx", names=['Id','R','Nome','Squadra','Qt. A','Qt. I','VAL'])
    x=pd.read_excel("./excel/giocatori.xlsx")
    quotazioni['Nome'] = quotazioni['Nome'].apply(lambda nome : nome.upper())
    x['Nome'] = x['Nome'].apply(lambda nome : nome.upper())
    t=x.loc[(x['R']=='D')]       
    quotazioni=quotazioni.loc[(quotazioni['R']=='D')]     


    lista=[]
    try:
        f=open("./src/rigoristi.txt","r")
        lista=f.readlines()
        f.close()
    except:
        pass
    while(i!=9):


        #input("Premere Invio per continuare ")
        os.system('CLS')      
     
        print("Budget Totale:",u)
        print("Budget Reparto:",budget)
        buff=""
        for el in reparto_finale.keys():
            buff+=el+" "
        print("Reparto Attuale:",buff)
        for el in valori:
            valore_reparto+=el/(len(acquistati)+1)
        print("#"+str(i))
        
        giocatore=input("Difensore ").upper()
        if len(giocatore)<3:
            print("Inserire almeno 3 caratteri.")
            input("Premere Invio per continuare ")
            #acquistati.remove(giocatore)
            acquistati=[]
            continue
        trovato=0
        for g in quotazioni['Nome']:
            
            if giocatore.upper() == g.upper():
                trovato=1
                break
        if trovato==0:
            gx=calcola_giocatore_simile(giocatore,quotazioni)
            if len(gx)==0:
                input("Nessun giocatore trovato, riprova. Premere Invio per continuare ")
                acquistati=[]
                continue
            print(colored(("Nessun giocatore con questo nome, forse si intendeva", gx,"?[Y,n]"),'red'))
            scelta=input()
            if scelta !="y" and scelta !="Y" and len(scelta)>0:
                print(colored("Giocatore non trovato, riprova.",'red'))
                input("Premere Invio per continuare ")
                #acquistati.remove(giocatore)
                acquistati=[]
                continue
            else:
                giocatore=gx
                
        
        if giocatore in reparto_finale.keys() or giocatore in giachiamati:
            print(colored("Giocatore già acquistato.",'red'))
            input("Premere Invio per continuare ")
            acquistati=[]
            continue
        
        for el in reparto_finale.keys():
            acquistati.append(el)
        acquistati.append(giocatore)
        ok,prezzo,tit_risultato=dif(giocatore,acquistati,budget,giachiamati)
        for el in lista:
            if giocatore.upper().strip()==el.strip():
                print(colored("Probabile rigorista",'green'))
        print("Possibile squadra:")
        #print("Nome\t\tPrezzo\t\tGol scorso anno\t\tTitolarietà")
        lista_print=[[]]
        ptpr=0
        prt=0
        xxx=0
        tit=0
        px=0
        try:
            with open("./categorie/difensori.json","r") as r:
                data = json.load(r)
            r.close() 
        except:
            data={}
        try:
            with open("./infortunii/infortunati.txt","r") as r:
                infortunati=r.readlines()
            r.close()
        except:
            infortunati=[]
        try:
            with open("./infortunii/squalificati.txt","r") as r:
                squalificati=r.readlines()
            r.close()
        except:
            squalificati=[]  
            
        for el in acquistati:
            if el in reparto_finale.keys():
                p=int(reparto_finale[el])
                prezzo_probabile=p
            else:    
                try:
                    p=int(quotazioni[quotazioni['Nome'].str.contains(el.upper())]['Qt. A'].values[0])
                except:
                    p=0
                try:
                    prezzo_probabile=int(quotazioni[quotazioni['Nome'].str.contains(el.upper())]['VAL'].values[0])
                except:
                    prezzo_probabile=0                    

            ptpr+=p
            prt+=prezzo_probabile
            
            
            ###cat###

            cat="-"
            trovato=0
            for categoria in data.keys():
                if el.upper() in str(data[categoria]).upper():
                    cat=categoria
                if trovato==1:
                    break
               
            ####
 
            inf="-"
            for e in infortunati:
                if el.upper().strip() in e.strip() or e.strip() in el.upper().strip():
                    inf="Sì"
            squ="-"
            for e in squalificati:
                if el.upper().strip() in e.strip():
                    squ=e.split("(")[1].split(")")[0]
                    
            ####
            
            try:
                gf=(t[t['Nome'].str.contains(el.upper())]['Gf'].values[0])
            except:
                gf=0
            try:
                with open("./indice/titolari.txt","r") as r:
                    l=r.readlines()
                r.close()
                for s in l:
                    if el in s:
                        tit=s.split(":")[1].replace("%","")
                        trovato=1
                        break
                if trovato==0:
                    with open("./indice/riserve.txt","r") as r:
                        l=r.readlines()
                    r.close()
                    for s in l:
                        if el in s:
                            tit=s.split(":")[1].replace("%","")
                            trovato=1
                            break
                xxx+=int(tit)
            except:
                tit=0
            try:    
                s=quotazioni[quotazioni['Nome'].str.contains(el.upper())]['Squadra'].values[0]
            except:
                s=""
                
            if el.upper() == giocatore.upper():
                tx=int(tit)#round(round(int(tit)/38,2)*100,2)
                px=prezzo_probabile
            lista_print.append([el,s,p,int(prezzo_probabile),gf,str(tit).strip()+"%",cat,inf,squ])
            #print(el,"\t\t",p,"\t\t",gf,"\t\t",round(round(int(tit)/38,2)*100,2),"%")
        lista_print.append(["","","","","","","",""])
        lista_print.append(["Prezzo Totale Previsto:",int(ptpr),"","","","","",""])
        lista_print.append(["Prezzo Totale Probabile:",int(prt),"","","","","",""])
        prezzo=int(prezzo)    
        lista_print.append(["Indice titolarietà medio squadra:",str(int(xxx)/len(acquistati))+"%","","","","",""])
        print(tabulate(lista_print, headers=["Nome", "Squadra", "Prezzo Previsto","Prezzo Probabile", "Gol Scorso Anno","Titolarietà", "Categoria","Infortunato","Squalificato"]))
        lista_print.clear()

        valore_temp=(valore_reparto+prezzo)/(len(acquistati)+1)
        if int((valore_temp-valore_prima)*100) >150:
        
            print(colored((int((valore_temp-valore_prima)*100),"% qualità alla squadra."),'green'))
        elif int((valore_temp-valore_prima)*100) >100:
            print(colored((int((valore_temp-valore_prima)*100),"% qualità alla squadra."),'yellow'))
        else:
            print(colored((int((valore_temp-valore_prima)*100),"% qualità alla squadra."),'red'))

        if prezzo>budget-(8-len(new_acquisti)) or int(px)>budget:
            print(colored(("Mmm, costa tanto, circa ",int(px)),'yellow'))

        elif valore_temp > valore_prima and tx>55:
            print(colored(("Si acquistalo ma al massimo spendi:",int(px)),'green'))
            print("Probabile prezzo d'asta: circa",int(px))
        else:
            print(colored("Non acquistarlo.",'red'))
        valore_reparto=0
        quanto=input("Se lo hai comprato, a quanto? (se no premere 0 o invio) ")
        if len(quanto)==0:

            acquistati=[]
            giachiamati.append(giocatore)
            continue
        try:
            if int(quanto)>0:
                giachiamati.append(giocatore)                            
                reparto_finale[giocatore]=quanto
                budget=budget-int(quanto)
                u-=int(quanto)
                valori.append(prezzo)
                valore_prima=valore_temp
                new_acquisti.append(giocatore)
                i+=1
            acquistati=[]
        except:
            print("", end="\r")
            acquistati=[]
            giachiamati.append(giocatore)  
            continue
        print("", end="\r")
    return reparto_finale
def centr(giocatore_chiamato,acquistati,budget_rimasto,giachiamati):
    tit_risultato=[]
    quotazioni=pd.read_excel("./excel/Quotazioni_Fantacalcio.xlsx", names=['Id','R','Nome','Squadra','Qt. A','Qt. I','VAL'])
    quotazioni['Nome'] = quotazioni['Nome'].apply(lambda nome : nome.upper())
    da_comprare=8-len(acquistati)
    x=pd.read_excel("./excel/giocatori.xlsx")
    x['Nome'] = x['Nome'].apply(lambda nome : nome.upper())
    t=x.loc[(x['R']=='C')]

    try:
        p=int(quotazioni[quotazioni['Nome'].str.contains(giocatore_chiamato.upper())]['VAL'].values[0])
    except:
        return 1,0,[]
    prezzo_probabile=p
    if prezzo_probabile <=0:
        prezzo_probabile=p
    try:
        gf=(t[t['Nome'].str.contains(giocatore_chiamato.upper())]['Gf'].values[0])
    except:
        gf=0        
    print("Gol scorsa stagione:",gf)
    #print("Prezzo di valore:",p)
    #print("Prezzo probabile d'asta:",int(prezzo_probabile))
    centrocampisti=quotazioni.loc[(quotazioni['R'] == 'C')]
    cs=list(quotazioni.loc[(quotazioni['R'] == 'C')].sort_values(by='VAL', ascending=False)['Nome'].values)
    squadre=[]
    valore_reparto=0
    valore=0
    if len(acquistati)!=0:
        for g in acquistati:
            squadre.append(centrocampisti[centrocampisti['Nome'].str.contains(g.upper())]['Squadra'].values[0])
            valore_reparto+=int(quotazioni[quotazioni['Nome'].str.contains(g.upper())]['Qt. A'].values[0])
        valore=round(valore_reparto/len(acquistati),0)
    #print("Valore Reparto attuale:",valore)
    if  budget_rimasto -da_comprare <= 0:
        cs=list(quotazioni.loc[(quotazioni['R'] == 'C') & (quotazioni['Qt. A'] < 5)]['Nome'].values)
        for k in range(0,da_comprare):
            cx=random.choice(cs)
            if cx.upper() not in acquistati and cx.upper() not in giachiamati:
                acquistati.append(cx)
                ##
                trovato=0
                try:
                    with open("./indice/titolari.txt","r") as r:
                        l=r.readlines()
                    r.close()
                    for el in l:
                        if cx in el:
                            tit=el.split(":")[1].replace("%","")
                            trovato=1
                            break
                    if trovato==0:
                        with open("./indice/riserve.txt","r") as r:
                            l=r.readlines()
                        r.close()
                        for el in l:
                            if cx in el:
                                tit=el.split(":")[1].replace("%","")
                                trovato=1
                                break
                    if trovato==0:
                        tit=(t[t['Nome'].str.contains(cx.upper())]['Pg'].values[0])
                        tit=round(round(int(tit)/38,2)*100,2)
                except:
                    tit=1                  
                ##
                try:
                    v=int(quotazioni[quotazioni['Nome'].str.contains(cx.upper())]['Qt. A'].values[0])
                except:
                    v=1
                budget_rimasto=budget_rimasto-v

                titolarieta=int(tit)
                tit_risultato.append(titolarieta)
                k+=1
        return 0,p,tit_risultato
    while(len(acquistati)!=8):
        cx=random.choice(cs)
        if cx.upper() in acquistati or cx.upper() in giachiamati:
            continue
        try:
            with open("./indice/titolari.txt","r") as r:
                l=r.readlines()
            r.close()
            for el in l:
                if cx in el:
                    tit=el.split(":")[1].replace("%","")
                    trovato=1
                    break
            if trovato==0:
                with open("./indice/riserve.txt","r") as r:
                    l=r.readlines()
                r.close()
                for el in l:
                    if cx in el:
                        tit=el.split(":")[1].replace("%","")
                        trovato=1
                        break
            if trovato==0:
                tit=int(t[t['Nome'].str.contains(cx.upper())]['Pg'].values[0])
                tit=round(round(int(tit)/38,2)*100,2)
        except:
            tit=0          

        try:
            v=int(quotazioni[quotazioni['Nome'].str.contains(cx.upper())]['VAL'].values[0])
        except:
            v=1 
        if int(tit)==0 and v<20:#evito che giocatori nuovi e forti non vengano considerati
            continue
        titolarieta=int(tit)
        try:
            gf=(t[t['Nome'].str.contains(cx.upper())]['Gf'].values[0])
        except:
            gf=0        
        if titolarieta>10 or gf>3:
            prezzo_previsto=int(v)
            new_budg=budget_rimasto-prezzo_previsto#v
            if new_budg > da_comprare:
                acquistati.append(cx)
                da_comprare-=1
                prezzo=budget_rimasto-new_budg
                budget_rimasto=new_budg
                tit_risultato.append(titolarieta)
                cs=list(quotazioni.loc[(quotazioni['R'] == 'C')]['Nome'].values)#& ((quotazioni['Qt. A'])< 5)
                if cx in cs:
                    cs.remove(cx)
            if budget_rimasto <= da_comprare:
                cs=list(quotazioni.loc[(quotazioni['R'] == 'C') & ((quotazioni['Qt. A']) < budget_rimasto)]['Nome'].values)
                k=0
                while(k <da_comprare):
                    cx=random.choice(cs)
                    if cx not in acquistati and cx.upper() not in giachiamati:
                        acquistati.append(cx)
                        prezzo=1
                        budget_rimasto=budget_rimasto-1
                        ##
                        try:
                            with open("./indice/titolari.txt","r") as r:
                                l=r.readlines()
                            r.close()
                            for el in l:
                                if cx in el:
                                    tit=el.split(":")[1].replace("%","")
                                    trovato=1
                                    break
                            if trovato==0:
                                with open("./indice/riserve.txt","r") as r:
                                    l=r.readlines()
                                r.close()
                                for el in l:
                                    if cx in el:
                                        tit=el.split(":")[1].replace("%","")
                                        trovato=1
                                        break
                            if trovato==0:
                                tit=(t[t['Nome'].str.contains(cx.upper())]['Pg'].values[0])
                                tit=round(round(int(tit)/38,2)*100,2)
                        except:
                            tit=1
                        ##
                        titolarieta=int(tit)
                        tit_risultato.append(titolarieta)
                        k+=1
                return 0,p,tit_risultato
            else:
                continue
        else:
            continue
    return 0,p,tit_risultato
def centrocampisti(u,budget):
    i=1
    acquistati=[]
    reparto_finale={}
    new_acquisti=[]
    valore_prima=0
    valori=[]
    valore_reparto=0
    giachiamati=[]
    quotazioni=pd.read_excel("./excel/Quotazioni_Fantacalcio.xlsx", names=['Id','R','Nome','Squadra','Qt. A','Qt. I','VAL'])
    x=pd.read_excel("./excel/giocatori.xlsx")
    x['Nome'] = x['Nome'].apply(lambda nome : nome.upper())
    quotazioni['Nome'] = quotazioni['Nome'].apply(lambda nome : nome.upper())
    t=x.loc[(x['R']=='C')]       
    quotazioni=quotazioni.loc[(quotazioni['R']=='C')]     


    lista=[]
    try:
        f=open("./src/rigoristi.txt","r")
        lista=f.readlines()
        f.close()
    except:
        pass
        
    try:
        with open("./infortunii/infortunati.txt","r") as r:
            infortunati=r.readlines()
        r.close()
    except:
        infortunati=[]
    try:
        with open("./categorie/centrocampisti.json","r") as r:
            data = json.load(r)
        r.close()        
    except:
        data={}
    try:
        with open("./infortunii/squalificati.txt","r") as r:
            squalificati=r.readlines()
        r.close()
    except:
        squalificati=[]     
        
    while(i!=9):
        #input("Premere Invio per continuare ")
       

        os.system('CLS')   
        print("Budget Totale:",u)        
        print("Budget Reparto:",budget)
        buff=""
        for el in reparto_finale.keys():
            buff+=el+" "
        print("Reparto Attuale:",buff)

        for el in valori:
            valore_reparto+=el/(len(acquistati)+1)
        print("#"+str(i))
        giocatore=input("Centrocampista ").upper()
        if len(giocatore)<3:
            print(colored("Inserire almeno 3 caratteri.",'red'))
            input("Premere Invio per continuare ")
            #acquistati.remove(giocatore)
            acquistati=[]
            continue
        trovato=0
        for g in quotazioni['Nome']:
            if giocatore.upper()==g.upper():
                trovato=1
                break
        if trovato==0:
            gx=calcola_giocatore_simile(giocatore,quotazioni)
            if len(gx)==0:
                input("Nessun giocatore trovato, riprova. Premere Invio per continuare ")
                acquistati=[]
                continue
            print(colored(("Nessun giocatore con questo nome, forse si intendeva", gx,"?[Y,n]"),'red'))
            scelta=input()
            if scelta !="y" and scelta !="Y" and len(scelta)>0:
                print(colored("Giocatore non trovato, riprova.",'red'))
                input("Premere Invio per continuare ")
                #acquistati.remove(giocatore)
                acquistati=[]
                continue
            else:
                giocatore=gx
        if giocatore in reparto_finale.keys() or giocatore.upper() in giachiamati:
            print(colored("Giocatore già acquistato.",'red'))
            input("Premere Invio per continuare ")
            acquistati=[]
            continue
        for el in reparto_finale.keys():
            acquistati.append(el)
        acquistati.append(giocatore)
        ok,prezzo,tit_risultato=centr(giocatore,acquistati,budget, giachiamati)
        for el in lista:
            if giocatore.upper().strip()==el.strip():
                print(colored("Probabile rigorista",'green'))
        print("Possibile squadra:")
        #print("Nome\t\tPrezzo\t\tGol scorso anno\t\tTitolarietà")
        lista_print=[[]]
        ptpr=0
        prt=0
        xxx=0
        tit=0
        px=0
        for el in acquistati:
            if el in reparto_finale.keys():
                p=int(reparto_finale[el])
                prezzo_probabile=p
            else:    
                try:
                    p=int(quotazioni[quotazioni['Nome'].str.contains(el.upper())]['Qt. A'].values[0])
                except:
                    p=0
                try:
                    prezzo_probabile=int(quotazioni[quotazioni['Nome'].str.contains(el.upper())]['VAL'].values[0])
                except:
                    prezzo_probabile=1

            ptpr+=p
            prt+=prezzo_probabile

            cat="-"
            for categoria in data.keys():
                if el.upper() in str(data[categoria]).upper() :
                    cat=categoria
                    break
                for d in data[categoria]:
                    if el.upper() in d.upper() or d.upper() in el.upper() :
                        cat=categoria
                        break
            inf="-"
            for e in infortunati:
                if el.upper().strip() in e.strip() or e.strip() in el.upper().strip():
                    inf="Sì"
            squ="-"
            for e in squalificati:
                if el.upper().strip() in e.strip():
                    squ=e.split("(")[1].split(")")[0]
                                  
            try:
                gf=(t[t['Nome'].str.contains(el.upper())]['Gf'].values[0])
            except:
                gf=0
            try:
                with open("./indice/titolari.txt","r") as r:
                    l=r.readlines()
                r.close()
                trovato=0
                for s in l:
                    if el in s:
                        tit=int(s.split(":")[1].replace("%",""))
                        trovato=1
                        break
                
                if trovato==0:
                    with open("./indice/riserve.txt","r") as r:
                        l=r.readlines()
                    r.close()
                    for s in l:
                        if el in s:
                            tit=int(s.split(":")[1].replace("%",""))
                            trovato=1
                            break
                xxx+=int(tit)
            except:
                tit=0
            try:    
                s=quotazioni[quotazioni['Nome'].str.contains(el.upper())]['Squadra'].values[0]
            except:
                s=""                
            if el.upper() == giocatore.upper():
                    tx=int(tit)
                    px=prezzo_probabile
            lista_print.append([el,s,p,int(prezzo_probabile),gf,str(tit).strip()+"%",cat,inf,squ])
            #print(el,"\t\t",p,"\t\t",gf,"\t\t",round(round(int(tit)/38,2)*100,2),"%")
        lista_print.append(["","","","","","","",""])
        lista_print.append(["Prezzo Totale Previsto:",int(ptpr),"","","","","",""])
        lista_print.append(["Prezzo Totale Probabile:",int(prt),"","","","","",""])
        prezzo=int(prezzo)    
 
        
        lista_print.append(["Indice titolarietà medio reparto:",str(int(xxx)/len(acquistati))+"%","","","","",""])
        print(tabulate(lista_print, headers=["Nome","Squadra", "Prezzo Previsto","Prezzo Probabile", "Gol Scorso Anno","Titolarietà","Categoria","Infortunato","Squalificato"]))
        lista_print.clear()
        valore_temp=(valore_reparto+prezzo)/(len(acquistati)+1)
        if int((valore_temp-valore_prima)*100) >150:
        
            print(colored((int((valore_temp-valore_prima)*100),"% qualità alla squadra."),'green'))
        elif int((valore_temp-valore_prima)*100) >100:
            print(colored((int((valore_temp-valore_prima)*100),"% qualità alla squadra."),'yellow'))
        else:
            print(colored((int((valore_temp-valore_prima)*100),"% qualità alla squadra."),'red'))

        if prezzo>budget-(8-len(new_acquisti)) or px>budget:
            print(colored(("Mmm, costa tanto, circa ",int(px)),'yellow'))
        elif valore_temp > valore_prima and tx > 55:
            print(colored(("Si acquistalo ma al massimo spendi:",int(px)),'green'))
            print("Probabile prezzo d'asta: circa",int(px))
        else:
            print(colored("Non acquistarlo.",'red'))
        valore_reparto=0
        quanto=input("Se lo hai comprato, a quanto? (se no premere 0 o invio) ")
        if len(quanto)==0:

            acquistati=[]
            giachiamati.append(giocatore)
            continue
        try:
            if int(quanto)>0:

                giachiamati.append(giocatore.upper())                    
                reparto_finale[giocatore]=quanto
                budget=budget-int(quanto)
                u-=int(quanto)
                valori.append(prezzo)
                valore_prima=valore_temp
                new_acquisti.append(giocatore.upper())
                i+=1
            acquistati=[]
        except:
            giachiamati.append(giocatore.upper())  
            print("", end="\r")
            acquistati=[]
            continue
        print("", end="\r")
    return reparto_finale
def att(giocatore_chiamato,acquistati,budget_rimasto, giachiamati):
    tit_risultato=[]    
    quotazioni=pd.read_excel("./excel/Quotazioni_Fantacalcio.xlsx", names=['Id','R','Nome','Squadra','Qt. A','Qt. I','VAL'])
    quotazioni['Nome'] = quotazioni['Nome'].apply(lambda nome : nome.upper())
    da_comprare=6-len(acquistati)
    x=pd.read_excel("./excel/giocatori.xlsx")
    x['Nome'] = x['Nome'].apply(lambda nome : nome.upper())
    t=x.loc[(x['R']=='A')]
    

    try:
        p=int(quotazioni[quotazioni['Nome'].str.contains(giocatore_chiamato.upper())]['VAL'].values[0])
    except:
        return 1,0,1,[]
    prezzo_probabile=p
      
    
    if prezzo_probabile <=0:
        prezzo_probabile=1
    try:
        gf=(t[t['Nome'].str.contains(giocatore_chiamato.upper())]['Gf'].values[0])
    except:
        gf=0      
        
    prezzo_ritorno=int(prezzo_probabile)
    print("Gol scorsa stagione:",gf)
    #print("Prezzo di valore:",p)
    #print("Prezzo probabile d'asta:",int(prezzo_probabile))
    attaccanti=quotazioni.loc[(quotazioni['R'] == 'A')]
    ass=list(quotazioni.loc[(quotazioni['R'] == 'A')].sort_values(by='Qt. A', ascending=False)['Nome'].values)
    squadre=[]
    valore_reparto=0
    valore=0
    


    if  budget_rimasto -da_comprare <= 0:
        ass=list(quotazioni.loc[(quotazioni['R'] == 'A') & (quotazioni['Qt. A'] < 5)]['Nome'].values)
        for k in range(0,da_comprare):
            ax=random.choice(ass)
            if ax.upper() not in acquistati and ax.upper() not in giachiamati:
                acquistati.append(ax)
                prezzo=1
                budget_rimasto=budget_rimasto-1
                try:
                    with open("./indice/titolari.txt","r") as r:
                        l=r.readlines()
                    r.close()
                    for el in l:
                        if ax in el:
                            tit=el.split(":")[1].replace("%","")
                            trovato=1
                            break
                    if trovato==0:
                        with open("./indice/riserve.txt","r") as r:
                            l=r.readlines()
                        r.close()
                        for el in l:
                            if ax in el:
                                tit=el.split(":")[1].replace("%","")
                                trovato=1
                                break
                    if trovato==0:
                        tit=(t[t['Nome'].str.contains(ax.upper())]['Pg'].values[0])
                        tit=round(round(int(tit)/38,2)*100,2)
                except:
                    tit=1
                titolarieta=int(tit)
                tit_risultato.append(titolarieta)
                
                k+=1
        return 0,p,prezzo_ritorno,tit_risultato
    tentativi=0
    
    ############################
    ############################
    try:
        with open("./indice/riserve.txt","r") as r:
            riserve=r.readlines()
        r.close()    
    except:
        riserve=[]
    try:
        with open("./indice/titolari.txt","r") as r:
            titolari=r.readlines()
        r.close()                
    except:
        titolari=[]
    i=0
    while(len(acquistati)!=6):
        ax=random.choice(ass)
        #try:
        #    ax=ass[i]
        #except:
        #    ax=random.choice(ass)
        
        ############
        try:
            v=int(quotazioni[quotazioni['Nome'].str.contains(ax.upper())]['VAL'].values[0])
        except:
            v=1
            
        
        if budget_rimasto-v-da_comprare<=0:
            continue
        try:
            for el in titolari:
                if ax in el:
                    tit=el.split(":")[1].replace("%","")
                    trovato=1
                    break
            if trovato==0:
                for el in riserve:
                    if ax in el:
                        tit=el.split(":")[1].replace("%","")
                        trovato=1
                        break
            if trovato==0:
                tit=round(round(int(tit)/38,2)*100,2)
                tit=int(t[t['Nome'].str.contains(ax.upper())]['Pg'].values[0])
        except:
            tit=0
     
        if int(tit)==0 and v<50:
            continue
        titolarieta=int(tit)
        try:
            gf=(t[t['Nome'].str.contains(ax.upper())]['Gf'].values[0])
        except:
            gf=0
        prezzo_previsto=v
        if prezzo_previsto<=0:
            continue
        

        if  (titolarieta>10  or gf>5 or v>50 )   and not (ax.upper() in acquistati or ax.upper() in giachiamati) :
            
            new_budg=budget_rimasto-prezzo_previsto
            if new_budg > da_comprare:
                acquistati.append(ax)
                da_comprare-=1
                
                budget_rimasto=new_budg
                tit_risultato.append(titolarieta)                
                ass=list(quotazioni.loc[(quotazioni['R'] == 'A')& (quotazioni['Qt. A'] < budget_rimasto )]['Nome'].values)#& ((quotazioni['Qt. A'])<= 5)
            elif new_budg <= da_comprare:
                
                ass=list(quotazioni.loc[(quotazioni['R'] == 'A') & (quotazioni['Qt. A'] < 5)]['Nome'].values)
                k=0
                while(k<da_comprare):
                    ax=random.choice(ass)
                    if ax not in acquistati and ax not in giachiamati:
                        acquistati.append(ax)
                        giachiamati.append(ax)
                        prezzo=1
                        budget_rimasto=new_budg-1
                        try:
                            with open("./indice/titolari.txt","r") as r:
                                l=r.readlines()
                            r.close()
                            for el in l:
                                if ax in el:
                                    tit=el.split(":")[1].replace("%","")
                                    trovato=1
                                    break
                            if trovato==0:
                                with open("./indice/riserve.txt","r") as r:
                                    l=r.readlines()
                                r.close()
                                for el in l:
                                    if ax in el:
                                        tit=el.split(":")[1].replace("%","")
                                        trovato=1
                                        break
                            if trovato==0:
                                tit=(t[t['Nome'].str.contains(ax.upper())]['Pg'].values[0])
                                tit=round(round(int(tit)/38,2)*100,2)                                
                        except:
                            tit=1
                        titolarieta=int(tit)
                        tit_risultato.append(titolarieta)
                        k+=1
                        
                return 0,p,prezzo_ritorno,tit_risultato
        else:
            tentativi+=1 
            
            if tentativi > 200:

                ass=list(quotazioni.loc[(quotazioni['R'] == 'A') & (quotazioni['Qt. A'] < 5)]['Nome'].values)
                k=0 
                while(k<da_comprare):
                    ax=random.choice(ass)
                    if ax not in acquistati and ax not in giachiamati:
                        
                        prezzo=1
                        budget_rimasto=new_budg-1
                        try:
                            with open("./indice/titolari.txt","r") as r:
                                l=r.readlines()
                            r.close()
                            for el in l:
                                if d in el:
                                    tit=el.split(":")[1].replace("%","")
                                    trovato=1
                                    break
                            if trovato==0:
                                with open("./indice/riserve.txt","r") as r:
                                    l=r.readlines()
                                r.close()
                                for el in l:
                                    if d in el:
                                        tit=el.split(":")[1].replace("%","")
                                        trovato=1
                                        break
                            if trovato==0:
                                tit=(t[t['Nome'].str.contains(d.upper())]['Pg'].values[0])
                                tit=round(round(int(tit)/38,2)*100,2)
                        except:
                            tit=1
                        titolarieta=int(tit)
                        tit_risultato.append(titolarieta)
                        k+=1
                        acquistati.append(ax)
                        giachiamati.append(ax)
                return 0,p,prezzo_ritorno,tit_risultato
    return 0,p,prezzo_ritorno,tit_risultato
def attaccanti(u,budget):
    i=1
    acquistati=[]
    reparto_finale={}
    new_acquisti=[]
    valore_prima=0
    valori=[]
    giachiamati=[]
    valore_reparto=0
    quotazioni=pd.read_excel("./excel/Quotazioni_Fantacalcio.xlsx", names=['Id','R','Nome','Squadra','Qt. A','Qt. I','VAL'])
    quotazioni['Nome'] = quotazioni['Nome'].apply(lambda nome : nome.upper())
    
    
    x=pd.read_excel("./excel/giocatori.xlsx")
    x['Nome'] = x['Nome'].apply(lambda nome : nome.upper())
    t=x.loc[(x['R']=='A')]
    quotazioni=quotazioni.loc[(quotazioni['R']=='A')]     
    


    lista=[]
    try:
        f=open("./src/rigoristi.txt","r")
        lista=f.readlines()
        f.close()
    except:
        pass
    try:
        with open("./infortunii/infortunati.txt","r") as r:
            infortunati=r.readlines()
        r.close()
    except:
        infortunati=[]
    try:
        with open("./infortunii/squalificati.txt","r") as r:
            squalificati=r.readlines()
        r.close()
    except:
        squalificati=[]     
    try:
        with open("./categorie/attaccanti.json","r") as r:
            data = json.load(r)
        r.close()
    except:
        data={}
        


    while(i!=7):
        
        #input("Premere Invio per continuare ")
        os.system('CLS')        
        print("Budget Totale:",u)
        print("Budget Reparto:",budget)
        buff=""
        for el in reparto_finale.keys():
            buff+=el+" "
        print("Reparto Attuale:",buff)
        for el in valori:
            valore_reparto+=el/(len(acquistati)+1)
        print("#"+str(i))
        giocatore=input("Attaccante ").upper()
        if len(giocatore)<3:
            print(colored("Inserire almeno 3 caratteri.",'red'))
            input("Premere Invio per continuare ")
            #acquistati.remove(giocatore)
            acquistati=[]
            continue        

        trovato=0
        for g in quotazioni['Nome']:
            if giocatore.upper()==g.upper():
                trovato=1
                break
        if trovato==0:
            gx=calcola_giocatore_simile(giocatore,quotazioni)
            if len(gx)==0:
                input("Nessun giocatore trovato, riprova. Premere Invio per continuare ")
                acquistati=[]
                continue
            print(colored(("Nessun giocatore con questo nome, forse si intendeva", gx,"?[Y,n]"),'red'))
            scelta=input()
            if scelta !="y" and scelta !="Y" and len(scelta)>0:
                print(colored("Giocatore non trovato, riprova.",'red'))
                input("Premere Invio per continuare ")
                #acquistati.remove(giocatore)
                acquistati=[]
                continue
            else:
                giocatore=gx
        if giocatore in reparto_finale.keys() or giocatore.upper() in giachiamati:
            print(colored("Giocatore già acquistato.",'red'))
            input("Premere Invio per continuare ")
            acquistati=[]
            continue
        for el in reparto_finale.keys():
            acquistati.append(el)
        acquistati.append(giocatore)
        ok,prezzo,pr,tit_risultato=att(giocatore,acquistati,budget, giachiamati)
        for el in lista:
            if giocatore.upper().strip()==el.strip():
                print(colored("Probabile rigorista",'green'))
        print("Possibile squadra:")
        #print("Nome\t\tPrezzo\t\tGol scorso anno\t\tTitolarietà")
        lista_print=[[]]
        ptpr=0
        prt=0
        xxx=0
        px=0
        for el in acquistati:
            tit=0
            if el in reparto_finale.keys():
                p=int(reparto_finale[el])
                prezzo_probabile=p
            else:    
                try:
                    p=int(quotazioni[quotazioni['Nome'].str.contains(el.upper())]['Qt. A'].values[0])
                except:
                    p=0
                try:
                    prezzo_probabile=int(quotazioni[quotazioni['Nome'].str.contains(el.upper())]['VAL'].values[0])
                except:
                    prezzo_probabile=1  
            ptpr+=p
            prt+=prezzo_probabile
            with open("./categorie/attaccanti.json","r") as r:
                data = json.load(r)
            r.close()
            cat="-"
            for categoria in data.keys():
                if el.upper() in str(data[categoria]).upper():
                    cat=categoria
                    break
            inf="-"
            for e in infortunati:
                if el.upper().strip() in e.strip() or e.strip() in el.upper().strip():
                    inf="Sì"
            squ="-"
            for e in squalificati:
                if el.upper().strip() in e.strip():
                    squ=e.split("(")[1].split(")")[0]
                             
            try:
                gf=(t[t['Nome'].str.contains(el.upper())]['Gf'].values[0])
            except:
                gf=0
            try:
                with open("./indice/titolari.txt","r") as r:
                    l=r.readlines()
                r.close()
                for s in l:
                    if el.upper() in s.upper():
                        tit=int(s.split(":")[1].replace("%",""))
                        trovato=1
                        break
                if trovato==0:
                    with open("./indice/riserve.txt","r") as r:
                        l=r.readlines()
                    r.close()
                    for s in l:
                        if el.upper() in s.upper():
                            tit=int(s.split(":")[1].replace("%",""))
                            break
                xxx+=int(tit)
            except:
                tit=0
            try:
                s=quotazioni[quotazioni['Nome'].str.contains(el.upper())]['Squadra'].values[0]
            except:
                s=""
            if el.upper() == giocatore.upper():
                tx=int(tit)
                px=prezzo_probabile
            lista_print.append([el,s,p,int(prezzo_probabile),gf,str(tit).strip()+"%",cat,inf,squ])
        lista_print.append(["","","","","","","",""])
        lista_print.append(["Prezzo Totale Previsto:",int(ptpr),"","","","","","",""])
        lista_print.append(["Prezzo Totale Probabile:",int(prt),"","","","","","",""])
        prezzo=int(prezzo)    
        tit=0
        for el in tit_risultato:
            tit+=round(round(int(el)/38,2)*100,2)
        lista_print.append(["Indice titolarietà medio reparto:",str(int(xxx/len(acquistati)))+"%","","","","",""])
        print(tabulate(lista_print, headers=["Nome", "Squadra","Prezzo Previsto","Prezzo Probabile", "Gol Scorso Anno","Titolarietà","Categoria","Infortunato","Squalificato"]))
        lista_print.clear()
        valore_temp=(valore_reparto+prezzo)/(len(acquistati)+1)
        if int((valore_temp-valore_prima)*100) >150:
        
            print(colored((int((valore_temp-valore_prima)*100),"% qualità alla squadra."),'green'))
        elif int((valore_temp-valore_prima)*100) >100:
            print(colored((int((valore_temp-valore_prima)*100),"% qualità alla squadra."),'yellow'))
        else:
            print(colored((int((valore_temp-valore_prima)*100),"% qualità alla squadra."),'red'))

        if prezzo>budget-(6-len(new_acquisti)) or int(px)>budget:
            print(colored(("Mmm, costa tanto, circa ",pr),'yellow'))
        elif valore_temp > valore_prima or tx > 50:
            
            print(colored(("Si acquistalo ma al massimo spendi:",int(px)),'green'))
            print("Probabile prezzo d'asta: circa",int(px))
        else:
            print(colored("Non acquistarlo.",'red'))
        valore_reparto=0
        quanto=input("Se lo hai comprato, a quanto? (se no premere 0 o invio) ")
        if len(quanto)==0:

            acquistati=[]
            giachiamati.append(giocatore)
            continue
        try:
            if int(quanto)>0:
   
                reparto_finale[giocatore]=quanto
                budget=budget-int(quanto)
                u=u-int(quanto)
                valori.append(prezzo)
                valore_prima=valore_temp
                new_acquisti.append(giocatore.upper())
                giachiamati.append(giocatore.upper())
                i+=1
            acquistati=[]
        except:
            print("", end="\r")
            acquistati=[]
            giachiamati.append(giocatore)
            continue
        print("", end="\r")
    return reparto_finale
def a(budget_tot,budg_portieri, budg_dif,budg_centr,budg_att):
    if budg_att> budget_tot:
        budg_att=budget_tot
    reparto=attaccanti(budget_tot,budg_att)
    print(reparto)
    w_d=open("./src/attaccanti.txt", "w")
    spesa=0
    for el in reparto:
        spesa+=int(reparto[el])
        buff=""+el+" : "+reparto[el]
        w_d.write(buff)
        w_d.write("\n")
    if spesa> int(budg_att):
        print("Hai speso troppo, multa. :(")
        print("Crediti spesi in più:",abs(budg_att-spesa))
        print("CREDITI RIMASTI TOTALE:",(budget_tot-spesa))
        salvasuFile(budget_tot,budg_att-spesa,0,0,0,0)
    else:
        print("Crediti rimasti:",(budg_att-spesa))
        print("CREDITI RIMASTI TOTALE:",(budget_tot-spesa))
        salvasuFile(budget_tot-spesa,(budg_att-spesa),0,0,0,0)
def c(budget_tot,budg_portieri, budg_dif,budg_centr,budg_att):
    if budg_centr> budget_tot:
        budg_centr=budget_tot
    reparto=centrocampisti(budget_tot,budg_centr)
    print(reparto)
    w_c=open("./src/centrocampisti.txt", "w")
    spesa=0
    for el in reparto:
        spesa+=int(reparto[el])
        buff=""+el+" : "+reparto[el]
        w_c.write(buff)
        w_c.write("\n")
    if spesa> int(budg_centr):
        print(colored("Hai speso troppo, verranno scalati crediti sugli attaccanti.",'red'))
        print("Crediti spesi in più:",abs(budg_centr-spesa))
        print("Att:",budg_att-abs(budg_centr-spesa))
        print("CREDITI RIMASTI TOTALE:",(budget_tot-spesa))
        salvasuFile(budget_tot,budget_tot-spesa,0,0,0,budg_att-abs(budg_centr-spesa))
    else:
        print("Crediti rimasti (verranno aggiunti agli attaccanti):",(budg_centr-spesa))
        print("Att:",budg_att+(budg_centr-spesa))
        print("CREDITI RIMASTI TOTALE:",(budget_tot-spesa))
        salvasuFile(budget_tot,budget_tot-spesa,0,0,0,budg_att+(budg_centr-spesa))
def d(budget_tot,budg_portieri, budg_dif,budg_centr,budg_att):
    if budg_dif> budget_tot:
        budg_dif=budget_tot
    reparto=(difensori(budget_tot,budg_dif))
    print(reparto)
    w_d=open("./src/difensori.txt", "w")
    spesa=0
    for el in reparto:
        spesa+=int(reparto[el])
        buff=""+el+" : "+reparto[el]
        w_d.write(buff)
        w_d.write("\n")
    if spesa> int(budg_dif):
        print("Hai speso troppo, verranno scalati crediti sui centrocampisti.")
        print("Crediti spesi in più:",abs(budg_dif-spesa))
        print("Centr:",budg_centr-abs(budg_dif-spesa))
        print("Att:",budg_att+(budg_dif-spesa))
        print("CREDITI RIMASTI TOTALE:",(budget_tot-spesa))
        salvasuFile(budget_tot,budget_tot-spesa,0,0,budg_centr-abs(budg_dif-spesa),budg_att+(budg_dif-spesa))
    else:
        print("Crediti rimasti (verranno aggiunti agli attaccanti):",(budg_dif-spesa))
        print("Cent:",budg_centr)
        print("Att:",budg_att+(budg_dif-spesa))
        print("CREDITI RIMASTI TOTALE:",(budget_tot-spesa))
        salvasuFile(budget_tot,budget_tot-spesa,0,0,budg_centr,budg_att+(budg_dif-spesa))
def p(budget_tot,budg_portieri, budg_dif,budg_centr,budg_att):
    w_p=open("./src/portieri.txt", "w")
    print("BUDGET PORTIERI:",budg_portieri)
    print("Lista portieri migliori a seconda del calendario: fattore casa e difficoltà partita:")
    print(genera_portieri(1))
    print("##############")
    print("PUNTA SU")
    print("1) VICARIO")
    print("2) GOLLINI")
    print("3) DRAGOWSKI")
    print("###############")
    spesa=0
    j=1
    while(j<4):
        
        p=input("Inserire il portiere #"+str(j)+":")
        prezzi=input("Inserire i crediti spesi: ")
        
        try:
            spesa+=int(prezzi)
        except:
            print("Inserire un valore intero.")
            continue
        buff=""+p.upper()+" : "+prezzi
        w_p.write(buff)
        w_p.write("\n")
        spesa+=int(prezzi)
        j+=1
    
    
    if spesa> int(budg_portieri):
        print("Hai speso troppo, verranno scalati crediti sui difensori.")
        print("Crediti spesi in più:",abs(budg_portieri-spesa))
        print("Dif:",budg_dif-abs(budg_portieri-spesa))
        print("Cent:",budg_centr)
        print("Att:",budg_att+(budg_portieri-spesa))
        print("CREDITI RIMASTI TOTALE:",(budget_tot-spesa))
        salvasuFile(budget_tot,budget_tot-spesa,0,budg_dif-abs(budg_portieri-spesa),budg_centr,budg_att+(budg_portieri-spesa))
    else:
        print("Crediti rimasti (verranno aggiunti agli attaccanti):",(budg_portieri-spesa))
        print("Dif:",budg_dif)
        print("Cent:",budg_centr)
        print("Att:",budg_att+(budg_portieri-spesa))
        print("CREDITI RIMASTI TOTALE:",(budget_tot-spesa))
        salvasuFile(budget_tot,budget_tot-spesa,0,budg_dif,budg_centr,budg_att+(budg_portieri-spesa))
def salvaTutto():
    
    w_p=open("./src/portieri.txt", "r")
    p=w_p.readlines()
    w_p.close()
    w_p=open("./src/difensori.txt", "r")
    d=w_p.readlines()
    w_p.close()
    w_p=open("./src/centrocampisti.txt", "r")
    c=w_p.readlines()
    w_p.close()
    w_p=open("./src/attaccanti.txt", "r")
    a=w_p.readlines()
    w_p.close()
    
    w_f=open("./SQUADRAFINALE.txt", "w")
    
    for el in p:
        w_f.write(el)
        w_f.write("\n")
    for el in d:
        w_f.write(el)
        w_f.write("\n")
    for el in c:
        w_f.write(el)
        w_f.write("\n")
    for el in a:
        w_f.write(el)
        w_f.write("\n")        
    w_f.close()
def salvasuFile(tot,rimasti,port,dif,centr,att):
    t=str(tot)
    r=str(rimasti)
    p=str(port)
    d=str(dif)
    c=str(centr)
    a=str(att)
    with open("./src/crediti.txt", "w") as fin:
        el="crediti_iniziali="+t
        fin.write(el)
        fin.write("\n")
        el="crediti_rimasti="+r
        fin.write(el)
        fin.write("\n")
        el="crediti_portieri="+p
        fin.write(el)
        fin.write("\n")
        el="crediti_difensori="+d
        fin.write(el)
        fin.write("\n")        
        el="crediti_centrocampisti="+c
        fin.write(el)
        fin.write("\n")         
        el="crediti_attaccanti="+a
        fin.write(el)
        fin.write("\n")   
        input("Premere Invio per continuare ")
      

def aggiorna_rigoristi():
    try:
        
        l=rigoristi()
        if len(l)==0:
            return 1
        f=open("./src/rigoristi.txt","w")
        for el in l:
            f.write(el.upper())
            f.write("\n")
        f.close()
        return 0
    except:
        return 1
    
def readCredito():
    with open("./src/crediti.txt", "r") as fin:
            linee=fin.readlines()
    budget_tot=linee[0].split("=")[1].split("\n")[0]
    crediti_rimasti=linee[1].split("=")[1].split("\n")[0]
    budg_portieri=linee[2].split("=")[1].split("\n")[0]
    budg_dif=linee[3].split("=")[1].split("\n")[0]
    budg_centr=linee[4].split("=")[1].split("\n")[0]
    budg_att=linee[5].split("=")[1].split("\n")[0]    
    return budget_tot,crediti_rimasti,budg_portieri,budg_dif,budg_centr,budg_att
    
def generaCategorie():
    
    p=lista_portieri()

    with open("./categorie/portieri.txt","w") as w:
        w.write(str(p))
    w.close()
    
    d=lista_difensori()

    with open("./categorie/difensori.json","w") as w:
        json.dump(d, w, indent=4)
    w.close()
    
    c=lista_centrocampisti()
    with open("./categorie/centrocampisti.json","w") as w:
        json.dump(c, w, indent=4)
    w.close()    
    
    a=lista_attaccanti()
    with open("./categorie/attaccanti.json","w") as w:
        json.dump(a, w, indent=4)
    w.close()
    

    
def main():
    
    os.system('CLS')
    os.system('color')
    #f = Figlet(font='slant')
    #print(colored(f.renderText('Fantacalcio di Carlotto'),'yellow'))

    print("Generazione file di sistema in corso, attendere...")
    try:
        if not path.exists("./src/"):
            os.makedirs("./src/")
            w_p=open("./src/portieri.txt", "w")
            w_d=open("./src/difensori.txt", "w")
            w_c=open("./src/centrocampisti.txt", "w")
            w_a=open("./src/attaccanti.txt", "w")
            w_p.close()    
            w_d.close()
            w_c.close()
            w_a.close()
        if not path.exists("./categorie/"):
            os.makedirs("./categorie/")
        if not path.exists("./src/portieri.txt"):
            w_p=open("./src/portieri.txt", "w")
            w_p.close()
        if not path.exists("./src/difensori.txt"):
            w_d=open("./src/difensori.txt", "w")
            w_d.close()
        if not path.exists("./src/centrocampisti.txt"):
            w_c=open("./src/centrocampisti.txt", "w")
            w_c.close()
        if not path.exists("./src/attaccanti.txt"):
            w_a=open("./src/attaccanti.txt", "w")
            w_a.close()
        
        generaCategorie()
        pertit()
        getInfortunati()
    except:
        os.system('CLS')
        #print(colored(f.renderText('Fantacalcio di Carlotto'),'yellow'))
        print(colored("Errore nella generazione dei file di sistema, esco.",'red'))
        exit()
    os.system('CLS')
    #print(colored(f.renderText('Fantacalcio di Carlotto'),'yellow'))
    print(colored("Generazione file di sistema completata.",'green'))
    print("Lettura dei crediti disponibili...")
    budget_tot,crediti_rimasti,budg_portieri,budg_dif,budg_centr,budg_att=readCredito()
    
    
    os.system('CLS')
    #print(colored(f.renderText('Fantacalcio di Carlotto'),'yellow'))
    print(colored("Generazione file di sistema completata.",'green'))
    print(colored("Lettura dei crediti disponibili completata",'green'))
    print("Aggiornamento listone...")
    r=calcola_quotazioni()
    ok=0
    ok2=0
    if r==0:
        os.system('CLS')
        #print(colored(f.renderText('Fantacalcio di Carlotto'),'yellow'))
        print(colored("Generazione file di sistema completata.",'green'))
        print(colored("Lettura dei crediti disponibili completata",'green'))
        print(colored("Aggiornamento listone completato.",'green'))
    else:
        os.system('CLS')
        #print(colored(f.renderText('Fantacalcio di Carlotto'),'yellow'))
        print(colored("Generazione file di sistema completata.",'green'))
        print(colored("Lettura dei crediti disponibili completata",'green'))    
        print(colored("Errore nell'aggiornamento del listone.",'red'))
        ok=1
        
        
    print("Aggiornamento rigoristi...")
    r=aggiorna_rigoristi()
    if r==0:
        if ok==0:
            os.system('CLS')
            #print(colored(f.renderText('Fantacalcio di Carlotto'),'yellow'))
            print(colored("Generazione file di sistema completata.",'green'))
            print(colored("Lettura dei crediti disponibili completata",'green'))
            print(colored("Aggiornamento listone completato.",'green'))
            print(colored("Aggiornamento rigoristi completato.",'green'))
        else:
            os.system('CLS')
            #print(colored(f.renderText('Fantacalcio di Carlotto'),'yellow'))
            print(colored("Generazione file di sistema completata.",'green'))
            print(colored("Lettura dei crediti disponibili completata",'green'))
            print(colored("Errore nell'aggiornamento del listone.",'red'))
    else:
        if ok==0:
            os.system('CLS')
            #print(colored(f.renderText('Fantacalcio di Carlotto'),'yellow'))
            print(colored("Generazione file di sistema completata.",'green'))
            print(colored("Lettura dei crediti disponibili completata",'green'))
            print(colored("Aggiornamento listone completato.",'green'))
            print(colored("Errore nell'aggiornamento dei rigoristi.",'red'))
            ok2=1
        else:
            os.system('CLS')
            #print(colored(f.renderText('Fantacalcio di Carlotto'),'yellow'))
            print(colored("Generazione file di sistema completata.",'green'))
            print(colored("Lettura dei crediti disponibili completata",'green'))
            print(colored("Errore nell'aggiornamento del listone.",'red'))    
            print(colored("Errore nell'aggiornamento dei rigoristi.",'red'))
            ok2=1
        
    print("Aggiornamento classifica...")
    r=calcola_classifica()
    if r==0:
        if ok==0:
            if ok2==0:
                os.system('CLS')
                #print(colored(f.renderText('Fantacalcio di Carlotto'),'yellow'))
                print(colored("Generazione file di sistema completata.",'green'))
                print(colored("Lettura dei crediti disponibili completata",'green'))
                print(colored("Aggiornamento listone completato.",'green'))
                print(colored("Aggiornamento rigoristi completato.",'green'))
                print(colored("Aggiornamento classifica completato.",'green'))
            else:
                os.system('CLS')
                #print(colored(f.renderText('Fantacalcio di Carlotto'),'yellow'))
                print(colored("Generazione file di sistema completata.",'green'))
                print(colored("Lettura dei crediti disponibili completata",'green'))
                print(colored("Aggiornamento listone completato.",'green'))
                print(colored("Errore nell'aggiornamento dei rigoristi.",'red'))
                print(colored("Aggiornamento classifica completato.",'green'))                
        else:
            if ok2==0:
                os.system('CLS')
                #print(colored(f.renderText('Fantacalcio di Carlotto'),'yellow'))
                print(colored("Generazione file di sistema completata.",'green'))
                print(colored("Lettura dei crediti disponibili completata",'green'))
                print(colored("Errore nell'aggiornamento del listone.",'red'))
                print(colored("Aggiornamento rigoristi completato.",'green'))
                print(colored("Aggiornamento classifica completato.",'green'))   
            else:
                os.system('CLS')
                #print(colored(f.renderText('Fantacalcio di Carlotto'),'yellow'))
                print(colored("Generazione file di sistema completata.",'green'))
                print(colored("Lettura dei crediti disponibili completata",'green'))
                print(colored("Errore nell'aggiornamento del listone.",'red'))
                print(colored("Errore nell'aggiornamento dei rigoristi.",'red'))
                print(colored("Aggiornamento classifica completato.",'green'))           
                
    else:
        if ok==0:
            if ok2==0:
                os.system('CLS')
                #print(colored(f.renderText('Fantacalcio di Carlotto'),'yellow'))
                print(colored("Generazione file di sistema completata.",'green'))
                print(colored("Lettura dei crediti disponibili completata",'green'))
                print(colored("Aggiornamento listone completato.",'green'))
                print(colored("Aggiornamento rigoristi completato.",'green'))
                print(colored("Errore nell'aggiornamento della classifica.",'red'))
            else:
                os.system('CLS')
                #print(colored(f.renderText('Fantacalcio di Carlotto'),'yellow'))
                print(colored("Generazione file di sistema completata.",'green'))
                print(colored("Lettura dei crediti disponibili completata",'green'))
                print(colored("Aggiornamento listone completato.",'green'))
                print(colored("Errore nell'aggiornamento dei rigoristi.",'red'))
                print(colored("Errore nell'aggiornamento della classifica.",'red'))               
        else:
            if ok2==0:
                os.system('CLS')
                #print(colored(f.renderText('Fantacalcio di Carlotto'),'yellow'))
                print(colored("Generazione file di sistema completata.",'green'))
                print(colored("Lettura dei crediti disponibili completata",'green'))
                print(colored("Errore nell'aggiornamento del listone.",'red'))
                print(colored("Aggiornamento rigoristi completato.",'green'))
                print(colored("Errore nell'aggiornamento della classifica.",'red'))   
            else:
                os.system('CLS')
                #print(colored(f.renderText('Fantacalcio di Carlotto'),'yellow'))
                print(colored("Generazione file di sistema completata.",'green'))
                print(colored("Lettura dei crediti disponibili completata",'green'))
                print(colored("Errore nell'aggiornamento del listone.",'red'))
                print(colored("Errore nell'aggiornamento dei rigoristi.",'red'))
                print(colored("Errore nell'aggiornamento della classifica.",'red'))



 
   
    if not path.exists("./excel/calendario.xlsx") or not path.exists("./excel/giocatori.xlsx") or not path.exists("./excel/Quotazioni_Fantacalcio.xlsx") or not path.exists("./excel/classifica.xlsx"):
        ris=genera_excel()
        if ris!="OK":
            print(colored("Errore imprevisto, termino.",'red'))
            exit()
    print(colored("I file sono a posto.",'green'))
    while(True):
        
        print("1) Genera portieri")
        print("2) Genera difensori")
        print("3) Genera centrocampisti")
        print("4) Genera attaccanti")
        with open("./src/crediti.txt", "r") as fin:
            linee=fin.readlines()
        crediti_rimasti=linee[1].split("=")[1].split("\n")[0]
        scelta=input()
        if scelta!="1" and scelta!="2" and scelta!="3" and scelta!="4":
            print("Inserire una scelta valida.")
            input("Premere invio per continuare")
            os.system('CLS')
            #print(colored(f.renderText('Fantacalcio di Carlotto'),'yellow'))
            continue
        if scelta=="1":
            w_p=open("./src/portieri.txt", "r") 
            linee=w_p.readlines()
            w_p.close()
            if len(linee)==3:
                print(colored("Portieri già presenti.",'red'))
                input("Premere invio per continuare")
                os.system('CLS')
                #print(colored(f.renderText('Fantacalcio di Carlotto'),'yellow'))
                continue
            os.system('CLS')
            p(int(budget_tot),int(budg_portieri),int(budg_dif),int(budg_centr),int(budg_att))
            
            os.system('CLS')
            #print(colored(f.renderText('Fantacalcio di Carlotto'),'yellow'))
        elif scelta=="2":
            budget_tot,crediti_rimasti,budg_portieri,budg_dif,budg_centr,budg_att=readCredito()
            w_d=open("./src/difensori.txt", "r") 
            linee=w_d.readlines()
            w_d.close()
            if len(linee)==8:
                print(colored("Difensori già presenti.",'red'))
                input("Premere invio per continuare")
                os.system('CLS')
                #print(colored(f.renderText('Fantacalcio di Carlotto'),'yellow'))
                continue
            d(int(crediti_rimasti),int(budg_portieri),int(budg_dif),int(budg_centr),int(budg_att))
            os.system('CLS')
            #print(colored(f.renderText('Fantacalcio di Carlotto'),'yellow'))
        elif scelta=="3":
            budget_tot,crediti_rimasti,budg_portieri,budg_dif,budg_centr,budg_att=readCredito()
            w_c=open("./src/centrocampisti.txt", "r") 
            linee=w_c.readlines()
            w_c.close()
            if len(linee)==8:
                print(colored("Centrocampisti già presenti.",'red'))
                input("Premere invio per continuare")
                os.system('CLS')
                #print(colored(f.renderText('Fantacalcio di Carlotto'),'yellow'))
                continue        
            c(int(crediti_rimasti),int(budg_portieri),int(budg_dif),int(budg_centr),int(budg_att))
            os.system('CLS')
        elif scelta=="4":
            budget_tot,crediti_rimasti,budg_portieri,budg_dif,budg_centr,budg_att=readCredito()
            w_a=open("./src/attaccanti.txt", "r") 
            linee=w_a.readlines()
            w_a.close()
            if len(linee)==6:
                print(colored("Attaccanti già presenti, hai già completato il fanta.",'red'))
                input("Premere invio per continuare")
                os.system('CLS')
                #print(colored(f.renderText('Fantacalcio di Carlotto'),'yellow'))
                continue
            a(int(crediti_rimasti),int(budg_portieri),int(budg_dif),int(budg_centr),int(budg_att))
            salvaTutto()
            os.system('CLS')
            #print(colored(f.renderText('Fantacalcio di Carlotto'),'yellow'))
if __name__ == "__main__":
    main()





