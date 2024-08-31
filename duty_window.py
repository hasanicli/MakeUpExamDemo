import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from data import Data
from teacher import Teacher


class DutyWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.geometry("800x800")
        self.resizable = False
        self.title("Öğretmenler")
        self.grab_set()

        self._arrange_form()

        self.load_list()

    def _arrange_form(self):
        self.teachers_lbl = ttk.Label(self, text="  Öğretmenler")
        self.teachers_lbl.place(x=10, y=10, width=100, height=20)

        self.teachers_lbl = ttk.Label(self, text="  Dersler")
        self.teachers_lbl.place(x=400, y=10, width=200, height=20)

        self.teacher_lb = tk.Listbox(self, exportselection=False)
        self.teacher_lb.place(x=10, y=30, width=300, height=400)
        self.teacher_lb.bind("<<ListboxSelect>>", self.write_teacher_info)

        self.lesson_lb = tk.Listbox(self, exportselection=False)
        self.lesson_lb.place(x=400, y=30, width=300, height=400)
        self.lesson_lb.bind("<<ListboxSelect>>", self.write_lesson_info)

        self.teacher_duty_lbl = ttk.Label(self, text="")
        self.teacher_duty_lbl.config(anchor=tk.NW)
        self.teacher_duty_lbl.place(x=10, y=440, width=300, height=300)

        self.lesson_teacher_lbl = ttk.Label(self, text="")
        self.lesson_teacher_lbl.config(anchor=tk.NW)
        self.lesson_teacher_lbl.place(x=400, y=440, width=300, height=300)

        self.duty_limit_lbl = ttk.Label(self, text="Günlük görev limiti:")
        self.duty_limit_lbl.place(x=170, y=10, width=120, height=20)

        self.duty_limit_txt = ttk.Entry(self)
        self.duty_limit_txt.place(x=290, y=10, width=20, height=20)
        self.duty_limit_txt.insert(0, "3")

        self.assign_duty_btn = ttk.Button(self, text='-->>', command=self.assign_teacher_to_lesson)
        self.assign_duty_btn.place(x=330, y=170, width=50, height=30)

        self.cancel_duty_btn = ttk.Button(self, text='<<--', command=self.cancel_teacher_duty)
        self.cancel_duty_btn.place(x=330, y=220, width=50, height=30)

    def load_list(self):
        teacher_control = Teacher()
        data_control = Data("data.json")
        branch_and_name = teacher_control.get_branch_and_name()
        lessons = data_control.get_all_lessons()
        self.teacher_lb.delete(0, tk.END)
        self.teacher_lb.insert(0, *branch_and_name)
        self.lesson_lb.delete(0, tk.END)
        self.lesson_lb.insert(0, *lessons)

    def get_student_count_for_lesson(self):
        pass

    def get_lesson_teachers(self):
        pass

    def get_lesson_date_and_time(self):
        pass

    def get_teacher_lessons(self):
        pass

    def update_info(self, teacher_index, lesson_index):
        self.teacher_lb.selection_set(teacher_index)
        self.lesson_lb.selection_set(lesson_index)
        self.teacher_lb.event_generate("<<ListboxSelect>>")
        self.lesson_lb.event_generate("<<ListboxSelect>>")

    def assign_teacher_to_lesson(self):
        data_control = Data("data.json")
        limit = self.duty_limit_txt.get()
        if not limit.isdigit():
            limit = "3"
        limit = int(limit)

        teacher_index = self.teacher_lb.curselection()
        lesson_index = self.lesson_lb.curselection()

        if teacher_index and lesson_index:
            teacher = self.teacher_lb.get(teacher_index).split("_")[1]
            lesson = self.lesson_lb.get(lesson_index)

            result = data_control.assign_duty_for_teacher(teacher, lesson, limit)
            if result:
                tk.messagebox.showerror("Hata", result, parent=self)
            self.update_info(teacher_index, lesson_index)

    def cancel_teacher_duty(self):
        data_control = Data("data.json")
        teacher_index = self.teacher_lb.curselection()
        lesson_index = self.lesson_lb.curselection()

        if teacher_index and lesson_index:
            teacher = self.teacher_lb.get(teacher_index).split("_")[1]
            lesson = self.lesson_lb.get(lesson_index)
            data_control.remove_duty_for_teacher(teacher, lesson)
            self.update_info(teacher_index, lesson_index)

    def write_teacher_info(self, event):
        data_control = Data("data.json")
        selection = event.widget.curselection()
        if selection:
            teacher_name = self.teacher_lb.get(selection[0]).split("_")[1]
            info = data_control.get_duty_info_for_teachers(teacher_name)
            self.teacher_duty_lbl.config(text=info)

    def write_lesson_info(self, event):
        data_control = Data("data.json")
        selection = event.widget.curselection()
        if selection:
            lesson_name = self.lesson_lb.get(selection[0])
            lesson_info = data_control.get_lesson_info(lesson_name)
            self.lesson_teacher_lbl.config(text=lesson_info)
