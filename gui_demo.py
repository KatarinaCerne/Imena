__author__ = 'Neza'

from tkinter import *
from dolvleka import*

class Imena:
    def prenos1(name, gender):
        with urllib.request.urlopen('http://www.stat.si/imena_baza_imena.asp?ime={0}&priimek=&spol={1}'.format(name, gender)) as f:
            stran = str(f.read())
            vzorec = re.compile(r'<p>\s*<span class="naslov2">(.*)</span>s*.*<b>(\d+)\. mesto</b>')
            podatki = re.findall(vzorec, stran)
            return podatki
    
    def prikazi(self, *argumenti):
        print('Kliknili so me!')
        self.platno.configure(background='#FF69B4')
        try:
            print(self.ime, self.spol)
        except ValueError:
            pass

    def __init__(self, root):
        root.title('Say my name')       

        okvir = Frame(root, padx=10, pady=10)
        okvir.grid(column=0, row=0)
        
        self.ime = StringVar()
        self.spol = StringVar()
        
        vnosno_polje1 = Entry(okvir, textvariable=self.ime)
        vnosno_polje1.grid(column=2, row=1)

        vnosno_polje2 = Entry(okvir, textvariable=self.spol)
        vnosno_polje2.grid(column=2, row=2)
        
        Label(okvir, text='Vnesi ime:').grid(column=1, row=1)
        Label(okvir, text='Vnesi spol: (moški = M, ženski = Z)').grid(column=1, row=2) 

        Button(okvir, text='Išči!', command=self.prikazi).grid(column=3, row=3)  # dodam mu funkcijo - callback

        self.platno = Canvas(okvir)
        self.platno.grid(column=1, row=4)

        for otrok in okvir.winfo_children():  # gre po vseh graficnih gradnikih v okvirju
            # da ne nastavljamo pri vsakemu posebej
            otrok.grid_configure(padx=2, pady=2)

        # hocemo, da se gumb pritisne, ce kliknemo Enter
        root.bind('<Return>', self.prikazi)  # ta fn. se poklice na Enter
        vnosno_polje1.focus()  # takoj se nam postavi v okence, da lahko pisemo vanj cim se okno odpre


master = Tk()
Imena(master)
master.mainloop()  # poskrbi, da se okno ne zapre, dokler ga mi ne zapremo na krizec
