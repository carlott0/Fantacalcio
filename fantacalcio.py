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

def calcola_calendario():
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
def calcola_quotazioni():
    #link ='https://www.fantacalcio.it//Servizi/Excel.ashx?type=0&r=1&t=1652767828000' vecchio
    #link="https://www.fantacalcio.it/api/v1/Excel/prices/17/1" nuovo
    
    if path.exists("./excel/Quotazioni_Fantacalcio.xlsx"):
        return 0
    
    if path.exists("./excel/q.xlsx"):
        data = pd.read_excel("./excel/q.xlsx", header=1)
        data.to_excel('./excel/Quotazioni_Fantacalcio.xlsx')
    else:
        print("Scaricare il file dal link: https://www.fantacalcio.it/api/v1/Excel/prices/17/1 e chiamarlo q.xlsx")
        return 1
    return 0

def calcola_giocatori():
    #link ='https://www.fantacalcio.it/Servizi/Excel.ashx?type=2&r=1&t=1614489243000&s=2020-21' link vecchio
    #link="https://www.fantacalcio.it/api/v1/Excel/stats/16/1"

        
    if path.exists("./excel/giocatori.xlsx"):
        return 0
    #TODO
    if path.exists("./excel/s.xlsx"):
        data = pd.read_excel("./excel/s.xlsx", header=1)
        data.to_excel('./excel/giocatori.xlsx')
    else:
        print("Scaricare il file dal link: https://www.fantacalcio.it/api/v1/Excel/stats/16/1 e chiamarlo q.xlsx")
        return 1
    return 0

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
                if value > 15 and casa==1:
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
    p=list(d_giocatori.loc[(d_giocatori['R'] == 'P') & (d_giocatori['Pg'] > 1)]['Nome'].values)
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
    if scelta==1:
        return ret_diz
    elif scelta==2:
        return ret_marks
    return
def dif(giocatore_chiamato,acquistati,budget_rimasto,x1,y1):
    giocatori_risultato=[]
    
    valori_risultato=[]
    tit_risultato=[]
    quotazioni=pd.read_excel("./excel/Quotazioni_Fantacalcio.xlsx", names=['Id','R','Nome','Squadra','Qt. A','Qt. I','Diff.'])
    quotazioni['Nome'] = quotazioni['Nome'].apply(lambda nome : nome.upper())
    da_comprare=8-len(acquistati)   
    x=pd.read_excel("./excel/giocatori.xlsx")
    x['Nome'] = x['Nome'].apply(lambda nome : nome.upper())

    t=x.loc[(x['R']=='D')]       
    ### funzione prezzo
    #x1 = [1,5,10,15,20,25,30]
    #y1 = [1,10,15,20,30,40,50]
    a,b,c = np.polyfit(x1, y1, 2)
    try:
        p=int(quotazioni[quotazioni['Nome'].str.contains(giocatore_chiamato.upper())]['Qt. A'].item())
    except:
        return 1,0,[]
    prezzo_probabile=a*p*p+b*p+c
    try:
        gf=(t[t['Nome'].str.contains(giocatore_chiamato.upper())]['Gf'].values[0])

    except:
        gf=0        

    print("Gol scorsa stagione:",gf)
    print("Prezzo di valore:",p)
    print("Prezzo probabile d'asta:",prezzo_probabile)
    difensori=quotazioni.loc[(quotazioni['R'] == 'D')]
    ds=list(quotazioni.loc[(quotazioni['R'] == 'D')]['Nome'].values)
    prezzo_ris=int(quotazioni[quotazioni['Nome'].str.contains(giocatore_chiamato.upper())]['Qt. A'].item())
    squadre=[]
    valore_reparto=0
    valore=0
    if len(acquistati)!=0:
        for g in acquistati:
            squadre.append(difensori[difensori['Nome'].str.contains(g.upper())]['Squadra'].item())
            valore_reparto+=int(quotazioni[quotazioni['Nome'].str.contains(g.upper())]['Qt. A'].item())
        valore=round(valore_reparto/len(acquistati),0)
    if  budget_rimasto -da_comprare <= 0:
        print("Si ha sforato il budget, verranno suggeriti solo giocatori a poco")
        ds=list(quotazioni.loc[(quotazioni['R'] == 'D') & (quotazioni['Qt. A'] == 1)]['Nome'].values)
        for k in range(0,da_comprare):
            d=random.choice(ds)
            if d.upper() not in acquistati:
                acquistati.append(d)
                
                prezzo=1
                budget_rimasto=budget_rimasto-1
                try:
                    tit=(t[t['Nome'].str.contains(ax.upper())]['Pg'].values[0])
                   
                except:
                    tit=1  

                titolarieta=int(tit)
                tit_risultato.append(titolarieta)
                valori_risultato.append("1")
                giocatori_risultato.append(d)
                k+=1
        return 0,prezzo_ris,tit_risultato
    while(len(acquistati)!=8):
        d=random.choice(ds)
        if len(t[t['Nome'].str.contains(d.upper())]['Pg'])==0:
            
            continue
        tit=int(t[t['Nome'].str.contains(d.upper())]['Pg'].values[0])
        if int(tit)==0:
            
            continue
        titolarieta=int(tit)
        try:
            gf=(t[t['Nome'].str.contains(d.upper())]['Gf'].values[0])
        except:
            gf=0        
        
        if d.upper() not in acquistati and (titolarieta>10 or gf>3):
            if len(quotazioni[quotazioni['Nome'].str.contains(d.upper())]['Qt. A'])>1:
                
                continue
            v=int(quotazioni[quotazioni['Nome'].str.contains(d.upper())]['Qt. A'].item())
            prezzo_previsto=int(a*v*v+b*v+c)
            new_budg=budget_rimasto-v
            if new_budg<=0:
                
                continue
            if new_budg > da_comprare:
                acquistati.append(d)
                da_comprare-=1
                prezzo=budget_rimasto-new_budg
                budget_rimasto=new_budg
                tit_risultato.append(titolarieta)
                valori_risultato.append(v)
                giocatori_risultato.append(d)
                
                ds=list(quotazioni.loc[(quotazioni['R'] == 'D') & ((quotazioni['Qt. A'])<= budget_rimasto)]['Nome'].values)
                if d in ds:
                    ds.remove(d)
            if budget_rimasto <= da_comprare:
                ds=list(quotazioni.loc[(quotazioni['R'] == 'D') & (quotazioni['Qt. A'] == 1)]['Nome'].values)
                for k in range(0,da_comprare):
                    d=random.choice(ds)
                    if d not in acquistati:
                        acquistati.append(d)
                        
                        prezzo=1
                        budget_rimasto=budget_rimasto-1
                        try:
                            tit=(t[t['Nome'].str.contains(ax.upper())]['Pg'].values[0])
                        except:
                            tit=1
                        titolarieta=int(tit)
                        tit_risultato.append(titolarieta)
                        valori_risultato.append("1")
                        giocatori_risultato.append(d)
                        k+=1
                return 0,prezzo_ris,tit_risultato
            else:
                
                continue
        else:
            continue
    return 0,prezzo_ris,tit_risultato
