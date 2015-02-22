import re
import urllib.request
import threading
from urllib.parse import quote

#spol je enak 'Z' ali 'M'
#prvo bova povlekli podatke s statisticnega urada RS
def prenos1(name, gender):
    ime = quote(name, encoding="windows-1250")   # enkodiramo utf-8 niz v windows-1250 ter zakodiramo v način, ki je primeren za URL povezave
    povezava = 'http://www.stat.si/imena_baza_imena.asp?ime={0}&priimek=&spol={1}'.format(ime, gender)
    with urllib.request.urlopen(povezava) as f:
        stran = f.read().decode("windows-1250")  # namesto str(f.read()) se uporabi metodo decode
        vzorec = re.compile(r'<p>\s*<span class="naslov2">(.*)</span>s*.*<b>(\d+)\. mesto</b>')
        podatki = re.findall(vzorec, stran)
        return podatki
    #podatki so oblike: [(št. ljudi s tem imenom-tekst, številka pogostosti-število)]


#se prenos podatkov iz wikipedije
def prenos2(name, gender):
    #to je slovar, ki bo vseboval vse podatke
    sl={'pomen': "Ni podatka",
    'izvor': "Ni podatka",
    'izvorna oblika': "Ni podatka",
    'god': "Ni podatka"}
    
    ime = name.capitalize()
    #ime = quote(name, encoding="utf-8")
    if gender == "Z":
        seznam = [ime, ime+"_(osebno_ime)", ime+"_(ime)", ime+"_(žensko_ime)"]
    elif gender == "M":
        seznam = [ime, ime+"_(osebno_ime)", ime+"_(ime)", ime+"_(moško_ime)"]
    #seznam sem ločila na ženska in moška imena, ker so nekatera imena tako ženska kot moška npr. Sava
        
    for element in seznam:
        element = quote(element, encoding="utf-8")
        print(element)
        povezava = 'http://sl.wikipedia.org/wiki/{0}'.format(element)
        
        try:
            with urllib.request.urlopen(povezava) as f:
                stran = f.read().decode("utf-8")
          
                vzorec_pomen = re.compile(r'<th>Pomen</th>\s*<td><i>(.*)</i></td>')
                pomen = re.findall(vzorec_pomen, stran)
                print(pomen)
                if pomen != []:
                    sl["pomen"] = pomen[0]

                vzorec_izvor = re.compile(r'<th>Izvor</th>\s*<td>(.[^<]*\w+)</td>')
                izvor = re.findall(vzorec_izvor, stran)
                print(izvor)
                if izvor != []:
                    sl["izvor"] = izvor[0]
                
                vzorec_izvorna_oblika = re.compile(r'<th>Izvorna oblika</th>\s*<td>(.[^<]*\w+)</td>')
                izvorna_oblika = re.findall(vzorec_izvorna_oblika, stran)
                print(izvorna_oblika)
                if izvorna_oblika != []:
                    sl["izvorna oblika"] = izvorna_oblika[0] 

                vzorec_god = re.compile(r'<th>God</th>\s*<td>(.[^<]*\w+)</td>')
                god = re.findall(vzorec_god, stran)
                print(god)
                if god != []:
                    sl["god"] = god[0]
        except:
            print("error")
            continue
        
    
        if sl["pomen"]==sl["izvor"]==sl["izvorna oblika"]==sl["god"]:
            print("to ime je čudno")
            pass
        else:
            break
        
    #v primeru, da je naš prvi slovar brez podatkov,
    #bomo slovar napolni s podatki imena izvorne oblike
    if sl["izvorna oblika"] != 'Ni podatka':
        ime = quote(sl["izvorna oblika"], encoding="utf-8")
        povezava = 'http://sl.wikipedia.org/wiki/{0}'.format(ime)
        print('brskali bomo po izvorni obliki')
        slovarcek = dict()
        try:
            with urllib.request.urlopen(povezava) as f:
                stran = f.read().decode("utf-8")
          
                vzorec_pomen = re.compile(r'<th>Pomen</th>\s*<td><i>(.*)</i></td>')
                pomen = re.findall(vzorec_pomen, stran)
                if pomen != []:
                    slovarcek["pomen"] = pomen[0]

                vzorec_izvor = re.compile(r'<th>Izvor</th>\s*<td>(.[^<]*\w+)</td>')
                izvor = re.findall(vzorec_izvor, stran)
                if izvor != []:
                    slovarcek["izvor"] = izvor[0]
                
                vzorec_izvorna_oblika = re.compile(r'<th>Izvorna oblika</th>\s*<td>(.[^<]*\w+)</td>')
                izvorna_oblika = re.findall(vzorec_izvorna_oblika, stran)
                if izvorna_oblika != []:
                    slovarcek["izvorna oblika"] = izvorna_oblika[0]
                    
                vzorec_god = re.compile(r'<th>God</th>\s*<td>(.[^<]*\w+)</td>')
                god = re.findall(vzorec_god, stran)
                if god != []:
                    slovarcek["god"] = god[0]

            if sl['izvor'] == 'Ni podatka':
                sl['izvor'] = slovarcek['izvor'] + '*'
            if sl['pomen'] == 'Ni podatka':
                sl['pomen'] = slovarcek['pomen'] + '*'
            if sl['god'] == 'Ni podatka':
                sl['god'] = slovarcek['god'] + '*'
            #zraven izpisa dodamo še zvezdico, da vemo, da smo malček pogoljufali pri zbiranju podatkov
        except:
            pass
        
    return sl
    
