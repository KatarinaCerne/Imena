import re
import urllib.request
import threading
from urllib.parse import quote

class Ime:

    def __init__(self, ime, spol, pomen, izvor, izvornaoblika, god):
        self.ime = ime
        self.spol = spol
        self.pomen = pomen
        self.izvor = izvor
        self.izvornaoblika = izvornaoblika
        self.god = god

    def __repr__(self):
        return 'Ime({})'.format(self.ime)

    def __str(self):
        return '{}'.format(self.ime)

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
def prenos2(name):
    name = name.capitalize()
    povezava = 'http://sl.wikipedia.org/wiki/{0}'.format(name)
    with urllib.request.urlopen(povezava) as f:
        stran = str(f.read())
##    name = name.capitalize()
##    ime = quote(name, encoding="utf-8")
##    povezava = 'http://sl.wikipedia.org/wiki/{0}'.format(ime)
##    with urllib.request.urlopen(povezava) as f:
##        stran = f.read().decode("utf-8")

        sl={'pomen': "Ni podatka",
            'izvor': "Ni podatka",
            'izvorna oblika': "Ni podatka",
            'god': "Ni podatka"} #to je slovar, ki bo vseboval vse podatke
        
        vzorec_pomen = re.compile(r'<th>Pomen</th>\\n<td><i>(.*)</i></td>')
        pomen = re.findall(vzorec_pomen, stran) #seznam z 1 elementom (niz)
        print(pomen)
        if pomen != []:
            sl["pomen"] = pomen[0]
        

        vzorec_izvor = re.compile(r'<th>Izvor</th>\\n<td>(.[^<]*\w+)</td>')
        izvor = re.findall(vzorec_izvor, stran)
        print(izvor)
        if izvor != []:
            sl["izvor"] = izvor[0]
            

        vzorec_izvorna_oblika = re.compile(r'<th>Izvorna oblika</th>\\n<td>(\(?.[^<]*\w+\)?)</td>')
        #problem, ce je poleg se kaksen link v oklepaju itd.
        izvorna_oblika = re.findall(vzorec_izvorna_oblika, stran)
        print(izvorna_oblika)
        if izvorna_oblika != []:
            sl["izvorna oblika"] = izvorna_oblika[0]
            

        vzorec_god = re.compile(r'<th>God</th>\\n<td>(.[^<]*\w+)</td>')
        god = re.findall(vzorec_god, stran)
        print(god)
        if god != []:
            sl["god"] = god[0]

        return sl
    
