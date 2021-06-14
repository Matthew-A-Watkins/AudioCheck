from tkinter import Button, Scale, Tk, Label, Text
import sounddevice as sd
import numpy as np
from playsound import playsound
import threading

# init the program is NOT running
running = False

# init the sound limit
sound_limit = 1

# find current sound_limit for constant program
def resetScaleAmount():
    global sound_limit

    # check if current sound threshold is already set to the slider number
    if soundRange.get() == sound_limit:
        display.insert('1.0',"The sound threshold is already set to {}!\n\n".format(soundRange.get()))
    
    # assign to current slide number
    else:
        # find current scale amount
        sound_limit = soundRange.get()

        # display 
        display.insert('1.0',"Setting threshold to {}\n\n".format(sound_limit))

# check sound level and play noise
def beep(indata, outdata, frames, time, status):

    # finds current sound level
    volume_norm = np.linalg.norm(indata)*10

    global sound_limit

    # check if the sound level is beyond a certain limit
    if int(volume_norm) >=  sound_limit:
        display.insert('1.0',"Volume has exceeded sound threshold of {} at {} playing beep.\n\n".format(sound_limit, str(volume_norm)))
        playsound('beep.mp3')


# funtion to run beep
def check():
    global running

    # runs beep
    while running:  
        with sd.Stream(callback=beep):
            sd.sleep(1000)


# start program by setting running to True
def start():
    global running

    if running == True:
        display.insert('1.0', "Program is already running!\n\n")
        pass

    else:
        display.insert('1.0', "Starting program.\n\n")
        running = True

        # open a new thread to run program preventing overlap on current thread
        newThread = threading.Thread(target=check)
        newThread.start()

# disable program by setting running = to false
def stop():
    global running 
    
    if running == False:
        display.insert('1.0', "Program is not running!\n\n")
        pass

    else:
        display.insert('1.0', "Stopping program.\n\n")
        running = False

if __name__ == '__main__':
    # init window function
    master = Tk()

    # set window title
    master.title('Audio Checker')

    # set window size to 400x400
    master.geometry('400x400')

    # removes max button
    master.resizable(0,0)

    # console
    display = Text(master, height=15, width = 40)

    # label for sound slider
    soundLabel = Label(master, text='Sound Threshold')

    # declare slider for sound max
    soundRange = Scale(master, from_=1,to=300, orient='horizontal')

    # declare the exit button for the program (generally useless but cool)
    exitButton = Button(master, text='exit', command=master.destroy)

    # set the current scale int to sound_limit button init
    newAmount = Button(master, text='set to new amount', command=resetScaleAmount)

    # start the sound check init
    start = Button(master, text='start', command=start)

    # stop the sound check button init
    stop = Button(master, text='stop', command=stop)

    # formatting for program elements 
    start.grid(row=1,column=1)
    stop.grid(row=1,column=2)
    soundLabel.grid(row=0,column=0)
    soundRange.grid(row=0,column=1)
    newAmount.grid(row=0, column=2)
    exitButton.place(x=180, y=350)
    display.place(x=40,y=100)

    master.mainloop()
