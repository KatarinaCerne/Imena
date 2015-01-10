import re
import urllib.request
import threading

#poskus funkcije, ki naj bi delala tudi za imena, ki imajo v url .../ime_(osebno_ime) ali .../ime_(ime) itd.
#funkcija ne deluje pravilno
#za (moško ime) in (žensko ime) ne deluje zaradi šumnikov
#za (ime) iz neznanega razloga ne deluje (???????)
#deluje samo za http://sl.wikipedia.org/wiki/Tonka_(ime), ker stran avtomatično preusmeri na http://sl.wikipedia.org/wiki/Anton
#prav tako iz neznanega razloga

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

    def __str__(self):
        return '{}'.format(self.ime)
    

def prenos2(name, gender):
    name = name.capitalize()
    if gender == "Z":
        seznam = [name, name+"_(osebno_ime)", name+"_(ime)", name+"_(žensko_ime)"]
    elif gender == "M":
        seznam = [name, name+"_(osebno_ime)", name+"_(ime)", name+"_(moško_ime)"]
    #seznam sem ločila na ženska in moška imena, ker so nekatera imena tako ženska kot moška npr. Sava
    for element in seznam:
        with urllib.request.urlopen('http://sl.wikipedia.org/wiki/{0}'.format(element)) as f:
            stran = str(f.read())

            sl={} #to je slovar, ki bo vseboval vse podatke
            vzorec_pomen = re.compile(r'<th>Pomen</th>\\n<td><i>(.*)</i></td>')
            pomen = re.findall(vzorec_pomen, stran) #seznam z 1 elementom (niz)
            #print(pomen)
            if pomen !=[]:
                sl["pomen"]= pomen
            else:
                sl["pomen"]= ["Ni podatka"]
            

            vzorec_izvor = re.compile(r'<th>Izvor</th>\\n<td>(.[^<]*\w+)</td>')
            izvor = re.findall(vzorec_izvor, stran)
            #print(izvor)
            if izvor !=[]:
                sl["izvor"]= izvor
            else:
                sl["izvor"]= ["Ni podatka"]

            vzorec_izvorna_oblika = re.compile(r'<th>Izvorna oblika</th>\\n<td>(.[^<]*\w+)</td>')
            #problem, ce je poleg se kaksen link v oklepaju itd.
            izvorna_oblika = re.findall(vzorec_izvorna_oblika, stran)
            #print(izvorna_oblika)
            if izvorna_oblika !=[]:
                sl["izvorna oblika"]= izvorna_oblika
            else:
                sl["izvorna oblika"]= ["Ni podatka"]

            vzorec_god1 = re.compile(r'<th>God</th>\\n<td>(.[^<]*\w+)</td>')
            #zgornji vzorec je ok, ce nimamo linka
            god1 = re.findall(vzorec_god1, stran)
            #print(god1)
            vzorec_god2 = re.compile(r'<th>God</th>\\n<td>.*<a href=".*">([0-9]*\.\w+)</a>.*</td>')
            #linkan datum hocemo ven
            god2 = re.findall(vzorec_god2, stran)
            #print(god2)
            if god1 != []:
                sl["god"] = sl.get("god", [])+god1
            else:
                pass
            if god2 != []:
                sl["god"] = sl.get("god",[])+god2
            else:
                pass
            if god1 == [] and god2 ==[]:
                sl["god"] = ["Ni podatka"]

            if sl["pomen"]==sl["izvor"]==sl["izvorna oblika"]==sl["god"]:
                pass
            else:
                print(element)
                return sl

