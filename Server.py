import socket
from sqlite3 import connect
import threading
import json
import os
import os.path
import imghdr
from requests import request


HEADER = 64
PORT = 5050
users = []
SERVER = socket.gethostbyname('localhost')
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"



class Store_User:
    def __init__(self, username, password):
        self.Name = username
        self.Pass = password

class Note:
  def __init__(self,ID, typeFile,content, nameFileOriginal):
    self.ID = ID
    self.Type = typeFile
    self.Content = content
    self.FileOriginal = nameFileOriginal

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

server.listen(10)
print('[LISTENING] Server is listening on ',SERVER)



def writeNoteToFile(conn,filename,newnote):
  file_exists = os.path.exists(filename)

  if file_exists == False:
    f = open(filename, 'w')
    json_object = json.dumps(newnote, indent = 2)
    f.write(json_object)
    f.close()
    return
  else :
    f = open(filename, 'r+')
    listNote = []  
    note = json.load(f)
    listNote += note
    print('L: ',listNote)
    listNote.append(newnote)
    f.seek(0)
    json.dump(listNote, f, indent = 2)
    f.close()
  print('Finish sending')  
  
def saveFileNote(nameFileNote,conn,size):
  with open(nameFileNote, 'wb') as f: 
    print('Start saving')
    time = 0
    
    if size%(1024*10) !=0:
      time = int (size/(1024*10)) +1
    else:
      time = int (size/(1024*10))
    
    
    count = 0
    
    while count < time: 
      data = conn.recv(1024*10)
      f.write(data)

      count += 1
 
  f.close()
  print('Finish saving')
  
    
def getsizeToSendNote(conn,nameFileID):
  print("hihihihi")
  size = os.path.getsize(nameFileID)
  print(size)
  size = str(size)
  conn.send(size.encode(FORMAT))
  temp = conn.recv(1024*10).decode(FORMAT)
  size = int(size)
  
  readFileNote(conn,nameFileID,size)
  
def receiveSize(self,filename):
  self.size = self.client.recv(1024*10).decode(FORMAT)
  self.size = int(self.size)
  print(self.size)
  self.client.send("receive".encode(FORMAT))
  self.saveFileNote(filename)
  
def readFileNote(conn,nameFileID,size):
  with open(nameFileID, 'rb') as f:
    time = 0
    if size%(1024*10) !=0:
      time = int (size/(1024*10)) +1
    else:
      time = int (size/(1024*10))
      
    count = 0
    data = f.read(1024*10)
    print(data)
    while count < time:
      conn.send(data)
      count +=1
      data = f.read(1024*10)

  print('Done sending')
  f.close()

  
  
def printNoteTable(conn,filename):
  print(filename)
  file_exists = os.path.exists(filename)
  print(file_exists)
  listNote = [] 
  if file_exists:
    with open(filename,'r') as file:
      list = json.load(file)
  
    print('\tID\t\t\t\tType\t\t\tContent')
    listNote += list
    size = str(len(listNote))
    print (size)
    conn.send(size.encode(FORMAT))
    receive = conn.recv(1024*10).decode(FORMAT)
    for x in range(len(listNote)):
      conn.send(listNote[x]['ID'].encode(FORMAT))
      receive = conn.recv(1024*10).decode(FORMAT)
      conn.send(listNote[x]['FileOriginal'].encode(FORMAT))
      receive = conn.recv(1024*10).decode(FORMAT)
      conn.send(listNote[x]['Type'].encode(FORMAT))
      receive = conn.recv(1024*10).decode(FORMAT)
      conn.send(listNote[x]['Content'].encode(FORMAT))
      receive = conn.recv(1024*10).decode(FORMAT)
      file.close()
  else:
    reply = "No data"
    conn.send(reply.encode(FORMAT))
  return listNote
   
    
