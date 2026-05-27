class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def printInfo(self):
        print("Person(id: {0}, name: {1})".format(self.id, self.name))


class Manager(Person):
    def __init__(self, id, name, title):
        super().__init__(id, name)
        self.title = title

    def printInfo(self):
        print("Manager(id: {0}, name: {1}, title: {2})".format(self.id, self.name, self.title))


class Employee(Person):
    def __init__(self, id, name, skill):
        super().__init__(id, name)
        self.skill = skill

    def printInfo(self):
        print("Employee(id: {0}, name: {1}, skill: {2})".format(self.id, self.name, self.skill))


if __name__ == "__main__":
    people = [
        Person(1, "전우치"),
        Person(2, "이몽룡"),
        Person(3, "성춘향"),
        Manager(4, "홍길동", "팀장"),
        Manager(5, "심청", "부장"),
        Manager(6, "유관순", "과장"),
        Employee(7, "강감찬", "Python"),
        Employee(8, "이순신", "Data Analysis"),
        Employee(9, "김유신", "Web Development"),
        Employee(10, "장보고", "Machine Learning"),
    ]

    for person in people:
        person.printInfo()