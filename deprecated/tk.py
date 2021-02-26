try:
    import tkinter as tk                # python 3
    from tkinter import font as tkfont  # python 3
    from tkinter import StringVar, Tk
except ImportError:
    import Tkinter as tk     # python 2
    import tkFont as tkfont  # python 2
from pynput.keyboard import Listener
import time


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        root = tk.Tk.__init__(self, *args, **kwargs)
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
        self.root = Tk()

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def log_keystroke(self, key):
        key = str(key).replace("'", "")

        if key == 'S' or key == '0' or key == '1' or key == '2' or key == '3' or key == '4' or key == '5' or key == '6' or key == '7' or key == '8' or key == '9':
            scanned_item.append(key)
        else:
            pass

    def scan(self):
        #Scan for 5 secs and return 
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
        while running:
            global scanned_item
            scanned_item = []
            self.scan()
            
            scanned_item = [] if len(scanned_item) != 9 else scanned_item
            var.set(str(scanned_item)) if scanned_item != [] else var
            self.root.update_idletasks()

            if len(scanned_item) != 0:
                #Send barcode to ETH
                pass        

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame( width=100, height=100, background="bisque")
        self.controller = controller
        self['bg']='#4974a5'
        global var
        var = StringVar()
        var.set("Ready...")

        label = tk.Label(self, text="ETH Covid Test", font=controller.title_font,background='#4974a5')
        label.pack(side="top", fill="x", pady=10)

        label2 = tk.Label(self, textvariable = var)
        label2.pack()

        button1 = tk.Button(self, text="Scan Legi",
                            command=lambda: controller.run_scanner())
        # button2 = tk.Button(self, text="Go to Page Two",
        #                     command=lambda: controller.show_frame("PageTwo"))
        button1.pack()
        # button2.pack()


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