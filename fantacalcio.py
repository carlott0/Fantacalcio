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
def genera_excel():
    try:
        os.makedirs("./excel/")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    #quotazioni
    link ='https://www.fantacalcio.it//Servizi/Excel.ashx?type=0&r=1&t=1652767828000'
    data = pd.read_excel(link, header=1)
    data.to_excel('./excel/Quotazioni_Fantacalcio.xlsx')
    #giocatori
    link ='https://www.fantacalcio.it/Servizi/Excel.ashx?type=2&r=1&t=1614489243000&s=2020-21'
    data = pd.read_excel(link, header=1)
    data.to_excel('./excel/giocatori.xlsx')
    #calendario
    link="https://www.fantacalcio.it/Servizi/Excel.ashx?type=3&t=1629207892000"
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
    #classifica
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
    df=pd.DataFrame(squadre, columns=["SQUADRE"])
    df.to_excel('./excel/classifica.xlsx')

    return "OK"
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
    ret_diz={k: v for k, v in sorted(new_diz.items(), key=lambda item: item[1],reverse=True)}
    if scelta==1:
        return ret_diz
    elif scelta==2:
        return ret_marks
    return
def dif(giocatore_chiamato,acquistati,budget_rimasto):
    giocatori_risultato=[]
    valori_risultato=[]
    tit_risultato=[]
    quotazioni=pd.read_excel("./excel/Quotazioni_Fantacalcio.xlsx", names=['Id','R','Nome','Squadra','Qt. A','Qt. I','Diff.'])
    da_comprare=8-len(acquistati)   
    x=pd.read_excel("./excel/giocatori.xlsx")
    t=x.loc[(x['R']=='D')]       
    ### funzione prezzo
    x1 = [1,5,10,15,20,25,30]
    y1 = [1,10,15,20,30,40,50]
    a,b,c = np.polyfit(x1, y1, 2)
    try:
        p=int(quotazioni[quotazioni['Nome'].str.contains(giocatore_chiamato.upper())]['Qt. A'].item())
    except:
        return 1,0,[]
    prezzo_probabile=a*p*p+b*p+c
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
    i=0
    if  budget_rimasto < 0:
        print("Si ha sforato il budget, verranno suggeriti solo giocatori a poco")
        ds=list(quotazioni.loc[(quotazioni['R'] == 'D') & (quotazioni['Qt. A'] == 1)]['Nome'].values)
        for k in range(0,da_comprare):
            d=random.choice(ds)
            if d not in acquistati:
                acquistati.append(d)
                i=0
                prezzo=1
                budget_rimasto=budget_rimasto-1
                titolarieta=1#(int(t[t['Nome'].str.contains(d.upper())]['Pg'].item()))
                tit_risultato.append(titolarieta)
                valori_risultato.append("1")
                giocatori_risultato.append(d)
                k+=1
        return 0,prezzo_ris,tit_risultato
    while(len(acquistati)!=8):
        d=random.choice(ds)
        if len(t[t['Nome'].str.contains(d.upper())]['Pg'])==0:
            i+=1
            continue
        tit=int(t[t['Nome'].str.contains(d.upper())]['Pg'].values[0])
        if int(tit)==0:
            i+=1
            continue
        titolarieta=38/int(tit)
        if d not in acquistati and titolarieta>0.7:
            if len(quotazioni[quotazioni['Nome'].str.contains(d.upper())]['Qt. A'])>1:
                i+=1
                continue
            v=int(quotazioni[quotazioni['Nome'].str.contains(d.upper())]['Qt. A'].item())
            prezzo_previsto=int(a*v*v+b*v+c)
            new_budg=budget_rimasto-v
            if new_budg<=0:
                i+=1
                continue
            if new_budg > da_comprare:
                acquistati.append(d)
                da_comprare-=1
                prezzo=budget_rimasto-new_budg
                budget_rimasto=new_budg
                tit_risultato.append(tit)
                valori_risultato.append(v)
                giocatori_risultato.append(d)
                i=0
                ds=list(quotazioni.loc[(quotazioni['R'] == 'D') & ((quotazioni['Qt. A'])<= budget_rimasto)]['Nome'].values)
                if d in ds:
                    ds.remove(d)
            if budget_rimasto <= da_comprare:
                ds=list(quotazioni.loc[(quotazioni['R'] == 'D') & (quotazioni['Qt. A'] == 1)]['Nome'].values)
                for k in range(0,da_comprare):
                    d=random.choice(ds)
                    if d not in acquistati:
                        acquistati.append(d)
                        i=0
                        prezzo=1
                        budget_rimasto=budget_rimasto-1
                        titolarieta=1
                        tit_risultato.append(titolarieta)
                        valori_risultato.append("1")
                        giocatori_risultato.append(d)
                        k+=1
                return 0,prezzo_ris,tit_risultato
            else:
                i+=1
                continue
        else:
            i+=1
    return 0,prezzo_ris,tit_risultato
