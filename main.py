# /usr/bin/python3

import sqlite3
from PIL import Image,ImageTk,ImageDraw
import tkinter as tktk
import os
import uuid
import time

import numpy as np
import face_recognition as fr

from img_show import showImageOnTk
from strings import DB_FILENAME, PHOTO_DIR

class FoldersWalker():
    def __init__(self, folder):
        self.folder = folder
        self.folders = list()
        self.walkerGo(self.folder)

    def walkerGo(self,folderPath):
        for root, _, files in os.walk(folderPath):
            if not root.endswith("\\"):
                root += "\\"
            for f in files:
                if f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".png") or f.endswith(".JPG")\
                    or f.endswith(".JPEG") or f.endswith(".PNG"):
                    self.folders.append(''.join([root,f]))
    def getFiles(self):
        return self.folders

# CREATE A DATABASE FOR SAVING INFO OF PHOTOS
# DB FILE NAME IS IN strings.py
class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILENAME)
        self.conn.execute("CREATE TABLE IF NOT EXISTS face\
            (id INTEGER PRIMARY KEY AUTOINCREMENT,\
            uuuid TEXT,\
            face_encoding TEXT,\
            file_location TEXT,\
            t INTEGER,r INTEGER,\
            b INTEGER, l INTEGER)")
        self.conn.execute("CREATE TABLE IF NOT EXISTS names\
            (uuuid TEXT,\
            name TEXT)")

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def pushData(self,uuuid,face_encoding,file_location,t,r,b,l):
        uuuid = str(uuuid)
        print("- Pushing:{}:{}".format(uuuid,file_location))
        self.conn.execute("INSERT INTO face (uuuid,face_encoding,file_location,\
            t,r,b,l) VALUES (?,?,?,?,?,?,?)",\
            (uuuid,face_encoding,file_location,t,r,b,l))
    
    def getNameByUUID(self,uuuid) ->str:
        n = self.conn.execute("SELECT name FROM names WHERE uuuid=?",(uuuid,)).fetchall()
        if n == []:
            return False
        return n[0]
    
    def getAllFacesByUUIDs(self,uuids):
        faces = []
        for uuuid in uuids:
            faces.append(self.conn.execute("SELECT * FROM face WHERE uuuid=?",(uuuid[0],)).fetchall()[0])
        return faces
    
    def getAllFacesByUUID(self,uuuid) ->list:
        n = self.conn.execute("SELECT * FROM face WHERE uuuid=?",(uuuid,)).fetchall()
        return n

    def getAllUUIDs(self) ->list:
        return self.conn.execute("SELECT uuuid FROM names").fetchall()
    
    def pushUUIDsAndName(self,uuuid,name):
        uuuid = str(uuuid)
        name  = str(name)
        self.conn.execute("INSERT INTO names (uuuid,name) VALUES (?,?)",(uuuid,name))
    
    def checkFileExist(self,filename):
        res = self.conn.execute("SELECT id FROM face WHERE file_location=?",(filename,)).fetchall()
        if res == []:
            return False
        return True

# convert face data into bytes so that it can be stored in database
def encodeFace(face):
    return face.tobytes()
def decodeFace(face):
    return np.frombuffer(face)

# main loop
class FaceRunner:
    def __init__(self):
        self.folders = PHOTO_DIR
        self.db = Database()
    def run(self):
        #LOAD PHTOTS
        wk = FoldersWalker(self.folders)
        photos = wk.getFiles()

        #ANALIZE PHOTOS
        for photo in photos:
            print(f"\n\n****************************************\nFILE:{photo}")
            if self.db.checkFileExist(photo):
                print(f"FILE:{photo} : exists, jumpted.")
                continue

            # Load photos and scale them so that the photo can be analysed faster
            fr_img = fr.load_image_file(photo)
            pi_img = Image.fromarray(fr_img)
            scale = 1
            while pi_img.height > 700:
                pi_img = pi_img.resize((pi_img.width//2, pi_img.height//2))
                scale *= 2
            fr_img = np.asarray(pi_img)

            # analyse the photo
            encs = fr.face_encodings(fr_img)
            locs = fr.face_locations(fr_img)
            print(f"FILE:{photo} : has {len(encs)} faces")
            for i in range(len(encs)):
                t,r,b,l = locs[i]
                t *= scale
                r *= scale
                b *= scale
                l *= scale
                uuids = self.db.getAllUUIDs()
                if uuids == []:
                    uuuid = uuid.uuid4()
                    self.db.pushData(uuuid,encodeFace(encs[i]),photo,t,r,b,l)
                    self.db.pushUUIDsAndName(uuuid,uuuid)
                    continue
                faceDatas = self.db.getAllFacesByUUIDs(uuids)
                res = False
                '''
                im_c = Image.fromarray(fr_img[t//scale:b//scale,l//scale:r//scale])
                showImageOnTk(im_c)
                '''
                for faceData in faceDatas:
                    res = fr.compare_faces([decodeFace(faceData[2])],encs[i],tolerance=0.4)[0]
                    if res:
                        print("FILE:{} : {}: FETCH: {} in {}".format(photo,i,faceData[1],faceData[3]))
                        self.db.pushData(faceData[1],encodeFace(encs[i]),photo,t,r,b,l)
                        break
                if not res:
                    uuuid = uuid.uuid4()
                    self.db.pushData(uuuid,encodeFace(encs[i]),photo,t,r,b,l)
                    self.db.pushUUIDsAndName(uuuid,uuuid)
        del self.db

# PROGRAM INTERFACE START FROM HERE
runner = FaceRunner()
runner.run()
