import os
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk
import threading
from mutagen.mp3 import MP3
import time
from pygame import mixer


root = tk.ThemedTk()
root.get_themes()
root.set_theme("scidgreen")



status_Bar=ttk.Label(root,text='Welcome to Tuner',relief = SUNKEN, anchor=CENTER,font = 'Times 12 italic')
status_Bar.pack(side=BOTTOM, fill=X)

#add menubar

menu_Bar=Menu(root)
root.config(menu=menu_Bar)

#add submenu

sub_Menu=Menu(menu_Bar, tearoff=0)

playlist = []        # contains full path and file name (required to play music)

def file_browse():
    global f_path
    f_path=filedialog.askopenfilename()
    add_to_playlist(f_path)

def add_to_playlist(f_name):
    f_name = os.path.basename(f_name)
    index = 0
    playlistbox.insert(index, f_name)
    playlist.insert(index,f_path)
    index=index+1


menu_Bar.add_cascade(label="File", menu=sub_Menu ,font = 'Arial 15 bold')
sub_Menu.add_command(label="Open",command=file_browse)
sub_Menu.add_command(label="Close")

def about_us():
    tkinter.messagebox.showinfo('About Tuner','This is a Audio Player created using Pyhton3 tkinter by Utsab084')

def playback():
    tkinter.messagebox.showinfo('Playback','Under Construction')

def tools():
    tkinter.messagebox.showinfo('Tools','Under Construction')

def setting():
    tkinter.messagebox.showinfo('Setting','Under Construction')


sub_Menu=Menu(menu_Bar, tearoff=0)
menu_Bar.add_cascade(label="Playback", menu=sub_Menu, font = 'Arial 15 bold')
sub_Menu.add_command(label="Info" ,command=playback)

sub_Menu=Menu(menu_Bar, tearoff=0)
menu_Bar.add_cascade(label="Tools", menu=sub_Menu, font = 'Arial 15 bold')
sub_Menu.add_command(label="Info" ,command=tools)

sub_Menu=Menu(menu_Bar, tearoff=0)
menu_Bar.add_cascade(label="Setting", menu=sub_Menu, font = 'Arial 15 bold')
sub_Menu.add_command(label="Info" ,command=setting)

sub_Menu=Menu(menu_Bar, tearoff=0)
menu_Bar.add_cascade(label="Help", menu=sub_Menu, font = 'Arial 15 bold')
sub_Menu.add_command(label="About us" ,command=about_us)


#initializing with mixer

mixer.init()


root.title("Tuner")
#root.geometry('400x400')
root.iconbitmap(r'Images/favicon.ico')

filelabel=Label(root,text = 'Refresh yourself with SANGEET!',font = 'Times 15 italic',fg='green')
filelabel.pack()

leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30 , pady=30)

filelabel1=Label(leftframe,text = 'Playlist',font = 'Times 15 roman',fg='green')
filelabel1.pack()

playlistbox = Listbox(leftframe)
playlistbox.pack()



addbtn = ttk.Button(leftframe,text="Creat",command=file_browse)
addbtn.pack(side=LEFT)

def rem_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)


rembtn = ttk.Button(leftframe,text="Remove",command = rem_song)
rembtn.pack(side=RIGHT)

rightframe = Frame(root)
rightframe.pack()



# top frame
def play_sangeet():
    global paused
    if paused:
        mixer.music.unpause()
        status_Bar['text'] = 'Music Resumed'
        paused=False
    else:
        try:
            stop_sangeet()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            status_Bar['text']='You Are Enjoying Music'+' : '+os.path.basename(play_it)
            show_top(play_it)
        except:
            tkinter.messagebox.showerror('File not Found','Please recheck you had browsed the file or not!')


def stop_sangeet():
    mixer.music.stop()
    status_Bar['text'] = 'Music Stopped'

paused=False

def pause_sangeet():
    global paused
    paused=True
    mixer.music.pause()
    status_Bar['text'] = 'Music Paused'

topframe=Frame(rightframe)
topframe.pack(pady=30,padx=30)


