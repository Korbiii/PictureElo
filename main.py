import glob
import os
import shutil
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk,ImageEnhance
import random
from random import randrange

class GUI:
    baseHeight = 1000
    numIterations = 10
    currIterator = 0 
    kValue = 64 
    picturesSelected = False 

    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("green")

    def __init__(self): 
        self.root = ctk.CTk()  
        
        self.root.title("PictureElo")
        self.root.grid_columnconfigure(1, weight=1)

        self.KvalueSlider = ctk.CTkSlider(self.root, from_=32, to=128,command =self.updateKvalue)
        self.KvalueSlider.set(self.kValue)
        self.KvalueSlider.grid(row=0,column=0,columnspan=4)

        self.IterationSlider = ctk.CTkSlider(self.root, from_=3, to=12,command =self.updateIterationValue)
        self.IterationSlider.set(self.numIterations)
        self.IterationSlider.grid(row=1,column=0,columnspan=4)

        self.KvalueLabel = ctk.CTkLabel(self.root,text="K_Value: "+str(self.kValue))
        self.KvalueLabel.grid(row=0,column=4)

        self.IterationsLabel = ctk.CTkLabel(self.root,text="Iterations: "+str(self.numIterations))
        self.IterationsLabel.grid(row=1,column=4)

        self.pathLabel = ctk.CTkLabel(self.root,text="No Pictures Selected")
        self.pathLabel.grid(row=3,column=0,columnspan=3,pady=5,padx=5)

        self.selectFolderButton = ctk.CTkButton(self.root,text="Choose Pictures Path!",command=self.choosePath)
        self.selectFolderButton.grid(row=3,column=3,pady=5,padx=5)

        self.startButton = ctk.CTkButton(self.root,text="Start!",command=self.startComparison, state= tk.DISABLED)
        self.startButton.grid(row=3,column=4,pady=5,padx=5)

        self.root.mainloop()
        
    def updateKvalue(self,event):
         self.kValue = self.KvalueSlider.get()
         self.KvalueLabel.configure(text="K_Value: "+str(int(self.kValue)))

    def updateIterationValue(self,event):
         self.numIterations = int(self.IterationSlider.get())
         self.IterationsLabel.configure(text="Iterations: "+str(self.numIterations))

    def choosePath(self):
        self.picture_path = filedialog.askdirectory()
        self.Pathlist = glob.glob(self.picture_path+"/*.jpg")  
        self.numPictures = len(self.Pathlist)
        self.pathLabel.configure(text = str(self.numPictures) + " Pictures selected")
        if self.numPictures>0:
            self.startButton.configure(state=tk.ACTIVE)


    def startComparison(self): 
        self.Eloranking = [1000] * self.numPictures
        tempSequence = None
        tempSequence = list(range(0,self.numPictures))
        self.sequence = []
        for i in range(self.numIterations):
            random.shuffle(tempSequence)
            self.sequence = self.sequence+tempSequence    
        
        self.setupGUI() 
        self.newPictures()
        



    def setupGUI(self):        
        for widget in self.root.winfo_children():
            widget.destroy()

        self.rightPictureLabel = tk.Label(self.root)
        self.rightPictureLabel.pack(side='right')

        self.leftPictureLabel = tk.Label(self.root)
        self.leftPictureLabel.pack(side='left')
        
        self.leftPictureLabel.bind("<Button-1>", self.on_left_image_click)
        self.leftPictureLabel.bind('<Enter>', self.on_enter_left)
        self.leftPictureLabel.bind('<Leave>',self.on_leave_left)

        self.rightPictureLabel.bind("<Button-1>", self.on_right_Image_clicked)
        self.rightPictureLabel.bind('<Enter>', self.on_enter_right)
        self.rightPictureLabel.bind('<Leave>',self.on_leave_right)
    
    def on_enter_left(self,event):
        self.leftPictureLabel.configure(image=self.newLeftPictureHover)

    def on_leave_left(self,event):
        self.leftPictureLabel.configure(image=self.newLeftPicture)

    def on_enter_right(self,event):
        self.rightPictureLabel.configure(image=self.newRightPictureHover)

    def on_leave_right(self,event):
        self.rightPictureLabel.configure(image=self.newRightPicture)

    def newPictures(self):
        self.currLeftPos = self.sequence[self.currIterator]
        self.currRightPos = self.sequence[self.currIterator+1]

        leftPic = self.Pathlist[self.currLeftPos]
        rightPic = self.Pathlist[self.currRightPos]
        self.newLeftPicture = Image.open(leftPic)        
        self.spercent = (self.baseHeight/float(self.newLeftPicture.size[1]))
        self.wsize = int((float(self.newLeftPicture.size[0])*float(self.spercent)))
        self.newLeftPicture= self.newLeftPicture.resize((self.wsize,self.baseHeight), Image.Resampling.LANCZOS)
        enhancer = ImageEnhance.Brightness(self.newLeftPicture)
        self.newLeftPictureHover = enhancer.enhance(1.1)
        self.newLeftPictureHover = ImageTk.PhotoImage(self.newLeftPictureHover)
        self.newLeftPicture = ImageTk.PhotoImage(self.newLeftPicture)
        self.leftPictureLabel.configure(image=self.newLeftPicture)

        self.newRightPicture = Image.open(rightPic)        
        self.spercent = (self.baseHeight/float(self.newRightPicture.size[1]))
        self.wsize = int((float(self.newRightPicture.size[0])*float(self.spercent)))
        self.newRightPicture= self.newRightPicture.resize((self.wsize,self.baseHeight), Image.Resampling.LANCZOS)
        enhancer = ImageEnhance.Brightness(self.newRightPicture)
        self.newRightPictureHover = enhancer.enhance(1.1)
        self.newRightPictureHover = ImageTk.PhotoImage(self.newRightPictureHover)
        self.newRightPicture = ImageTk.PhotoImage(self.newRightPicture)
        self.rightPictureLabel.configure(image=self.newRightPicture)

     
    def on_left_image_click(self,event):
        self.calculateElo(1,0)
        if self.currIterator < self.numPictures*self.numIterations:
            self.newPictures()
            self.currIterator = self.currIterator+2
        else:
            destination_folder = self.picture_path + "/ranked"
            if not os.path.exists(destination_folder):
                os.mkdir(destination_folder)
            for file in self.Pathlist:
                shutil.copy(file, destination_folder)
            print("Done!")            
            self.addElotoFile()
            self.root.destroy()

    def on_right_Image_clicked(self,event):        
        self.calculateElo(0,1)
        if self.currIterator < self.numPictures*self.numIterations:
            self.newPictures()
            self.currIterator = self.currIterator+2
        else:
            destination_folder = self.picture_path + "/ranked"
            if not os.path.exists(destination_folder):
                os.mkdir(destination_folder)
            for file in self.Pathlist:
                shutil.copy(file, destination_folder)
            self.root.destroy()
            self.addElotoFile()
            print("Done!")

    def calculateElo(self,left,right):
        self.currEloLeft = 10 ** (self.Eloranking[self.currLeftPos]/400)
        self.currEloRight = 10 ** (self.Eloranking[self.currRightPos]/400)

        self.expectedLeft = self.currEloLeft/(self.currEloLeft+self.currEloRight)  
        self.expectedRight = self.currEloRight/(self.currEloLeft+self.currEloRight)

        self.Eloranking[self.currLeftPos] = self.Eloranking[self.currLeftPos] + self.kValue * (left-self.expectedLeft)
        self.Eloranking[self.currRightPos] = self.Eloranking[self.currRightPos] + self.kValue * (right-self.expectedRight)

    def addElotoFile(self):
        intEloranking = list(map(int,self.Eloranking))
        folderpath = self.picture_path + "/ranked"
        files = os.listdir(folderpath)

        for i,file_name in enumerate(files):
            old_path = os.path.join(folderpath, file_name)
            new_name = f"{intEloranking[i]}_{file_name}"
            new_path = os.path.join(folderpath, new_name)
            os.rename(old_path, new_path)


GUI()
