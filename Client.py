import tkinter as tk
from tkinter import ttk
from tkinter import *
import socket
import imghdr
import os
import subprocess
from tkinter import messagebox
from PIL import ImageTk, Image  
from tkinter import filedialog
from tkinter import filedialog
from tkinter.filedialog import askopenfilename

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


class Client():
  def __init__(self):  
    HEADER = 64
    PORT = 5050
   
    DISCONNECT_MESSAGE = "!DISCONNECT"
    SERVER = "127.0.0.1"
    ADDR = (SERVER, PORT)
    self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    self.client.connect(ADDR)
    
    
  def WindowLogin(self):
    self.windowLogin = Tk()
    self.windowLogin.title('E-Note')
    self.windowLogin.geometry('500x450')
    self.windowLogin.configure(bg = 'dark sea green')
    self.StartLoginPage() 
    
    self.windowLogin.mainloop()
  
  
  def StartLoginPage(self):
    self.frameStartLoginPage =Frame(self.windowLogin, width=300, height=300,bg = 'dark sea green')
 
    self.frameStartLoginPage.grid(row=0, column=0,sticky="nsew")
    self.frameStartLoginPage.tkraise()
    tempspace = Label(self.frameStartLoginPage,text = "                          ",bg = 'dark sea green')
    tempspace.grid(column=0,row=0)
    self.labelStartPage = Label(self.frameStartLoginPage, text = "Welcome to E-Note",font = ("Arial", 25),bg = 'dark sea green')
    self.labelStartPage.grid(column =6,row =1)
    

    self.loginButtonMenu = Button(self.frameStartLoginPage,text = "Log In",command= self.Login,width = 20,height= 5 )
    self.loginButtonMenu.grid(column =5,row=2, columnspan= 2,rowspan=2)
    
    self.signUpButtonMenu = Button(self.frameStartLoginPage,text = "Sign Up",command= self.Signup,width = 20,height= 5 )
    self.signUpButtonMenu.grid(column =5,row=5, columnspan= 2,rowspan=2)

    self.ButtonExit = Button(self.frameStartLoginPage,text = "Exit",command= self.ExitProgram,width = 20,height= 5 )
    self.ButtonExit.grid(column =5,row=8 ,columnspan= 2,rowspan=2)


  def ExitProgram(self):
    self.windowLogin.destroy()
    
  def Login(self): 
    
    self.FrameLogin =Frame(self.windowLogin,bg = 'dark sea green')
    
    self.FrameLogin.grid(row=0, column=0,sticky="nsew")
    self.FrameLogin.tkraise()
    
    Label(self.FrameLogin , text="Log in",fg="white",font=("Arial", 15),background= 'dark sea green').place(x=220,y=10)

    self.labelUsernameLogin = Label(self.FrameLogin,text="Username * ",bg = 'dark sea green').place(x=120,y=40)
   

    self.labelPasswordLogin = Label(self.FrameLogin,text="Password * ",bg = 'dark sea green').place(x=120,y=80)
   
    
    self.usernameLogin = StringVar()
    self.passwordLogin = StringVar()
    
    self.usernameEntry = Entry(self.FrameLogin,textvariable= self.usernameLogin).place(x=190,y=42)
    

    self.passwordEntry = Entry(self.FrameLogin,textvariable= self.passwordLogin,show="*").place(x=190,y=82)
    
    self.client.send("2".encode(FORMAT))
    self.temp = Label(self.FrameLogin,text = "",bg = 'dark sea green').place(x=95,y=100)

    
    self.ButtonLogin = Button(self.FrameLogin,text = "Login", command =  self.sendUserLogin,width=10, height=1, bg="orange").place(x=210,y=130)

    
    self.ButtonReturnLogin = Button(self.FrameLogin,text = "Return", command =  self.ReturnPageLogin,width=10).place(x = 210, y = 170)



  def ReturnPageLogin(self):
    self.client.send("Return".encode(FORMAT))
    self.frameStartLoginPage.tkraise()
    
    
  def sendUserLogin(self):
    username = self.usernameLogin.get()
    password = self.passwordLogin.get()
    reply = self.client.recv(1024*10).decode(FORMAT)
    self.client.send(username.encode(FORMAT))
    reply = self.client.recv(1024*10).decode(FORMAT)
    self.client.send(password.encode(FORMAT))
    reply = self.client.recv(1024*10).decode(FORMAT)
    if reply == "Login successfully!":
      print ("Login successfully!")
      # self.temp.config(text = "")
      messagebox.showinfo("Announcement","Login successfully!")
      self.windowLogin.destroy()
      self.mainWindow()
      
    else:
      messagebox.showerror("error","username or password invalid")

      self.usernameEntry.delete(0,END)
      self.passwordEntry.delete(0,END)

  def Signup(self):
    
    self.FrameSignup =Frame(self.windowLogin,bg = 'dark sea green')
   
    self.FrameSignup.grid(row=0, column=0,sticky="nsew")
    
    self.FrameSignup.tkraise()
    
    Label(self.FrameSignup , text="Sign up",fg="white",font=("Arial", 15),bg = 'dark sea green').place(x=220,y=10)
    
    self.labelUsernameSignUp = Label(self.FrameSignup,text="Username * ",bg = 'dark sea green').place(x=120,y=40)
   
    self.labelPasswordSignup = Label(self.FrameSignup,text="Password * ",bg = 'dark sea green').place(x=120,y=80)

    
    self.usernameSignUp = StringVar()
    self.passwordSignUp = StringVar()

    self.usernameEntry = Entry(self.FrameSignup,textvariable= self.usernameSignUp).place(x=190,y=42)

    self.passwordEntry = Entry(self.FrameSignup,textvariable= self.passwordSignUp,show="*").place(x=190,y=82)
    self.client.send("1".encode(FORMAT))
    
    self.temp = Label(self.FrameSignup,text = "",bg = 'dark sea green').place(x=95,y=100)
  
    self.ButtonSignUp = Button(self.FrameSignup,text = "Sign Up", command =  self.sendUserSignUp,width=10, height=1, bg="orange").place(x=210,y=130)
    
    self.ButtonReturnSignup = Button(self.FrameSignup,text = "Return", command =  self.ReturnPageLogin,width=10).place(x = 210, y = 170)
    
    
  def sendUserSignUp(self):
    username = self.usernameSignUp.get()
    password = self.passwordSignUp.get()
    reply = self.client.recv(1024*10).decode(FORMAT)
    self.client.send(username.encode(FORMAT))
    reply = self.client.recv(1024*10).decode(FORMAT)
    self.client.send(password.encode(FORMAT))
    reply = self.client.recv(1024*10).decode(FORMAT)
    if reply == "Sign up successfully!":
      print ("Sign up successfully!")
      messagebox.showinfo("Announcement","Sign up successfully!")
      self.windowLogin.destroy()
      self.mainWindow()
      
    elif reply == "Username contains at least 5 letters": 
      messagebox.showerror('Error', 'Username contains at least 5 letters \n please fill it')
      self.usernameEntry.delete(0,END)
      self.passwordEntry.delete(0,END)
    elif reply == "Password contains at least 3 letters" :
      messagebox.showerror('Error', 'Password contains at least 3 letters \n please fill it')
      self.usernameEntry.delete(0,END)
      self.passwordEntry.delete(0,END)
    else:
      messagebox.showerror('Error', 'User is invalid or already taken \n please fill it again')
      self.usernameEntry.delete(0,END)
      self.passwordEntry.delete(0,END)
       
  def mainWindow(self):
    self.noteWindow = Tk()
    self.noteWindow.title('E-Note')
    self.noteWindow.geometry('1000x400')
    self.noteWindow.configure(bg='dark sea green')
    self.startWindowNote() 
    
    self.noteWindow.mainloop()

  def startWindowNote(self):
    
    self.frameStartWindowNote = Frame(self.noteWindow,bg='dark sea green')
   
    
    self.frameStartWindowNote.grid(row=0, column=0,sticky="nsew")
    self.frameStartWindowNote.tkraise()
    

    tempspace = Label(self.frameStartWindowNote,text = "                                                             ",bg='dark sea green')
    tempspace.grid(column=0,row=0)
    tempspace2 = Label(self.frameStartWindowNote,text = "                                                                         ",bg='dark sea green')
    tempspace2.grid(column=1,row=0)

   
    labelStartPage = Label(self.frameStartWindowNote, text = "Your choose!!",font = ("Arial", 25),bg='dark sea green')


    labelStartPage.grid(column =10,row =0)

    
    
    sendNoteButton = Button(self.frameStartWindowNote,text = "Send Note",command =self.SendNote,width = 20 ,height =5, bg= 'yellow')
    sendNoteButton.grid(column =10,row=3, columnspan= 2,rowspan=2)
 

    viewNoteButton = Button(self.frameStartWindowNote,text = "View Note",command =self.ViewNote,width = 20 ,height =5, bg= 'yellow')
    viewNoteButton.grid(column =10,row=7,columnspan= 2,rowspan=2)

    


  def SendNote(self):
    print("Send note")
    self.client.send("Send note".encode(FORMAT))
    self.FrameSendNote = Frame(self.noteWindow,bg='dark sea green')
    self.FrameSendNote.grid(row=0, column=0,sticky="nsew")
   
    self.FrameSendNote.tkraise()
    tempspace = Label(self.FrameSendNote,text = "                                                   ",bg='dark sea green')
    tempspace.grid(column=0,row=0)
    tempspace2 = Label(self.FrameSendNote,text = "                                                               ",bg='dark sea green')
    tempspace2.grid(column=1,row=0)
    self.LabelMenuSendNote = Label(self.FrameSendNote,text = "WHICH TYPES DO YOU WANT TO SEND?",font = ("Arial", 12),bg = 'dark sea green')
    self.LabelMenuSendNote.grid(column =2,row =1,columnspan=2,rowspan=2)
    
    self.ButtonTypeTxt = Button(self.FrameSendNote, text = "Text",width = 20 ,height =5,command= self.sendNoteTypeTxt, bg= 'yellow')
    self.ButtonTypeTxt.grid(column =2,row =4,columnspan=2,rowspan=2)
    
    self.ButtonTypeImage = Button(self.FrameSendNote, text = "Image",width = 20 ,height =5, command= self.sendNoteTypeImage, bg= 'yellow')
    self.ButtonTypeImage.grid(column =2,row =7,columnspan=2,rowspan=2)
    
    self.ButtonTypeFile = Button(self.FrameSendNote, text = "File",width = 20 ,height =5, command= self.sendNoteTypeFile, bg= 'yellow')
    self.ButtonTypeFile.grid(column =2,row =10,columnspan=2,rowspan=2)
    
    self.ButtonReturn = Button(self.FrameSendNote,text = "Return", command= self.Return,width=20,height=5, bg= 'yellow')
    self.ButtonReturn.grid(column = 2,row =14,columnspan=2)
  
  def Return(self):
    self.client.send("return".encode(FORMAT))
    self.frameStartWindowNote.tkraise()
      
  def checkFillFileName(self):
    if self.nameText == "":
      messagebox.showerror('Error', ' Name File has not been filled yet \n please fill it')
      return False
    return True
  
  def sendTextToServer(self):
  
    self.nameText = self.FileNameTxt.get()
    content_txt = self.NoteContent.get('1.0', 'end')
    check = self.checkFillFileName()
    if check == True:
      self.nameText += ".txt"
      self.client.send(self.nameText.encode(FORMAT))
      self.client.recv(1024).decode(FORMAT)
      print(content_txt)
      self.client.send(content_txt.encode(FORMAT))
      messagebox.showinfo("Announcement","Sending Successfully")
      self.WindowToSendNote.destroy()
      
  def writeNoteToFileText(self):
    filename = self.FileName.get()
    contentNote = self.NoteContent.get(1.0, "end-1c")
    with open(filename+".txt","w") as file:
      file.write(contentNote)
    
    file.close()
    messagebox.showinfo("Message","You send note sucessfully")

    
  def sendNoteTypeTxt(self):
    self.WindowToSendNote = Toplevel(self.FrameSendNote, bg='dark sea green')
    self.WindowToSendNote.title("Write Note")
    self.WindowToSendNote.geometry("520x420")
    self.client.send("Text".encode(FORMAT))
    self.client.recv(1024*10).decode(FORMAT)
    
    self.LabelFileName =Label(self.WindowToSendNote,text= "Write name of file text: ",bg = 'dark sea green')
    self.LabelFileName.grid(row= 1, column=1,columnspan=2)
    
    self.FileNameTxt = StringVar()
    self.EntryFileName = Entry(self.WindowToSendNote,textvariable=self.FileNameTxt,width= 30)
    self.EntryFileName.grid(row =1, column= 3,columnspan =3)

    
    self.topicLabel = Label(self.WindowToSendNote, text = "Write note to here:",bg = 'dark sea green')
    self.topicLabel.grid(column=1, row = 2,columnspan= 2)
    
    space = Label(self.WindowToSendNote, text = "",bg = 'dark sea green')
    space.grid(column=1, row = 3)
    
    self.NoteContent = StringVar()
    self.NoteContent = tk.Text(self.WindowToSendNote, height = 20,width = 60,  bg = "light yellow",borderwidth=2)
    self.NoteContent.grid(column=1,row =4,rowspan=10,columnspan=10)
    
  
    self.ButtonSendNoteTypeText = Button(self.WindowToSendNote,text = "Send", command= self.sendTextToServer, bg="deep sky blue", fg='black')
    self.ButtonSendNoteTypeText.place(relx=1.0, rely=1.0, anchor=SE)

  def upload_file(self):
    global img
    f_types = [('Jpg Files', '*.jpg'), ('png Files', '*.png')]
    self.filenameImage = filedialog.askopenfilename(filetypes=f_types)
    img = Image.open(fp= self.filenameImage)
    resized_image= img.resize((650, 400), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(resized_image)
    Button(self.right_frame, image=img).grid(row=0,column=0, padx=5, pady=5)
    self.chosen_Image.config(text = "Image is chosen")


  def sendImageAndDestroy(self):
    self.sendImageToServer()
    messagebox.showinfo("Announcement","Sending Successfully")
    self.WindowToSendImage.destroy()
    self.FrameSendNote.tkraise()
  
  def sendFileAndDestroy(self):
    self.sendImageToServer()
    messagebox.showinfo("Adnnouncement","Sending Successfully")
    self.WindowToSendFile.destroy()
    
  def sendImageToServer(self):
    self.client.send(self.filenameImage.encode(FORMAT))
    print("2:",self.filenameImage)
    self.client.recv(1024).decode(FORMAT)

    size = os.path.getsize(self.filenameImage)
    size = str(size)
    self.client.send(size.encode(FORMAT))
    size = int(size)
    with open(self.filenameImage, 'rb') as f:
      time = 0

      if size%(1024*10) !=0:
        time = int (size/(1024*10)) +1
      else:
        time = int (size/(1024*10))
        
      count = 0
      data = f.read(1024*10)
      print(data)
      while count < time:
        self.client.send(data)
        count +=1
        data = f.read(1024*10)

    print('Done sending')
    f.close()
    
    
  def sendNoteTypeImage(self):
    self.WindowToSendImage = Toplevel(self.FrameSendNote)
    self.WindowToSendImage.title("Send Image")
    self.WindowToSendImage.maxsize(900, 600) 
    self.WindowToSendImage.config(bg="skyblue")
    self.WindowToSendImage.tkraise()

    left_frame = Frame(self.WindowToSendImage, width=200, height=400, bg='grey')
    left_frame.grid(row=0, column=0, padx=10, pady=5)
    self.right_frame = Frame(self.WindowToSendImage, width=650, height=400, bg='bisque2')
    self.right_frame.grid(row=0, column=1, padx=10, pady=5)

    Button(left_frame, text="choose file Image", command = self.upload_file, bg= 'red').grid(row=0, column=0, padx=5, pady=5)
    self.chosen_Image = Label(left_frame, text= 'no image is chosen')
    self.chosen_Image.grid(row=1, column=0, padx=5, pady=5)

    tool_bar = Frame(left_frame, width=180, height=185)
    tool_bar.grid(row=2, column=0, padx=5, pady=5)
    #, relief=RAISED,
    send_button = Button(tool_bar, text="Send", relief=RAISED, command= self.sendImageAndDestroy).grid(row=0, column=0, padx=5, pady=3, ipadx=10)
    self.client.send("Image".encode(FORMAT))
    temp = self.client.recv(1024*10).decode(FORMAT)

 
  def sendFileToServer(self):
    file_size_in_bytes = 0
    count_file = len(self.filelst)
    print(count_file)
    self.client.send(str(count_file).encode(FORMAT)) 
    for file in self.filelst:
      size = os.path.getsize(file)
      file_size_in_bytes = size.to_bytes(8,byteorder= 'big')
      self.client.send(file_size_in_bytes)
      for file in self.filelst:
        with open(file, encoding="utf-8") as f1:
          self.client.send(f1.read())
        
  def sendNoteTypeFile(self):
    self.WindowToSendFile = Toplevel(self.FrameSendNote,bg = 'dark sea green')
    self.WindowToSendFile.title("Write Note")
    self.WindowToSendFile.geometry("750x500")
    
    self.client.send("File".encode(FORMAT))
    temp = self.client.recv(1024*10).decode(FORMAT)

    adharbtn = Button(self.WindowToSendFile, text ='Choose File', command = self.UploadAction ) 
    adharbtn.grid(row=3, column=1)
    self.label1 = tk.Label(self.WindowToSendFile,text='Please choose a file',bg = 'dark sea green')
    self.label1.grid(row = 2, column=0)
    send_button = Button(self.WindowToSendFile, text= "Send", width=5, height= 2, command= self.sendFileAndDestroy)
    send_button.place(relx=1.0, rely=1.0, anchor=SE)
      
  def UploadAction(self):
    self.filenameImage = askopenfilename()
    
    check_file = self.filenameImage.endswith(('.txt'))
    if check_file == True:
      messagebox.showerror('Error', 'File chosen should be not Txt \n please choose again')
    elif imghdr.what(self.filenameImage) != None:
      messagebox.showerror('Error', 'File chosen should be not Image \n please choose again')
    else:
      print('Selected:', self.filenameImage)
      self.label1['text'] = self.filenameImage
  def ViewNote(self):
    self.client.send("View Note".encode(FORMAT))
    self.FrameViewNote = Frame(self.noteWindow,width=700, height=300,bg='dark sea green')
 
    self.FrameViewNote.grid(row=0, column=0,sticky="nsew")
    self.FrameViewNote.tkraise()
    
    self.tree = self.receiveListNote()
    if self.tree != False:
 
      self.ButtonView = Button(self.FrameViewNote,text= "View File",command= self.ChooseViewFile,width=10,height=4)
      self.ButtonView.grid(column=5,row=25,columnspan=4)
      
      self.ButtonDownload = Button(self.FrameViewNote,text= "Download File",command= self.ChooseDownloadFile,width=10,height=4)
      self.ButtonDownload.grid(column=15,row=25,columnspan=4)
      
      self.ButtonReturn = Button(self.FrameViewNote,text= "Return",command= self.ChooseReturn,width=10,height=4)
      self.ButtonReturn.grid(column=23,row=25,columnspan=10)


  def ChooseReturn(self):
    checkReturn = "Return"
    self.client.send(checkReturn.encode(FORMAT))
    self.frameStartWindowNote.tkraise() 
    
    
  def ChooseViewFile(self):
    self.client.send("View File".encode(FORMAT))
    self.windowViewFile = Toplevel(self.FrameViewNote,bg='dark sea green')
    self.windowViewFile.geometry("500x350")
    self.windowViewFile.title("View File")
    self.LabelViewFile = Label(self.windowViewFile,text= "           Input ID Note to view: ",bg = 'dark sea green')
    self.LabelViewFile.grid(column=2,row =2,columnspan=2)
    self.IDNoteToView = StringVar()
    self.EntryViewFile= Entry(self.windowViewFile,textvariable= self.IDNoteToView,width=40)
    self.EntryViewFile.grid(column=5,row=2,columnspan=15)

    self.buttonView = Button(self.windowViewFile,text= "View",command= self.showFile)
    self.buttonView.grid(column=21,row=2)
    
    
    
  def ChooseDownloadFile(self):
    self.client.send("Download File".encode(FORMAT))
    self.windowDownloadFile = Toplevel(self.FrameViewNote,bg='dark sea green')
    self.windowDownloadFile.geometry("500x350")
    self.windowDownloadFile.title("Download File")
    self.LabelDownloadFile = Label(self.windowDownloadFile,text= "           Input ID Note to Download: ",bg = 'dark sea green')
    self.LabelDownloadFile.grid(column=2,row =2,columnspan=2)
    self.IDNoteToDownload = StringVar()
    self.EntryDownloadFile= Entry(self.windowDownloadFile,textvariable= self.IDNoteToDownload,width=40)
    self.EntryDownloadFile.grid(column=5,row=2,columnspan=15)

    self.buttonToDownload = Button(self.windowDownloadFile,text= "Download",command= self.DownloadFunction)
    self.buttonToDownload.grid(column=20,row=20)
    
    
  def DownloadFunction(self):
    self.IdDownload = self.IDNoteToDownload.get()
    self.client.send(self.IdDownload.encode(FORMAT))
    
    self.filenameDownload = self.client.recv(1024*10).decode(FORMAT)
    self.client.send("receive".encode(FORMAT))
    print(self.filenameDownload)
    self.windowDownloadFile.destroy()
    self.receiveSize(self.filenameDownload)
    print("Done Download")
    
  def receiveListNote(self):
      data = self.client.recv(1024).decode(FORMAT)
      self.client.send("receive".encode(FORMAT))
      print (data)
      if data == "No data":
        messagebox.showerror("Error","No data")
        
        self.frameStartWindowNote.tkraise()
        return False
      else:
        self.columns = ('ID', 'NameFile', 'Type', 'Content')
        tree = ttk.Treeview(self.FrameViewNote, columns= self.columns)
        tree.heading('ID', text= 'ID')
        tree.heading('NameFile', text= 'NameFile')
        tree.heading('Type', text= 'Type')
        tree.heading('Content', text= 'Content')
        tree.column("#0",stretch=NO, minwidth=15,width=0)
        tree.column("#1",stretch=NO, minwidth=15,width=200)
        tree.column("#2",stretch=NO, minwidth=15,width=200)
        tree.column("#3",stretch=NO, minwidth=25,width=100)
        tree.column("#4",stretch=NO, minwidth=25,width=400)

        tree.grid(row = 1, column= 1, sticky= tk.NSEW, columnspan=30, rowspan=15)
    
        yscrollbar = ttk.Scrollbar(self.FrameViewNote, orient= tk.VERTICAL, command= tree.yview)

        yscrollbar.grid(row = 1, column= 31, sticky='ns', rowspan=16)
      
        StoreList = []
        
        size = int(data)
        
        
        for i in range(size):
          ID = self.client.recv(1024*10).decode(FORMAT)
          self.client.send("receive".encode(FORMAT))
          text = ""
          text = text+ ID +"\t\t"
          NameFile = self.client.recv(1024*10).decode(FORMAT)
          self.client.send("receive".encode(FORMAT))
          text = text+ NameFile +"\t\t\t"
          Type = self.client.recv(1024*10).decode(FORMAT)
          self.client.send("receive".encode(FORMAT))
          text = text+ Type +"\t\t"
          Content = self.client.recv(1024*10).decode(FORMAT)
          self.client.send("receive".encode(FORMAT))
          text = text+ Content +"\n"
          StoreList.append((ID, NameFile, Type, Content))
          print(ID)
        for item in StoreList:
          tree.insert('', tk.END, values= item)
      
        return tree
      
  def showFile(self):
    
    self.Id = self.IDNoteToView.get()
    self.client.send(self.Id.encode(FORMAT))
    self.filenameView = self.client.recv(1024*10).decode(FORMAT)
    self.client.send("receive".encode(FORMAT))
    self.windowViewFile.destroy()
    self.receiveSize(self.filenameView)
   
    subprocess.run(self.filepath, shell= True)
    os.remove(self.filepath)
    print ("Done View")

  def des_Img(self):
    cmd = "del/Q " + self.filepath
    subprocess.run(cmd, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    self.WindowviewImage.destroy()

    
  def saveFileNote(self,filename ):
    with open(filename, 'wb') as f: 
      print('Start saving')
      time = 0
      
      if self.size%(1024*10) !=0:
        time = int (self.size/(1024*10)) +1
      else:
        time = int (self.size/(1024*10))
      
      count = 0
      
      while count < time: 
        data = self.client.recv(1024*10)
        print(data)
        f.write(data)

        count += 1
    print("Done Sending")
    self.filepath = os.path.abspath(filename)
    print(os.path.abspath(filename))
    f.close()
    
    
  def receiveSize(self,filename):
    self.size = self.client.recv(1024*10).decode(FORMAT)
    self.size = int(self.size)
    print(self.size)
    self.client.send("receive".encode(FORMAT))
    self.saveFileNote(filename)
 
        

if __name__ == '__main__':   
       

  c = Client()
  c.WindowLogin()
    
  