def difensori(u,budget):
    i=1
    acquistati=[]
    reparto_finale={}
    new_acquisti=[]
    valore_prima=0
    valori=[]
    valore_reparto=0
    quotazioni=pd.read_excel("./excel/Quotazioni_Fantacalcio.xlsx", names=['Id','R','Nome','Squadra','Qt. A','Qt. I','Diff.'])
    x=pd.read_excel("./excel/giocatori.xlsx")
    quotazioni['Nome'] = quotazioni['Nome'].apply(lambda nome : nome.upper())
    x['Nome'] = x['Nome'].apply(lambda nome : nome.upper())
    t=x.loc[(x['R']=='D')]       
    quotazioni=quotazioni.loc[(quotazioni['R']=='D')]     
    ### funzione prezzo
    x1 = [1,5,10,15,20,25,30]
    y1 = [1,10,15,20,30,40,50]
      
    
    while(i!=9):
        a,b,c = np.polyfit(x1, y1, 2)
        #input("Premere Invio per continuare ")
        os.system('CLS')      
        print("Budget Totale:",u)
        print("Budget Reparto:",budget)
        for el in valori:
            valore_reparto+=el/(len(acquistati)+1)
        print("#"+str(i))
        giocatore=input("Difensore ")
        if giocatore in reparto_finale.keys():
            print("Giocatore già acquistato.")
            input("Premere Invio per continuare ")
            continue
            
        trovato=0
        for g in quotazioni['Nome']:
            if giocatore.upper()==g.upper():
                trovato=1
                break
        if trovato==0:
            gx=calcola_giocatore_simile(giocatore,quotazioni)
            print("Nessun giocatore con questo nome, forse si intendeva", gx,"?[Y,n]")
            scelta=input()
            if (scelta !="y" or scelta !="Y") and len(scelta)>0:
                print("Giocatore non trovato, riprova.")
                input("Premere Invio per continuare ")
                #acquistati.remove(giocatore)
                acquistati=[]
                continue
            else:
                giocatore=gx
        for el in reparto_finale.keys():
            acquistati.append(el)
        acquistati.append(giocatore)
        ok,prezzo,tit_risultato=dif(giocatore,acquistati,budget,x1,y1)

        print("Possibile squadra:")
        #print("Nome\t\tPrezzo\t\tGol scorso anno\t\tTitolarietà")
        lista_print=[[]]
        ptpr=0
        prt=0
        for el in acquistati:
            if el in reparto_finale.keys():
                p=int(reparto_finale[el])
                prezzo_probabile=p
            else:    
                try:
                    p=int(quotazioni[quotazioni['Nome'].str.contains(el.upper())]['Qt. A'].item())
                except:
                    p=0
                prezzo_probabile=a*p*p+b*p+c
            ptpr+=p
            prt+=prezzo_probabile
            try:
                gf=(t[t['Nome'].str.contains(el.upper())]['Gf'].values[0])
            except:
                gf=0
            try:
                tit=int(t[t['Nome'].str.contains(el.upper())]['Pg'].values[0])
            except:
                tit=0
            if el.upper() == giocatore.upper():
                tx=round(round(int(tit)/38,2)*100,2)
            lista_print.append([el,p,int(prezzo_probabile),gf,str(round(round(int(tit)/38,2)*100,2))+"%"])
            #print(el,"\t\t",p,"\t\t",gf,"\t\t",round(round(int(tit)/38,2)*100,2),"%")
        lista_print.append(["","","","",""])
        lista_print.append(["Prezzo Totale Previsto:",int(ptpr),"","",""])
        lista_print.append(["Prezzo Totale Probabile:",int(prt),"","",""])
        prezzo=int(prezzo)    
        tit=0
        for el in tit_risultato:
            tit+=round(round(int(el)/38,2)*100,2)
        lista_print.append(["Indice titolarietà medio squadra:",str(round(tit/8,2))+"%","","",""])
        print(tabulate(lista_print, headers=["Nome", "Prezzo Previsto","Prezzo Probabile", "Gol Scorso Anno","Titolarietà"]))
        lista_print.clear()

        valore_temp=(valore_reparto+prezzo)/(len(acquistati)+1)
        if valore_temp>valore_prima:
        
            print("+",int((valore_temp-valore_prima)*100),"% qualità alla squadra.")
        else:
            print("",int((valore_temp-valore_prima)*100),"% qualità alla squadra.")
        if prezzo>budget-(8-len(new_acquisti)):
            print("Mmm, costa tanto, circa ",int(a*prezzo*prezzo+b*prezzo+c))

        elif valore_temp > valore_prima and tx>55:
            print("Si acquistalo ma al massimo spendi:",prezzo)
            print("Probabile prezzo d'asta: circa",int(a*prezzo*prezzo+b*prezzo+c))
        else:
            print("Non acquistarlo.")
        valore_reparto=0
        quanto=input("Se lo hai comprato, a quanto? (se no premere 0) ")
        if len(quanto)==0:
            q=int(input("A quanto è andato? "))
            x1.append(prezzo)
            y1.append(q)        
            print("", end="\r")
            acquistati=[]
            continue        
        try:
            if int(quanto)>0:
                x1.append(prezzo)
                y1.append(int(quanto))            
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
            continue
        print("", end="\r")
    return reparto_finale
