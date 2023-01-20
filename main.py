import glob
import os
import shutil
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import random
from random import randrange

class GUI:
    Pathlist ={}
    Eloranking = None
    baseHeight = 500
    numPictures = None
    numIterations = 1
    rightPictureLabel = None
    leftPictureLabel = None
    currLeftPos= None
    currRightPos = None
    currIterator = 0
    sequence = []

    def __init__(self):     
        # self.picture_path = "D:\\_Bilder\\Archiv\\2022\\10\\10_30 Bodensee"
        self.picture_path = filedialog.askdirectory()
        self.Pathlist = glob.glob(self.picture_path+"/*.jpg")  
        self.numPictures = len(self.Pathlist)
        self.Eloranking = [1000] * self.numPictures
        tempSequence = None
        tempSequence = list(range(0,self.numPictures))
        for i in range(self.numIterations):
            random.shuffle(tempSequence)
            self.sequence = self.sequence+tempSequence    
        self.root = tk.Tk()  
        self.setupGUI() 
        self.newPictures()
        self.root.mainloop()

    def setupGUI(self):
        rightPicture = Image.open("testimage.png")
        rightPicture = ImageTk.PhotoImage(rightPicture)
        self.rightPictureLabel = tk.Label(self.root, image=rightPicture)
        self.rightPictureLabel.pack(side='right')

        leftPicture = Image.open("testimage.png")
        leftPicture = ImageTk.PhotoImage(leftPicture)
        self.leftPictureLabel = tk.Label(self.root, image=leftPicture)
        self.leftPictureLabel.pack(side='left')
        
        self.leftPictureLabel.bind("<Button-1>", self.on_left_image_click)
        self.rightPictureLabel.bind("<Button-1>", self.on_right_Image_clicked)
    
    def newPictures(self):
        self.currLeftPos = self.sequence[self.currIterator]
        self.currRightPos = self.sequence[self.currIterator+1]

        leftPic = self.Pathlist[self.currLeftPos]
        rightPic = self.Pathlist[self.currRightPos]
        self.newLeftPicture = Image.open(leftPic)        
        self.spercent = (self.baseHeight/float(self.newLeftPicture.size[1]))
        self.wsize = int((float(self.newLeftPicture.size[0])*float(self.spercent)))
        self.newLeftPicture= self.newLeftPicture.resize((self.wsize,self.baseHeight), Image.Resampling.LANCZOS)
        self.newLeftPicture = ImageTk.PhotoImage(self.newLeftPicture)
        self.leftPictureLabel.configure(image=self.newLeftPicture)

        self.newRightPicture = Image.open(rightPic)        
        self.spercent = (self.baseHeight/float(self.newRightPicture.size[1]))
        self.wsize = int((float(self.newRightPicture.size[0])*float(self.spercent)))
        self.newRightPicture= self.newRightPicture.resize((self.wsize,self.baseHeight), Image.Resampling.LANCZOS)
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
            print("Done!")

    def calculateElo(self,left,right):
        self.currEloLeft = 10 ** (self.Eloranking[self.currLeftPos]/400)
        self.currEloRight = 10 ** (self.Eloranking[self.currRightPos]/400)

        self.expectedLeft = self.currEloLeft/(self.currEloLeft+self.currEloRight)  
        self.expectedRight = self.currEloRight/(self.currEloLeft+self.currEloRight)

        self.Eloranking[self.currLeftPos] = self.Eloranking[self.currLeftPos] + 32 * (left-self.expectedLeft)
        self.Eloranking[self.currRightPos] = self.Eloranking[self.currRightPos] + 32 * (right-self.expectedRight)
        print(self.Eloranking)


GUI()
