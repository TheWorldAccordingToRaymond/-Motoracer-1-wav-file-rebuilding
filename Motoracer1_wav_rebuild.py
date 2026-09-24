import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

# create the root window
root = tk.Tk()
root.title('Motoracer 1 wav files rebuilding')
root.resizable(False, False)
root.geometry('500x150')

magic = bytearray(b'\x52\x49\x46\x46')
head  = bytearray(b'\x57\x41\x56\x45\x66\x6D\x74\x20\x10\x00\x00\x00\x01\x00\x01\x00\x11\x2B\x00\x00\x22\x56\x00\x00\x02\x00\x10\x00\x4C\x49\x53\x54\x1A\x00\x00\x00\x49\x4E\x46\x4F\x49\x53\x46\x54\x0E\x00\x00\x00\x4C\x61\x76\x66\x35\x37\x2E\x38\x33\x2E\x31\x30\x30\x00\x64\x61\x74\x61')

signature = bytes([0x72, 0x6D, 0x6E, 0x72]) # orginal Motoracer 1 WAV start by "rmnr"

def select_files():
    filetypes=[("wav Files", "*.wav")]

    filenames = fd.askopenfilenames(
        title='Open Motoracer 1 .wav files',
        initialdir='/',
        filetypes=filetypes)

    for filename in filenames:
        file = open(filename, "rb")
        first4bytes = file.read(4)
        if first4bytes != signature:
            break

        buffer1 = bytearray()
        file.seek(0x2f)
        byte = file.read(2)
        a_soustraire=-0x7fff + (byte[0]*0x100) + byte[1];
        pos=0
        while byte and len(byte)>1:
            valint= (byte[0]*0x100) + byte[1]
            res=valint - a_soustraire
            a_soustraire+=0x800
            if a_soustraire > 0x7fff  : a_soustraire=-0x7fff;
            lsb = res & 0xff;
            msb = ((res & 0xff00)>>8) + 0x80;
            if msb>0xff : msb-=0x100
            buffer1 += bytearray(2)
            buffer1[pos] = lsb
            buffer1[pos+1] = msb

            byte = file.read(2)
            pos=pos+2

        file.close

        newFile = open(filename+"_ok.wav", "wb")
        # write to file
        newFile.write(magic)
        newFile.write((len(buffer1)+0x46).to_bytes(4, byteorder='little'))
        newFile.write(head)
        newFile.write(len(buffer1).to_bytes(4, byteorder='little'))
        for byte in buffer1:
            newFile.write(byte.to_bytes(1, byteorder='big'))
        #newFile.write(b'\x00')
        newFile.close

        showinfo(
            title='Generated File',
            message=filename+"_ok.wav"
        )

def save():
    # a developper
    files = [('All Files', '*.*'),
             ('wav Files', '*.wav')]
    asksaveasfile(filetypes = files, defaultextension = files)

# open button
open_button = ttk.Button(
    root,
    text='Open Motoracer 1 .wav files',
    command=select_files
)

open_button.pack(expand=True)

root.mainloop()