def centr(giocatore_chiamato,acquistati,budget_rimasto,x1,y1):
    giocatori_risultato=[]
    valori_risultato=[]
    tit_risultato=[]
    quotazioni=pd.read_excel("./excel/Quotazioni_Fantacalcio.xlsx", names=['Id','R','Nome','Squadra','Qt. A','Qt. I','Diff.'])
    quotazioni['Nome'] = quotazioni['Nome'].apply(lambda nome : nome.upper())
    da_comprare=8-len(acquistati)
    x=pd.read_excel("./excel/giocatori.xlsx")
    x['Nome'] = x['Nome'].apply(lambda nome : nome.upper())
    t=x.loc[(x['R']=='C')]
    ### funzione prezzo
    #x1 = [1,5,10,15,20,25,30,35]
    #y1 = [1,10,20,30,35,40,50,60]
    a,b,c = np.polyfit(x1, y1, 2)
    try:
        p=int(quotazioni[quotazioni['Nome'].str.contains(giocatore_chiamato.upper())]['Qt. A'].item())
    except:
        return 1,0,[]
    prezzo_probabile=a*p*p+b*p+c
    try:
        gf=(t[t['Nome'].str.contains(giocatore_chiamato.upper())]['Gf'].values[0])
    except:
        gf=0        

    print("Gol scorsa stagione:",gf)
    print("Prezzo di valore:",p)
    print("Prezzo probabile d'asta:",prezzo_probabile)
    centrocampisti=quotazioni.loc[(quotazioni['R'] == 'C')]
    cs=list(quotazioni.loc[(quotazioni['R'] == 'C')]['Nome'].values)
    prezzo_ris=int(quotazioni[quotazioni['Nome'].str.contains(giocatore_chiamato.upper())]['Qt. A'].item())
    squadre=[]
    valore_reparto=0
    valore=0
    if len(acquistati)!=0:
        for g in acquistati:
            squadre.append(centrocampisti[centrocampisti['Nome'].str.contains(g.upper())]['Squadra'].item())
            valore_reparto+=int(quotazioni[quotazioni['Nome'].str.contains(g.upper())]['Qt. A'].item())
        valore=round(valore_reparto/len(acquistati),0)
    i=0
    if  budget_rimasto -da_comprare <= 0:
        print("Si ha sforato il budget, verranno suggeriti solo giocatori a poco")
        cs=list(quotazioni.loc[(quotazioni['R'] == 'C') & (quotazioni['Qt. A'] == 1)]['Nome'].values)
        for k in range(0,da_comprare):
            cx=random.choice(cs)
            if cx.upper() not in acquistati:
                acquistati.append(cx)
                i=0
                prezzo=1
                budget_rimasto=budget_rimasto-1
                try:
                    tit=(t[t['Nome'].str.contains(ax.upper())]['Pg'].values[0])
                except:
                    tit=1
                titolarieta=int(tit)
                tit_risultato.append(titolarieta)
                valori_risultato.append("1")
                giocatori_risultato.append(cx)
                k+=1
        return 0,prezzo_ris,tit_risultato
    while(len(acquistati)!=8):
        cx=random.choice(cs)
        if len(t[t['Nome'].str.contains(cx.upper())]['Pg'])==0:
            #forse giocatore nuovo, ma non lo considero
            continue
        tit=int(t[t['Nome'].str.contains(cx.upper())]['Pg'].values[0])
        if int(tit)==0:
            continue
        titolarieta=int(tit)
        
        try:
            gf=(t[t['Nome'].str.contains(cx.upper())]['Gf'].values[0])
        except:
            gf=0        
        
        if cx.upper() not in acquistati and (titolarieta>10 or gf>5):
            if len(quotazioni[quotazioni['Nome'].str.contains(cx.upper())]['Qt. A'])>1:
                continue
            v=int(quotazioni[quotazioni['Nome'].str.contains(cx.upper())]['Qt. A'].item())
            prezzo_previsto=int(a*v*v+b*v+c)
            new_budg=budget_rimasto-v
            if new_budg<=0:
                continue
            if new_budg > da_comprare:
                acquistati.append(cx)
                da_comprare-=1
                prezzo=budget_rimasto-new_budg
                budget_rimasto=new_budg
                tit_risultato.append(titolarieta)
                valori_risultato.append(v)
                giocatori_risultato.append(cx)
                cs=list(quotazioni.loc[(quotazioni['R'] == 'C') & ((quotazioni['Qt. A'])<= budget_rimasto)]['Nome'].values)
                if cx in cs:
                    cs.remove(cx)
            if budget_rimasto <= da_comprare:
                cs=list(quotazioni.loc[(quotazioni['R'] == 'C') & (quotazioni['Qt. A'] == 1)]['Nome'].values)
                for k in range(0,da_comprare):
                    cx=random.choice(cs)
                    if cx not in acquistati:
                        acquistati.append(cx)
                        prezzo=1
                        budget_rimasto=budget_rimasto-1
                        try:
                            tit=(t[t['Nome'].str.contains(ax.upper())]['Pg'].values[0])
                        except:
                            tit=1
                        titolarieta=int(tit)
                        tit_risultato.append(titolarieta)
                        valori_risultato.append("1")
                        giocatori_risultato.append(cx)
                        k+=1
                return 0,prezzo_ris,tit_risultato
            else:
                continue
        else:
            continue
    return 0,prezzo_ris,tit_risultato
