from data import Data
from json_file import JsonFile


class Teacher:
    def __init__(self):
        self.teacher_data = JsonFile.read("teachers.json")
        if not self.teacher_data:
            self.teacher_data = {}

    def add_or_update(self, teacher_name, **kwargs):
        item_dict = {}
        for key, value in kwargs.items():
            item_dict[key] = value
        self.teacher_data[teacher_name] = item_dict
        JsonFile.write("teachers.json", self.teacher_data)
        self.__init__()

    def delete(self, teacher_name):
        data_control = Data("data.json")
        if data_control.control_of_recorded_teacher(teacher_name):
            return False
        else:
            del self.teacher_data[teacher_name]
            JsonFile.write("teachers.json", self.teacher_data)
            self.__init__()
            return True

    def get_item(self, item_name):
        if item_name in self.teacher_data.keys():
            return self.teacher_data[item_name].values()
        return None

    def get_names(self):
        return list(self.teacher_data.keys())

    def get_branches(self):
        return sorted(list(set([v for key, value in self.teacher_data.items() for k, v in value.items()])))

    def get_item_as_dict(self, item_name):
        if item_name in self.teacher_data.keys():
            return self.teacher_data[item_name]
        return None

    def get_branch_and_name(self):
        branch_and_name = []
        teachers = self.teacher_data
        if teachers:
            for key, value in teachers.items():
                combine_str = value["branch"] + "_" + str(key)
                branch_and_name.append(combine_str)
            branch_and_name.sort()
        return branch_and_name
