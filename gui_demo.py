__author__ = 'Neza&Katarina'

from tkinter import *
from dolvleka import*

class Imena:
    def prenos1(name, gender):
        with urllib.request.urlopen('http://www.stat.si/imena_baza_imena.asp?ime={0}&priimek=&spol={1}'.format(name, gender)) as f:
            stran = str(f.read())
            vzorec = re.compile(r'<p>\s*<span class="naslov2">(.*)</span>s*.*<b>(\d+)\. mesto</b>')
            podatki = re.findall(vzorec, stran)
            return podatki

    def prenos2(name):
    
        name = name.capitalize()
        with urllib.request.urlopen('http://sl.wikipedia.org/wiki/{0}'.format(name)) as f:
            stran = str(f.read())


            vzorec_pomen = re.compile(r'<th>Pomen</th>\\n<td><i>(.*)</i></td>')
            pomen = re.findall(vzorec_pomen, stran)
            if pomen !=[]:
                sl["pomen"] = pomen
            else:
                sl["pomen"] = ["Ni podatka"]
            

            vzorec_izvor = re.compile(r'<th>Izvor</th>\\n<td>(.[^<]*\w+)</td>')
            izvor = re.findall(vzorec_izvor, stran)
            if izvor !=[]:
                sl["izvor"] = izvor
            else:
                sl["izvor"] = ["Ni podatka"]


            vzorec_izvorna_oblika = re.compile(r'<th>Izvorna oblika</th>\\n<td>(.[^<]*\w+)</td>')
            izvorna_oblika = re.findall(vzorec_izvorna_oblika, stran)
            if izvorna_oblika !=[]:
                sl["izvorna oblika"] = izvorna_oblika
            else:
                sl["izvorna oblika"] = ["Ni podatka"]

            vzorec_god1 = re.compile(r'<th>God</th>\\n<td>(.[^<]*\w+)</td>')
            god1 = re.findall(vzorec_god1, stran)
            vzorec_god2 = re.compile(r'<th>God</th>\\n<td>.*<a href=".*">([0-9]*\.\w+)</a>.*</td>')
            god2 = re.findall(vzorec_god2, stran)
            if god1 != []:
                sl["god"] = sl.get("god", []) + god1
            else:
                pass
            if god2 != []:
                sl["god"] = sl.get("god",[]) + god2
            else:
                pass
            if god1 == [] and god2 == []:
                sl["god"] = ["Ni podatka"]

            return sl
    
    def prikazi(self, *argumenti):
        print('Kliknili so me!')
        try:
            imeP = self.ime.get()
            spolP = self.spol.get()
            k = prenos1(imeP,spolP)
            self.stevilo.set(k[0][0])
            self.pogostost.set("To ime je po pogostosti na " + k[0][1] + str(". mestu."))

            s = prenos2(imeP)
            self.pomen.set(s["pomen"][0])
            self.izvor.set(s["izvor"][0])
            self.izvornaoblika.set(s["izvorna oblika"][0])
            self.god.set(s["god"][0])
            
            #print(self.ime, self.spol)
        except ValueError:
            pass

    def __init__(self, root):
        root.title('Say my name')       

        okvir = Frame(root, padx=10, pady=10)
        okvir.grid(column=0, row=0)

       
        self.ime = StringVar()
        self.spol = StringVar()
        
        self.stevilo = StringVar()
        self.pogostost = StringVar()
        
        self.pomen = StringVar()
        self.izvor = StringVar()
        self.izvornaoblika = StringVar()
        self.god = StringVar()

        vnosno_polje1 = Entry(okvir, textvariable=self.ime)
        vnosno_polje1.grid(column=2, row=1)

        vnosno_polje2 = Entry(okvir, textvariable=self.spol)
        vnosno_polje2.grid(column=2, row=2)
        
        Label(okvir, text='Vnesi ime:', justify=RIGHT).grid(column=1, row=1, sticky=E) #sticky pozicionira tekst
        Label(okvir, text='Vnesi spol: (moški = M, ženski = Z)').grid(column=1, row=2, sticky=E) #N,S,E,W pridejo v postev

        Button(okvir, text='Išči!', font=("Tahoma", 14), fg='#ff0000', command=self.prikazi).grid(column=3, row=3)  # dodam mu funkcijo - callback

        Label(okvir, text="Število:", font=("Tahoma", 14), fg='#48b427').grid(column=1, row=4, sticky=E)
        Label(okvir, textvariable=self.stevilo, font=("Helvetica", 12)).grid(column=2, row=4, sticky=W)
        Label(okvir, text="Pogostost:", font=("Tahoma", 14), fg='#48b427').grid(column=1, row=5, sticky=E)
        Label(okvir, textvariable=self.pogostost, font=("Helvetica", 12)).grid(column=2, row=5, sticky=W)

        Label(okvir, text="Pomen:", font=("Tahoma", 14), fg='#2e2230').grid(column=1, row=6, sticky=E)
        Label(okvir, textvariable=self.pomen, font=("Helvetica", 12)).grid(column=2, row=6, sticky=W)
        Label(okvir, text="Izvor:", font=("Tahoma", 14), fg='#2e2230').grid(column=1, row=7, sticky=E)
        Label(okvir, textvariable=self.izvor, font=("Helvetica", 12)).grid(column=2, row=7, sticky=W)
        Label(okvir, text="Izvorna oblika:", font=("Tahoma", 14), fg='#2e2230').grid(column=1, row=8, sticky=E)
        Label(okvir, textvariable=self.izvornaoblika, font=("Helvetica", 12)).grid(column=2, row=8, sticky=W)
        Label(okvir, text="God:", font=("Tahoma", 14), fg='#2e2230').grid(column=1, row=9, sticky=E)
        Label(okvir, textvariable=self.god, font=("Helvetica", 12)).grid(column=2, row=9, sticky=W)
        

        for otrok in okvir.winfo_children():  # gre po vseh graficnih gradnikih v okvirju
            # da ne nastavljamo pri vsakemu posebej
            otrok.grid_configure(padx=4, pady=2)

        # hocemo, da se gumb pritisne, ce kliknemo Enter
        root.bind('<Return>', self.prikazi)  # ta fn. se poklice na Enter
        vnosno_polje1.focus()  # takoj se nam postavi v okence, da lahko pisemo vanj cim se okno odpre


master = Tk()
Imena(master)
master.mainloop()  # poskrbi, da se okno ne zapre, dokler ga mi ne zapremo na krizec