def centrocampisti(u,budget):
    i=1
    acquistati=[]
    reparto_finale={}
    new_acquisti=[]
    valore_prima=0
    valori=[]
    valore_reparto=0
    quotazioni=pd.read_excel("./excel/Quotazioni_Fantacalcio.xlsx", names=['Id','R','Nome','Squadra','Qt. A','Qt. I','Diff.'])
    x=pd.read_excel("./excel/giocatori.xlsx")
    x['Nome'] = x['Nome'].apply(lambda nome : nome.upper())
    quotazioni['Nome'] = quotazioni['Nome'].apply(lambda nome : nome.upper())
    t=x.loc[(x['R']=='C')]       
    quotazioni=quotazioni.loc[(quotazioni['R']=='C')]     

    
    x1 = [1,5,10,15,20,25,30,35]
    y1 = [1,10,20,30,35,40,50,60]
    while(i!=9):
        #input("Premere Invio per continuare ")
        a,b,c = np.polyfit(x1, y1, 2)

        os.system('CLS')   
        print("Budget Totale:",u)        
        print("Budget Reparto:",budget)
        for el in valori:
            valore_reparto+=el/(len(acquistati)+1)
        print("#"+str(i))
        giocatore=input("Centrocampista ")
        if giocatore in reparto_finale.keys():
            print("Giocatore già acquistato.")
            input("Premere Invio per continuare ")
            acquistati=[]
            continue
        trovato=0
        for g in quotazioni['Nome']:
            if giocatore.upper()==g.upper():
                trovato=1
                break
        if trovato==0:
            gx=calcola_giocatore_simile(giocatore,quotazioni)
            print("Nessun giocatore con questo nome, forse si intendeva", gx,"?[Y,n]")
            scelta=input()
            if (scelta !="y" or scelta !="Y") and len(scelta)>0:
                print("Giocatore non trovato, riprova.")
                input("Premere Invio per continuare ")
                #acquistati.remove(giocatore)
                acquistati=[]
                continue
            else:
                giocatore=gx
        for el in reparto_finale.keys():
            acquistati.append(el)
        acquistati.append(giocatore)
        ok,prezzo,tit_risultato=centr(giocatore,acquistati,budget,x1,y1)

        print("Possibile squadra:")
        #print("Nome\t\tPrezzo\t\tGol scorso anno\t\tTitolarietà")
        lista_print=[[]]
        ptpr=0
        prt=0
        for el in acquistati:
            if el in reparto_finale.keys():
                p=int(reparto_finale[el])
                prezzo_probabile=p
            else:    
                try:
                    p=int(quotazioni[quotazioni['Nome'].str.contains(el.upper())]['Qt. A'].item())
                except:
                    p=0
                prezzo_probabile=a*p*p+b*p+c
            ptpr+=p
            prt+=prezzo_probabile
            try:
                gf=(t[t['Nome'].str.contains(el.upper())]['Gf'].values[0])
            except:
                gf=0
            try:
                tit=int(t[t['Nome'].str.contains(el.upper())]['Pg'].values[0])
            except:
                tit=0
            if el.upper() == giocatore.upper():
                    tx=round(round(int(tit)/38,2)*100,2)
            lista_print.append([el,p,int(prezzo_probabile),gf,str(round(round(int(tit)/38,2)*100,2))+"%"])
            #print(el,"\t\t",p,"\t\t",gf,"\t\t",round(round(int(tit)/38,2)*100,2),"%")
        lista_print.append(["","","","",""])
        lista_print.append(["Prezzo Totale Previsto:",int(ptpr),"","",""])
        lista_print.append(["Prezzo Totale Probabile:",int(prt),"","",""])
        prezzo=int(prezzo)    
        tit=0
        for el in tit_risultato:
            tit+=round(round(int(el)/38,2)*100,2)
        lista_print.append(["Indice titolarietà medio squadra:",str(round(tit/8,2))+"%","","",""])
        print(tabulate(lista_print, headers=["Nome", "Prezzo Previsto","Prezzo Probabile", "Gol Scorso Anno","Titolarietà"]))
        lista_print.clear()
        valore_temp=(valore_reparto+prezzo)/(len(acquistati)+1)
        if valore_temp>valore_prima:
        
            print("+",int((valore_temp-valore_prima)*100),"% qualità alla squadra.")
        else:
            print("",int((valore_temp-valore_prima)*100),"% qualità alla squadra.")
        if prezzo>budget-(8-len(new_acquisti)):
            print("Mmm, costa tanto, circa ",int(a*prezzo*prezzo+b*prezzo+c))
        elif valore_temp > valore_prima and tx > 55:
            print("Si acquistalo ma al massimo spendi:",prezzo)
            print("Probabile prezzo d'asta: circa",int(a*prezzo*prezzo+b*prezzo+c))
        else:
            print("Non acquistarlo.")
        valore_reparto=0
        quanto=input("Se lo hai comprato, a quanto? (se no premere 0) ")
        if len(quanto)==0:
            q=int(input("A quanto è andato? "))
            x1.append(prezzo)
            y1.append(q)        
            print("", end="\r")
            acquistati=[]
            continue        
        try:
            if int(quanto)>0:
                x1.append(prezzo)
                y1.append(int(quanto))            
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
            continue
        print("", end="\r")
    return reparto_finale
