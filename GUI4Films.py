import subprocess
import os
import tkinter as tk
import sys
import win32file
import glob

def locate_usb():
    drive_list = []
    drivebits = win32file.GetLogicalDrives()
    for d in range(1, 26):
        mask = 1 << d
        if drivebits & mask:
            # here if the drive is at least there
            drname = '%c:\\' % chr(ord('A') + d)
            t = win32file.GetDriveType(drname)
            if t == win32file.DRIVE_REMOVABLE:
                drive_list.append(drname)
    return drive_list

def find_files(dir):
        types = ('*.mkv' ,'*.mp4' , '*.avi')
        file_list = []
        os.chdir(dir)
        for file in types:
            file_list.extend(glob.glob(file))
        return file_list

def select_drive():
    try:
        selected_line = drives_list.curselection()
        selected = drives_list.get(selected_line)
        global selected_drive
        selected_drive = selected
        label['text'] = selected  
        fill_lb(find_files(selected), True) 
    except:
        label.configure(text = "Nessuna chiavetta selezionata", foreground = 'red')

def fill_lb(files, type):
    n = 0
    drives_list.delete(0,tk.END)
    for file in files:
        drives_list.insert(n, file)
        n = n+1
    if(type):
        #if the files are videos
        drives_list.insert(n, indietro_text)
        label.configure(text = "Seleziona film", foreground='white')
        b1.configure(command=play_video)
    
def play_video():
    close = False
    try:
        selected_line = drives_list.curselection()
        selected = drives_list.get(selected_line)
        if(selected == indietro_text):
            label.configure(text = "Seleziona chiavetta", foreground='white')
            b1.configure(command=select_drive)
            fill_lb(usb_sticks, False)
        else:
            global selected_video
            selected_video = selected
            subprocess.Popen([vlc_dir, selected_drive + selected_video, "-f"])
            close = True
    except:
        label.configure(text = "Nessun film selezionato", foreground = 'red')
    if(close == True):
        sys.exit(1)

# Set various sizes and configs
color_bg = "#364787"
color_fg = "#292929"
text_size = 25
text_font = 'Helvetica'
vlc_dir = "D:\\VLC\\vlc.exe"
selected_drive = ""
selected_video = ""
indietro_text = ' ← Indietro'

# Set screensize to fullscreen
window = tk.Tk()
ws = window.winfo_screenwidth()
hs = window.winfo_screenheight()
w = ws/2+100
h = hs/2+100
window.title("Lista Film")
window.configure(background=color_bg)
window.geometry(str(int(w))+"x"+str(int(h))+"+300+100")
#window.state('zoomed')

# Search for the usb drive
usb_sticks = locate_usb()

label = tk.Label(
    text="Seleziona la chiavetta",
    foreground="white",  # Set the text color to white
    background=color_bg,
    font=(text_font, text_size),  # Set the background color to black
    width=200
)
label.pack()

drives_list = tk.Listbox(
    selectmode = "SINGLE",
    font=(text_font, text_size),
    relief = 'flat',
    background = '#dfded9',
    highlightcolor = '#FFFFFF',
    highlightthickness = 0,
    exportselection=0,
    selectbackground = '#265ca3',
    selectborderwidth = 3,
    foreground = color_fg,
    width = 40,
    activestyle = 'none'
    )
fill_lb(usb_sticks, False)
drives_list.pack()

frame1 = tk.Frame(master=window, width=1, height=20, bg=color_bg)
frame1.pack(fill=tk.X)

b1 = tk.Button(
    window,
    background = '#d9d5d1',
    text='Seleziona',
    width=20, 
    height=2,
    command=select_drive,
    font=(text_font, text_size),
    )
b1.pack()

window.mainloop()