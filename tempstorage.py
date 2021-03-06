from bluetooth import *
import pymysql
import time

username = ''
blank = 0
try:
    sok = BluetoothSocket(RFCOMM)
    sok.connect(("98:D3:31:FD:4A:30",1))
    conn = pymysql.connect(host="localhost", user="root", password="pi1234", db="Mtemp", charset="utf8")
    curs = conn.cursor()
    while True:
        time.sleep(1.5)
        sok.send("a") #아무 단어
        r = sok.recv(1024)
        temp = str(r)[-6:-1]
        try:
            temp = float(temp)
            if temp >60 or temp <30:#사람 사용 아닌경우
                blank = 1
                continue
            blank = 0
        except ValueError:#잘못된 값이면 되돌리기
            blank = 1   
            continue
        sql = "update usertemp set temp = %s where temp is null"
        print(float(temp))
        curs.execute(sql, (float(temp)))
        conn.commit()
        
except KeyboardInterrupt:
    print("\nterminate connection")
finally:
    sok.close()
    conn.close()