def difensori(budget):
    i=1
    acquistati=[]
    reparto_finale={}
    new_acquisti=[]
    valore_prima=0
    valori=[]
    valore_reparto=0
    x1 = [1,5,10,15,20,25,30]
    y1 = [1,10,15,20,30,40,50]
    a,b,c = np.polyfit(x1, y1, 2)
    while(i!=9):
        input()
        os.system('CLS')        
        print("Budget:",budget)
        for el in valori:
            valore_reparto+=el/(len(acquistati)+1)
        print("#"+str(i))
        giocatore=input("Difensore ")
        if giocatore in reparto_finale.keys():
            print("Giocatore già acquistato.")
            continue
        for el in new_acquisti:
            acquistati.append(el)
        acquistati.append(giocatore)
        ok,prezzo,tit_risultato=dif(giocatore,acquistati,budget)
        if ok==1:
            print("Giocatore non trovato, riprova.")
            acquistati.remove(giocatore)
            continue
        print("Possibile squadra:")
        print(acquistati)
        prezzo=int(prezzo)    
        tit=0
        for el in tit_risultato:
            tit+=float(el)
        print("",tit)
        valore_temp=(valore_reparto+prezzo)/(len(acquistati)+1)
        if prezzo>budget-(8-len(new_acquisti)):
            print("Mmm, costa circa ",prezzo)
        elif valore_temp > valore_prima or tit > 30:
            print("Si acquistalo ma al massimo spendi:",int(a*prezzo*prezzo+b*prezzo+c))
            print("Probabile prezzo d'asta: circa",int(a*prezzo*prezzo+b*prezzo+c))
        else:
            print("Non acquistarlo la squadra perde valore")
        valore_reparto=0
        quanto=input("Se lo hai comprato, a quanto? (se no premere 0) ")
        try:
            if int(quanto)>0:
                reparto_finale[giocatore]=quanto
                budget=budget-int(quanto)
                valori.append(prezzo)
                valore_prima=valore_temp
                new_acquisti.append(giocatore)
                i+=1
            acquistati=[]
        except:
            print("", end="\r")
            continue
        print("", end="\r")
    return reparto_finale
