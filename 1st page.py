import tkinter as tk
from PIL import Image,ImageTk
from tkvideo import tkvideo


root=tk.Tk()
root.configure(background='white')
w,h=root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w,h))
root.title("hello")



video_label = tk.Label(root)
video_label.pack()

player = tkvideo("127351 (720p).mp4", video_label, loop=1, size=(w, h))
player.play()


# image2=Image.open("C:/Users/COMPUTER/Downloads/weather6.jpg")
# image2=image2.resize((w,h),Image.ANTIALIAS)

# background_image= ImageTk.PhotoImage(image2)

# background_label=tk.Label(root,image=background_image)

# background_label.image=background_image
  # background_label.place(x=0,y=0)


label=tk.Label(root,text="Weather Prediction And forcasting using Machine Learning ",font=("Calibri",40),
               bg="#8DB6CD",
               width=58,
               height=1)
label.place(x=0,y=0)        



def log():
    from subprocess import call
    call(['python','Login from1.py'])

btn=tk.Button(root,text="Login",command=log,font=("Arial",15),width=7,
              bg="light gray",
              #fg="white",
            )
btn.place(x=980,y=400)

def reg():
    from subprocess import call
    call(['python','final Reg.py'])

btn=tk.Button(root,text="Register",command=reg,font=("Arial",15),width=7,
              bg="light gray",
              #fg="white",
            )
btn.place(x=1120,y=400)







register1=tk.Label(root,text="Kindly register here...." ,font=('Cambria',10)).place(x=1130,y=350)





root.mainloop()