def att(giocatore_chiamato,acquistati,budget_rimasto,x1,y1):
    giocatori_risultato=[]
    valori_risultato=[]
    tit_risultato=[]    
    quotazioni=pd.read_excel("./excel/Quotazioni_Fantacalcio.xlsx", names=['Id','R','Nome','Squadra','Qt. A','Qt. I','Diff.'])
    quotazioni['Nome'] = quotazioni['Nome'].apply(lambda nome : nome.upper())
    da_comprare=6-len(acquistati)
    x=pd.read_excel("./excel/giocatori.xlsx")
    x['Nome'] = x['Nome'].apply(lambda nome : nome.upper())
    t=x.loc[(x['R']=='A')]
    ### funzione prezzo
    #x1 = [1,5,10,15,20,25,30,35,40,45]
    #y1 = [1,10,30,40,50,70,90,120,150,180]
    a,b,c = np.polyfit(x1, y1, 2)
    try:
        p=int(quotazioni[quotazioni['Nome'].str.contains(giocatore_chiamato.upper())]['Qt. A'].item())
    except:
        return 1,0,[]
    prezzo_probabile=a*p*p+b*p+c
    
    try:
        gf=(t[t['Nome'].str.contains(giocatore_chiamato.upper())]['Gf'].values[0])
    except:
        gf=0        

    print("Gol scorsa stagione:",gf)
    print("Prezzo di valore:",p)
    print("Prezzo probabile d'asta:",prezzo_probabile)
    attaccanti=quotazioni.loc[(quotazioni['R'] == 'A')]
    ass=list(quotazioni.loc[(quotazioni['R'] == 'A')]['Nome'].values)
    prezzo_ris=int(quotazioni[quotazioni['Nome'].str.contains(giocatore_chiamato.upper())]['Qt. A'].item())
    squadre=[]
    valore_reparto=0
    valore=0
    if len(acquistati)!=0:
        for g in acquistati:
            squadre.append(attaccanti[attaccanti['Nome'].str.contains(g.upper())]['Squadra'].item())
            valore_reparto+=int(quotazioni[quotazioni['Nome'].str.contains(g.upper())]['Qt. A'].item())
        valore=round(valore_reparto/len(acquistati),0)
    
    if  budget_rimasto -da_comprare <= 0:
        print("Si ha sforato il budget, verranno suggeriti solo giocatori a poco")
        ass=list(quotazioni.loc[(quotazioni['R'] == 'A') & (quotazioni['Qt. A'] == 1)]['Nome'].values)
        for k in range(0,da_comprare):
            ax=random.choice(ass)
            if ax.upper() not in acquistati:
                acquistati.append(ax)
                prezzo=1
                budget_rimasto=budget_rimasto-1
                try:
                
                    tit=(t[t['Nome'].str.contains(ax.upper())]['Pg'].values[0])
                except:
                    tit=1
                titolarieta=int(tit)
                tit_risultato.append(titolarieta)
                valori_risultato.append("1")
                giocatori_risultato.append(ax)
                k+=1
        return 0,prezzo_ris,tit_risultato
    while(len(acquistati)!=6):
        ax=random.choice(ass)
        if len(t[t['Nome'].str.contains(ax.upper())]['Pg'])==0:
            continue
        tit=int(t[t['Nome'].str.contains(ax.upper())]['Pg'].values[0])
        if int(tit)==0:
            continue
        titolarieta=int(tit)
        try:
            gf=(t[t['Nome'].str.contains(d.upper())]['Gf'].values[0])
        except:
            gf=0        
        
        if ax.upper() not in acquistati and (titolarieta>10 or gf>0):
            if len(quotazioni[quotazioni['Nome'].str.contains(ax.upper())]['Qt. A'])>1:
                continue
            v=int(quotazioni[quotazioni['Nome'].str.contains(ax.upper())]['Qt. A'].item())
            prezzo_previsto=int(a*v*v+b*v+c)
            new_budg=budget_rimasto-prezzo_previsto
            if new_budg<=0:
                new_budg=budget_rimasto-v
                continue
            if new_budg > da_comprare:
                acquistati.append(ax)
                da_comprare-=1
                prezzo=budget_rimasto-new_budg
                budget_rimasto=new_budg
                tit_risultato.append(titolarieta)
                valori_risultato.append(v)
                giocatori_risultato.append(ax)
                
                ass=list(quotazioni.loc[(quotazioni['R'] == 'A') & ((quotazioni['Qt. A'])<= budget_rimasto)]['Nome'].values)
                if ax in ass:
                    ass.remove(ax)
            if budget_rimasto <= da_comprare:
                ass=list(quotazioni.loc[(quotazioni['R'] == 'A') & (quotazioni['Qt. A'] == 1)]['Nome'].values)
                for k in range(0,da_comprare):
                    ax=random.choice(ass)
                    if ax not in acquistati:
                        acquistati.append(ax)
                        
                        prezzo=1
                        budget_rimasto=budget_rimasto-1
                        try:
                            tit=(t[t['Nome'].str.contains(ax.upper())]['Pg'].values[0])
                        except:
                            tit=1
                        titolarieta=int(tit)
                        tit_risultato.append(titolarieta)
                        valori_risultato.append("1")
                        giocatori_risultato.append(ax)
                        k+=1
                return 0,prezzo_ris,tit_risultato
            else:
                
                continue
        else:
            continue
    return 0,prezzo_ris,tit_risultato
