__author__ = 'Neza&Katarina'

from tkinter import *
from dolvleka import*
from urllib.parse import quote

class Imena:
    def prenos1(name, gender):
        ime = quote(name, encoding="windows-1250")   # enkodiramo utf-8 niz v windows-1250 ter zakodiramo v način, ki je primeren za URL povezave
        povezava = 'http://www.stat.si/imena_baza_imena.asp?ime={0}&priimek=&spol={1}'.format(ime, gender)
        with urllib.request.urlopen(povezava) as f:
            stran = f.read().decode("windows-1250")  # namesto str(f.read()) se uporabi metodo decode
            vzorec = re.compile(r'<p>\s*<span class="naslov2">(.*)</span>s*.*<b>(\d+)\. mesto</b>')
            podatki = re.findall(vzorec, stran)
            return podatki

    def prenos2(name):
        name = name.capitalize()
        ime = quote(name, encoding="utf-8")
        povezava = 'http://sl.wikipedia.org/wiki/{0}'.format(ime)
        with urllib.request.urlopen(povezava) as f:
            stran = f.read().decode("utf-8")

            sl={'pomen': "Ni podatka",
                'izvor': "Ni podatka",
                'izvorna oblika': "Ni podatka",
                'god': "Ni podatka"} #to je slovar, ki bo vseboval vse podatke
            
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
            self.pomen.set(s["pomen"])
            self.izvor.set(s["izvor"])
            self.izvornaoblika.set(s["izvorna oblika"])
            self.god.set(s["god"])
        except ValueError:
            pass

    def __init__(self, root):
        root.title('Say my name')

        okvir = Frame(root, padx=10, pady=10)
        okvir.configure(background="#F2F7BB")
        okvir.grid(column=0, row=0)

        self.ime = StringVar()
        self.spol = StringVar()
        self.spol.set("M")
        
        self.stevilo = StringVar()
        self.pogostost = StringVar()
        
        self.pomen = StringVar()
        self.izvor = StringVar()
        self.izvornaoblika = StringVar()
        self.god = StringVar()

        vnosno_polje1 = Entry(okvir, textvariable=self.ime)
        vnosno_polje1.grid(column=2, row=1)
        
        k1 = Label(okvir, text='Vnesi ime:',background="#F2F7BB")
        k1.grid(column=1, row=1, sticky=E)#sticky pozicionira tekst
        k2 = Label(okvir, text='Spol:',background="#F2F7BB")
        k2.grid(column=1, row=2, sticky=E) #N,S,E,W pridejo v postev
        
        moski = Radiobutton(okvir, text='Moški', variable=self.spol, value='M',background="#F2F7BB")
        moski.grid(column=2, row=2)
        zenski = Radiobutton(okvir, text='Ženski', variable=self.spol, value='Z',background="#F2F7BB")
        zenski.grid(column=3, row=2)

        k0=Button(okvir, text='Išči!', font=("Tahoma", 14), fg='#ff0000', command=self.prikazi, background="#FFFFFF")
        k0.grid(column=4, row=3)  # dodam mu funkcijo - callback

        k3 = Label(okvir, text="Število:", font=("Tahoma", 14), fg='#48b427',background="#F2F7BB")
        k3.grid(column=1, row=4, sticky=E)
        k4 = Label(okvir, textvariable=self.stevilo, font=("Helvetica", 12),background="#F2F7BB")
        k4.grid(column=2, row=4, sticky=W)
        k5 = Label(okvir, text="Pogostost:", font=("Tahoma", 14), fg='#48b427',background="#F2F7BB")
        k5.grid(column=1, row=5, sticky=E)
        k6 = Label(okvir, textvariable=self.pogostost, font=("Helvetica", 12),background="#F2F7BB")
        k6.grid(column=2, row=5, sticky=W)

        k7 = Label(okvir, text="Pomen:", font=("Tahoma", 14), fg='#2e2230',background="#F2F7BB")
        k7.grid(column=1, row=6, sticky=E)
        k8 = Label(okvir, textvariable=self.pomen, font=("Helvetica", 12),background="#F2F7BB")
        k8.grid(column=2, row=6, sticky=W)
        k9 = Label(okvir, text="Izvor:", font=("Tahoma", 14), fg='#2e2230',background="#F2F7BB")
        k9.grid(column=1, row=7, sticky=E)
        k10 = Label(okvir, textvariable=self.izvor, font=("Helvetica", 12),background="#F2F7BB")
        k10.grid(column=2, row=7, sticky=W)
        k11 = Label(okvir, text="Izvorna oblika:", font=("Tahoma", 14), fg='#2e2230',background="#F2F7BB")
        k11.grid(column=1, row=8, sticky=E)
        k12 = Label(okvir, textvariable=self.izvornaoblika, font=("Helvetica", 12),background="#F2F7BB")
        k12.grid(column=2, row=8, sticky=W)
        k13 = Label(okvir, text="God:", font=("Tahoma", 14), fg='#2e2230',background="#F2F7BB")
        k13.grid(column=1, row=9, sticky=E)
        k14 = Label(okvir, textvariable=self.god, font=("Helvetica", 12),background="#F2F7BB")
        k14.grid(column=2, row=9, sticky=W)    

        for otrok in okvir.winfo_children():  # gre po vseh graficnih gradnikih v okvirju
            # da ne nastavljamo pri vsakemu posebej
            otrok.grid_configure(padx=4, pady=2)

        # hocemo, da se gumb pritisne, ce kliknemo Enter
        root.bind('<Return>', self.prikazi)  # ta fn. se poklice na Enter
#        root.bind("<Escape>", quit) # na pritisk tipke Esc se program zakljuci
        vnosno_polje1.focus()  # takoj se nam postavi v okence, da lahko pisemo vanj cim se okno odpre
        
master = Tk()
Imena(master)
master.mainloop()  # poskrbi, da se okno ne zapre, dokler ga mi ne zapremo na krizec

