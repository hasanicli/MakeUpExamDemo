from tkinter import ttk
import tkinter as tk


def write_to_object(obj, text):
    if type(obj) is ttk.Entry:
        obj.configure(state="normal")
        obj.delete(0, tk.END)
        obj.insert(0, text)
        obj.configure(state="disable")
    elif type(obj) is ttk.Label or type(obj) is tk.Label:
        obj.config(text=text)
    else:
        pass


def date_control(date):
    date1 = date.split("/")
    enable = True
    if len(date1) != 3:
        enable = False
    for i in date1:
        if i.isdigit() and (len(i) == 2 or len(i) == 4):
            pass
        else:
            enable = False
            break
    return enable


def time_control(time):
    time1 = time.split(":")
    enable = True
    if len(time1) != 2:
        enable = False
    for i in time1:
        if i.isdigit() and len(i) == 2:
            pass
        else:
            enable = False
            break
    return enable
