import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime
from tkinter import filedialog, messagebox
import utility
from data import Data

from excel_file import ExcelFile

from json_file import JsonFile

import os
import locale

from limits_window import LimitWindow
from teacher_window import TeacherWindow
from combine_window import CombineWindow
from department_window import DepartmentWindow
from duty_window import DutyWindow
from lesson_window import LessonWindow
from date_window import DateWindow
from report_window import ReportWindow
from fixed_data_window import FixedDataWindow

locale.setlocale(locale.LC_ALL, 'turkish')


class MainWindow:
    def __init__(self):

        self.window = tk.Tk()
        self.window.geometry("800x600")
        self.window.resizable = False
        self.window.title("Anasayfa")

        self._create_widgets()

        self.widget_list = [self.get_folder_button, self.lessons_button, self.department_button,
                            self.combine_lesson_button, self.coterie_button, self.date_button, self.teacher_button,
                            self.duty_button, self.fixed_info_button, self.report_button]

        for obj in self.widget_list[1:]:
            obj["state"] = "disabled"

        self._fill_student_listbox()

    def _fill_student_listbox(self):
        """filling student listbox and lesson listbox with students and exams"""
        data_control = Data("data.json")
        if data_control.data:
            for obj in self.widget_list[1:]:
                obj["state"] = "normal"
            students_list = data_control.get_student_numbers_with_names()
            self.student_listbox.delete(0, tk.END)
            self.student_listbox.insert(0, *students_list)
            if not data_control.data:
                JsonFile.write("info.json", [])
            self._load_file_info()

    def _load_file(self):
        """get Excel file path"""
        if tk.messagebox.askyesno("MESAJ KUTUSU", "Bu işlem sizi en başa döndürür.\n Devam etmek istiyor musunuz?"):
            file_name = filedialog.askopenfilename()
            if not os.path.isfile(file_name):
                messagebox.showerror("HATA", "Dosya seçmediniz.")
                return None
            elif not file_name.split(".")[-1] == "xlsx":
                messagebox.showerror("HATA", "Dosya xlsx uzantılı olmalı.")
                return None
            utility.write_to_object(self.tb_path, file_name)
            return file_name

    def _create_data(self):
        """Create ExcelFile and send file name"""
        file_name = self._load_file()
        if file_name:
            exc = ExcelFile(file_name)
            data = exc.create_data()
            if data:
                JsonFile.write("data.json", data)
                self.save_record_info(file_name)

            else:
                messagebox.showerror("HATA", "Dosya içeriği uygun değil.")
            self._fill_student_listbox()

    @staticmethod
    def save_record_info(path):
        date = datetime.today()
        date = date.strftime("%d/%m/%Y-%H:%M %A")
        info_dict = {"path": path, "date": date}
        JsonFile.write("info.json", info_dict)

    def _fill_lessons(self, event):
        if event.widget.curselection():
            data_control = Data("data.json")
            data = event.widget.get(event.widget.curselection()[0])
            number = str(data).split("_")[0] if str(data).split("_")[0].isdigit() else str(data).split("_")[1]
            student_lessons = data_control.get_student_lessons(number)
            self.lessons_listbox.delete(0, tk.END)
            self.lessons_listbox.insert(0, *student_lessons)

    def _load_file_info(self):
        info = JsonFile.read("info.json")
        if info:
            utility.write_to_object(self.tb_path, info["path"])
            utility.write_to_object(self.file_info_lbl, ("Cari dosya bilgisi: " + info["date"]))
        else:
            utility.write_to_object(self.tb_path, "")
            utility.write_to_object(self.file_info_lbl, "")

    def _create_widgets(self):
        self.get_folder_button = ttk.Button(self.window, text='Dosya Seç', command=self._create_data)
        self.get_folder_button.place(x=10, y=10, width=90, height=30)

        self.tb_path = ttk.Entry(self.window, state="disable")
        self.tb_path.place(x=120, y=10, width=360, height=30)

        self.file_info_lbl = tk.Label(self.window, text="")
        self.file_info_lbl.place(x=490, y=10, width=300, height=30)

        self.lessons_button = ttk.Button(self.window, text='Dersler', command=lambda: LessonWindow())
        self.lessons_button.place(x=10, y=90, width=90, height=30)

        self.department_button = ttk.Button(self.window, text='Alanlar', command=lambda: DepartmentWindow())
        self.department_button.place(x=10, y=130, width=90, height=30)

        self.combine_lesson_button = ttk.Button(self.window, text='Ders Birleştir', command=lambda: CombineWindow())
        self.combine_lesson_button.place(x=10, y=170, width=90, height=30)

        self.coterie_button = ttk.Button(self.window, text='Zümreler', command=lambda: LimitWindow())
        self.coterie_button.place(x=10, y=210, width=90, height=30)

        self.date_button = ttk.Button(self.window, text='Tarih-Saat', command=lambda: DateWindow())
        self.date_button.place(x=10, y=250, width=90, height=30)

        self.teacher_button = ttk.Button(self.window, text='Öğretmen', command=lambda: TeacherWindow())
        self.teacher_button.place(x=10, y=290, width=90, height=30)

        self.duty_button = ttk.Button(self.window, text='Görev Dağıt', command=lambda: DutyWindow())
        self.duty_button.place(x=10, y=330, width=90, height=30)

        self.fixed_info_button = ttk.Button(self.window, text='Sabit bilgiler', command=lambda: FixedDataWindow())
        self.fixed_info_button.place(x=10, y=370, width=90, height=30)

        self.report_button = ttk.Button(self.window, text='Data Kontrol', command=lambda: ReportWindow())
        self.report_button.place(x=10, y=410, width=90, height=30)

        self.student_listbox = tk.Listbox(self.window)
        self.student_listbox.place(x=120, y=50, width=300, height=400)
        self.student_listbox.bind('<<ListboxSelect>>', self._fill_lessons)

        self.lessons_listbox = tk.Listbox(self.window)
        self.lessons_listbox.place(x=430, y=50, width=350, height=400)

    def run(self):
        self.window.mainloop()



