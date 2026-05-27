# DB연습2.py
import sqlite3

#연결객체(물리적인 파일에 저장) 
con = sqlite3.connect("c:\\work\\sample.db")

#커서객체 리턴
cur = con.cursor()

#테이블 생성 
cur.execute("create table if not exists " + 
    " PhoneBook (Name text, PhoneNum text);")

#입력 
cur.execute("insert into PhoneBook values('홍길동', '010-1234-5678');")
#입력 파라메터로 처리 
cur.execute("insert into PhoneBook values(?, ?);", ('박문수', '010-9876-5432'))
#여러건을 입력 
datalist = [('이순신', '010-1111-2222'), ('전우치', '010-3333-4444')]
cur.executemany("insert into PhoneBook values(?, ?);", datalist)

#검색 
for row in cur.execute("select * from PhoneBook;"):
    print(row)

#정상완료
con.commit()
con.close()