def centr(giocatore_chiamato,acquistati,budget_rimasto):
    giocatori_risultato=[]
    valori_risultato=[]
    tit_risultato=[]
    quotazioni=pd.read_excel("./excel/Quotazioni_Fantacalcio.xlsx", names=['Id','R','Nome','Squadra','Qt. A','Qt. I','Diff.'])
    da_comprare=8-len(acquistati)
    x=pd.read_excel("./excel/giocatori.xlsx")
    t=x.loc[(x['R']=='C')]
    ### funzione prezzo
    x1 = [1,5,10,15,20,25,30,35]
    y1 = [1,10,20,30,35,40,50,60]
    a,b,c = np.polyfit(x1, y1, 2)
    try:
        p=int(quotazioni[quotazioni['Nome'].str.contains(giocatore_chiamato.upper())]['Qt. A'].item())
    except:
        return 1,0,[]
    prezzo_probabile=a*p*p+b*p+c
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
    if  budget_rimasto < 0:
        print("Si ha sforato il budget, verranno suggeriti solo giocatori a poco")
        cs=list(quotazioni.loc[(quotazioni['R'] == 'C') & (quotazioni['Qt. A'] == 1)]['Nome'].values)
        for k in range(0,da_comprare):
            cx=random.choice(cs)
            if cx not in acquistati:
                acquistati.append(cx)
                i=0
                prezzo=1
                budget_rimasto=budget_rimasto-1
                titolarieta=1#(int(t[t['Nome'].str.contains(d.upper())]['Pg'].item()))
                tit_risultato.append(titolarieta)
                valori_risultato.append("1")
                giocatori_risultato.append(cx)
                k+=1
        return 0,prezzo_ris,tit_risultato
    while(len(acquistati)!=8):
        cx=random.choice(cs)
        if len(t[t['Nome'].str.contains(cx.upper())]['Pg'])==0:
            i+=1
            continue
        tit=int(t[t['Nome'].str.contains(cx.upper())]['Pg'].values[0])
        if int(tit)==0:
            i+=1
            continue
        titolarieta=38/int(tit)
        if cx not in acquistati and titolarieta>0.7:
            if len(quotazioni[quotazioni['Nome'].str.contains(cx.upper())]['Qt. A'])>1:
                i+=1
                continue
            v=int(quotazioni[quotazioni['Nome'].str.contains(cx.upper())]['Qt. A'].item())
            prezzo_previsto=int(a*v*v+b*v+c)
            new_budg=budget_rimasto-v
            if new_budg<=0:
                i+=1
                continue
            if new_budg > da_comprare:
                acquistati.append(cx)
                da_comprare-=1
                prezzo=budget_rimasto-new_budg
                budget_rimasto=new_budg
                tit_risultato.append(tit)
                valori_risultato.append(v)
                giocatori_risultato.append(cx)
                i=0
                cs=list(quotazioni.loc[(quotazioni['R'] == 'C') & ((quotazioni['Qt. A'])<= budget_rimasto)]['Nome'].values)
                if cx in cs:
                    cs.remove(cx)
            if budget_rimasto <= da_comprare:
                cs=list(quotazioni.loc[(quotazioni['R'] == 'C') & (quotazioni['Qt. A'] == 1)]['Nome'].values)
                for k in range(0,da_comprare):
                    cx=random.choice(cs)
                    if cx not in acquistati:
                        acquistati.append(cx)
                        i=0
                        prezzo=1
                        budget_rimasto=budget_rimasto-1
                        titolarieta=1
                        tit_risultato.append(titolarieta)
                        valori_risultato.append("1")
                        giocatori_risultato.append(cx)
                        k+=1
                return 0,prezzo_ris,tit_risultato
            else:
                i+=1
                continue
        else:
            i+=1
    return 0,prezzo_ris,tit_risultato
def centrocampisti(budget):
    i=1
    acquistati=[]
    reparto_finale={}
    new_acquisti=[]
    valore_prima=0
    valori=[]
    valore_reparto=0
    x1 = [1,5,10,15,20,25,30,35]
    y1 = [1,10,20,30,35,40,50,60]
    a,b,c = np.polyfit(x1, y1, 2)
    while(i!=9):
        input()
        os.system('CLS')        
        print("Budget:",budget)
        for el in valori:
            valore_reparto+=el/(len(acquistati)+1)
        print("#"+str(i))
        giocatore=input("Centrocampista ")
        if giocatore in reparto_finale.keys():
            print("Giocatore già acquistato.")
            continue
        for el in new_acquisti:
            acquistati.append(el)
        acquistati.append(giocatore)
        ok,prezzo,tit_risultato=centr(giocatore,acquistati,budget)
        if ok==1:
            print("Giocatore non trovato, riprova.")
            acquistati.remove(giocatore)
            continue
        print("Possibile squadra:")
        print(acquistati)
        prezzo=int(prezzo)    
        tit=0
        for el in tit_risultato:
            tit+=float(el)
        print("",tit)
        valore_temp=(valore_reparto+prezzo)/(len(acquistati)+1)
        if prezzo>budget-(8-len(new_acquisti)):
            print("Mmm, costa circa ",prezzo)
        elif valore_temp > valore_prima or tit > 30:
            print("Si acquistalo ma al massimo spendi:",int(a*prezzo*prezzo+b*prezzo+c))
            print("Probabile prezzo d'asta: circa",int(a*prezzo*prezzo+b*prezzo+c))
        else:
            print("Non acquistarlo la squadra perde valore")
        valore_reparto=0
        quanto=input("Se lo hai comprato, a quanto? (se no premere 0) ")
        try:
            if int(quanto)>0:
                reparto_finale[giocatore]=quanto
                budget=budget-int(quanto)
                valori.append(prezzo)
                valore_prima=valore_temp
                new_acquisti.append(giocatore)
                i+=1
            acquistati=[]
        except:
            print("", end="\r")
            continue
        print("", end="\r")
    return reparto_finale
