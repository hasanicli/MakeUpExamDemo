from json_file import JsonFile
import itertools


class Data:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = JsonFile.read(self.file_name)

    def get_student_numbers_with_names(self):
        """ NEW Returns a sorted list of student numbers."""
        student_numbers = set()
        for dataset in self.data:
            for student in dataset["students"]:
                student_numbers.add(student["number"] + "_" + student["name"])
        student_numbers = list(student_numbers)
        student_numbers.sort(key=lambda x: int(x.split("_")[0]))
        return student_numbers

    def get_student_names_with_numbers(self):
        """ NEW Returns a sorted list of student names."""
        student_names = set()
        for dataset in self.data:
            for student in dataset["students"]:
                student_names.add(student["name"] + "_" + student["number"])
        student_names = list(student_names)
        student_names.sort()
        return student_names

    def get_student_lessons(self, number):
        """NEW numarası bilinen öğrencinin sınavlarını liste halinde döndürür."""
        return sorted([ds["name"] for ds in self.data for st in ds["students"] if st["number"] == number])

    def get_student_dates(self, number):
        return sorted(list(set([dataset["date_and_time"] for dataset in self.data for student in dataset["students"] if
                                number == student["number"]])))

    def get_date_and_time(self, lesson_name):
        for dataset in self.data:
            if dataset["name"] == lesson_name:
                return dataset["date_and_time"]
        else:
            return ""

    def get_all_date_and_time(self):
        return sorted(list(set(ds["date_and_time"] for ds in self.data)))

    def get_teachers_of_lesson(self, lesson_name):
        return sorted([teacher for ds in self.data if ds["name"] == lesson_name for teacher in ds["teachers"]])

    def get_dataset_of_date(self, date):
        data = sorted([(dataset["name"], dataset["date_and_time"].split()[1]) for dataset in self.data if
                       dataset["date_and_time"].split()[0] == date],
                      key=lambda x: x[1])
        return data

    def sort_lessons(self, option):
        if option == 1:
            self.data.sort(key=lambda x: x["name"])
        elif option == 2:
            self.data.sort(key=lambda x: x["name"], reverse=True)
        elif option == 3:
            self.data.sort(key=lambda x: len(x["students"]))
        elif option == 4:
            self.data.sort(key=lambda x: len(x["students"]), reverse=True)
        elif option == 5:
            self.data.sort(key=lambda x: len(x["name"].split("_")))
        else:
            return False
        JsonFile.write(self.file_name, self.data)
        self.__init__(self.file_name)
        return True

    def get_all_lessons(self, option=1):
        """NEW"""
        if self.sort_lessons(option):
            return [lesson["name"] for lesson in self.data]
        return []

    def get_lessons_with_numbers(self):
        lessons_with_numbers = {}
        lessons = [lesson["name"] for lesson in self.data]
        for lesson in lessons:
            numbers = set([student["number"] for dataset in self.data if dataset["name"] == lesson for student in
                           dataset["students"]])
            lessons_with_numbers[lesson] = numbers
        return lessons_with_numbers

    def get_lesson_dataset(self, lesson_name):
        """NEW"""
        for dataset in self.data:
            if dataset["name"] == lesson_name:
                return dataset
        else:
            return {}

    def count_student_of_lesson(self, lesson_name):
        """NEW"""
        dataset = self.get_lesson_dataset(lesson_name)
        students = dataset.get("students", [])
        return len(students)

    def _add_extension(self, lesson, dataset):
        departments_set = set([i["department"] for i in dataset["students"]])
        departments_list = list(departments_set)
        departments_list.sort()
        for dep in departments_list:
            new_exam = {"name": lesson + "_" + dep, "students": [], "teachers": [], "date_and_time": ""}
            for student in dataset["students"]:
                if student["department"] == dep:
                    new_exam["students"].append(student)  # sort belki
            self.data.append(new_exam)

    def _delete_extension(self, lesson, dataset):
        new_lesson_name = "_".join(lesson.split("_")[0:3])
        for i in self.data:
            if i["name"] == new_lesson_name:
                i["students"] += dataset["students"]  # sort belki
                break
        else:
            new_exam = {"name": new_lesson_name, "students": dataset["students"], "teachers": [], "date_and_time": ""}
            self.data.append(new_exam)

    def reset_times_and_duties(self):
        """Reset tasks and time when exams are merged and their extensions are changed."""
        for i in self.data:
            i["date_and_time"] = ""
            i["teachers"] = []
        JsonFile.write("data.json", self.data)
        JsonFile.write("temp_dates.json", {})
        self.__init__(self.file_name)

    def change_extension(self, lessons):
        """NEW Adds/removes department name at the end of the lesson."""
        for lesson in lessons:
            dataset = {}
            for index, value in enumerate(self.data):
                if value["name"] == lesson:
                    dataset = value
                    del self.data[index]
                    break
            if len(lesson.split("_")) == 4:
                self._delete_extension(lesson, dataset)
            elif len(lesson.split("_")) == 3:
                self._add_extension(lesson, dataset)
            else:
                pass
        self.reset_times_and_duties()

    def get_departments(self):
        """Get all departments."""
        departments = list(set([student["department"] for dataset in self.data for student in dataset["students"]]))
        departments.sort()
        return departments

    def change_department_name(self, old_name, new_name):
        for dataset in self.data:
            if len(dataset["name"].split("_")) == 4:
                if dataset["name"].split("_")[-1] == old_name:
                    dataset["name"] = "_".join(dataset["name"].split("_")[:-1] + [new_name])
            for student in dataset["students"]:
                if student["department"] == old_name:
                    student["department"] = new_name
        self.reset_times_and_duties()

    def combine_lessons(self, lessons: list, new_name: str):
        """new"""
        datasets = [dataset for lesson in lessons for dataset in self.data if dataset["name"] == lesson]
        all_numbers = [student["number"] for dataset in datasets for student in dataset["students"]]
        if len(all_numbers) == len(set(all_numbers)):
            students = [student for dataset in datasets for student in dataset["students"]]
            self.data.append({"name": new_name, "students": students, "teachers": [], "date_and_time": ""})
            for lesson in lessons:
                for index, value in enumerate(self.data):
                    if value["name"] == lesson:
                        self.data.pop(index)
                        break
            self.reset_times_and_duties()
            return True
        else:
            return False

    def get_coterie_list(self):
        return sorted(list(set(["_".join(i.split("_")[1:2]) if len(i.split("_")) == 3 else i.split("_")[-1] for i in
                                self.get_all_lessons(1)])))

    def save_limit(self, lesson_name, count):
        data = self.get_coterie_data()
        data[lesson_name] = count
        JsonFile.write("coterie.json", data)

    def save_limits(self, lessons):
        data = self.get_coterie_data()
        if not data:
            data = {}
        for lesson in lessons:
            data.setdefault(lesson, 1)
        JsonFile.write("coterie.json", data)

    @staticmethod
    def get_coterie_data():
        return JsonFile.read("coterie.json")

    @staticmethod
    def _limit_exceeded(param_lesson, param_list):
        limits = JsonFile.read("coterie.json")
        coterie = param_lesson.split("_")[1] if len(param_lesson.split("_")) == 3 else param_lesson.split("_")[-1]
        lesson_list = [i.split("_")[1] if len(i.split("_")) == 3 else i.split("_")[-1] for i in param_list]
        if lesson_list.count(coterie) >= limits[coterie]:
            return True
        return False

    def make_group(self):
        lessons_with_numbers = self.get_lessons_with_numbers()
        groups = {}
        counter = 1
        for base_key, base_value in lessons_with_numbers.items():
            if not groups:
                groups[counter] = {base_key: base_value}
                counter += 1
                continue
            for group_key, group_value in groups.items():
                for lesson, numbers in group_value.items():
                    if self._limit_exceeded(base_key, list(group_value.keys())):
                        break
                    if not base_value.isdisjoint(numbers):
                        break
                else:
                    group_value.update({base_key: base_value})
                    break
            else:
                groups[counter] = {base_key: base_value}
                counter += 1
        return groups
    @staticmethod
    def arrange_days(lesson_groups, student_exam_limit, day_exam_limit):
        all_list = []
        for k, v in lesson_groups.items():
            numbers = []
            lessons = []
            for key, value in v.items():
                numbers += list(value)
                lessons.append(key)
            numbers.sort(key=lambda x: int(x))
            all_list.append({"lessons": lessons, "numbers": numbers})

        sessions = {}
        counter = 1
        for i in all_list:
            if not sessions:
                sessions[counter] = [i]
                counter += 1
                continue
            for key, value in sessions.items():
                combined_numbers = [j["numbers"] for j in value] + [i["numbers"]]
                combined_numbers = list(itertools.chain.from_iterable(combined_numbers))
                if (max({i: combined_numbers.count(i) for i in combined_numbers}.values()) <= student_exam_limit and
                        len(value) < day_exam_limit):
                    sessions[key].append(i)
                    break
            else:
                sessions[counter] = [i]
                counter += 1

        new_dict = {}
        for key, value in sessions.items():
            temp_list = []
            for i in value:
                temp_list.append(i["lessons"])
            else:
                new_dict[key] = temp_list
        return new_dict

    def control_of_recorded_teacher(self, name):
        for dataset in self.data:
            if name in dataset["teachers"]:
                return True
        else:
            return False

    def get_duty_info_for_teachers(self, teacher_name):
        teacher_lessons = [dataset["name"] for dataset in self.data if teacher_name in dataset["teachers"]]
        info = ""
        for lesson in teacher_lessons:
            date_and_time = self.get_date_and_time(lesson)
            info += lesson + "\n\t\t\t" + date_and_time + "\n"
        return info

    def get_lesson_info(self, lesson_name):
        student_count = self.count_student_of_lesson(lesson_name)
        date_and_time = self.get_date_and_time(lesson_name)

        teachers_of_lesson = self.get_teachers_of_lesson(lesson_name)

        teacher_text = ""
        if teachers_of_lesson:
            for teacher in teachers_of_lesson:
                teacher_text += "\t" + teacher + "\n"

        info = "Sınav Tarihi- Saati: " + "-" + str(date_and_time) + "\n\nÖğrenci sayısı: " + str(
            student_count) + "\n\nÖğretmenler:\n" + teacher_text
        return info

    def assign_duty_for_teacher(self, teacher_name, lesson_name, limit):
        dates = [i.split()[0] for i in self.get_duty_dates_for_teachers(teacher_name)]
        dates_full = self.get_duty_dates_for_teachers(teacher_name)

        if teacher_name not in [teacher for dataset in self.data if lesson_name == dataset["name"] for teacher in
                                dataset["teachers"]]:
            lesson_date = self.get_date_and_time(lesson_name).split()[0]
            lesson_date_full = self.get_date_and_time(lesson_name)
            if lesson_date:
                if dates.count(lesson_date) <= limit:
                    if lesson_date_full not in dates_full:
                        [ds["teachers"].append(teacher_name) for ds in self.data if ds["name"] == lesson_name]
                        JsonFile.write("data.json", self.data)
                        self.__init__(self.file_name)
                        return ""
                    else:
                        return "Aynı gün ve saate iki görev verilmez"
                else:
                    return "Öğretmen için limit aşımı var"
            else:
                return "Sınav tarihi ayarlanmamış"
        else:
            return ""

    def get_duty_dates_for_teachers(self, teacher_name):
        return [dataset["date_and_time"] for dataset in self.data if teacher_name in dataset["teachers"]]

    def get_task_dates_and_tasks_for_teachers(self, teacher_name):
        return sorted([(ds["name"], ds["date_and_time"]) for ds in self.data if teacher_name in ds["teachers"]],
                      key=lambda x: x[1])

    def remove_duty_for_teacher(self, teacher_name, lesson_name):
        if teacher_name in [teacher for ds in self.data if lesson_name == ds["name"] for teacher in ds["teachers"]]:
            [ds["teachers"].remove(teacher_name) for ds in self.data if ds["name"] == lesson_name]
            JsonFile.write("data.json", self.data)
            self.__init__(self.file_name)
