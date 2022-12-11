#coding=gbk
from tkinter import Tk, Label, Button
from tkinter import filedialog
from pydub import AudioSegment
import os
import sys
import tkinter
import tkinter.ttk



class ProcessBar():
    
    def __init__(self):        
        self.process = ttk.Progressbar(root, length=200, mode="determinate",maximum=100,orient=tk.HORIZONTAL)   
        self.process.place(x=100, y=10)
 
    def value(self, per):
        self.process["value"]  = per
        root.update()



class GUI:
    def __init__(self, master):
        self.master = master





        sw = master.winfo_screenwidth()
        # 得到屏幕宽度
        sh = master.winfo_screenheight()

        # 得到屏幕高度
        ww = 450
        wh = 50

        x = (sw - ww) / 2
        y = (sh - wh) / 2
        master.geometry("%dx%d+%d+%d" % (ww, wh, x, y))

        master.title("ClickBuilder for MegaHackBot - by Funoke & Lwhe")


        self.label = Label(master, text="Click it and choose a json file!")
        self.label.pack()

        self.greet_button = Button(master, text="BOOM", command=self.greet)
        self.greet_button.pack()

    def greet(self):

        root1 = tkinter.Tk()
        root1.title("Progress Bar")
        root1.geometry('150x25')
        progressbarOne = tkinter.ttk.Progressbar(root1)
        progressbarOne.pack(side=tkinter.TOP)

        filepath = filedialog.askopenfilename()
        
        file_object = open(filepath,'r',encoding='utf-8')
        try:
            thefile = file_object.readlines()
        finally:
            file_object.close()

        count = 0
        for line in thefile:
            count = count + 1

        f = float(thefile[count-3][-4:-1])

        f1 = float(thefile[count-10][12:-2])

        s=0
        B1=[]
        while s<=f1:
            B1.append(0)
            s=s+1
        s=0
        h=(count-8)/8
        print(h)
        while s<h:
            if "true" in str(thefile[int(5+8*s)]):
                f2 = int(thefile[int(6+8*s)][12:-2])
                B1[f2]=1
                s=s+1
                print(s)
            elif "false" in str(thefile[int(5+8*s)]):
                f2 = int(thefile[int(6+8*s)][12:-2])
                B1[f2]=2
                s=s+1
                print(s)
            else: s=s+1
        s=0
        s1=0
        print(B1)
        B2=[]
        while s<=f1:
            if B1[s]==0:
                s=s+1
            elif B1[s]==2:
                s=s+1
            elif B1[s]==1:
                B2.append((s-s1)/f)
                s1=s
                s=s+1
        s=0
        s1=0
        B3=[]
        while s<=f1:
            if B1[s]==0:
                s=s+1
            elif B1[s]==1:
                s=s+1
            elif B1[s]==2:
                B3.append((s-s1)/f)
                s1=s
                s=s+1

        print(B2)
        print(B3)

        s=0
        s1=0
        B4=[]
        while s<len(B2):
            if B2[s]<0.001:
                B2[s+1]=float(B2[s]+B2[s+1])
                s=s+1
            if B2[s]>=0.001:
                B4.append(B2[s])
                s=s+1
        s=0
        s1=0
        B5=[]
        while s<len(B3):
            if B3[s]<0.001:
                B3[s+1]=float(B3[s]+B3[s+1])
                s=s+1
            if B3[s]>=0.001:
                B5.append(B3[s])
                s=s+1
        B5[0]=B5[0]+0.05
        print(B4)
        print(B5)



        


        croot = str(os.getcwd())
        cpa = str("\\release\\c\\c.wav")
        rpa = str("\\release\\r\\r.wav")
        repa = str("\\result\\result.wav")
        c = AudioSegment.from_wav(str(croot+cpa))
        r = AudioSegment.from_wav(str(croot+rpa))
        t1=len(c)
        t2=len(r)


        def match_target_amplitude(sound, target_dBFS):
            change_in_dBFS = target_dBFS - sound.dBFS
            return sound.apply_gain(change_in_dBFS)


        m1=AudioSegment.empty()
        s=0

        



        while s<len(B4):
            if B4[s]>(t1/1000):
                m2=AudioSegment.silent(duration=(1000*(B4[s]-(t1/1000))))
                if B4[s]<=0.22:
                    db = c.dBFS
                    c = match_target_amplitude(c, db - 5)
                m1=m1+m2+c
                if B4[s]<=0.22:
                    db = c.dBFS
                    c = match_target_amplitude(c, db + 5)
                s=s+1
            elif B4[s]<(t1/1000):
                m2=c[:(B4[s])*1000]
                db = m2.dBFS
                m2 = match_target_amplitude(m2, db - 10)
                m1=m1+m2
                s=s+1
            progressbarOne['maximum'] = 100
            progressbarOne['value'] = s/len(B4)*100
            root1.update()
            print(s/len(B4))


        s=0
        m3=AudioSegment.empty()
        while s<len(B5):
            if B5[s]>(t2/1000):
                m2=AudioSegment.silent(duration=(1000*(B5[s]-(t2/1000))))
                if B5[s]<=0.22:
                    db = r.dBFS
                    r = match_target_amplitude(r, db - 5)
                m3=m3+m2+r
                if B5[s]<=0.22:
                    db = r.dBFS
                    r = match_target_amplitude(r, db + 5)
                s=s+1
            elif B5[s]<(t2/1000):
                m2=r[:(B5[s])*1000]
                db = m2.dBFS
                m2 = match_target_amplitude(m2, db - 10)
                m3=m3+m2
                s=s+1
            progressbarOne['maximum'] = 100
            progressbarOne['value'] = s/len(B4)*100
            root1.update()
            print(s/len(B5))

        output = m3.overlay(m1)
        output.export("result.wav",format="wav")







root = Tk()
my_gui = GUI(root)
root.mainloop()