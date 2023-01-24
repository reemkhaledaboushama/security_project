import os.path
import customtkinter as ctk
from ftplib import FTP
from customtkinter import filedialog
from Crypto.Cipher import AES, DES, DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
CHUNK_SIZE = 16
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
    with FTP() as ftp:
        ftp.connect(host=host, port=port)
        ftp.login(user, password)
        with open(val, "wb") as file:

            ftp.retrbinary(f"RETR {val}", file.write)
        ftp.quit()
        
    file_in = open(val, "rb")
    ciphertext = file_in.read()

    masterkey_file_out=open("master_key.txt","rb")
    master_key=masterkey_file_out.read()
    cipher = AES.new(master_key, AES.MODE_ECB)

    file_out = open("keys.txt", "rb")
    cipherkey=file_out.read()
    plainkey = cipher.decrypt(cipherkey)
    file_out.close()

    file_in = open("keys.txt", "wb")
    file_in.write(plainkey)
    file_in.close()

    keys_file_in=open("keys.txt","rb")
    global AES_key_internal
    global DES3_key_internal
    global DES_key_internal
    AES_key_internal=keys_file_in.read(16)
    DES3_key_internal=keys_file_in.read(16)
    DES_key_internal=keys_file_in.read(8)
    keys_file_in.close()
    
    file_number=0
    file_out = open(val, "rb")
    with open("decrypt_"+val, "wb") as file_in :
        while True:
            cipher_text_chunck=file_out.read(CHUNK_SIZE)
            if len(cipher_text_chunck) == 0:
                break
            elif len(cipher_text_chunck) % 16 !=0:
                cipher_text_chunck += ' ' * (16 - len(cipher_text_chunck) % 16)
            
            plaintext_chunk = round_robin_decrypt(cipher_text_chunck, file_number)
            #print("upload")
            
            file_in.write(plaintext_chunk) 
            #ciphertext +=ciphertext_chunk
            #print(file_number)
            file_number += 1
            #plain_text_chunck = fileobj.read(CHUNK_SIZE)    
            
        file_out.close()
    
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
        #ftp.cwd("/uploaded")
        fileitems = ftp.nlst()

    combobox = ctk.CTkOptionMenu(master=frame, values=fileitems)
    combobox.pack(padx=20, pady=10)
    selected=combobox.get()
    download_button = ctk.CTkButton(master=frame, text="Download", command=lambda: download(selected))
    download_button.pack(pady=12, padx=10)
    home_button = ctk.CTkButton(master=frame, text="Home", command=lambda: chooseGUI())
    home_button.pack(pady=12, padx=10)

    root.mainloop()

def create_keys():
    global AES_key
    global DES_key
    global DES3_key
    AES_key = get_random_bytes(16)
    DES3_key = get_random_bytes(16)
    DES_key = get_random_bytes(8)
    
    file_out = open("keys.txt", "wb")
    file_out.write(AES_key)
    file_out.write(DES3_key)
    file_out.write(DES_key)
    file_out.write(b'        ')
    file_out.close()

def encrypt_AES(msg):
    #fileobj=open(filepath, "rb")
    
    cipher = AES.new(AES_key, AES.MODE_ECB)
    print("plaintext")
    print(msg)
    ciphertext = cipher.encrypt(msg.encode("utf-8"))
    print("ciphertext")
    print(ciphertext)
    
    return ciphertext


def decrypt_AES(ciphertext):
    
    print(ciphertext)
    print(ciphertext)
    cipher = AES.new(AES_key_internal, AES.MODE_ECB)
    
    data = cipher.decrypt(ciphertext)
    print("plaintext")
    print(data)

    return data

def upload():
    
    with FTP() as ftp:
        ftp.connect(host=host, port=port)
        ftp.login(user, password)
        filepath = filedialog.askopenfilename(initialdir="C:\\Users\\olaal\\OneDrive\\Documents\\Sem 9\\Networks Security\\Project") #u can change this to your own default directory or remove it at all
        filename=os.path.basename(filepath)
        create_keys()

        file_number = 0
        
        ciphertext= b''
        
        filename=os.path.basename(filepath)
        file_out = open("encrypted_"+filename, "wb")
        with open(filepath, "r") as fileobj :
            while True:
                plain_text_chunck=fileobj.read(CHUNK_SIZE)
                if len(plain_text_chunck) == 0:
                    break
                elif len(plain_text_chunck) % 16 !=0:
                    plain_text_chunck += ' ' * (16 - len(plain_text_chunck) % 16)
                
                ciphertext_chunk = round_robin_encrypt(plain_text_chunck, file_number)
                file_out.write(ciphertext_chunk) 
                file_number += 1  
                
        file_out.close()

        masterkey_file_in=open("master_key.txt","wb")
        master_key=get_random_bytes(16)
        masterkey_file_in.write(master_key)
        masterkey_file_in.close()
        cipher = AES.new(master_key, AES.MODE_ECB)
        
        file_out = open("keys.txt", "rb")
        plaintext=file_out.read()
        ciphertext = cipher.encrypt(plaintext)
        file_out.close()

        file_in = open("keys.txt", "wb")
        file_in.write(ciphertext)
        file_in.close()
        
        fileobj=open("keys.txt", "rb")
        ftp.storbinary("STOR " + "keys.txt", fileobj)
        fileobj.close()
        fileobj=open("encrypted_"+filename, "rb")
        ftp.storbinary("STOR " + "encrypted_"+filename, fileobj)
        fileobj.close()

        uploadeditems()
        ftp.quit()
       
    root.mainloop()

def round_robin_encrypt(plain_text_chunck, file_number):
    if file_number%3 == 0:
        return encrypt_AES(plain_text_chunck)
    elif file_number%3 == 1:
        return encrypt_DES3(plain_text_chunck)
    elif file_number%3 == 2:
        return encrypt_DES(plain_text_chunck)

def round_robin_decrypt(cipher_text_chunck, file_number):
    if file_number%3 == 0:
        return decrypt_AES(cipher_text_chunck)
    elif file_number%3 == 1:
        return decrypt_DES3(cipher_text_chunck)
    elif file_number%3 == 2:
        return decrypt_DES(cipher_text_chunck)

def fileuploadGUI():
   upload()

def accessFTP():
    ftp=FTP()
    global user
    user = username_entry.get()
    global password
    password = password_entry.get()
    ftp.connect(host=host, port=port)
    ftp.login(user=user, passwd=password)
    login_response = ftp.login(user, password)
    chooseGUI()
    return user, password


def encrypt_DES(msg):
    cipher = DES.new(DES_key, DES.MODE_ECB)
    ciphertext= cipher.encrypt(msg.encode('ascii'))
    return ciphertext

def decrypt_DES(ciphertext):
    cipher = DES.new(DES_key_internal, DES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext


def encrypt_DES3(msg):
    cipher = DES3.new(DES3_key, DES3.MODE_ECB)
    ciphertext= cipher.encrypt(msg.encode('ascii'))
    return ciphertext

def decrypt_DES3(ciphertext):
    cipher = DES3.new(DES3_key_internal, DES3.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext
    
login_button = ctk.CTkButton(master=frame, text="Join ftp server", command=accessFTP)
login_button.pack(pady=12, padx=10)

root.mainloop()