def attaccanti(u,budget):
    i=1
    acquistati=[]
    reparto_finale={}
    new_acquisti=[]
    valore_prima=0
    valori=[]
    valore_reparto=0
    quotazioni=pd.read_excel("./excel/Quotazioni_Fantacalcio.xlsx", names=['Id','R','Nome','Squadra','Qt. A','Qt. I','Diff.'])
    quotazioni['Nome'] = quotazioni['Nome'].apply(lambda nome : nome.upper())
    x=pd.read_excel("./excel/giocatori.xlsx")
    x['Nome'] = x['Nome'].apply(lambda nome : nome.upper())
    t=x.loc[(x['R']=='A')]
    quotazioni=quotazioni.loc[(quotazioni['R']=='A')]     
    
    x1 = [1,5,10,15,20,25,30,35,40,45]
    y1 = [1,10,30,40,50,70,90,120,150,180]
    
    while(i!=7):
        a,b,c = np.polyfit(x1, y1, 2)
        #input("Premere Invio per continuare ")
        os.system('CLS')        
        print("Budget Totale:",u)
        print("Budget Reparto:",budget)
        
        for el in valori:
            valore_reparto+=el/(len(acquistati)+1)
        print("#"+str(i))
        giocatore=input("Attaccante ")
        if giocatore in reparto_finale.keys():
            print("Giocatore già acquistato.")
            input("Premere Invio per continuare ")
            acquistati=[]
            continue
            
        trovato=0
        for g in quotazioni['Nome']:
            if giocatore.upper()==g.upper():
                trovato=1
                break
        if trovato==0:
            gx=calcola_giocatore_simile(giocatore,quotazioni)
            print("Nessun giocatore con questo nome, forse si intendeva", gx,"?[Y,n]")
            scelta=input()
            if (scelta !="y" or scelta !="Y") and len(scelta)>0:
                print("Giocatore non trovato, riprova.")
                input("Premere Invio per continuare ")
                #acquistati.remove(giocatore)
                acquistati=[]
                continue
            else:
                giocatore=gx
        for el in reparto_finale.keys():
            acquistati.append(el)
        acquistati.append(giocatore)
        ok,prezzo,tit_risultato=att(giocatore,acquistati,budget,x1,y1)

        print("Possibile squadra:")
        #print("Nome\t\tPrezzo\t\tGol scorso anno\t\tTitolarietà")
        lista_print=[[]]
        ptpr=0
        prt=0
        for el in acquistati:
            if el in reparto_finale.keys():
                p=int(reparto_finale[el])
                prezzo_probabile=p
            else:    
                try:
                    p=int(quotazioni[quotazioni['Nome'].str.contains(el.upper())]['Qt. A'].item())
                except:
                    p=0
                prezzo_probabile=a*p*p+b*p+c
            ptpr+=p
            prt+=prezzo_probabile
            try:
                gf=(t[t['Nome'].str.contains(el.upper())]['Gf'].values[0])
            except:
                gf=0
            try:
                tit=int(t[t['Nome'].str.contains(el.upper())]['Pg'].values[0])
            except:
                tit=0
            if el.upper() == giocatore.upper():
                tx=round(round(int(tit)/38,2)*100,2)
            lista_print.append([el,p,int(prezzo_probabile),gf,str(round(round(int(tit)/38,2)*100,2))+"%"])
        lista_print.append(["","","","",""])
        lista_print.append(["Prezzo Totale Previsto:",int(ptpr),"","",""])
        lista_print.append(["Prezzo Totale Probabile:",int(prt),"","",""])
        prezzo=int(prezzo)    
        tit=0
        for el in tit_risultato:
            tit+=round(round(int(el)/38,2)*100,2)
        lista_print.append(["Indice titolarietà medio reparto:",str(round(tit/8,2))+"%","","",""])
        print(tabulate(lista_print, headers=["Nome", "Prezzo Previsto","Prezzo Probabile", "Gol Scorso Anno","Titolarietà"]))
        lista_print.clear()
        valore_temp=(valore_reparto+prezzo)/(len(acquistati)+1)
        if valore_temp>valore_prima:
        
            print("+",int((valore_temp-valore_prima)*100),"% qualità al reparto.")
        else:
            print("",int((valore_temp-valore_prima)*100),"% qualità al reparto.")
        if prezzo>budget-(6-len(new_acquisti)) or int(a*prezzo*prezzo+b*prezzo+c)>budget:
            print("Mmm, costa tanto, circa ",int(a*prezzo*prezzo+b*prezzo+c))
        elif valore_temp > valore_prima or tx > 50:
            
            print("Si acquistalo ma al massimo spendi:",int(a*prezzo*prezzo+b*prezzo+c))
            print("Probabile prezzo d'asta: circa",int(a*prezzo*prezzo+b*prezzo+c))
        else:
            print("Non acquistarlo.")
        valore_reparto=0
        quanto=input("Se lo hai comprato, a quanto? (se no premere 0) ")
        if len(quanto)==0:
            q=int(input("A quanto è andato? "))
            x1.append(prezzo)
            y1.append(q)
            print("", end="\r")
            acquistati=[]
            continue        
        try:
            if int(quanto)>0:
                x1.append(prezzo)
                y1.append(int(quanto))
                reparto_finale[giocatore]=quanto
                budget=budget-int(quanto)
                u=u-int(quanto)
                valori.append(prezzo)
                valore_prima=valore_temp
                new_acquisti.append(giocatore)
                i+=1
            acquistati=[]
        except:
            print("", end="\r")
            acquistati=[]
            continue
        print("", end="\r")
    return reparto_finale
