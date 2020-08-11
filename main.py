# /usr/bin/python3

import sqlite3
from PIL import Image,ImageTk,ImageDraw
import tkinter as tktk

import face_recognition as fr

from img_show import showImageOnTk
import strings


# CREATE A DATABASE FOR SAVING INFO OF PHOTOS
# DB FILE NAME IS IN strings.py
class Database:
    def __init__(self):
        self.conn = sqlite3.connect(strings.DB_FILENAME)
        self.conn.execute("CREATE TABLE IF NOT EXISTS face\
            (id INTEGER PRIMARY KEY AUTOINCREMENT,\
            name TEXT,\
            face_encoding TEXT,\
            file_location TEXT,\
            md5 TEXT)")

    # YOU MUST RUN TIHS METHOD:def close(self) TO ENSURE 
    # THE INFORMATION IS COMMITED AND DB IS CLOSED
    def close(self):
        self.conn.commit()
        self.conn.close()

    def pushData(self,name,face_encoding,file_location,md5):
        tp = (name,face_encoding,file_location,md5)
        self.conn.execute("INSERT INTO face VALUES \
            (name,face_encoding,file_location,md5)",tp)
    
    def getDataByMD5(self,md5:str):
        """
        :param md5: the MD5 of the file
        :return: False if not exist or (id,name,face_encoding,file_location,md5)
        """
        found_items = self.conn.execute("SELECT * FROM face WHERE md5=?",(md5,)).fetchall()
        if found_items == []:
            return False
        return found_items[0]

    def getDataByFace(self,face):
        pass

im = Image.open("trump.jpg")
(kuan,gao) = (im.width //2 ,im.height // 2)
im1 = im.resize((114,514))
showImageOnTk(im1)
