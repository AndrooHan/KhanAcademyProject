class User(object):
    def __init__(self, name, version='1.0'):
        self.name = name
        self.teacher = set() # set of class IDs
        self.enrolled = set() # set of class IDs
        self.version = version


class Graph(object):
    def __init__(self):
        self.user_map = {}
        self.classmembers = {} # dict of classroom id to users

    def get_user(self,name):
        return self.user_map.get(name,None)

    def add_user(self, user):
        if user.name not in self.user_map:
            self.user_map[user.name] = user

    def set_classroom(self, teacher, students):
        class_ID = str(len(self.classmembers))
        self.classmembers[class_ID] = {teacher}
        self.add_user(teacher)
        teacher.teacher.add(class_ID)
        for student in students:
            self.classmembers[class_ID].add(student)
            self.add_user(student)
            student.enrolled.add(class_ID)


