__author__ = 'jiacheng'
#!/usr/bin/env python3
# -*- coding: utf-8 -*
from tkinter import *
import tkinter
from tkinter.messagebox import *
from pixivmain import *

fields = 'username', 'passsword'

def fetch(entries):
    b = runss(entries[0].get(),entries[1].get())
    if b == True :
        showinfo("finish", 'download finish, please whit some time to save picture')



def makefrom(root, fields):
    entries = []
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=10, text=field)
        if field == 'passsword':
            ent = Entry(row, show='*')
        else:
            ent = Entry(row)
        row.pack(side=TOP, fill=X)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)

        entries.append(ent)
    return entries




root = tkinter.Tk()
ents = makefrom(root, fields)
root.bind('<Return>', (lambda event: fetch(ents)))
Button(root, text='complete', command=(lambda: fetch(ents))).pack(side=RIGHT)
root.mainloop()
