import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.geometry("500x500")

frame1 = ctk.CTkFrame(master=root)
frame1.pack(pady=20, padx=60, fill="both", expand=True)
label= ctk.CTkLabel(master=frame1, text="Login to FTP")
label.pack(pady=12, padx=10)

root.mainloop()