def a(budget_tot,budg_portieri, budg_dif,budg_centr,budg_att):
    print("Lista attaccanti puntando sul valore:")
    print("BUDGET ATTACCANTI",budg_att)
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
        salvasuFile(budget_tot,budget_tot-spesa,budg_portieri,budg_dif,budg_centr,budg_att-spesa)
    else:
        print("Crediti rimasti:",(budg_att-spesa))
        print("CREDITI RIMASTI TOTALE:",(budget_tot-spesa))
        salvasuFile((budg_att-spesa),budget_tot-spesa,budg_portieri,budg_dif,budg_centr,budg_att)
def c(budget_tot,budg_portieri, budg_dif,budg_centr,budg_att):
    print("Lista centrocampisti puntando sulla titolarità:")
    print("BUDGET CENTROCAMPISTI",budg_centr)
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
        print("Hai speso troppo, verranno scalati crediti sugli attaccanti.")
        print("Crediti spesi in più:",abs(budg_centr-spesa))
        print("Att:",budg_att-abs(budg_centr-spesa))
        print("CREDITI RIMASTI TOTALE:",(budget_tot-spesa))
        salvasuFile(budget_tot,budget_tot-spesa,budg_portieri,budg_dif,0,budg_att-abs(budg_centr-spesa))
    else:
        print("Crediti rimasti (verranno aggiunti agli attaccanti):",(budg_centr-spesa))
        print("Att:",budg_att+(budg_centr-spesa))
        print("CREDITI RIMASTI TOTALE:",(budget_tot-spesa))
        salvasuFile(budget_tot,budget_tot-spesa,budg_portieri,budg_dif,budg_centr,budg_att+(budg_centr-spesa))
