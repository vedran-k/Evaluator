from sqlite3 import *
from tkinter import *

class Baza(Frame):
    def __init__(self, prozor):
        self.prozor = prozor
        #self.prozor.title('Unesi učenika')
        super().__init__(self.prozor)
        self.grid(rows = 1, columns = 1)
        self.conn=connect('baza.db')
        self.cur=self.conn.cursor()
        self.KreirajSucelje()
        return
    
    def KreirajSucelje(self):
        f=('Calibri',12,'bold')
        self.B1 = Button(self, text = 'Restart baze', command = self.Restart, font=f)
        self.B1.grid(row = 1, column = 1, padx=10, pady=10)
        return

    def Restart(self):
        s="DROP TABLE Ucenici"
        self.cur.execute(s)
        self.conn.commit()
        s="CREATE TABLE Ucenici ("
        s+="ID INTEGER PRIMARY KEY AUTOINCREMENT, "
        s+="Ime TEXT, "
        s+="Prezime TEXT, "
        s+="Razred TEXT,"
        s+="Ocjena TEXT)"
        ##s='INSERT INTO Ucenici (ID, Ime, Prezime, Razred, Ocjena) '
        ##s+='VALUES (3,"k","k","h","k")'
        self.cur.execute(s)
        self.conn.commit()
        self.conn.close()
        return

##def main():
##    p = Baza(Tk())
##    mainloop()
##    return
##    
##main()
