from pynput.keyboard import Listener
import time

def log_keystroke(key):
    key = str(key).replace("'", "")

    if key == 'Key.shift':
        pass
    else :
        try: scanned_item.append(key)


def scan():
    #Scan for 5 secs and return 
    listener = Listener(on_press=log_keystroke) 
    listener.start()
    time.sleep(0.3)
    listener.stop()



if __name__ == "__main__":
    running = True 
    while running:
        global scanned_item
        scanned_item = []
        scan()

        if len(scanned_item) != 0:
            #Send barcode to ETH
            pass

         
            


        print(scanned_item)



