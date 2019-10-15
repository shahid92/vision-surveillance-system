from tkinter import *
import cv2
import time
import keyboard
import imutils
from PIL import Image,ImageTk
import datetime
# -------begin capturing and saving video
sample=1
counter=0
firstFrame = None
def callout():
   time.sleep(10)
   keyboard.press_and_release('q')
   
def startrecording():
   global sample,firstFrame,counter
   cap = cv2.VideoCapture(-1)
   #cam=cv2.VideoCapture(1)
   fourcc = cv2.VideoWriter_fourcc(*'XVID')
   video_name="{}.avi".format(sample)
   out = cv2.VideoWriter('recorded files/video'+video_name,fourcc,  20.0, (640,480))
   #callout()
   while True:
      
      ret, frame = cap.read()
      ret, frame1=cap.read()
      if ret==True:
         text = "nothing happend"
         if frame is None:
            break
         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
         gray = cv2.GaussianBlur(gray, (21, 21), 0)
         if firstFrame is None:
            firstFrame = gray
            continue
         frameDelta = cv2.absdiff(firstFrame, gray)
         thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
         thresh = cv2.dilate(thresh, None, iterations=1)
         cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
         cnts = cnts[0] if imutils.is_cv2() else cnts[1]
         for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.putText(frame, "DEFECT", (x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            text = "moment occured"
         if(text!="moment occured"):
            cv2.putText(frame,"Security Status2: {}".format(text), (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
         #counter=0
         else:
            cv2.putText(frame,"Security Status1: {}".format(text), (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            out.write(frame1)
            counter+=1
            if counter==1:
               attackDetails="Attack happen\t[TIME:"+str(datetime.datetime.now().strftime("%H:%M"))+"]"+"\t[DATE:"+str(datetime.date.today())+"]"
               print(attackDetails)
               ATTfile=open("attackdetails.txt","a+")
               ATTfile.write(attackDetails+"\n")
               ATTfile.close()
         cv2.imshow("recorder",frame)
         cv2.imshow("frame1",frame1)
      else:
         break
      k=cv2.waitKey(1)
      if k==ord('q'):
         break
   sample=sample+1
   out.release()
   cap.release()
   #cam.release()
   cv2.destroyAllWindows()

def MainModule():
   global main
   main=Tk()
   main.title("SAE(security asylum evident)")
   main.maxsize(500,500)
   main.minsize(500,500)
   main.iconbitmap("images/saeICO.ico")
   main.configure(bg="white")

   #FIRST FRAME
   FirstFrame=Frame(main,bg="white")
   
   back=Image.open("images/saeICO.ico")
   background=ImageTk.PhotoImage(back)

   
   
   Label(FirstFrame,bg="white",width=300, height=300,border=0,highlightthickness=0,image=background).pack()
   Label(FirstFrame,bg="white",fg="sky blue",width=3, height=1,text="SAE",border=0,font="helvetica 50 bold").pack(side=TOP)

   Label(FirstFrame,bg="white",fg="sky blue",text="RECORDING SYSTEM",border=0,font="helvetica 15 bold").pack()
   
   FirstFrame.grid(row=0,column=0)
   
   #SECOND FRAME
   SecondFrame=Frame(main)

   image1=Image.open("images/masterButton.png")
   master=ImageTk.PhotoImage(image1)
   image2=Image.open("images/helpButton.png")
   Help=ImageTk.PhotoImage(image2)
   image3=Image.open("images/exitButton.png")
   quitB=ImageTk.PhotoImage(image3)
   
   masterButton=Button(SecondFrame,image=master,border=0,highlightthickness=0,command=startrecording)
   masterButton.grid(row=0,column=1)
   #helpButton=Button(SecondFrame,image=Help,border=0,highlightthickness=0,command=HelpModule)
   #helpButton.grid(row=2,column=1)
   quitButton=Button(SecondFrame,image=quitB,border=0,highlightthickness=0,command=quit)
   quitButton.grid(row=3,column=1)
   
   SecondFrame.grid(row=0,column=1)
   
   main.mainloop()

MainModule()
