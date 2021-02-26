import tkinter as tk                # python 3
from tkinter import font as tkfont  # python 3
from tkinter import StringVar, Tk
from pynput.keyboard import Listener
import RPi.GPIO as GPIO
import time
from time import sleep
from rpi_python_drv8825.stepper import StepperMotor

######### GPIO setup
## MotorName = StepperMotor(enablePin, stepPin, dirPin)

enable_pin = 23
step_pin = 24
dir_pin = 25
motor_sample = StepperMotor(enable_pin, step_pin, dir_pin)
motor_solution = StepperMotor(enable_pin, step_pin, dir_pin)
#########

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        self.root = tk.Tk.__init__(self, *args, **kwargs)
        #fullscreen
        self.attributes('-fullscreen',True)
        self.bind("<Escape>", self.quitFullScreen)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry('1200x1200')
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self, width=600, height=600, background="#4974a5")
        self['bg']='#4974a5'
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, LegiPage, MotorPage, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.attributes("-fullscreen", self.fullScreenState)

    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.attributes("-fullscreen", self.fullScreenState)

    def log_keystroke(self, key):
        key = str(key).replace("'", "")

        if key == 'S' or key == '0' or key == '1' or key == '2' or key == '3' or key == '4' or key == '5' or key == '6' or key == '7' or key == '8' or key == '9':
            scanned_item.append(key)
        else:
            pass

    def scan(self):
        #Scan for 0.5 secs and return 
        listener = Listener(on_press=self.log_keystroke) 
        listener.start()
        time.sleep(0.5)
        listener.stop()

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def run_scanner(self):
        running = True 
        i=0
        while running:
            global scanned_item
            scanned_item = []
            self.scan()

            scanned_item = [] if len(scanned_item) != 9 else scanned_item
            print_scan = ''.join(scanned_item)
            var.set(print_scan) if scanned_item != [] else var
            self.update_idletasks()

            if scanned_item == ['S','1','4','9','4','3','7','5','7']:
                var.set("--") 
                var2.set("Please activate scanner!") 
                break
            # elif scanned_item == ['S','1','1','9','4','7','8','7','6']:
            #     var.set("--") 
            #     var2.set("Please activate scanner!") 
                # break
            else:
                pass    


            if i % 4 == 0:
                var2.set("scaning")
            elif i % 4 == 1:
                var2.set("scanning.")
            elif i % 4 == 2:
                var2.set("scanning..")
            elif i % 4 == 3:
                var2.set("scanning...")
            i+=1
            self.update_idletasks() 

    def limit_switch(self):
        GPIO.setmode(GPIO.BCM)

        pushpin = 2 # set input push button pin
        GPIO.setup(pushpin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # with pull up resistor

        iteration = 30
        i = 0
        while i < iteration:
            to_console = GPIO.input(pushpin)
            var.set(str(to_console))
            self.update_idletasks()
            sleep(0.2)
            i+=1

    def refresh(self):
        self.destroy()
        self.__init__()


    def movemotor_sample(event):
        # Enable motor and run motor script        
        motor1.enable(True)        # enables stepper driver
        motor1.run(1600, True)     # run motor 6400 steps clowckwise
        sleep(0.5)
        motor1.run(1600, False)    # run motor 6400 steps counterclockwise
        motor1.enable(False)       # disable stepper driver

    def movemotor_solution(event):
        # Enable motor and run motor script        
        motor2.enable(True)        # enables stepper driver
        motor2.run(1600, True)     # run motor 6400 steps clowckwise
        sleep(0.5)
        motor2.run(1600, False)    # run motor 6400 steps counterclockwise
        motor2.enable(False)       # disable stepper driver

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame( width=100, height=100, background="bisque")
        self.controller = controller
        self['bg']='#4974a5'
        global var

        label = tk.Label(self, text="Covid Test Station Hack Panel", font=controller.title_font,background='#4974a5')
        label.pack(side="top", fill="x", pady=10)


        button1 = tk.Button(self, text="Scan Legi",
                            command=lambda: controller.show_frame("LegiPage"), height = 3, width = 25)
        # button2 = tk.Button(self, text="Limit Switch",
        #                     command=lambda: controller.limit_switch(), height = 2, width = 10)
        button3 = tk.Button(self, text="Motor Controls",
                            command=lambda: controller.show_frame("MotorPage"), height = 3, width = 25)       
        button4 = tk.Button(self, text="--EXIT--",
                            command=lambda: controller.refresh(), height = 3, width = 15)

        #button1.place(pady=40)
        button1.place(x=200, y=200)
        # button2.place(x=320, y=250)
        button3.place(x=200, y=300)
        button4.pack(side="bottom")

class LegiPage(tk.Frame):
#include legipage in self.frames = {}
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self['bg']='#4974a5'

        #Definition of variables that are supposed to be updated
        #To show legi number
        global var
        var = StringVar()
        var.set("--") 

        #To show readyness
        global var2
        var2 = StringVar()
        var2.set("Please activate scanner!") 

        label = tk.Label(self, text="Scanner Page", font=tkfont.Font(family='Helvetica', size=25, weight="bold"),background='#4974a5')
        label.pack(side="top", fill="x", pady=10)

        label2 = tk.Label(self, textvariable = var, font=controller.title_font,background='#4974a5')
        label2.pack()

        label3 = tk.Label(self, textvariable = var2, font=tkfont.Font(family='Helvetica', size=25),background='#4974a5')
        label3.pack()

        button1 = tk.Button(self, text="Start Scan",
                            command=lambda: controller.run_scanner())
        button = tk.Button(self, text="Go to Hack Panel",
                           command=lambda: controller.show_frame("StartPage"),height = 3, width = 25)
        button1.pack()
        button.pack(side="bottom") 


class MotorPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self['bg']='#4974a5'

        button1 = tk.Button(self, text="Dispenser Sample Tube",
                            command=lambda: controller.movemotor_sample(), height = 3, width = 25)
        button2 = tk.Button(self, text="Dispenser Transport Solution",
                            command=lambda: controller.movemotor_solution(), height = 3, width = 25)
        # button3 = tk.Button(self, text="Move Motor 3",
        #                     command=lambda: controller.movemotor())

        button = tk.Button(self, text="Go to Hack Panel",
                           command=lambda: controller.show_frame("StartPage"), height = 3, width = 25)
        button1.place(x=200, y=200)
        button2.place(x=200, y=300)
        # button3.place(x=200, y=300)
        button.pack(side="bottom")


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self['bg']='#4974a5'
        label = tk.Label(self, text="Scan Legi", font=controller.title_font,background='#4974a5')
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()