from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from sqlite3 import *


class unesiBazu(Frame):
    def __init__(self, prozor):
        self.prozor = prozor
        #self.prozor.title('Unesi učenika')
        super().__init__(self.prozor)
        self.grid(rows = 11, columns = 3)
        self.conn=connect('baza.db')
        self.cur=self.conn.cursor()
        self.KreirajSucelje()
        return
    
    def KreirajSucelje(self):
        f=('Calibri',12,'bold')
        L1 = Label(self, text = "Upiši ime", font=f)
        L1.grid(row = 1, column = 1, pady = 5)
        self.tE1=StringVar()
        self.E1 = Entry(self,textvariable=self.tE1)
        self.E1.grid(row = 2, column = 1, padx=20, pady=10)

        L2 = Label(self, text = "Upiši prezime", font=f)
        L2.grid(row = 1, column = 2, pady = 5)
        self.tE2=StringVar()
        self.E2 = Entry(self,textvariable=self.tE2)
        self.E2.grid(row = 2, column = 2, padx=20, pady=10)

        L3 = Label(self, text = "Upiši razred", font=f)
        L3.grid(row = 1, column = 3, pady = 5)
        self.tE3=StringVar()
        self.E3 = Entry(self,textvariable=self.tE3)
        self.E3.grid(row = 2, column = 3, padx=20, pady=10)

        self.B1 = Button(self, text = 'Unos učenika u bazu', command = self.Insert, font=f)
        self.B1.grid(row = 2, column = 4, padx=10, pady=10)

        self.B2 = Button(self, text = 'Unos više uč. iz dat.', command = self.FromFile, font=f)
        self.B2.grid(row = 4, column = 1, padx=10, pady=10)

        self.B3 = Button(self, text = 'Prikaži bazu', command = self.Show, font=f)
        self.B3.grid(row = 5, column = 1, padx=10, pady=10)
        return

    def Insert(self):
        s="SELECT ID FROM Ucenici"
        ident=self.cur.execute(s)
        id_br=0
        for i in ident:
            id_br=i[0]
        ime=""
        if self.tE1.get():
            ime=self.tE1.get()
        prezime=""
        if self.tE2.get():
            prezime=self.tE2.get()
        razred=""
        if self.tE3.get():
            razred=self.tE3.get()
        s='INSERT INTO Ucenici (ID, Ime, Prezime, Razred, Ocjena) '
        s+='VALUES ({0},"{1}","{2}","{3}","{4}")'.format(id_br+1,ime,prezime,razred,"")
        print(s)
        self.cur.execute(s)
        self.conn.commit()
        return
    
    def FromFile(self):
        pathDatoteke = askopenfilename(filetypes=[('Datoteke baze', '*.csv'),
                                           ('Sve datoteke', '*.*')], title = 'Odaberi datoteku')
        pathDatoteke=pathDatoteke.replace("/","\\")
        s="SELECT ID FROM Ucenici"
        ident=self.cur.execute(s)
        id_br=0
        for i in ident:
            id_br=i[0]
        if pathDatoteke:
            try:
                f=open(pathDatoteke, "r")
                for red in f.readlines():
                    r=red.split("\t")
                    print(r)
                    s='INSERT INTO Ucenici (ID, Ime, Prezime, Razred, Ocjena) '
                    s+='VALUES ({0},"{1}","{2}","{3}","{4}")'.format(id_br+1,r[0],r[1],r[2],"")
                    print(s)
                    self.cur.execute(s)
                    self.conn.commit()
                    id_br+=1
            except:
                showerror('Unos u bazu', 'Datoteka ne postoji')
        return

    def Show(self):
        s="SELECT * FROM Ucenici"
        g=self.cur.execute(s)    
        for i in g:
            print(i)
        return
 
##def main():
##    
##    p = Program(Tk())
##    mainloop()
##    return
##    
##main()
