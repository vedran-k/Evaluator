from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from sqlite3 import *


class prikaziBazu(Frame):
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
        self.razredi=["1D","2A","2B","3D","4G"]
        
        self.L1 = Label(self, text = 'Odaberi razred', font=f)
        self.L1.grid(row = 1, column = 1, padx=10, pady=10)
        self.Razred = Listbox(self, height=4,selectforeground = 'red', selectmode = SINGLE, font = f, fg = 'blue')
        self.Razred.grid(row = 2, column = 1, padx=(10,0), pady=10)
        for t in self.razredi:
            self.Razred.insert(END, t)
        self.Razred.bind("<<ListboxSelect>>", self.ShowStudents)
        scrollbar1 = Scrollbar(self,orient=VERTICAL)
        scrollbar1.grid(column=2,row=2,sticky=N+S, pady = 10)
        self.Razred['yscrollcommand']= scrollbar1.set
        scrollbar1['command'] = self.Razred.yview
        
        L2 = Label(self, text = "Rezultati", font=f)
        L2.grid(row = 3, column = 1, pady = 5)
        self.Ucenik = Listbox(self, height=4,selectforeground = 'red', selectmode = SINGLE, font = f, fg = 'blue')
        self.Ucenik.grid(row = 4, column = 1, padx=(10,0), pady=10)
        scrollbar2 = Scrollbar(self,orient=VERTICAL)
        scrollbar2.grid(column=2,row=4,sticky=N+S, pady = 10)
        self.Ucenik['yscrollcommand']= scrollbar2.set
        scrollbar2['command'] = self.Ucenik.yview
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

    def ShowStudents(self,e=None):
        s="SELECT Ime, Prezime, Ocjena FROM Ucenici"
        g=self.cur.execute(s)    
        for i in g:
            self.Ucenik.insert(END, i[0]+" "+i[1] + " " + i[2])
        return 
 
##def main():
##    
##    p = Program(Tk())
##    mainloop()
##    return
##    
##main()