playImage=PhotoImage(file='Images/play.png')
playButton=ttk.Button(topframe, image=playImage, command=play_sangeet)
#playButton.pack(side=LEFT,padx=10)
playButton.grid(row=1,column=0,padx=10)

txt1 = ttk.Label(topframe,text = 'Play Music',font = 'Arial 15 bold')
txt1.grid(row=0,column=1,padx=10,pady = 15)


stopImage=PhotoImage(file='Images/stop.png')
stopButton=ttk.Button(topframe, image=stopImage, command=stop_sangeet)
#stopButton.pack(side=LEFT,padx=10)
stopButton.grid(row=1,column=2,padx=10)


pauseImage=PhotoImage(file='Images/pause.png')
pauseButton=ttk.Button(topframe, image=pauseImage, command=pause_sangeet)
#pauseButton.pack(side=LEFT,padx=10)
pauseButton.grid(row=1,column=1,padx=10)





def show_top(play_song):

    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        mp3 = MP3(play_song)
        total_duration = mp3.info.length
    else:
        a = mixer.sound(play_song)
        total_duration = a.get_length()

    m,s = divmod(total_duration,60)   # assigning result in m and remainder in s
    m = round(m)
    s = round(s)
    timeformat = '{:02d}:{:02d}'.format(m,s)
    file_length['text'] = 'Total Duration' + ' : ' + timeformat

    t1 = threading.Thread(target = start_count , args=(total_duration,))
    t1.start()

def start_count(t):
    global paused
    # stop the music
    while t and mixer.music.get_busy():
        if paused:
            continue
        else:
            m, s = divmod(t,60)  # assigning result in m and remainder in s
            m = round(m)
            s = round(s)
            timeformat = '{:02d}:{:02d}'.format(m, s)
            currenttimelabel['text'] = 'Remaining Duration' + ' : ' + timeformat
            time.sleep(1)
            t = t-1





def rewind_sangeet():
    play_sangeet()
    status_Bar['text'] = 'Music Rewound'


def cng_vol(val):
    #volume=int(val)/100
    mixer.music.set_volume(float(val)/100)

muted=False
def mute_sangeet():
    global muted
    if muted:
        muted=False
        mixer.music.set_volume(0.4)
        speakerButton.configure(image=speakerImage)
        scale.set(40)
    else:
        muted=True
        mixer.music.set_volume(0)
        speakerButton.configure(image=muteImage)
        scale.set(0)




# middle frame

middle_frame=Frame(rightframe)
middle_frame.pack(pady=10)

rewindImage=PhotoImage(file='Images/rewind.png')
rewindButton=ttk.Button(middle_frame, image=rewindImage, command=rewind_sangeet)
#stopButton.pack(side=LEFT,padx=10)
rewindButton.grid(row=0,column=1,padx=10,pady=10)


muteImage=PhotoImage(file='Images/mute.png')
speakerImage=PhotoImage(file='Images/speaker.png')
speakerButton=ttk.Button(middle_frame, image=speakerImage, command=mute_sangeet)
speakerButton.grid(row=0,column=2,padx=10,pady=10)


scale=ttk.Scale(middle_frame,from_=0,to=100, orient=HORIZONTAL, command=cng_vol)
scale.set(40)
mixer.music.set_volume(0.4)
scale.grid(row=0,column=0,pady=20,padx=40)


# bottom frame
bottom_frame = Frame(rightframe)
bottom_frame.pack(pady=30)

file_length = ttk.Label(bottom_frame,text = 'Duration - 00:00',relief = GROOVE, font = 'Arial 15 roman')
file_length.grid(row=0,column=0,padx=20)

currenttimelabel = ttk.Label(bottom_frame,text = 'Current Time - 00:00', relief = GROOVE, font = 'Arial 15 roman')
currenttimelabel.grid(row=0,column=1,padx=20)


def on_closing():
    # tkinter.messagebox.showinfo('Prank',"You have been pranked!")
    stop_sangeet()
    root.destroy()


root.protocol("WM_DELETE_WINDOW",on_closing)
root.mainloop()
