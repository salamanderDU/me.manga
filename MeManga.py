# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 14:06:02 2020

@author: speedDuke
"""

from tkinter import *
import requests, os, bs4, threading
from bs4 import BeautifulSoup
from tkinter import filedialog
from PIL import Image
# from fpdf import FPDF
from tkinter.ttk import *

def download_Me():
    urlToon = urlEntry.get()
    
    res = requests.get(urlToon)
    res.raise_for_status()
    
    soup = BeautifulSoup(res.text,'html.parser')

    comicElem = soup.select(define_tag())
    #----------show after press start----------------------
    downloadBar.grid(row=4, column=1, columnspan=3, sticky=W)
    startBuuton.grid_forget()
    #------------------------------------------------------
    count = 0
    #-----------shown after preess start ---------------------00
    # v = StringVar()
    v.set('Downloading')
    textInformation = Label(window, textvariable=v).grid(row=5, column=1)
    
    imglist = []
    for i in comicElem:
        if comicElem == []:
            popup_edit('No picture')
    
        else:
            count += 1
            #--------------------------------------------00
            v.set('Downloading '+str(count)+" from "+str(len(comicElem)))
            comicUrl =  i.get('src')
            #-----------------------------------
            upadatebar(count, len(comicElem))
            #------------------------------------
            try:
                res = requests.get(comicUrl)
                res.raise_for_status()
            except Exception as e:
                continue
            
            pathFile = os.path.join(directEntry.get() ,str(count)+"-"+os.path.basename(comicUrl))
            imageFile = open(pathFile, 'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)           
            imageFile.close()
            imglist.append(pathFile)
    v.set("Initializing file please wait ...")
    if p.get() == 1:
        v.set("Making pdf file ...")
        toPdf(imglist, directEntry.get())
    popup_Done()
def select_folder():
    folder_selected = filedialog.askdirectory()
    directEntry.insert(0, folder_selected)
    
def close(): 
    window.destroy() #root.withdraw
    
def InUrl(te):
    label = Label(window, text=te)
    label.pack()
    label2 = Label(window, text = r.get()).pack()
    
def popup_Done():
    messagebox.showinfo("information", "Done")
    
def popup_Error():
    messagebox.showinfo("Error", "url error!")
def popup_edit(text):
    messagebox.showinfo("", text)
    
def define_tag():
    tag =" "
    if webDropdown.get() == OPTIONS[1]:
        tag = '#image-container img'
    elif webDropdown.get() == OPTIONS[0]:
        tag = '#main img'
    elif webDropdown.get() == OPTIONS[2]:
        tag = '#manga_alphabet img'
    return tag
def threadddddd():
    th = threading.Thread(target=lambda :download_Me())
    th.start()
    
def toPdf(listimg, pathfile):
    imagelist = []
    for i in listimg:
        im = Image.open(i).convert('RGB')
        imagelist.append(im)
        
    imagelist[0].save(pathfile+"/manga.pdf",save_all=True, append_images=imagelist[1:])
    v.set("Now you can close program")
def pastee():
    link = window.clipboard_get()
    urlEntry.insert(0, link)
def upadatebar(process, lenght):
    downloadBar['value']=(process*100)/lenght
    window.update_idletasks()
    
        
    # comicElem = soup.select(tag)    

window = Tk()
window.title("Manga Downloader")
pic = PhotoImage(file = r"C:\Users\speedDuke\Desktop\me.manga\MeManga\icon.png")
window.iconphoto(False,pic)
window.geometry('480x170')
window.resizable(width=False, height=False)

OPTIONS = ["Kinngmanga","Niceoppai","Oremanga"]

#create wibjet zone ------------------------------------------------------------
urlLaasdbel = Label(window, text=" ").grid(row=0, column=0, ipadx=30, pady=5)

urlLabel = Label(window, text="URL:")
urlEntry = Entry(window, width=60)
pasteButton = Button(window, text="paste", width=5 ,command=lambda:pastee())
webLabel = Label(window, text="Website :")
webDropdown = Combobox(window, value=OPTIONS)
webDropdown.set('--choose web--')
saveAsLabel = Label(window, text="Save As :")
directEntry = Entry(window, width=60)
datButton = Button(window, text="...", width=3, command=lambda:select_folder())
p = IntVar()
pdfRadio = Radiobutton(window, text="PDF", variable=p, value=1)
downloadBar = Progressbar(window,orient=HORIZONTAL,length=350,mode='determinate')
v = StringVar()
# v.set('Downloading')
textInformation = Label(window, textvariable=v)
startBuuton = Button(window, text="start", command=lambda:threadddddd())
#end widjet --------------------------------------------------------------------

#grid zone ---------------------------------------------------------------------
urlLabel.grid(row=0, column=0, sticky=E, padx=3)
urlEntry.grid(row=0, column=1, columnspan=2)
pasteButton.grid(row=0, column=3)
webLabel.grid(row=1, column=0, sticky=E, pady=5)
webDropdown.grid(row=1, column=1, columnspan=2, sticky=W)
saveAsLabel.grid(row=2, column=0, sticky=E, pady=5)
directEntry.grid(row=2, column=1, columnspan=2)
datButton.grid(row=2, column=3)
pdfRadio.grid(row=3, column=1, sticky=W)
# downloadBar.grid(row=4, column=1, columnspan=3, sticky=W)
startBuuton.grid(row=6, column=1, columnspan=2, pady=3)
#--------------------------------------------------------------------------------


window.mainloop()