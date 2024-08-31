import tkinter as tk
import tkinter.ttk as ttk
from json_file import JsonFile


class FixedDataWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.geometry("400x460")
        self.resizable = False
        self.title("Sabit Bilgiler")
        self.grab_set()

        self._create_widgets()
        self._load_city()
        self._load_info()

    def _create_widgets(self):
        self.fixed_info_lbl = ttk.Label(self, text="Sabit bilgiler:")
        self.fixed_info_lbl.place(x=10, y=10, width=100, height=20)

        # create a combobox for cities
        self.city = tk.StringVar()
        self.city_lbl = ttk.Label(self, text="İL:")
        self.city_lbl.place(x=10, y=40, width=60, height=20)
        self.city_cb = ttk.Combobox(self, textvariable=self.city, state="readonly")
        self.city_cb.place(x=70, y=40, width=100, height=20)
        self.city_cb.bind('<<ComboboxSelected>>', self._set_county)

        # create a combobox for counties
        self.county = tk.StringVar()
        self.county_lbl = ttk.Label(self, text="İLÇE:")
        self.county_lbl.place(x=10, y=70, width=60, height=20)
        self.county_cb = ttk.Combobox(self, textvariable=self.county, state="readonly")
        self.county_cb.place(x=70, y=70, width=100, height=20)
        # self.county_cb.bind('<<ComboboxSelected>>', self._set_county)

        self.school_name_lbl = ttk.Label(self, text="OKUL ADI:")
        self.school_name_lbl.place(x=10, y=100, width=60, height=20)
        self.school_name = ttk.Entry(self, font="Arial 10 bold")
        self.school_name.place(x=70, y=100, width=280, height=20)

        self.headmaster_lbl = ttk.Label(self, text="MÜDÜR:")
        self.headmaster_lbl.place(x=10, y=130, width=60, height=20)
        self.headmaster_name = ttk.Entry(self, font="Arial 10 bold")
        self.headmaster_name.place(x=70, y=130, width=150, height=20)

        self.exam_term_lbl = ttk.Label(self, text="DÖNEM:")
        self.exam_term_lbl.place(x=10, y=160, width=60, height=20)
        self.exam_term_name = ttk.Entry(self, font="Arial 10 bold")
        self.exam_term_name.place(x=70, y=160, width=100, height=20)

        self.date_lbl = ttk.Label(self, text="TARİH:")
        self.date_lbl.place(x=10, y=190, width=60, height=20)
        self.document_date = ttk.Entry(self, font="Arial 10 bold")
        self.document_date.place(x=70, y=190, width=100, height=20)

        self.document_number_lbl = ttk.Label(self, text="SAYI:")
        self.document_number_lbl.place(x=10, y=220, width=60, height=20)
        self.document_number = ttk.Entry(self, font="Arial 10 bold")
        self.document_number.place(x=70, y=220, width=100, height=20)

        self.record_button = ttk.Button(self, text='KAYDET', command=self._record_info)
        self.record_button.place(x=70, y=250, width=80, height=30)

    def _load_city(self):
        data = JsonFile.read("city.json")
        if data:
            cities = [(dataset["id"], dataset["name"]) for dataset in data]
            cities.sort(key=lambda x: int(x[0]))
            self.city_cb.delete(0, tk.END)
            self.city_cb["values"] = [city[1] for city in cities]
            self.city_cb.current(0)
            self._set_county(None)

    @staticmethod
    def _get_city_id(city_name):
        data = JsonFile.read("city.json")
        city_id = [dataset["id"] for dataset in data if dataset["name"] == city_name][0]
        if city_id:
            return city_id
        return 0

    def _set_county(self, event):
        city_id = self._get_city_id(self.city.get())
        if city_id:
            data = JsonFile.read("county.json")
            counties = [dataset["name"] for dataset in data if dataset["il_id"] == city_id]
            self.county_cb["values"] = counties
            self.county_cb.current(0)

    def _load_info(self):
        fixed_info = JsonFile.read("fixed_info.json")
        if fixed_info:
            self.city_cb.set(fixed_info["city"])
            self.county_cb.set(fixed_info["county"])
            self.school_name.delete(0, tk.END)
            self.school_name.insert(0, fixed_info["school_name"])
            self.headmaster_name.delete(0, tk.END)
            self.headmaster_name.insert(0, fixed_info["headmaster_name"])
            self.exam_term_name.delete(0, tk.END)
            self.exam_term_name.insert(0, fixed_info["exam_term_name"])
            self.document_date.delete(0, tk.END)
            self.document_date.insert(0, fixed_info["document_date"])
            self.document_number.delete(0, tk.END)
            self.document_number.insert(0, fixed_info["document_number"])

    def _record_info(self):
        info = {"city": self.city.get(), "county": self.county.get(), "school_name": self.school_name.get(),
                "headmaster_name": self.headmaster_name.get(), "exam_term_name": self.exam_term_name.get(),
                "document_date": self.document_date.get(), "document_number": self.document_number.get()}
        JsonFile.write("fixed_info.json", info)
