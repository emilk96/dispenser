import tkinter as tk #GUI
from tkinter import font as tkfont  
from tkinter import StringVar, Tk
from tkinter import simpledialog
from pynput.keyboard import Listener #Barcode
import RPi.GPIO as GPIO #Motors
from rpi_python_drv8825.stepper import StepperMotor
import time
from time import sleep

### GPIO setup
# Enable pin is the same for all motors, dir/step pins are unique (Check Raspberry GPIO pin diagram)
enable_pin = 23
step_pin1 = 24
dir_pin1 = 25
step_pin2 = 17
dir_pin2 = 27

motor_sample = StepperMotor(enable_pin, step_pin1, dir_pin1)
motor_solution = StepperMotor(enable_pin, step_pin2, dir_pin2)
###

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        self.root = tk.Tk.__init__(self, *args, **kwargs)
        #Fullscreen
        self.attributes('-fullscreen',True)
        self.bind("<Escape>", self.quitFullScreen)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry('800x480')
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self, width=800, height=480, background="#4974a5")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, LegiPage, PageOne, PageTwo, PageThree, PageFour, PageFive):
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

        # Only recognize symbols from legi
        if key == 'S' or key == 'P' or \
            key == '0' or key == '1' or key == '2' or key == '3' or key == '4' or key == '5' or key == '6' or key == '7' or key == '8' or key == '9':
            scanned_item.append(key)
        else:
            pass

    def scan(self):
        # Scan for 0.5s, scanner dumps legi number as keystrokes in a short time interval.
        # Not perfect because if the actual scanning doesn't completely happen during time.sleep it will split
        # the scanned data (sanity of data is checked at a later step, nontheless user will have to scan twice.)
        listener = Listener(on_press=self.log_keystroke) 
        listener.start()
        time.sleep(0.5)
        listener.stop()
            # listener.stop() sometimes runtime error because it can't stop the listener. 
            # Use additional thread to run scanner and kill from the outside?
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

            scanned_item = [] if len(scanned_item) != 9 else scanned_item # Check legi number
            print_scan = ''.join(scanned_item)
            var.set(print_scan) if scanned_item != [] else var
            self.update_idletasks()

            if scanned_item == ['S','1','4','9','4','3','7','5','7']:
                var.set("--") 
                var2.set("Please activate scanner!") 
                break
            elif scanned_item == ['S','1','1','9','4','7','8','7','6']:
                var.set("--") 
                var2.set("Please activate scanner!") 
                break
            else:
                pass    
                # Emil's and Felix's legi numbers stop the scan

            if i % 4 == 0:
                var2.set("scanning")
            elif i % 4 == 1:
                var2.set("scanning.")
            elif i % 4 == 2:
                var2.set("scanning..")
            elif i % 4 == 3:
                var2.set("scanning...")
                # Show system is ready to the user
            i+=1
            self.update_idletasks() 


    def demo(self):
        while True:
            global scanned_item
            scanned_item = []
            self.scan()

            scanned_item = [] if len(scanned_item) != 9 else scanned_item

            if len(scanned_item) == 9:
                self.movemotor_sample_forward()
                self.movemotor_solution_backward()
                break
            else:
                pass    
        
    """
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
    """

    def refresh(self):
        self.destroy()
        self.__init__()

    # def movemotor_sample_forward(event):
    #     # Enable motor and run motor script        
    #     motor_sample.enable(True)        # enables stepper driver
    #     motor_sample.run(1600, True)     # run motor 1600 steps clowckwise
    #     sleep(0.5)
    #     motor_sample.run(1600, False)    # run motor 1600 steps counterclockwise
    #     motor_sample.enable(False)       # disable stepper driver
    
    def movemotor_sample_forward(event):
        # Enable motor and run motor script        
        motor_sample.enable(True)        # enables stepper driver
        motor_sample.run(1600, True)     # run motor steps clowckwise
        motor_sample.enable(False)       # disable stepper driver

    def movemotor_sample_backward(event):
        # Enable motor and run motor script        
        motor_sample.enable(True)        # enables stepper driver
        motor_sample.run(1600, False)    # run motor steps counterclockwise
        motor_sample.enable(False)       # disable stepper driver

    def movemotor_solution_forward(event):
        # Enable motor and run motor script        
        motor_solution.enable(True)        # enables stepper driver
        motor_solution.run(1600, True)     # run motor steps clowckwise
        motor_solution.enable(False)       # disable stepper driver
    
    def movemotor_solution_backward(event):
        # Enable motor and run motor script        
        motor_solution.enable(True)        # enables stepper driver
        motor_solution.run(1600, False)    # run motor steps counterclockwise
        motor_solution.enable(False)       # disable stepper driver

