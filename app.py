from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
from prediction_model import train_and_plot
from data_to_bd import data_migrator

ctk.set_appearance_mode("dark")

def predict_weather():
    try:
        year = int(year_entry.get())
        parameter = combobox.get()
    except ValueError:
        messagebox.showerror("ПОМИЛКА", "Будь ласка, введіть ціле число")
        return

    train_and_plot(year, parameter)

root = root = ctk.CTk()
root.title("Прогноз погоди")
root.geometry("400x400")
root.resizable(False, False)

year_entry = ctk.CTkEntry(root, placeholder_text='Введіть рік', border_color="#3B8ED0")
year_entry.pack(pady=(40, 10))

combobox = ctk.CTkComboBox(root, values=["temperature", "precipitation", "wind_gust", "pressure"])
combobox.pack(pady=(0, 10))

button = ctk.CTkButton(root, text="Передбачити", command=predict_weather)
button.pack(pady=(0, 20))

db_button = ctk.CTkButton(root, text="Оновити базу даних", command=data_migrator, fg_color="#117A65")
db_button.pack()

root.mainloop()