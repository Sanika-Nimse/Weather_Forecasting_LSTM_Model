from tkinter import *
from tkinter.ttk import *
from time import strftime
import tkinter as tk
from PIL import Image,ImageTk



root=tk.Tk()
root.configure(background='white')
w,h=root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w,h))
#root.title("hello")

image2=Image.open("weather9.jpg")
image2=image2.resize((w,h),Image.ANTIALIAS)

background_image= ImageTk.PhotoImage(image2)

background_label=tk.Label(root,image=background_image)

background_label.image=background_image
  
background_label.place(x=0,y=0)

label=tk.Label(root,text="",font=("Calibri",45),
               bg="white",
               width=50,
               height=0)
label.place(x=0,y=0)



label=tk.Label(root,text="Weather Prediction And forcasting using Machine Learning ",font=("Calibri",40),
               bg="#8DB6CD",
               width=50,
               height=1)
label.place(x=0,y=0)        

# btn=tk.Button(root,text="Login",font=("Arial",15),width=7,
#               bg="light gray",
#               #fg="white",
#             )
# btn.place(x=1200,y=20)

# btn=tk.Button(root,text="Register",font=("Arial",15),width=7,
#               bg="light gray",
#               #fg="white",
#             )
# btn.place(x=1320,y=20)



#root.config(menu=menubar)


label=tk.Label(root,text='''
               Weather forecasting is the application of science and technology to predict
               the conditions of the atmosphere for a given location and time.
               People have attempted to predict the weather informally for
               millennia and formally since the 19th century.
               '''
               ,font=("Calibri",12),
               
               fg="black")
label.place(x=850,y=400)

label=tk.Label(root,text='''
               There is a vast variety of end uses for weather forecasts.
               Weather warnings are important because they are used to protect
               lives and property. Forecasts based on temperature and 
               precipitation are important to agriculture, and therefore
               to traders within commodity markets. Temperature forecasts
               are used by utility companies to estimate demand over coming days.
               '''
               ,font=("Calibri",12),
               
                fg="black")
label.place(x=850,y=200)


label=tk.Label(root,text='''
               There is a vast variety of end uses for weather forecasts.
               Weather warnings are important because they are used to protect 
               lives and property. Forecasts based on temperature and 
               precipitation are important to agriculture, and therefore
               to traders within commodity markets.
               ''',font=("Calibri",12),
                
                fg="black")
label.place(x=80,y=200)



label=tk.Label(root,text='''
               There is a vast variety of end uses for weather forecasts.
               Weather warnings are important because they are used to protect
               lives and property. Forecasts based on temperature and 
               precipitation are important to agriculture, and therefore
               to traders within commodity markets.
               ''',font=("Calibri",12),
                
                fg="black")
label.place(x=80,y=400)


root.mainloop()