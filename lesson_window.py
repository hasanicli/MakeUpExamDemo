import tkinter as tk
import tkinter.ttk as ttk
from data import Data


class LessonWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.geometry("480x600")
        self.resizable = False
        self.title("Dersler")
        self.grab_set()
        self._create_widgets()
        self._change_rb()
        # messagebox.showinfo("BİLGİ", "Sınav zamanı ve sınav görevlileri bilgileri sıfırlanacak.", parent=self)
        self.open_window()

    def _create_widgets(self):
        self.lesson_listbox = tk.Listbox(self, selectmode="multiple")
        self.lesson_listbox.place(x=10, y=10, width=460, height=500)

        self.rb_var = tk.IntVar(value=4)
        self.r1 = ttk.Radiobutton(self, text="Ders adı (+)", variable=self.rb_var, value=1, command=self._change_rb)
        self.r1.place(x=10, y=520, width=85, height=20)
        self.r2 = ttk.Radiobutton(self, text="Ders adı (-)", variable=self.rb_var, value=2, command=self._change_rb)
        self.r2.place(x=100, y=520, width=85, height=20)
        self.r3 = ttk.Radiobutton(self, text="Öğr. sayısı (+)", variable=self.rb_var, value=3, command=self._change_rb)
        self.r3.place(x=190, y=520, width=95, height=20)
        self.r4 = ttk.Radiobutton(self, text="Öğr. sayısı (-)", variable=self.rb_var, value=4, command=self._change_rb)
        self.r4.place(x=295, y=520, width=95, height=20)
        self.r5 = ttk.Radiobutton(self, text="Alan Bilg.", variable=self.rb_var, value=5, command=self._change_rb)
        self.r5.place(x=395, y=520, width=85, height=20)

        self.change_button = ttk.Button(self, text='Ders İsmini Alan İsmiyle İlişkilendir / İlişkiyi Kes',
                                        command=self.change_lesson_name)
        self.change_button.place(x=100, y=560, width=260, height=30)

    def _change_rb(self):
        option = self.rb_var.get()
        self._get_lessons(option)

    def _get_lessons(self, option):
        lessons = Data("data.json").get_all_lessons(option)
        # ihtiyaç olursa sayılarıyla birlikte
        # lessons_with_count = list(
        #     map(lambda lesson: lesson + "(" + str(data_control.count_student_of_lesson(lesson)) + ")", lessons))
        self.lesson_listbox.delete(0, tk.END)
        self.lesson_listbox.insert(0, *lessons)

    def change_lesson_name(self):
        data_control = Data("data.json")
        # eğer ders ismi öğrenci sayılı olursa burayı splitle böl birleştir ders ismini oluştur.
        lesson_list = [self.lesson_listbox.get(i) for i in self.lesson_listbox.curselection()]
        data_control.change_extension(lesson_list)
        data_control.save_limits(lesson_list)
        self._get_lessons(self.rb_var.get())

    def open_window(self):
        """Run the main loop."""
        self.mainloop()