def sendFileToShow(conn,listNote,filename):
  print("View Note")
  
  IdToView = conn.recv(1024*10).decode(FORMAT)
  filename =""
  for x in range(len(listNote)):
    if listNote[x]['ID'] == IdToView:
      filename = listNote[x]['FileOriginal']
      typee = listNote[x]['Type']
      break

  print(filename)
  dot = filename[-4:]
  print(dot)
  nameFileID = IdToView + dot
 
  conn.send(filename.encode(FORMAT))
  print("Hello")
  print(nameFileID)
  temp = conn.recv(1024*10).decode(FORMAT)
  
  getsizeToSendNote(conn,nameFileID)
  print("Done View")



def downloadFile(conn,listNote,filename):
  IdToDownload = conn.recv(1024*10).decode(FORMAT)
  filename =""
  for x in range(len(listNote)):
    if listNote[x]['ID'] == IdToDownload:
      filename = listNote[x]['FileOriginal']
      break


  dot = filename[-4:]
  nameFileID = IdToDownload + dot

  conn.send(nameFileID.encode(FORMAT))
  print("Hello")
  temp = conn.recv(1024*10).decode(FORMAT)

  getsizeToSendNote(conn,nameFileID)



def FrameViewNote(conn,filename):
  print(filename)
  listNote = printNoteTable(conn,filename)
  while True:
    choose = conn.recv(1024*10).decode(FORMAT)
    if choose == "View File":
      sendFileToShow(conn,listNote,filename)
    elif choose == "Download File":
      downloadFile(conn,listNote,filename)
    elif choose == "Return":
      print("returned")
      return
    

def mainWindow(conn,filename):
  while True:
    choose =conn.recv(1024*10).decode(FORMAT)
    print(choose)
    if choose == "Send note":
      print("Send note")
      receiveNote(conn,filename)
    elif choose == "View Note":
      FrameViewNote(conn,filename)
    else:
      break
  
def checkIsImage(conn,name):
  while True:
    if imghdr.what(name) != None:
      true = 'True'
      conn.send(true.encode(FORMAT));
      break
    else:
      request = 'You must input file image'
      conn.send(request.encode(FORMAT));
      name = conn.recv(1024*10).decode(FORMAT)
  return name
  
  
def receiveNote(conn,filename):
  while True:
    reply = conn.recv(1024*10).decode(FORMAT)
    print(reply)
    if reply == "return":
      break
    conn.send("received".encode(FORMAT))
    print("Client:", reply)
    typeFile = ""
    if reply == 'Text':
      typeFile = "Text"
    if reply == 'Image':
      typeFile = "Images"
    if reply == 'File':
      typeFile = "File"
    print("Type:",typeFile)
    request = 'Input the name of file'
    # conn.send(request.encode(FORMAT));
    
    name = conn.recv(1024).decode(FORMAT)
    conn.send("received".encode(FORMAT))
    print('type:', typeFile)
    print('Filename:', name)
    position = name.rfind('/')
    print (position)
    if position != -1:
      print("getname")
      name = name[position + 1: ]

    
    ID = str(hash(name))
    print(ID)
    #print(type(id))
    dot = name.find('.')
    print(dot)
    dotFile = name[dot:]
    print(dotFile)
    #print(type(dotFile))
    NameFileSave = ID + dotFile
    print(NameFileSave)
    if typeFile == "Images" or typeFile == "File":
      print("2")
      receiveFile_Image(conn, NameFileSave)
    else:
      print("3")
      receiveText(conn,NameFileSave)
    
    content = os.path.abspath(NameFileSave)
    print('Content',content)
    newnote = Note(ID,typeFile,content,name)
    print('Get note:', newnote)
    newnote = newnote.__dict__
    print('Got note')
    

    writeNoteToFile(conn,filename,newnote)
    print('Finish')

def receiveFile_Image(conn, filenameImage):
  size_Img_File = conn.recv(1024*10).decode(FORMAT)
  size_Img_File = int(size_Img_File)
  print("1")
  print(filenameImage)
  with open(filenameImage, 'wb') as f: 
      print('Start saving')
      time = 0
      
      if size_Img_File%(1024*10) !=0:
        time = int (size_Img_File/(1024*10)) +1
      else:
        time = int (size_Img_File/(1024*10))
      
      count = 0
      print(time)
      
      while count < time: 
        data = conn.recv(1024*10)
        #print(data)
        f.write(data)

        count += 1
  print("Done receive")
  f.close()
  
