#부모 클래스 정의 
class Person:
    def __init__(self, name, phoneNumber):
        self.name = name
        self.phoneNumber = phoneNumber
    def printInfo(self):
        print("Info(Name:{0}, Phone Number: {1})".format(self.name, 
            self.phoneNumber))

#자식 클래스 정의 
class Student(Person):
    #상속받고 재정의(덮어쓰기)
    def __init__(self, name, phoneNumber, subject, studentID):
        #부모의 초기화메서드
        super().__init__(name, phoneNumber)
        self.subject = subject
        self.studentID = studentID
    #상속받고 재정의
    def printInfo(self):
        #format-string
        print(f"Info(Name:{self.name}, Phone Number: {self.phoneNumber})")
        print(f"Info(학과:{self.subject}, 학번: {self.studentID})")

p = Person("전우치", "010-222-1234")
s = Student("이순신", "010-111-1234", "컴공", "261122")
p.printInfo()
s.printInfo() 


