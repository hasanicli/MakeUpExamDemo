import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from teacher import Teacher


class TeacherWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.resizable = False
        self.title("Öğretmenler")
        self.grab_set()
        self._arrange_form()
        self.load_list()

    def load_list(self):
        teacher_control = Teacher()
        teachers_with_branch = teacher_control.get_branch_and_name()
        self.teacher_lb.delete(0, tk.END)
        self.teacher_lb.insert(0, *teachers_with_branch)

    def add_or_update(self):
        teacher_control = Teacher()
        name = self.teacher_name_entry.get()
        branch = self.teacher_branch_entry.get()
        if name and branch:
            teacher_control.add_or_update(name, branch=branch)
            self.teacher_name_entry.delete(0, tk.END)
            self.teacher_branch_entry.delete(0, tk.END)
        self.load_list()

    def delete(self):
        name = self.teacher_name_entry.get()
        teacher_control = Teacher()
        if name and name in teacher_control.teacher_data:
            if teacher_control.delete(name):
                self.teacher_name_entry.delete(0, tk.END)
                self.teacher_branch_entry.delete(0, tk.END)
                self.load_list()
                tk.messagebox.showinfo("Bilgi", "Kişi silindi", parent=self)
            else:
                tk.messagebox.showerror("Hata", "Kişi üzerinde ders kaydı var silemezsiniz", parent=self)

    def set_teacher_info(self, event):
        selection = event.widget.curselection()
        if selection:
            self.teacher_name_entry.delete(0, tk.END)
            self.teacher_branch_entry.delete(0, tk.END)
            full_name = self.teacher_lb.get(selection[0])
            name = full_name.split("_")[1]
            branch = full_name.split("_")[0]
            self.teacher_name_entry.insert(0, name)
            self.teacher_branch_entry.insert(0, branch)

    def _arrange_form(self):
        self.list_lbl = ttk.Label(self, text="Kayıtlı öğretmenler")
        self.list_lbl.place(x=10, y=10, width=200, height=20)

        self.teacher_lb = tk.Listbox(self)
        self.teacher_lb.place(x=10, y=30, width=300, height=400)
        self.teacher_lb.bind("<<ListboxSelect>>", self.set_teacher_info)

        self.teacher_name_lbl = ttk.Label(self, text="Öğretmen adı:")
        self.teacher_name_lbl.place(x=10, y=440, width=100, height=20)
        self.teacher_name_entry = ttk.Entry(self, state="normal")
        self.teacher_name_entry.place(x=110, y=440, width=200, height=20)

        self.teacher_branch_lbl = ttk.Label(self, text="Öğretmen Branşı:")
        self.teacher_branch_lbl.place(x=10, y=470, width=100, height=20)
        self.teacher_branch_entry = ttk.Entry(self, state="normal")
        self.teacher_branch_entry.place(x=110, y=470, width=200, height=20)

        self.add_btn = ttk.Button(self, text='Kaydet/Güncelle', command=self.add_or_update)
        self.add_btn.place(x=40, y=510, width=100, height=30)

        self.delete_btn = ttk.Button(self, text='Sil', command=self.delete)
        self.delete_btn.place(x=180, y=510, width=100, height=30)
