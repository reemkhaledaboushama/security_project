import customtkinter as ctk


def initGUI():
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

    root.mainloop()


initGUI()