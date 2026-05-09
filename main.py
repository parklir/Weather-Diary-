import json
import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox

DATA_FILE = "weather_diary.json"

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=4)

def update_table():
    for row in table.get_children():
        table.delete(row)
    for record in records:
        table.insert("", tk.END, values=(
            record["date"],
            record["temp"],
            record["desc"],
            "Да" if record["rain"] else "Нет"
        ))

def add_record():
    date = entry_date.get().strip()
    temp = entry_temp.get().strip()
    desc = entry_desc.get().strip()
    rain = var_rain.get()

    if not date or not temp or not desc:
        messagebox.showwarning("Ошибка", "Заполните все поля")
        return

    # Проверка формата даты: ДД-ММ-ГГГГ
    try:
        datetime.strptime(date, "%d-%m-%Y")
    except ValueError:
        messagebox.showwarning("Ошибка", "Неверный формат даты. Используйте ДД-ММ-ГГГГ")
        return

    try:
        temp_val = float(temp)
    except ValueError:
        messagebox.showwarning("Ошибка", "Температура должна быть числом")
        return

    records.append({"date": date, "temp": temp_val, "desc": desc, "rain": rain})
    save_data()
    update_table()

    entry_date.delete(0, tk.END)
    entry_temp.delete(0, tk.END)
    entry_desc.delete(0, tk.END)
    var_rain.set(False)

def filter_by_date():
    date_filter = entry_filter_date.get().strip()
    if not date_filter:
        update_table()
        return

    # Проверка формата даты фильтра: ДД-ММ-ГГГГ
    try:
        datetime.strptime(date_filter, "%d-%m-%Y")
    except ValueError:
        messagebox.showwarning("Ошибка", "Неверный формат даты. Используйте ДД-ММ-ГГГГ")
        return

    for row in table.get_children():
        table.delete(row)

    for record in records:
        if record["date"] == date_filter:
            table.insert("", tk.END, values=(
                record["date"], record["temp"], record["desc"], "Да" if record["rain"] else "Нет"
            ))

def filter_by_temp():
    try:
        min_temp = float(entry_filter_temp.get())
    except ValueError:
        messagebox.showwarning("Ошибка", "Введите число")
        return

    for row in table.get_children():
        table.delete(row)

    for record in records:
        if record["temp"] > min_temp:
            table.insert("", tk.END, values=(
                record["date"], record["temp"], record["desc"], "Да" if record["rain"] else "Нет"
            ))

def reset_filter():
    entry_filter_date.delete(0, tk.END)
    entry_filter_temp.delete(0, tk.END)
    update_table()

records = load_data()

window = tk.Tk()
window.title("Weather Diary (Дневник погоды)")
window.geometry("600x550")

# === Форма добавления записи ===
input_frame = tk.LabelFrame(window, text="Новая запись", padx=10, pady=10)
input_frame.pack(fill="x", padx=10, pady=5)

# Изменена подпись
tk.Label(input_frame, text="Дата (ДД-ММ-ГГГГ):").grid(row=0, column=0, sticky="w")
entry_date = tk.Entry(input_frame)
entry_date.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="Температура:").grid(row=1, column=0, sticky="w")
entry_temp = tk.Entry(input_frame)
entry_temp.grid(row=1, column=1, padx=5)

tk.Label(input_frame, text="Описание:").grid(row=2, column=0, sticky="w")
entry_desc = tk.Entry(input_frame, width=40)
entry_desc.grid(row=2, column=1, padx=5)

var_rain = tk.BooleanVar()
tk.Checkbutton(input_frame, text="Осадки", variable=var_rain).grid(row=3, column=1, sticky="w")

tk.Button(input_frame, text="Добавить запись", command=add_record, bg="green", fg="white").grid(row=4, column=1, pady=5)

# === Фильтры ===
filter_frame = tk.LabelFrame(window, text="Фильтрация", padx=10, pady=10)
filter_frame.pack(fill="x", padx=10, pady=5)

tk.Label(filter_frame, text="Фильтр по дате (точное совпадение):").grid(row=0, column=0, sticky="w")
entry_filter_date = tk.Entry(filter_frame)
entry_filter_date.grid(row=0, column=1, padx=5)
tk.Button(filter_frame, text="Применить", command=filter_by_date).grid(row=0, column=2, padx=5)

tk.Label(filter_frame, text="Температура выше (°C):").grid(row=1, column=0, sticky="w")
entry_filter_temp = tk.Entry(filter_frame)
entry_filter_temp.grid(row=1, column=1, padx=5)
tk.Button(filter_frame, text="Применить", command=filter_by_temp).grid(row=1, column=2, padx=5)

tk.Button(filter_frame, text="Сбросить фильтры", command=reset_filter).grid(row=2, column=1, pady=5)

# === Таблица с записями ===
table_frame = tk.LabelFrame(window, text="Записи о погоде", padx=10, pady=10)
table_frame.pack(fill="both", expand=True, padx=10, pady=5)

columns = ("date", "temp", "desc", "rain")
table = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
table.heading("date", text="Дата")
table.heading("temp", text="Температура")
table.heading("desc", text="Описание")
table.heading("rain", text="Осадки")
table.column("date", width=100)
table.column("temp", width=80)
table.column("desc", width=300)
table.column("rain", width=80)
table.pack(fill="both", expand=True)

update_table()
window.mainloop()