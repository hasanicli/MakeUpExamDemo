import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

import utility
from data import Data


class CombineWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.geometry("1024x768")
        self.resizable = False
        self.title("Ders birleştir")
        self.grab_set()

        self._create_widgets()
        self._change_rb()

    def _create_widgets(self):
        self.lesson_listbox = tk.Listbox(self, selectmode="multiple")
        self.lesson_listbox.place(x=10, y=10, width=470, height=600)
        self.lesson_listbox.bind("<<ListboxSelect>>")

        self.sort_lessons_label = ttk.Label(self, text="Sıralama Seç", anchor="c")
        self.sort_lessons_label.place(x=330, y=615, width=90, height=20)

        self.rb_var = tk.IntVar(value=4)
        self.r1 = ttk.Radiobutton(self, text="Ders adı (+)", variable=self.rb_var, value=1, command=self._change_rb)
        self.r1.place(x=330, y=640, width=85, height=20)
        self.r2 = ttk.Radiobutton(self, text="Ders adı (-)", variable=self.rb_var, value=2, command=self._change_rb)
        self.r2.place(x=330, y=665, width=85, height=20)
        self.r3 = ttk.Radiobutton(self, text="Öğr. sayısı (+)", variable=self.rb_var, value=3, command=self._change_rb)
        self.r3.place(x=330, y=690, width=95, height=20)
        self.r4 = ttk.Radiobutton(self, text="Öğr. sayısı (-)", variable=self.rb_var, value=4, command=self._change_rb)
        self.r4.place(x=330, y=715, width=95, height=20)
        self.r5 = ttk.Radiobutton(self, text="Alan Bilg.", variable=self.rb_var, value=5, command=self._change_rb)
        self.r5.place(x=330, y=740, width=85, height=20)

        self.selected_lessons_label = ttk.Label(self, text="Seçilen Dersler:")
        self.selected_lessons_label.place(x=500, y=10, width=90, height=20)

        self.student_count_label = ttk.Label(self, text="Öğr. Sayı:")
        self.student_count_label.place(x=950, y=10, width=70, height=20)

        self.lesson1_label = ttk.Label(self, text="DERS1:")
        self.lesson1_label.place(x=500, y=40, width=40, height=20)
        self.lesson1 = ttk.Entry(self, state="disable")
        self.lesson1.place(x=540, y=40, width=400, height=20)
        self.lesson1_count_label = ttk.Label(self, text="", anchor="e")
        self.lesson1_count_label.place(x=950, y=40, width=30, height=20)

        self.lesson2_label = ttk.Label(self, text="DERS2:")
        self.lesson2_label.place(x=500, y=70, width=40, height=20)
        self.lesson2 = ttk.Entry(self, state="disable")
        self.lesson2.place(x=540, y=70, width=400, height=20)
        self.lesson2_count_label = ttk.Label(self, text="", anchor="e")
        self.lesson2_count_label.place(x=950, y=70, width=30, height=20)

        self.lesson3_label = ttk.Label(self, text="DERS3:")
        self.lesson3_label.place(x=500, y=100, width=40, height=20)
        self.lesson3 = ttk.Entry(self, state="disable")
        self.lesson3.place(x=540, y=100, width=400, height=20)
        self.lesson3_count_label = ttk.Label(self, text="", anchor="e")
        self.lesson3_count_label.place(x=950, y=100, width=30, height=20)

        self.lesson4_label = ttk.Label(self, text="DERS4:")
        self.lesson4_label.place(x=500, y=130, width=40, height=20)
        self.lesson4 = ttk.Entry(self, state="disable")
        self.lesson4.place(x=540, y=130, width=400, height=20)
        self.lesson4_count_label = ttk.Label(self, text="", anchor="e")
        self.lesson4_count_label.place(x=950, y=130, width=30, height=20)

        self.new_name_label = ttk.Label(self, text="Aşağıdaki alandan yeni isim oluşturunuz.")
        self.new_name_label.place(x=500, y=460, width=250, height=20)

        self.school_type_label = ttk.Label(self, text="OKUL TÜRÜ:")
        self.school_type_label.place(x=500, y=500, width=80, height=20)
        self.school_type = ttk.Entry(self, state="disable")
        self.school_type.place(x=580, y=500, width=250, height=20)

        self.lesson_label = ttk.Label(self, text="DERS ADI:")
        self.lesson_label.place(x=500, y=530, width=80, height=20)
        self.lesson_name = ttk.Entry(self, state="disable")
        self.lesson_name.place(x=580, y=530, width=250, height=20)

        self.level_label = ttk.Label(self, text="SINIF SEVİYESİ:")
        self.level_label.place(x=500, y=560, width=80, height=20)
        self.level = ttk.Entry(self, state="disable")
        self.level.place(x=580, y=560, width=250, height=20)

        self.department_label = ttk.Label(self, text="ALAN ADI:")
        self.department_label.place(x=500, y=590, width=80, height=20)
        self.department_name = ttk.Entry(self, state="disable")
        self.department_name.place(x=580, y=590, width=250, height=20)

        self.select_lesson_button = ttk.Button(self, text='Bu dersleri seçtim', command=self.select_lessons)
        self.select_lesson_button.place(x=10, y=620, width=150, height=30)

        self.combine_lesson_button = ttk.Button(self, text='Dersleri Birleştir', command=self.prepare_lessons)
        self.combine_lesson_button.place(x=500, y=620, width=150, height=30)

    def _change_rb(self):
        option = self.rb_var.get()
        self._get_lessons(option)

    def _get_lessons(self, option):
        lessons = Data("data.json").get_all_lessons(option)
        self.lesson_listbox.delete(0, tk.END)
        self.lesson_listbox.insert(0, *lessons)

    def select_lessons(self):
        data_control = Data("data.json")
        lesson_parts_widgets = [self.school_type, self.lesson_name, self.level, self.department_name]
        selected_lessons_widgets = [self.lesson1, self.lesson2, self.lesson3, self.lesson4]
        student_count_widgets = [self.lesson1_count_label, self.lesson2_count_label, self.lesson3_count_label,
                                 self.lesson4_count_label]
        combined_list = lesson_parts_widgets + selected_lessons_widgets + student_count_widgets

        for i, obj in enumerate(combined_list):
            utility.write_to_object(combined_list[i], "")

        lesson_list = [self.lesson_listbox.get(i) for i in self.lesson_listbox.curselection()]

        if self._control_selected_lessons(lesson_list):
            for i, lesson in enumerate(lesson_list):
                utility.write_to_object(selected_lessons_widgets[i], lesson)
                utility.write_to_object(student_count_widgets[i],
                                        str(data_control.count_student_of_lesson(lesson)))

            for j, part in enumerate(lesson_list[0].split("_")):
                lesson_parts_widgets[j].config(state="normal")
                lesson_parts_widgets[j].insert(j, part)
                if j == 1 or j == 2:
                    continue
                lesson_parts_widgets[j].config(state="disable")
            lesson_parts_widgets[3].config(state="disable")

    def _control_selected_lessons(self, lessons: list):
        """Buraya bir daha bakalım"""
        partial_lesson_list = [i.split("_") for i in lessons]
        if len(lessons) > 4:
            tk.messagebox.showinfo("Bilgi", "En fazla 4 ders birleştirilebilir.", parent=self)
            return False
        if len(lessons) == 0:
            tk.messagebox.showinfo("Bilgi", "Herhangi bir ders seçmediniz.", parent=self)
            return False
        if not all([parts[0] == partial_lesson_list[0][0] for parts in partial_lesson_list]):
            tk.messagebox.showinfo("Bilgi", "Farklı okul türleri için birleştirme yapılamaz.", parent=self)
            return False
        if not all([len(parts) == len(partial_lesson_list[0]) for parts in partial_lesson_list]):
            tk.messagebox.showinfo("Bilgi", "Alan dersi ile ortak ders birleşemez.", parent=self)
            return False

        if all([len(parts) == 4 for parts in partial_lesson_list]):
            if not all([parts[3] == partial_lesson_list[0][3] for parts in partial_lesson_list]):
                tk.messagebox.showinfo("Bilgi", "Farklı alan dersleri birleşemez.", parent=self)
                return False
        return True

    def prepare_lessons(self):
        data_control = Data("data.json")
        selected_lessons_widgets = [self.lesson1, self.lesson2, self.lesson3, self.lesson4]
        lesson_names = [i.get() for i in selected_lessons_widgets if i.get()]
        new_name_widgets = [self.school_type, self.lesson_name, self.level, self.department_name]
        new_name = "_".join([i.get() for i in new_name_widgets if i.get()])
        if self._control_new_name(lesson_names, new_name):
            result = data_control.combine_lessons(lesson_names, new_name)
            if not result:
                tk.messagebox.showerror("Hata", "Bu ders grubu birleşemez.", parent=self)
            # lesson_parts_widgets = [self.school_type, self.lesson_name, self.level, self.department_name]
            # selected_lessons_widgets = [self.lesson1, self.lesson2, self.lesson3, self.lesson4]
            # student_count_widgets = [self.lesson1_count_label, self.lesson2_count_label, self.lesson3_count_label,
            #                          self.lesson4_count_label]
            combined_list = [self.school_type, self.lesson_name, self.level, self.department_name,
                             self.lesson1, self.lesson2, self.lesson3, self.lesson4,
                             self.lesson1_count_label, self.lesson2_count_label, self.lesson3_count_label,
                             self.lesson4_count_label]

            for i, obj in enumerate(combined_list):
                utility.write_to_object(combined_list[i], "")
        self._get_lessons(self.rb_var.get())

    def _control_new_name(self, lesson_names, new_name):
        invalid_characters = ["/", "\\", "?", "*", ":", "<", ">", "|", "_"]
        lesson_name = self.lesson_name.get()
        level = self.level.get()
        if not (lesson_name and level):
            tk.messagebox.showerror("Hata", "Ders ismi ve sınıf alanları dolu olmalı.", parent=self)
            return False
        if any([i in invalid_characters for i in lesson_name]):
            tk.messagebox.showerror(
                "Hata", f"İsim alanında {" ".join(invalid_characters)} karakterleri olamaz", parent=self)
            return False
        if any([character in invalid_characters for character in level]):
            tk.messagebox.showerror(
                "Hata", f"Sınıf isminde {" ".join(invalid_characters)} karakterleri olamaz", parent=self)
            return False

        if new_name in lesson_names:
            tk.messagebox.showerror(
                "Hata", "Ders ismi değiştirilmemiş.", parent=self)
            return False
        return True
