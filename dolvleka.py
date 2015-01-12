import re
import urllib.request
import threading

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
    
    with urllib.request.urlopen('http://www.stat.si/imena_baza_imena.asp?ime={0}&priimek=&spol={1}'.format(name, gender)) as f:
        stran = str(f.read())
        vzorec = re.compile(r'<p>\s*<span class="naslov2">(.*)</span>s*.*<b>(\d+)\. mesto</b>')
        podatki = re.findall(vzorec, stran)
        return podatki
    #podatki so oblike: [(št. ljudi s tem imenom-tekst, številka pogostosti-število)]


#se prenos podatkov iz wikipedije
def prenos2(name):
    
    name = name.capitalize()
    with urllib.request.urlopen('http://sl.wikipedia.org/wiki/{0}'.format(name)) as f:
        stran = str(f.read())

        sl={} #to je slovar, ki bo vseboval vse podatke
        vzorec_pomen = re.compile(r'<th>Pomen</th>\\n<td><i>(.*)</i></td>')
        pomen = re.findall(vzorec_pomen, stran) #seznam z 1 elementom (niz)
        print(pomen)
        if pomen != []:
            sl["pomen"] = pomen
        else:
            sl["pomen"] = ["Ni podatka"]
        

        vzorec_izvor = re.compile(r'<th>Izvor</th>\\n<td>(.[^<]*\w+)</td>')
        izvor = re.findall(vzorec_izvor, stran)
        print(izvor)
        if izvor != []:
            sl["izvor"] = izvor
        else:
            sl["izvor"] = ["Ni podatka"]

        vzorec_izvorna_oblika = re.compile(r'<th>Izvorna oblika</th>\\n<td>(.[^<]*\w+)</td>')
        #problem, ce je poleg se kaksen link v oklepaju itd.
        izvorna_oblika = re.findall(vzorec_izvorna_oblika, stran)
        print(izvorna_oblika)
        if izvorna_oblika != []:
            sl["izvorna oblika"] = izvorna_oblika
        else:
            sl["izvorna oblika"] = ["Ni podatka"]

        vzorec_god1 = re.compile(r'<th>God</th>\\n<td>(.[^<]*\w+)</td>')
        #zgornji vzorec je ok, ce nimamo linka
        god1 = re.findall(vzorec_god1, stran)
        print(god1)
        vzorec_god2 = re.compile(r'<th>God</th>\\n<td>.*<a href=".*">([0-9]*\.\w+)</a>.*</td>')
        #linkan datum hocemo ven
        god2 = re.findall(vzorec_god2, stran)
        print(god2)
        if god1 != []:
            sl["god"] = sl.get("god", [])+god1
        else:
            pass
        if god2 != []:
            sl["god"] = sl.get("god",[])+god2
        else:
            pass
        if god1 == [] and god2 == []:
            sl["god"] = ["Ni podatka"]

        return sl
    
