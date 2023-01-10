import os.path

import customtkinter as ctk
from ftplib import FTP
from customtkinter import filedialog

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.geometry("500x500")
frame1 = ctk.CTkFrame(master=root)
frame1.pack(pady=20, padx=60, fill="both", expand=True)
label= ctk.CTkLabel(master=frame1, text="Login to FTP")
label.pack(pady=12, padx=10)

username_entry = ctk.CTkEntry(master=frame1, placeholder_text="Enter Username")
username_entry.pack(pady=12, padx=10)

password_entry = ctk.CTkEntry(master=frame1, placeholder_text="Enter Password", show="*")
password_entry.pack(pady=12, padx=10)





host = "127.0.0.1"
port = 6060







def upload():
    with FTP(host) as ftp:
        ftp.connect(host=host, port=port)
        ftp.login(user=username_entry.get(), passwd=password_entry.get())

        file = filedialog.askopenfilename(initialdir="D:\\semester9\\security_project\\security_project")
        fileobj=open(file, "rb")

        filename = os.path.basename(file)
        ftp.storbinary("STOR " + filename, fileobj)

        ftp.quit()




def fileuploadGUI():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    root.geometry("500x500")
    frame2 = ctk.CTkFrame(master=root)
    frame2.pack(pady=20, padx=60, fill="both", expand=True)
    label = ctk.CTkLabel(master=frame2, text="Secure Upload")
    label.pack(pady=12, padx=10)

    # select file btn
    #select_button = ctk.CTkButton(master=frame2, text="Select File", command= selectfile)
    #select_button.pack(pady=12, padx=10)


    #upload file btn
    secureupld_button = ctk.CTkButton(master=frame2, text="Secure Upload", command= upload)
    secureupld_button.pack(pady=12, padx=10)

    root.mainloop()



def accessFTP():
    with FTP(host) as ftp:
        user = username_entry.get()
        password = password_entry.get()
        ftp.connect(host=host, port=port)
        ftp.login(user=user, passwd=password)
        login_response = ftp.login(user, password)
        print(login_response)
        print(ftp.getwelcome())
        print(username_entry.get())

        fileuploadGUI()

        return user, password





login_button = ctk.CTkButton(master=frame1, text="Join ftp server", command=accessFTP)
login_button.pack(pady=12, padx=10)


root.mainloop()
