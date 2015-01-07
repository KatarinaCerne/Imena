import re
import urllib.request
import threading

class Ime:

    def __init__(self, ime, spol, pomen, izvor, god):
        self.ime = ime
        self.spol = spol
        self.pomen = pomen
        self.izvor = izvor
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
        print(podatki)


#se prenos podatkov iz wikipedije
def prenos2(name):
    
    name = name.capitalize()
    with urllib.request.urlopen('http://sl.wikipedia.org/wiki/{0}'.format(name)) as f:
        stran = str(f.read())
        
        vzorec_pomen = re.compile(r'<th>Pomen</th>\\n<td><i>(.*)</i></td>')
        pomen = re.findall(vzorec_pomen, stran) #seznam z 1 elementom (niz)
        print(pomen)

        vzorec_izvor = re.compile(r'<th>Izvor</th>\\n<td>(.[^<]*\w+)</td>')
        #tole ne deluje
        izvor = re.findall(vzorec_izvor, stran)
        print(izvor)

        vzorec_god = re.compile(r'<td>.*[^\d](\d+\.\w+).*</td>')
        #imamo problem, kjer je presledek in kjer ga ni - linki
        god = re.findall(vzorec_god, stran)
        print(god)