def att(giocatore_chiamato,acquistati,budget_rimasto):
    giocatori_risultato=[]
    valori_risultato=[]
    tit_risultato=[]    
    quotazioni=pd.read_excel("./excel/Quotazioni_Fantacalcio.xlsx", names=['Id','R','Nome','Squadra','Qt. A','Qt. I','Diff.'])
    da_comprare=8-len(acquistati)
    x=pd.read_excel("./excel/giocatori.xlsx")
    t=x.loc[(x['R']=='A')]
    ### funzione prezzo
    x1 = [1,5,10,15,20,25,30,35,40,45]
    y1 = [1,10,30,40,50,70,90,120,150,180]
    a,b,c = np.polyfit(x1, y1, 2)
    try:
        p=int(quotazioni[quotazioni['Nome'].str.contains(giocatore_chiamato.upper())]['Qt. A'].item())
    except:
        return 1,0,[]
    prezzo_probabile=a*p*p+b*p+c
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
    i=0
    if  budget_rimasto < 0:
        print("Si ha sforato il budget, verranno suggeriti solo giocatori a poco")
        ass=list(quotazioni.loc[(quotazioni['R'] == 'A') & (quotazioni['Qt. A'] == 1)]['Nome'].values)
        for k in range(0,da_comprare):
            ax=random.choice(ass)
            if ax not in acquistati:
                acquistati.append(ax)
                i=0
                prezzo=1
                budget_rimasto=budget_rimasto-1
                titolarieta=1
                tit_risultato.append(titolarieta)
                valori_risultato.append("1")
                giocatori_risultato.append(ax)
                k+=1
        return 0,prezzo_ris,tit_risultato
    while(len(acquistati)!=8):
        ax=random.choice(ass)
        if len(t[t['Nome'].str.contains(ax.upper())]['Pg'])==0:
            i+=1
            continue
        tit=int(t[t['Nome'].str.contains(ax.upper())]['Pg'].values[0])
        if int(tit)==0:
            i+=1
            continue
        titolarieta=38/int(tit)
        if d not in acquistati and titolarieta>0.7:
            if len(quotazioni[quotazioni['Nome'].str.contains(ax.upper())]['Qt. A'])>1:
                i+=1
                continue
            v=int(quotazioni[quotazioni['Nome'].str.contains(ax.upper())]['Qt. A'].item())
            prezzo_previsto=int(a*v*v+b*v+c)
            new_budg=budget_rimasto-prezzo_previsto
            if new_budg<=0:
                new_budg=budget_rimasto-v
            if new_budg<=0:
                i+=1
                continue
            if new_budg > da_comprare:
                acquistati.append(ax)
                da_comprare-=1
                prezzo=budget_rimasto-new_budg
                budget_rimasto=new_budg
                tit_risultato.append(tit)
                valori_risultato.append(v)
                giocatori_risultato.append(ax)
                i=0
                ass=list(quotazioni.loc[(quotazioni['R'] == 'A') & ((quotazioni['Qt. A'])<= budget_rimasto)]['Nome'].values)
                if ax in ass:
                    ass.remove(ax)
            if budget_rimasto <= da_comprare:
                ass=list(quotazioni.loc[(quotazioni['R'] == 'A') & (quotazioni['Qt. A'] == 1)]['Nome'].values)
                for k in range(0,da_comprare):
                    ax=random.choice(ass)
                    if ax not in acquistati:
                        acquistati.append(ax)
                        i=0
                        prezzo=1
                        budget_rimasto=budget_rimasto-1
                        titolarieta=1
                        tit_risultato.append(titolarieta)
                        valori_risultato.append("1")
                        giocatori_risultato.append(ax)
                        k+=1
                return 0,prezzo_ris,tit_risultato
            else:
                i+=1
                continue
        else:
            i+=1
    return 0,prezzo_ris,tit_risultato
