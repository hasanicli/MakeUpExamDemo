import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from data import Data


class DepartmentWindow(tk.Toplevel):  # ders ismi verilirken _ - . vb karakterleri önle
    def __init__(self):
        super().__init__()
        # self.data_control = Data("database.json")

        self.geometry("400x460")
        self.resizable = False
        self.title("Alanlar")
        self.grab_set()

        self._create_widgets()
        self.get_departments()

    def _create_widgets(self):
        self.department_listbox = tk.Listbox(self, selectmode="single")
        self.department_listbox.place(x=10, y=10, width=380, height=280)
        self.department_listbox.bind("<<ListboxSelect>>", self.set_new_name)

        self.department_old_name_label = ttk.Label(self, text="ALAN ESKİ ADI:")
        self.department_old_name_label.place(x=10, y=300, width=100, height=30)

        self.department_old_name = ttk.Entry(self)
        self.department_old_name.place(x=110, y=300, width=280, height=30)

        self.department_new_name_label = ttk.Label(self, text="ALAN YENİ ADI:")
        self.department_new_name_label.place(x=10, y=340, width=100, height=30)

        self.department_new_name = ttk.Entry(self)
        self.department_new_name.place(x=110, y=340, width=280, height=30)

        self.change_button = ttk.Button(self, text='Alan İsmini Değiştir', command=self.change_department_name)
        self.change_button.place(x=10, y=420, width=120, height=30)

    def set_new_name(self, event):
        selection = event.widget.curselection()
        if selection:
            self.department_old_name.delete(0, tk.END)
            self.department_old_name.insert(0, self.department_listbox.get(selection[0]))

    def change_department_name(self):
        try:
            data_control = Data("data.json")
            old_name = self.department_old_name.get()
            new_name = self.department_new_name.get()
            if (new_name != ""
                    and old_name != ""
                    and new_name not in self.department_listbox.get(0, tk.END)
                    and old_name in self.department_listbox.get(0, tk.END)):
                data_control.change_department_name(old_name, new_name)
                self.get_departments()
        except Exception:
            tk.messagebox.showinfo("Hata")

    def get_departments(self):
        data_control = Data("data.json")
        self.department_listbox.delete(0, tk.END)
        departments = data_control.get_departments()
        self.department_listbox.insert(0, *departments)
