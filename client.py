import os.path

import customtkinter as ctk
from ftplib import FTP
from customtkinter import filedialog

def selectfile():
    filepath= filedialog.askopenfilename()
    filename= os.path.basename(filepath)

    print(filepath)
    print(filename)
    return filename
def fileuploadGUI():
    root = ctk.CTk()
    root.geometry("500x500")
    frame2 = ctk.CTkFrame(master=root)
    frame2.pack(pady=20, padx=60, fill="both", expand=True)
    label = ctk.CTkLabel(master=frame2, text="Secure Upload")
    label.pack(pady=12, padx=10)

    # select file btn
    select_button = ctk.CTkButton(master=frame2, text="Select File", command= selectfile)
    select_button.pack(pady=12, padx=10)


    #upload file btn
    secureupld_button = ctk.CTkButton(master=frame2, text="Secure Upload")
    secureupld_button.pack(pady=12, padx=10)


    root.mainloop()


def loginGUI():
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

    login_button = ctk.CTkButton(master=frame1, text="Join ftp server", command=fileuploadGUI)
    login_button.pack(pady=12, padx=10)

    root.mainloop()
    return username_entry, password_entry

username_entry , password_entry = loginGUI()




loginGUI()