def attaccanti(budget):
    i=1
    acquistati=[]
    reparto_finale={}
    new_acquisti=[]
    valore_prima=0
    valori=[]
    valore_reparto=0
    x1 = [1,5,10,15,20,25,30,35,40,45]
    y1 = [1,10,30,40,50,70,90,120,150,180]
    a,b,c = np.polyfit(x1, y1, 2)
    while(i!=7):
        input()
        os.system('CLS')
        print("Budget:",budget)
        for el in valori:
            valore_reparto+=el/(len(acquistati)+1)
        print("#"+str(i))
        giocatore=input("Attaccante ")
        if giocatore in reparto_finale.keys():
            print("Giocatore già acquistato.")
            continue
        for el in new_acquisti:
            acquistati.append(el)
        acquistati.append(giocatore)
        ok,prezzo,tit_risultato=att(giocatore,acquistati,budget)
        if ok==1:
            print("Giocatore non trovato, riprova.")
            acquistati.remove(giocatore)
            continue
        print("Possibile squadra:")
        print(acquistati)
        prezzo=int(prezzo)    
        tit=0
        for el in tit_risultato:
            tit+=float(el)
        print("",tit)
        valore_temp=(valore_reparto+prezzo)/(len(acquistati)+1)
        pt=int(a*prezzo*prezzo+b*prezzo+c)
        if pt>budget-(8-len(new_acquisti)):
            print("Mmm, costa circa ",pt)
        elif valore_temp > valore_prima or tit > 30:
            print("Si acquistalo ma al massimo spendi:",int(a*prezzo*prezzo+b*prezzo+c))
            print("Probabile prezzo d'asta: circa",int(a*prezzo*prezzo+b*prezzo+c))
        else:
            print("Non acquistarlo la squadra perde valore")
        valore_reparto=0
        quanto=input("Se lo hai comprato, a quanto? (se no premere 0) ")
        try:
            if int(quanto)>0:
                reparto_finale[giocatore]=quanto
                budget=budget-int(quanto)
                valori.append(prezzo)
                valore_prima=valore_temp
                new_acquisti.append(giocatore)
                i+=1
            acquistati=[]
        except:
            print("", end="\r")
            continue
        print("", end="\r")
    return reparto_finale
def a(budget_tot,budg_portieri, budg_dif,budg_centr,budg_att):
    print("Lista attaccanti puntando sul valore:")
    print("BUDGET ATTACCANTI",budg_att)
    reparto=attaccanti(budg_att)
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
    reparto=centrocampisti(budg_centr)
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
    reparto=(difensori(budg_dif))
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
    p=input("Inserire i portieri scelti separati da ';': ").split(";")
    prezzi=input("Inserire i crediti spesi per ognuno in ordine separati da ';': ").split(";")
    i=0
    for el in p:
        buff=""+el+" : "+prezzi[i]
        w_p.write(buff)
        w_p.write("\n")
        i+=1
    spesa=0
    for el in prezzi:
        spesa+=int(el)
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
    input()
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
        scelta=input()
        if scelta!="1" and scelta!="2" and scelta!="3" and scelta!="4":
            print("Inserire una scelta valida.")
            continue
        if scelta=="1":
            p(int(budget_tot),int(budg_portieri),int(budg_dif),int(budg_centr),int(budg_att))
            os.system('CLS')
        elif scelta=="2":
            d(int(budget_tot),int(budg_portieri),int(budg_dif),int(budg_centr),int(budg_att))
            os.system('CLS')
        elif scelta=="3":
            c(int(budget_tot),int(budg_portieri),int(budg_dif),int(budg_centr),int(budg_att))
            os.system('CLS')
        elif scelta=="4":
            a(int(budget_tot),int(budg_portieri),int(budg_dif),int(budg_centr),int(budg_att))
            os.system('CLS')
if __name__ == "__main__":
    main()





