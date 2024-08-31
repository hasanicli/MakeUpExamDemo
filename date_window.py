import tkinter as tk
import tkinter.ttk as ttk
import datetime
from tkinter import messagebox

import utility
from data import Data
from json_file import JsonFile


class DateWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.resizable = False
        self.title("Tarih ve saat işlemleri")
        self.grab_set()

        self._arrange_form()
        self.sessions = {}
        self.load_day_combo()

    def _arrange_form(self):
        self.student_exam_limit_label = ttk.Label(self, text="Öğrenciler için günlük sınav limiti:")
        self.student_exam_limit_label.place(x=10, y=10, width=190, height=20)
        self.student_exam_limit_entry = ttk.Entry(self, state="normal")
        self.student_exam_limit_entry.insert(0, str(3))
        self.student_exam_limit_entry.place(x=200, y=10, width=20, height=20)

        self.day_exam_limit_label = ttk.Label(self, text="Günlük oturum sayısı:")
        self.day_exam_limit_label.place(x=10, y=40, width=240, height=20)
        self.day_exam_limit_entry = ttk.Entry(self, state="normal")
        self.day_exam_limit_entry.insert(0, str(4))
        self.day_exam_limit_entry.place(x=200, y=40, width=20, height=20)

        self.sort_order_label = ttk.Label(self, text="Sıralama düzeni:")
        self.sort_order_label.place(x=10, y=100, width=90, height=20)
        self.rb_var = tk.IntVar()
        self.r1 = ttk.Radiobutton(self, text="Ders adına göre artan sıralama (A...Z)", variable=self.rb_var, value=1,
                                  command=self._change_rb)
        self.r1.place(x=10, y=120, width=300, height=20)
        self.r2 = ttk.Radiobutton(self, text="Ders adına göre azalan sıralama (Z...A)", variable=self.rb_var, value=2,
                                  command=self._change_rb)
        self.r2.place(x=10, y=150, width=300, height=20)
        self.r3 = ttk.Radiobutton(self, text="Öğr. sayısına göre artan sıralama (1 -->>)", variable=self.rb_var,
                                  value=3, command=self._change_rb)
        self.r3.place(x=10, y=180, width=300, height=20)
        self.r4 = ttk.Radiobutton(self, text="Öğr. sayısına göre azalan sıralama (1 <<--)", variable=self.rb_var,
                                  value=4, command=self._change_rb)
        self.r4.place(x=10, y=210, width=300, height=20)
        self.r5 = ttk.Radiobutton(self, text="Alan adına göre gruplanmış sıralama", variable=self.rb_var, value=5,
                                  command=self._change_rb)
        self.r5.place(x=10, y=240, width=300, height=20)

        self.create_exams_button = ttk.Button(self, text='Oturum ayarla', command=self._create_exam_table)
        self.create_exams_button.place(x=10, y=300, width=200, height=30)

        # create a combobox for days
        self.selected_day = tk.StringVar()
        self.day_cb_lbl = ttk.Label(self, text="Oturum Günü:")
        self.day_cb_lbl.place(x=10, y=400, width=150, height=20)
        self.day_cb = ttk.Combobox(self, textvariable=self.selected_day, state="readonly")
        self.day_cb.place(x=120, y=400, width=50, height=20)
        self.day_cb.bind('<<ComboboxSelected>>', self.set_session_count)

        # create a combobox for sessions
        self.selected_session = tk.StringVar()
        self.session_cb_lbl = ttk.Label(self, text="Oturum Numarası:")
        self.session_cb_lbl.place(x=10, y=430, width=150, height=20)
        self.session_cb = ttk.Combobox(self, textvariable=self.selected_session, state="readonly")
        self.session_cb.place(x=120, y=430, width=50, height=20)
        self.session_cb.bind('<<ComboboxSelected>>', self.set_lessons)

        self.lesson_lb = tk.Listbox(self)
        self.lesson_lb.place(x=300, y=10, width=450, height=380)
        self.lesson_lb.bind("<<ListboxSelect>>", self.select_lesson)

        self.selected_lesson_lbl = ttk.Label(self, text="Seçili ders bilgileri:")
        self.selected_lesson_lbl.config(anchor=tk.NW)
        self.selected_lesson_lbl.place(x=300, y=400, width=380, height=200)

        self.date_lbl = ttk.Label(self, text="Tarih:")
        self.date_lbl.place(x=10, y=460, width=60, height=20)
        self.date_entry = ttk.Entry(self, state="enable")
        self.date_entry.place(x=70, y=460, width=100, height=20)

        self.time_lbl = ttk.Label(self, text="Saat:")
        self.time_lbl.place(x=10, y=490, width=60, height=20)
        self.time_entry = ttk.Entry(self, state="enable")
        self.time_entry.place(x=70, y=490, width=100, height=20)

        self.date_and_time_button = ttk.Button(self, text='Tarih-Saat gir', command=self.add_date_and_time)
        self.date_and_time_button.place(x=70, y=540, width=100, height=30)

    def _change_rb(self):
        data_control = Data("data.json")
        option = self.rb_var.get()
        result = data_control.sort_lessons(option)

    def _create_exam_table(self):
        data_control = Data("data.json")
        try:
            i = int(self.student_exam_limit_entry.get())
            j = int(self.day_exam_limit_entry.get())
            option = self.rb_var.get()
            assert option
        except ValueError:
            tk.messagebox.showerror("Hata", "Sayısal değer girilmeli", parent=self)
        except AssertionError:
            tk.messagebox.showerror("Hata", "Seçim yapmalısınız", parent=self)

        else:
            data_control.reset_times_and_duties()
            groups = data_control.make_group()
            sessions = data_control.arrange_days(groups, i, j)
            JsonFile.write("temp_dates.json", sessions)
            self.load_day_combo()

    def load_day_combo(self):
        self.sessions = JsonFile.read("temp_dates.json")
        if not self.sessions:
            self.sessions = {}

        if self.sessions:
            self.day_cb.config(values=list(self.sessions.keys()))
            self.day_cb.current(0)
            self.set_session_count(None)

    def set_session_count(self, event):
        number = self.selected_day.get()
        self.session_cb["values"] = [i + 1 for i in range(len(self.sessions[number]))]
        self.session_cb.current(0)
        self.set_lessons(None)

    def set_lessons(self, event):
        day = self.selected_day.get()
        order = self.selected_session.get()
        lessons = self.sessions[day][int(order) - 1]
        self.lesson_lb.delete(0, tk.END)
        self.lesson_lb.insert(0, *lessons)
        self._call_date_and_time()

    def _call_date_and_time(self):
        data_control = Data("data.json")
        lesson = self.lesson_lb.get(0)
        date_and_time = data_control.get_date_and_time(lesson)
        self.date_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        if date_and_time.split():
            self.date_entry.insert(0, date_and_time.split()[0])
            self.time_entry.insert(0, date_and_time.split()[1])

    def select_lesson(self, event):
        data_control = Data("data.json")
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            lesson_name = self.lesson_lb.get(index)
            msg = lesson_name + "\n" + str(data_control.get_date_and_time(lesson_name)) + "\n" + str(
                data_control.count_student_of_lesson(lesson_name)) + " Öğrenci"
            self.selected_lesson_lbl.config(text=msg)

    def add_date_and_time(self):
        data_control = Data("data.json")
        lessons_name = self.lesson_lb.get(0, tk.END)
        data = data_control.data

        date = self.date_entry.get()
        date = date.strip()
        date = date.replace(".", "/")
        date = date.replace("-", "/")
        date = date.replace(",", "/")

        time = self.time_entry.get()
        time = time.strip()
        time = time.replace(".", ":")
        time = time.replace("-", ":")
        time = time.replace(",", ":")

        if utility.date_control(date) and utility.time_control(time) and lessons_name:
            try:
                date_object = datetime.datetime.strptime(date, '%d/%m/%Y')
                date_str = date_object.strftime("%d/%m/%Y")
                time_object = datetime.datetime.strptime(time, '%H:%M')
                time_str = time_object.strftime('%H:%M')

                date_and_time = date_str + " " + time_str
                for lesson_name in lessons_name:
                    for i in data:
                        if i["name"] == lesson_name:
                            i["date_and_time"] = date_and_time

                JsonFile.write("data.json", data)
            except ValueError:
                tk.messagebox.showerror("Hata", "Tarih bilgisi işlerken hata oluştu", parent=self)
        else:
            tk.messagebox.showerror("Hata", "Girilen bilgilerle ilgili bir hata oluştu", parent=self)

    def get_day_count(self):
        return list(self.sessions.keys())
