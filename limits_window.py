import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from data import Data


class LimitWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.geometry("600x400")
        self.resizable = False
        self.title("Ders birleştir")
        self.grab_set()

        self._create_widgets()

        self.set_coterie()

    def _create_widgets(self):
        self.coterie_listbox = tk.Listbox(self)
        self.coterie_listbox.place(x=10, y=10, width=380, height=380)
        self.coterie_listbox.bind("<<ListboxSelect>>", self.load_count)

        self.count_label = ttk.Label(self, text="Üst Limit:")
        self.count_label.place(x=400, y=10, width=60, height=30)
        self.count_entry = ttk.Entry(self, state="enable")
        self.count_entry.place(x=460, y=10, width=30, height=30)
        self.save_button = ttk.Button(self, text='Kaydet', command=self.save_limit)
        self.save_button.place(x=500, y=10, width=60, height=30)

        self.lesson_label = ttk.Label(self, text="")
        self.lesson_label.place(x=400, y=50, width=150, height=30)

    def set_coterie(self):
        data_control = Data("data.json")
        data_control.save_limits(data_control.get_coterie_list())
        self.coterie_listbox.delete(0, tk.END)
        self.coterie_listbox.insert(0, *data_control.get_coterie_list())

    def load_count(self, event):
        data_control = Data("data.json")
        coterie_data = data_control.get_coterie_data()
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            self.lesson_label.config(text=event.widget.get(index))
            self.count_entry.delete(0, tk.END)
            result = coterie_data.get(self.lesson_label.cget("text"), False)
            self.count_entry.insert(0, result)

    def save_limit(self):
        data_control = Data("data.json")
        if self.lesson_label.cget("text") and self.count_entry.get().isdigit():
            if int(self.count_entry.get()) > 0:
                data_control.save_limit(self.lesson_label.cget("text"), int(self.count_entry.get()))
            else:
                print("sıfırdan büyük olsun")
        else:
            tk.messagebox.showerror("Hata", "Seçim yapmalı ve değer girelisiniz.", parent=self)


if __name__ == "__main__":
    pass