def readFileJSONtoCheckNote(filename,ID):
  with open(filename, "r") as check:
      note = json.load(check)
      for i in note:
          if i['ID'] in ID :
              return False
          else:
            return True
      return False


def receiveText(conn,nameFileNote):
  
  contentText = conn.recv(1024).decode(FORMAT)
  with open(nameFileNote, 'w') as f: 
    print('Start saving')
    print(contentText)
    f.write(contentText)
  f.close()



def validation(username, password):
    print("Log in")
    with open("info.json", "r") as login:
        user_lines = json.load(login)
        for i in user_lines:
            if i['Name'] == username and i['Pass'] == password:
                return True
        
        return False

def write_json(new_data, filename='info.json'):
    with open(filename, "r") as file:
        data = json.load(file)
        print(type(data))
        for x in range(len(data)):
          if data[x]['Name'] == new_data['Name']:
            return False
        
        data.append(new_data)
    file.close()
    with open(filename, "w") as file:
        json.dump(data,file)

    return True

def New_User(username, password):
  
    new = Store_User(username, password)
    new = new.__dict__
    print(type(new))
    print(new)
    if write_json(new) == False:
      return False
    return True

def client_signup(conn):
  print("Sign Up")
  username =""
  while True:
    conn.send("receive".encode(FORMAT))
    username = conn.recv(1024*10).decode(FORMAT)
    reply = conn.send("receive".encode(FORMAT))
    password = conn.recv(1024*10).decode(FORMAT)

    if len(username) < 5:
      request = "Username contains at least 5 letters"
      conn.send(request.encode(FORMAT))
      continue
    elif len(password) < 3:
      request = "Password contains at least 3 letters"
      conn.send(request.encode(FORMAT))
      continue
    #if username.isdigit() 
    else: 
      Check = New_User(username, password)
      if Check == True:
        reply = "Sign up successfully!"
        conn.send(reply.encode(FORMAT))
        break;
      else:
        request = "Username is invalid or already taken"
        conn.send(request.encode(FORMAT))
  return username
        
        
def Client_information(mess, conncect):
  for user in users:
      if users != conncect:
          try:
              user.sendall(bytes(mess, FORMAT))
          except:
              user.close()

def client_login(conn):
  print ("Log In")
  username = ""
  while True:
    conn.send("temp".encode(FORMAT))
    username = conn.recv(1024*10).decode(FORMAT)
    print("Username:",username)
    conn.send("reveice".encode(FORMAT))
    password = conn.recv(1024*10).decode(FORMAT)
    print("Password:",password)
    Check = validation(username, password)

    if Check == True:
      reply = "Login successfully!"
      print(reply)
      conn.send(reply.encode(FORMAT))
      break
    else: 
      reply = 'Username or password is error'
      conn.send(reply.encode(FORMAT))
  return username



def selectionFunction(conn):
  res_client = conn.recv(1024)
  res_client = res_client.decode(FORMAT)
  return res_client


def handle_client(conn, addr):
  print("[NEW CONNECTION]"," connected", addr)

  choice_login = conn.recv(1024).decode(FORMAT)
  print ("CHOOSE: ",choice_login)
  username =''
  if choice_login == "1":
      username = client_signup(conn)
  elif choice_login == "2":
      username = client_login(conn)
  
  
  filename = 'Data/' +username+ '.json'
  print(filename)
  #filename = '/Users/user/Downloads/Final/Data/' +"tram"+ '.json'
  mainWindow(conn,filename)
  conn.close()
  
   
  
nClient = 0
while (nClient < 10):
  try: 
    def start():
      conn, addr = server.accept()
      
      thread = threading.Thread(target=handle_client, args=(conn, addr))
      thread.daemon = True
      thread.start()
      print("[ACTIVE CONNECTIONS]" ,threading.activeCount() - 1)
        
    print("[STARTING] server is starting...")
    start()

  except:
    print("Error")
  nClient += 1

print ("End")
input()
server.close()
