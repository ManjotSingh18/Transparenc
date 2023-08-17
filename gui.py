import tkinter as tk
import time 
import home
from PIL import ImageTk, Image
from collections import defaultdict
class mainapp():
    def __init__(self, master):
        self.window=master
        self.window.geometry("800x800")
        self.data=[]
        self.offset=0
        self.move=defaultdict(list)
        self.frm0=tk.Frame()
        self.frm1=tk.Frame()
        self.frm0.pack()
        self.frm1.pack()
        self.pns=None
        self.icon=None
        self.creator = tk.Toplevel(self.window)
        self.creator.protocol("WM_DELETE_WINDOW", lambda: None)
        self.creator.grab_set()
        self.creator.wm_attributes("-topmost", True)
        self.creator.geometry("400x400")
        agree=tk.Button(self.creator,text="Agree", width=20, height=3,justify="center", command=self.agreed,bg="lightgrey")
        disagree=tk.Button(self.creator,text="Disagree", width=20, height=3,justify="center", command=self.disagreed,bg="lightgrey")
        disclaimer=tk.Label(self.creator, text="Medisee is provided for educational and informational purposes only and does not constitute providing medical advice or professional services. The information provided should not be used for diagnosing or treating a health problem or disease, and those seeking personal medical advice should consult with a licensed physician", height=10, wraplength=400, font=('Helvetica', 10, 'bold'))
        disclaimer.pack()
        agree.pack()
        disagree.pack()
        self.searcher()
    def searcher(self):
        self.icon=ImageTk.PhotoImage(Image.open("./img/logo.PNG"))
        searchmessage=tk.Label(self.frm0, image=self.icon, height=150)
        searchbox=tk.Text(self.frm0,height="1", font=("Helvetica", 20), bg="lightgrey")
        searchbox.tag_configure("center", justify='center')
        searchbutt=tk.Button(self.frm0,text="Search", width=20, height=3,justify="center", command=lambda: self.drawdata(self.frm1),bg="lightgrey")
        nextbutt=tk.Button(self.frm0,text="Next", justify="center",width=20, height=3, command=lambda: self.next(self.frm1),bg="lightgrey")
        prevbutt=tk.Button(self.frm0,text="Previous", justify="center",width=20, height=3,command=lambda: self.prev(self.frm1), bg="lightgrey")
        self.pns=pagesearch=tk.Entry(self.frm0, width=25, bg="lightgrey")
        self.pns.insert(0, f"Search page number")
        pagesearch.bind("<FocusIn>", self.temp_text)
        pagesearch.bind("<FocusOut>", self.temp_text2)
        pagesearch.bind("<Return>", self.pagesearcher)
        #searchmessage.pack_propagate(True)
        searchmessage.pack(fill="both", expand="True")
        searchbox.pack(fill="x")
        searchbutt.pack(side="left", pady="20", padx=(0, 100))
        nextbutt.pack(side="left", pady="20")
        prevbutt.pack(side="left", pady="20")
        self.pns.pack(side="left", pady="20", padx="30")
    def pagesearcher(self, e):
        if len(self.move) == 0 or not self.pns.get().isdigit() or int(self.pns.get()) > len(self.data)//5 or int(self.pns.get()) <= 0:
            pass
        else:
            self.delete(self.frm1)
            self.offset = int(self.pns.get())-1
            show=self.move[self.offset]
            for n in range(0, len(show)):
                test=tk.Label(self.frm1, text=f"Age: {show[n].age}, Sex: {show[n].sex}, Drugs: {', '.join(show[n].drugs)}\n\n Reactions: {', '.join(show[n].reactions)}\n\n", font=('Helvetica', 10, 'bold'), justify='center', wraplength=700, bg="#358797")
                test.pack(pady=10)
            page=tk.Label(self.frm1, text=f"Page {self.offset+1}", font=('Helvetica', 15, 'bold'))
            page.pack()
    def temp_text(self, e):
        self.pns.delete(0, "end")
    def temp_text2(self, e):
        self.pns.insert(0, f"Search page number")
    def drawdata(self, frames):
        self.offset=0
        self.data= home.apicall(self.frm0.winfo_children()[1].get("1.0","end-1c"))
        self.move.clear()
        for i in range(0, len(self.data)):
            self.move[i//3].append(self.data[i])
        self.delete(frames)
        x=0
        for case in self.data:
            if x == 3:
                break
            else:
                test=tk.Label(frames, text=f"Age: {case.age}, Sex: {case.sex}, Drugs: {', '.join(case.drugs)}\n\n Reactions: {', '.join(case.reactions)}\n\n", font=('Helvetica', 10, 'bold'), justify='center', wraplength=700, bg="#358797")
                test.pack(pady=10)
            x+=1
        page=tk.Label(frames, text=f"Page 1", font=('Helvetica', 15, 'bold'))
        page.pack()
    def next(self, frames):
        if self.offset < len(self.data)//3:
            self.delete(frames)
            self.offset+=1
            show=self.move[self.offset]
            for n in range(0, len(show)):
                test=tk.Label(frames, text=f"Age: {show[n].age}, Sex: {show[n].sex}, Drugs: {', '.join(show[n].drugs)}\n\n Reactions: {', '.join(show[n].reactions)}\n\n", font=('Helvetica', 10, 'bold'), justify='center', wraplength=700, bg="#358797")
                test.pack(pady=10)
            page=tk.Label(frames, text=f"Page {self.offset+1}", font=('Helvetica', 15, 'bold'))
            page.pack()
        else:
            pass
        

    def prev(self, frames):
        if self.offset > 0:
            self.delete(frames)
            self.offset-=1
            show=self.move[self.offset]
            for n in range(0, len(show)):
                test=tk.Label(frames, text=f"Age: {show[n].age}, Sex: {show[n].sex}, Drugs: {', '.join(show[n].drugs)}\n\n Reactions: {', '.join(show[n].reactions)}\n\n", font=('Helvetica', 10, 'bold'), justify='center', wraplength=700, bg="#358797")
                test.pack(pady=10)
            page=tk.Label(frames, text=f"Page {self.offset+1}", font=('Helvetica', 15, 'bold'))
            page.pack()
        else:
            pass
    def delete(self, frames):
        for w in frames.winfo_children():
            w.destroy()
    def agreed(self):
        self.creator.destroy()
    def disagreed(self):
        self.creator.destroy()
        self.window.destroy()
        quit()
    def quit(self):
        self.window.destroy()
        quit()

def appy():
    root= tk.Tk()
    app= mainapp(root)
    root.protocol("WM_DELETE_WINDOW", app.quit)
    root.mainloop()
appy()