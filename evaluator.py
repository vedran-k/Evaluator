from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import *
from sqlite3 import *
import subprocess
import sys
import os
import time

class Evaluator(Frame):
    def __init__(self, prozor):
        self.prozor = prozor
        #self.prozor.title('Evaluator')
        super().__init__(self.prozor)
        self.grid(rows = 11, columns = 3)
        self.conn=connect('baza.db')
        self.cur=self.conn.cursor()
        self.KreirajSucelje()
        return
    
    def KreirajSucelje(self):
        f=('Calibri',12,'bold')
        self.gradivo=""
        self.zadatak=""
        self.grupa=""
        self.pathZadatka=""
        self.pathRjesenja=""
        self.gradiva = ['Grananje','Petlje','String','Liste','Skup i rječnik','Datoteke']
        self.grupe=["GrupaA","GrupaB","GrupaC","GrupaD",]
        self.razredi=["1D","2A","2B","3D","4G"]

        self.L1 = Label(self, text = 'Odaberi gradivo', font=f)
        self.L1.grid(row = 1, column = 1, padx=10, pady=10)

        
        self.Test = Listbox(self, height=4, selectforeground = 'red', selectmode = SINGLE, font = f, fg = 'blue')
        self.Test.grid(row = 2, column = 1,sticky=N+E+S+W, padx = (10,0), pady=10)
        for t in self.gradiva:
            self.Test.insert(END, t) 
        scrollbar1 = Scrollbar(self,orient=VERTICAL)
        scrollbar1.grid(column=2,row=2,sticky=N+S,pady=10)
        #self.Test.config()
        self.Test['yscrollcommand']= scrollbar1.set
        scrollbar1['command'] = self.Test.yview
        
          
        self.Test.bind("<<ListboxSelect>>", self.OtvoriGradivo)

        self.E2 = Label(self, text = 'Odaberi grupu', font=f)
        self.E2.grid(row = 3, column = 1, padx=10, pady=10)
        self.Grupa = Listbox(self, height=4, selectforeground = 'red', selectmode = SINGLE, font = f, fg = 'blue')
        for t in self.grupe:
            self.Grupa.insert(END, t)   
        self.Grupa.grid(row = 4, column = 1,padx=10, pady=10)
        self.Grupa.bind("<<ListboxSelect>>", self.OtvoriGrupu)

        self.E3 = Label(self, text = 'Odaberi zadatak', font=f)
        self.E3.grid(row = 5, column = 1, padx=10, pady=10)
        self.Zadatak = Listbox(self, height=4,selectforeground = 'red', selectmode = SINGLE, font = f, fg = 'blue')
        self.Zadatak.grid(row = 6, column = 1, padx=10, pady=10)
        self.Zadatak.bind("<<ListboxSelect>>", self.OtvoriZadatak)

        self.tE1=StringVar()
        self.E1 = Entry(self,textvariable=self.tE1)
        self.E1.grid(row = 1, column = 3, padx=10, pady=10)
        self.B4 = Button(self, text = 'Evaulacija', command = self.Evaluate, font=f)
        self.B4.grid(row = 3, column = 3)
        self.B5 = Button(self, text = 'Odaberi dokument', command = self.OpenFile, font=f)
        self.B5.grid(row = 2, column = 3, padx=10, pady=10)
        self.tL4=StringVar()
        self.L4 = Label(self,textvariable=self.tL4, font = f)
        self.L4.grid(row = 4, column = 3)
        self.B6 = Button(self, text = 'Briši', command = self.DeleteFiles, font=f)
        self.B6.grid(row = 5, column = 3, padx=10, pady=10)


        self.L5 = Label(self, text = 'Odaberi razred', font=f)
        self.L5.grid(row = 1, column = 4, padx=10, pady=10)
        self.Razred = Listbox(self, height=4,selectforeground = 'red', selectmode = SINGLE, font = f, fg = 'blue')
        self.Razred.grid(row = 2, column = 4, padx=(10,0), pady=10)
        for t in self.razredi:
            self.Razred.insert(END, t)
        self.Razred.bind("<<ListboxSelect>>", self.ShowStudents)
        scrollbar2 = Scrollbar(self,orient=VERTICAL)
        scrollbar2.grid(column=5,row=2,sticky=N+S, pady = 10)
        self.Razred['yscrollcommand']= scrollbar2.set
        scrollbar2['command'] = self.Razred.yview
        
        self.Ucenik = Listbox(self, height=4,selectforeground = 'red', selectmode = SINGLE, font = f, fg = 'blue')
        self.Ucenik.grid(row = 3, column = 4, padx=(10,0), pady=10)
        scrollbar3 = Scrollbar(self,orient=VERTICAL)
        scrollbar3.grid(column=5,row=3,sticky=N+S, pady = 10)
        self.Ucenik['yscrollcommand']= scrollbar3.set
        scrollbar3['command'] = self.Ucenik.yview
        return

    def OtvoriGradivo(self,e=None):
        p=self.Test.curselection()
        if len(p)>0:
            self.gradivo=self.gradiva[int(p[0])]
        #print(self.gradivo)
        return
    
    def OtvoriGrupu(self,e=None):
        p=self.Grupa.curselection()
        if len(p)>0:
            self.grupa=self.grupe[int(p[0])]
            self.Zadaci = ['Zadatak1','Zadatak2','Zadatak3','Zadatak4']
            self.Zadatak.delete(0,len(self.Zadaci))
            for t in self.Zadaci:
                self.Zadatak.insert(END, t)
        #print(p)    
        return
    
    def OtvoriZadatak(self,e=None):
        p=self.Zadatak.curselection()
        if len(p)>0:
            self.zadatak=self.Zadaci[int(p[0])]
        return
    
    def OpenFile(self):
        self.pathRjesenja = askopenfilename(filetypes=[('Datoteke Pythona', '*.py'),('Tekstualne datoteke', '*.txt'),
                                           ('Sve datoteke', '*.*')], title = 'Odaberi datoteku')
        self.pathRjesenja=self.pathRjesenja.replace("/","\\")
        if self.pathRjesenja:
            try:
                p=self.pathRjesenja.split("\\")
                self.tE1.set(p[-1])       
            except:
                showerror('Evaluator', 'Datoteka ne postoji')
        return
    
    def DeleteFiles(self):
        for i in range(5):
            os.remove(self.pathZadatka+"UCout"+str(i)+".txt")
        return
    
    def Evaluate(self):
        self.pathZadatka="C:\\Users\\Korisnik\\Dropbox\\V.gimnazija\\Python\\Evaluator\\SluzbenaRjesenja\\"+self.gradivo+"\\"+self.grupa+"\\"+self.zadatak+"\\"    
        p=self.Ucenik.curselection()
        print(p)
        bodovi=0
        if self.pathRjesenja:
            try:
                for i in range(5):     
                    subprocess.Popen(self.pathRjesenja+" < "+self.pathZadatka+"in"+str(i)+".txt > "+self.pathZadatka+"UCout"+str(i)+".txt",stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)              
                    f_moj=open(self.pathZadatka+"out"+str(i)+".txt",'r')
                    time.sleep(1)
                    f_uc=open(self.pathZadatka+"UCout"+str(i)+".txt",'r')
                    uc=[]
                    for line in f_uc:
                        uc+=[line]
                    print(uc)
                    moj=[]
                    for line in f_moj:
                        moj+=[line]
                    print(moj)
                    gr=False
                    for j in range(len(moj)):
                        if j<len(uc) and moj[j]!=uc[j]:
                            gr=True
                    if not gr:
                        bodovi+=1
                    f_uc.close()
                self.tL4.set("Broj bodova: "+ str(bodovi))
                s="UPDATE Ucenici SET Ocjena={0} WHERE ID = {1}".format(str(bodovi),str(int(p[0])+1))
                self.cur.execute(s)
                self.conn.commit()
            except IOError:
                showerror('Evaluator', 'Datoteka ne postoji') 
        return

    def ShowStudents(self,e=None):
        s="SELECT Ime, Prezime FROM Ucenici"
        g=self.cur.execute(s)    
        for i in g:
            self.Ucenik.insert(END, i[0]+" "+i[1])
        return 
    
    
##def main():
##    
##    p = Evaluator(Tk())
##    #p.povezi()
##    mainloop()
##    return
##    
##main()