class numPad(simpledialog.Dialog):
    def __init__(self,master=None,parent=None):
        self.parent = parent
        self.top = tk.Toplevel(master=master)
        self.top.protocol("WM_DELETE_WINDOW",self.ok)
        self.createWidgets()

    def createWidgets(self):
        btn_list = ['7',  '8',  '9', '4',  '5',  '6', '1',  '2',  '3', '0',  'Close',  'Del']
        # create and position all buttons with a for-loop
        # r, c used for row, column grid values
        r = 1
        c = 0
        n = 0
        # list(range()) needed for Python3
        btn = []
        for label in btn_list:
            # partial takes care of function and argument
            cmd = lambda x = label: self.click(x)
            # create the button
            cur = tk.Button(self.top, text=label, width=10, height=5, command=cmd)
            btn.append(cur)
            # position the button
            btn[-1].grid(row=r, column=c)
            # increment button index
            n += 1
            # update row/column position
            c += 1
            if c == 3:
                c = 0
                r += 1

    def click(self,label):
        print(label)
        if label == 'Del':
            currentText = self.parent.textEntryVar.get()
            self.parent.textEntryVar.set(currentText[:-1])
        elif label == 'Close':
            self.ok()
        else:
            currentText = self.parent.textEntryVar.get()
            self.parent.textEntryVar.set(currentText+label)

    def ok(self):
        self.top.destroy()
        self.top.master.focus()



class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame( width=800, height=480, background="bisque")
        self.controller = controller
        # self['bg']='#4974a5'
        imageEx = tk.PhotoImage(file='ETH_bg.png')
        self.image = imageEx
        label_bg = tk.Label(self, image=imageEx)
        label_bg.place(x=0, y=0)

        button1 = tk.Button(self, text="Scan Legi", width=20, height=5,bg='#4974a5', fg='white',
                            command=lambda: controller.show_frame("LegiPage"))
        button2 = tk.Button(self, text="Sample", width=20, height=5,bg='#4974a5', fg='white',
                            command=lambda: controller.show_frame("PageOne"))
        button3 = tk.Button(self, text="Solution", width=20, height=5,bg='#4974a5', fg='white',
                            command=lambda: controller.show_frame("PageTwo"))
        button4 = tk.Button(self, text="Set Motor 1", width=20, height=5,bg='white', fg='white',
                            command=lambda: controller.show_frame("PageThree"))
        button5 = tk.Button(self, text="Set Motor 2", width=20, height=5,bg='white', fg='white',
                            command=lambda: controller.show_frame("PageFour"))
        button6 = tk.Button(self, text="Demo", width=20, height=5,bg='#4974a5', fg='white',
                            command=lambda: controller.show_frame("PageFive"))
        button7 = tk.Button(self, text="--EXIT--", width=20, height=3, bg='black', fg='white',
                            command=lambda: controller.refresh())

        x_firstcolumn = 100
        x_secondcolumn = 320
        x_thirdcolumn = 540
        y_firstrow = 100
        y_secondrow = 250
        y_thirdrow=400

        button1.place(x=x_firstcolumn, y=y_firstrow)
        button2.place(x=x_secondcolumn, y=y_firstrow)
        button3.place(x=x_thirdcolumn, y=y_firstrow)
        button4.place(x=x_firstcolumn, y=y_secondrow)
        button5.place(x=x_secondcolumn, y=y_secondrow)
        button6.place(x=x_thirdcolumn, y=y_secondrow)
        button7.place(x=x_secondcolumn, y=y_thirdrow)

class LegiPage(tk.Frame):
#include legipage in self.frames = {}
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self['bg']='#4974a5'
        imageBg = tk.PhotoImage(file='ETH_bg.png')
        self.image = imageBg
        label_bg = tk.Label(self, image=imageBg)
        label_bg.place(x=0, y=0)

        #Definition of variables that are supposed to be updated
        #To show legi number
        global var
        var = StringVar()
        var.set("--") 

        #To show readyness
        global var2
        var2 = StringVar()
        var2.set("Please activate scanner!") 

        x_firstcolumn = 220
        x_middlecolumn = 330
        x_secondcolumn = 440
        y_firstrow = 150

  
        label2 = tk.Label(self, textvariable = var, font=controller.title_font)
        label2.place(x=x_middlecolumn, y=50)

        label3 = tk.Label(self, textvariable = var2, font=controller.title_font)
        label3.place(x=x_middlecolumn, y=90)

        button1 = tk.Button(self, text="Start Scan",width=20, height=5,bg='#4974a5', fg='white',
                            command=lambda: controller.run_scanner())
        button = tk.Button(self, text="Go to Start page",
                           command=lambda: controller.show_frame("StartPage"))
        button1.place(x=x_middlecolumn, y=y_firstrow)
        button.place(x=350, y=400)




