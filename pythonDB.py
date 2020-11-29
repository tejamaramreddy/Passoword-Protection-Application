import mysql.connector
from mysql.connector import Error
import base64
from Cryptodome.Cipher import AES
from Cryptodome import Random
import hashlib
import pyperclip as pc 


BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-s[-1]]

def encrypt( password, key ):
    privateKey = hashlib.sha256(key.encode('utf-8')).digest()
    raw = pad(password)
    iv = Random.new().read( AES.block_size )
    cipher = AES.new( privateKey, AES.MODE_CBC, iv )
    return base64.b64encode( iv + cipher.encrypt( raw.encode('utf8') ) )
def decrypt(enc,key ):
    privateKey = hashlib.sha256(key.encode('utf-8')).digest()
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(privateKey, AES.MODE_CBC, iv )
    return unpad(cipher.decrypt( enc[16:] ))




def insert(mydbcursor,AppName,UserName,Password):
    try:
        mydbcursor.execute("INSERT INTO passwords(AppName, UserName, Passwrd) values(%s,%s,%s)", (AppName,UserName,Password))
        mydb.commit()
    except Error as e:
        print(e) 

def select(mydbcursor,AppName):
    try:
        Query = "SELECT Passwrd FROM passwords WHERE AppName = %s"
        mydbcursor.execute(Query,(AppName,))
        record = mydbcursor.fetchone()
        key = input("Enter private key: ")
        #print(decrypt(record[0],key))
        passwrd = str(decrypt(record[0],key))
        passwrd = passwrd[2:len(passwrd)-1]
        pc.copy(passwrd) 
        print("Password is copied to clip board !!!")
    except Error as e:
        print(e)

def update(mydb):
    mydbcursor = mydb.cursor()
    print("Enter 1. For UserName update \n 2. For password Update ")
    option = int(input())
    try:
        if(option == 1):
            AppName = input("Enter App Name to which you need to Update UserName: ")
            NewUserName = input("Enter new User Name: ")
            Query = "UPDATE passwords set UserName = %s where AppName = %s"
            mydbcursor.execute(Query,(NewUserName,AppName))
            mydb.commit()
        elif(option == 2):
            AppName = input("Enter App Name to which you need to Update Password : ")
            NewPassword = input("Enter new password: ")
            secretKey = input("Give Secret key : ")
            encrypted = encrypt(NewPassword,secretKey)
            Query = "UPDATE passwords set Passwrd = %s where AppName = %s"
            mydbcursor.execute(Query,(encrypted,AppName))
            mydb.commit()
    except Error as e:
        print(e)
def delete(mydb):
    AppName = input("Enter App name to remove :")
    mydbcursor = mydb.cursor()
    Query = "DELETE FROM passwords WHERE AppName = %s"
    mydbcursor.execute(Query,(AppName,))
    mydb.commit()



print("1. insert new password \n 2. Get password for App \n 3. Update Password \n 4. Delete password")
Action = int(input("Enter your option : "))
try:
    mydb = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="welcome",
                database ="my_first_db",
                auth_plugin='mysql_native_password'
                    )
    mydbcursor = mydb.cursor()


    if(Action == 1):
        print("Enter App Name :")
        AppName = input()
        AppName = AppName.lower()
        print("Enter User Name: ")
        UserName = input()
        print("Enter password for App :")
        Password = input()
        secretKey = input("Give Secret key : ")
        encrypted = encrypt(Password,secretKey)
        insert(mydbcursor,AppName,UserName,encrypted)


    elif(Action == 2):
        print("Enter AppName : ")
        AppName = input()
        AppName = AppName.lower()
        select(mydbcursor,AppName)
    elif(Action == 3):
        update(mydb)
    elif(Action == 4):
        delete(mydb)
except Error as e:
        print(e)