def d(budget_tot,budg_portieri, budg_dif,budg_centr,budg_att):
    print("Lista difensori puntando sulla titolarità:")
    print("BUDGET DIFENSORI",budg_dif)
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
        salvasuFile(budget_tot,budget_tot-spesa,budg_portieri,0,budg_centr-abs(budg_dif-spesa),budg_att+(budg_dif-spesa))
    else:
        print("Crediti rimasti (verranno aggiunti agli attaccanti):",(budg_dif-spesa))
        print("Cent:",budg_centr)
        print("Att:",budg_att+(budg_dif-spesa))
        print("CREDITI RIMASTI TOTALE:",(budget_tot-spesa))
        salvasuFile(budget_tot,budget_tot-spesa,budg_portieri,budg_dif-spesa,budg_centr,budg_att+(budg_dif-spesa))
def p(budget_tot,budg_portieri, budg_dif,budg_centr,budg_att):
    w_p=open("./src/portieri.txt", "w")
    print("BUDGET PORTIERI:",budg_portieri)
    print("Lista portieri migliori a seconda del calendario:")
    print(genera_portieri(1))
    print("Lista portieri migliori a seconda del valore")
    print(genera_portieri(2))
    spesa=0
    j=0
    for j in range(1,4):
        
        p=input("Inserire il portiere #"+str(j)+":")
        prezzi=input("Inserire i crediti spesi: ")

        buff=""+p.upper()+" : "+prezzi
        w_p.write(buff)
        w_p.write("\n")
        spesa+=int(prezzi)
    
    
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
        salvasuFile(budget_tot,budget_tot-spesa,budg_portieri,budg_dif,budg_centr,budg_att+(budg_portieri-spesa))
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
        
def main():
    if not path.exists("./excel/calendario.xlsx") or not path.exists("./excel/classifica.xlsx") or not path.exists("./excel/giocatori.xlsx") or not path.exists("./excel/Quotazioni_Fantacalcio.xlsx"):
        print("Generazione dei file excel in corso attendere...")
        ris=genera_excel()
        if ris!="OK":
            print("Errore imprevisto, termino.")
            exit()
    with open("./src/crediti.txt", "r") as fin:
        linee=fin.readlines()
    budget_tot=linee[0].split("=")[1].split("\n")[0]
    crediti_rimasti=linee[1].split("=")[1].split("\n")[0]
    budg_portieri=linee[2].split("=")[1].split("\n")[0]
    budg_dif=linee[3].split("=")[1].split("\n")[0]
    budg_centr=linee[4].split("=")[1].split("\n")[0]
    budg_att=linee[5].split("=")[1].split("\n")[0]
    w_d=open("./src/difensori.txt", "w")
    w_c=open("./src/centrocampisti.txt", "w")
    w_a=open("./src/attaccanti.txt", "w")
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
            continue
        if scelta=="1":
            p(int(budget_tot),int(budg_portieri),int(budg_dif),int(budg_centr),int(budg_att))
            os.system('CLS')
        elif scelta=="2":
            d(int(crediti_rimasti),int(budg_portieri),int(budg_dif),int(budg_centr),int(budg_att))
            os.system('CLS')
        elif scelta=="3":
            c(int(crediti_rimasti),int(budg_portieri),int(budg_dif),int(budg_centr),int(budg_att))
            os.system('CLS')
        elif scelta=="4":
            a(int(crediti_rimasti),int(budg_portieri),int(budg_dif),int(budg_centr),int(budg_att))
            os.system('CLS')
if __name__ == "__main__":
    main()