class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self['bg']='#4974a5'
        imageBg = tk.PhotoImage(file='ETH_bg.png')
        self.image = imageBg
        label_bg = tk.Label(self, image=imageBg)
        label_bg.place(x=0, y=0)

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))

        button.place(x=350, y=400)

        #Motor Functions, dispense and sample must move in opposite directions
        button1 = tk.Button(self, text="Dispense Sample Tube", width=20, height=5,bg='#4974a5', fg='white',
                            command=lambda: controller.movemotor_sample_forward())
        button2 = tk.Button(self, text="Move Back Mechanism", width=20, height=5,bg='#4974a5', fg='white',
                            command=lambda: controller.movemotor_sample_backward()) 

        x_firstcolumn = 220
        x_secondcolumn = 440
        y_firstrow = 150

        button1.place(x=x_firstcolumn, y=y_firstrow)
        button2.place(x=x_secondcolumn, y=y_firstrow)



class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        imageBg = tk.PhotoImage(file='ETH_bg.png')
        self.image = imageBg
        label_bg = tk.Label(self, image=imageBg)
        label_bg.place(x=0, y=0)

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.place(x=350, y=400)


        # IMPLEMENT MOTOR FUNCTION HERE
        button1 = tk.Button(self, text="Dispense Solution", width=20, height=5, bg='#4974a5', fg='white',
                            command=lambda: controller.movemotor_solution_forward())
        button2 = tk.Button(self, text="Move Back Mechanism", width=20, height=5, bg='#4974a5', fg='white',
                            command=lambda: controller.movemotor_solution_backward())

        x_firstcolumn = 220
        x_secondcolumn = 440
        y_firstrow = 150

        button1.place(x=x_firstcolumn, y=y_firstrow)
        button2.place(x=x_secondcolumn, y=y_firstrow)

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        imageBg = tk.PhotoImage(file='ETH_bg.png')
        self.image = imageBg
        label_bg = tk.Label(self, image=imageBg)
        label_bg.place(x=0, y=0)
        self.T=tk.Text(self, height=1, width=20)
        text="Please enter value"
        self.T.insert(tk.END, text)
        self.T.place(x=320, y=200)


        self.textEntryVar = StringVar()
        self.e = tk.Entry(self, width=15, background='white', textvariable=self.textEntryVar, justify=tk.CENTER,
                       font='-weight bold')
        self.e.grid(padx=10, pady=5, row=17, column=1, sticky='W,E,N,S')
        self.e.bind('<FocusIn>', self.numpadEntry)
        self.e.bind('<FocusOut>', self.numpadExit)
        self.e.pack(expand=1)
        self.edited = False

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.place(x=350, y=400)

    def numpadEntry(self, event):
        if self.edited == False:
            print("You Clicked on me")
            self.e['bg'] = '#ffffcc'
            self.edited = True
            new = numPad(self, self)
        else:
            self.edited = False

    def numpadExit(self, event):
        self.e['bg'] = '#ffffff'

class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        imageBg = tk.PhotoImage(file='ETH_bg.png')
        self.image = imageBg
        label_bg = tk.Label(self, image=imageBg)
        label_bg.place(x=0, y=0)

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.place(x=350, y=400)

class PageFive(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        imageBg = tk.PhotoImage(file='ETH_bg.png')
        self.image = imageBg
        label_bg = tk.Label(self, image=imageBg)
        label_bg.place(x=0, y=0)
        
        x_middlecolumn = 220*1.5
        x_firstcolumn = 220
        x_secondcolumn = 440
        y_firstrow = 150

        button1 = tk.Button(self, text="Start Demo",width=20, height=5,bg='#4974a5', fg='white',
                            command=lambda: controller.demo())
        button = tk.Button(self, text="Go to Start page",
                           command=lambda: controller.show_frame("StartPage"))
        button1.place(x=x_middlecolumn, y=y_firstrow)
        button.place(x=350, y=400)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()