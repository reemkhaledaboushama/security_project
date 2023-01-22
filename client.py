import os.path
import customtkinter as ctk
from ftplib import FTP
from customtkinter import filedialog
from Crypto.Cipher import AES, DES, DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Login")
root.geometry("500x500")
global frame
frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)
label= ctk.CTkLabel(master=frame, text="Login to FTP")
label.pack(pady=12, padx=10)

username_entry = ctk.CTkEntry(master=frame, placeholder_text="Enter Username")
username_entry.pack(pady=12, padx=10)

password_entry = ctk.CTkEntry(master=frame, placeholder_text="Enter Password", show="*")
password_entry.pack(pady=12, padx=10)

user = ""
password = ""

host = "127.0.0.1"
port = 6060

def uploadeditems():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root.title("Uploaded items")
    root.geometry("500x500")
    global frame
    frame.destroy()
    frame = ctk.CTkFrame(master=root)
    frame.place(height=250, width=500)
    frame.pack(pady=20, padx=60, fill="both", expand=True)
    label3 = ctk.CTkLabel(master=frame, text="Uploaded files")
    label3.pack(pady=12, padx=10)
    home_button = ctk.CTkButton(master=frame, text="Home", command=lambda: chooseGUI())
    home_button.pack(pady=12, padx=10)
    
    with FTP() as ftp:
        ftp.connect(host=host, port=port)
        ftp.login(user, password)
        fileitems = ftp.nlst()
        for i in fileitems:
            print(i)
            itemlabel = ctk.CTkLabel(master=frame, text=i, width=480, height=30, corner_radius=10, fg_color="#1f538d")
            itemlabel.place(relx=0.5, rely=0.5, anchor=ctk.W)
            itemlabel.pack(pady=5, padx=10)

    root.mainloop()

def chooseGUI():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    #root = ctk.CTk()
    root.title("Upload or Download")
    root.geometry("500x500")
    global frame
    frame.destroy()
    frame = ctk.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)
    label = ctk.CTkLabel(master=frame, text="upload or download")
    label.pack(pady=12, padx=10)
    download_button = ctk.CTkButton(master=frame, text="Download", command=lambda: filedownloadGUI())
    download_button.pack(pady=12, padx=10)
    upload_button = ctk.CTkButton(master=frame, text="Upload", command=lambda: fileuploadGUI())
    upload_button.pack(pady=12, padx=10)
    root.mainloop()

def download(combox):
    val = combox
    print(val)
    with FTP() as ftp:
        ftp.connect(host=host, port=port)
        ftp.login(user, password)
        with open(val, "wb") as file:

            ftp.retrbinary(f"RETR {val}", file.write)
            # quit and close the connection
        ftp.quit()
    decrypt_DES(val)



def filedownloadGUI():
    
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root.title("Download items")
    root.geometry("500x500")
    global frame
    frame.destroy()
    frame = ctk.CTkFrame(master=root)

    label4 = ctk.CTkLabel(master=frame, text="Download")
    frame.place(height=250, width=500)
    frame.pack(pady=20, padx=60, fill="both", expand=True)
    label4.pack(pady=12, padx=10)

    with FTP() as ftp:
        ftp.connect(host=host, port=port)
        ftp.login(user, password)
        fileitems = ftp.nlst()

    combobox = ctk.CTkOptionMenu(master=frame, values=fileitems)
    combobox.pack(padx=20, pady=10)
    selected=combobox.get()
    download_button = ctk.CTkButton(master=frame, text="Download", command=lambda: download(selected))
    download_button.pack(pady=12, padx=10)

    home_button = ctk.CTkButton(master=frame, text="Home", command=lambda: chooseGUI())
    home_button.pack(pady=12, padx=10)

    root.mainloop()

AES_key = get_random_bytes(0)
DES_key = get_random_bytes(0)
DES_key = get_random_bytes(0)

def create_keys():
    global AES_key
    global DES_key
    global DES3_key
    AES_key = get_random_bytes(16)
    DES_key = get_random_bytes(8)
    DES3_key = get_random_bytes(16)
    file_out = open("keys.txt", "wb")
    str="\n"
    file_out.write(AES_key)
    file_out.write(str.encode("utf-8"))
    file_out.write(DES_key)
    file_out.write(str.encode("utf-8"))
    file_out.write(DES3_key)
    file_out.close()


def encrypt_AES(filepath):
    #data = b'secret data'
    fileobj=open(filepath, "rb")
    global AES_key
    cipher = AES.new(AES_key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(fileobj.read())

    filename=os.path.basename(filepath)
    file_out = open("encrypted_"+filename, "wb")
    [ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
    file_out.close()

def encrypt_DES(filepath):
    #data = b'secret data'
    fileobj=open(filepath, "rb")
    
    global DES_key

    plain_text=fileobj.read()
    cipher = DES.new(DES_key, DES.MODE_EAX)
    ciphertext = cipher.encrypt(pad(plain_text, 8))

    filename=os.path.basename(filepath)
    file_out = open("encrypted_"+filename, "wb")
    
    file_out.write(ciphertext)
    file_out.close()

def encrypt_DES3(filepath):
    #data = b'secret data'
    fileobj=open(filepath, "rb")

    global DES3_key
    cipher = DES3.new(DES3_key, DES3.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(fileobj.read())

    filename=os.path.basename(filepath)
    file_out = open("encrypted_"+filename, "wb")
    [ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
    file_out.close()

def decrypt_AES(filename):
    file_in = open(filename, "rb")
    nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]

    cipher = AES.new(AES_key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    file_out = open("decrypt_"+filename, "w")
    file_out.write(data.decode("utf-8"))
    file_out.close()

def decrypt_DES(filename):
    file_in = open(filename, "rb")
    nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]
    #ciphertext=file_in.read()

    cipher = DES.new(DES_key, DES.MODE_EAX)
    data = cipher.decrypt(ciphertext)
    file_out = open("decrypt_"+filename, "w")
    str=unpad(data, 8)
    file_out.write(str.decode("utf-8"))
    file_out.close()

def decrypt_DES3(filename):
    file_in = open(filename, "rb")
    nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]

    cipher = DES3.new(DES3_key, DES3.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    file_out = open("decrypt_"+filename, "w")
    file_out.write(data)
    file_out.close()

def upload():
    
    with FTP() as ftp:
        ftp.connect(host=host, port=port)
        ftp.login(user, password)

        filepath = filedialog.askopenfilename() #u can change this to your own default directory or remove it at all
        filename=os.path.basename(filepath)
        create_keys()
        encrypt_DES(filepath)
      
        fileobj=open("encrypted_"+filename, "rb")
        ftp.storbinary("STOR " + "encrypted_"+filename, fileobj)

        fileobj=open("keys.txt", "rb")
        ftp.storbinary("STOR " + "keys.txt", fileobj)

        uploadeditems()
        ftp.quit()
       
    
    
    root.mainloop()




def fileuploadGUI():
   upload()



def accessFTP():
    #with FTP(host=host) as ftp:
    ftp=FTP()
    global user
    user = username_entry.get()
    global password
    password = password_entry.get()
    ftp.connect(host=host, port=port)
    ftp.login(user=user, passwd=password)
    login_response = ftp.login(user, password)
    print(login_response)
    print(ftp.getwelcome())
    print(username_entry.get())
    

    chooseGUI()

    return user, password





login_button = ctk.CTkButton(master=frame, text="Join ftp server", command=accessFTP)
login_button.pack(pady=12, padx=10)


root.mainloop()
