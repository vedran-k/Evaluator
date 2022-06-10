from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from sqlite3 import *
from unosBaze import *
from baza import *
from evaluator import*


class Program(Frame):
    def __init__(self, prozor):
        self.prozor = prozor
        self.prozor.title('Evaluator')
        super().__init__(self.prozor)
        self.grid(rows = 11, columns = 3)
        self.KreirajSucelje()
        return
    
    def KreirajSucelje(self):
        n = ttk.Notebook(self.prozor)
        #n.enable_traversal()
        n.grid(row=1,column=1)
        
        f1 = ttk.Frame(n)
        prozor1=Baza(f1)
        prozor1.grid(row=1,column=1)
        n.add(f1, text='Restart baze',underline=0)
        
        f2 = ttk.Frame(n)
        prozor2=unesiBazu(f2)
        prozor2.grid(row=1,column=1)
        n.add(f2, text='Unesi u bazu',underline=0)

        f3 = ttk.Frame(n)
        prozor3 = Evaluator(f3)
        prozor3.grid(row=1,column=1)
        n.add(f3, text='Evaluator', underline=0)
        return

def main():
    p = Program(Tk())
    mainloop()
    return
    
main()
