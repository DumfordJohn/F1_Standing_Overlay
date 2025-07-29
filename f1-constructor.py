import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
import threading
import time
import os

search_name = ""
stop_event = threading.Event()

def ordinal(n):
    n = int(n)
    if 10 <= n % 100 <=20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

def update_overlay():
    global search_name
    if not search_name:
        return

    try:
        url = "https://mcsocko.com/f1standings"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find_all("tr")

        found = False
        for row in rows:
            cells = row.find_all("td")
            if len(cells) < 4:
                continue


            driver = cells[2].get_text(strip=True)
            if search_name in driver.lower():
                position = cells[0].get_text(strip=True)
                position_with_suffix = ordinal(position)
                team = cells[1].get_text(strip=True)
                avgPlace = cells[3].get_text(strip=True)

                context = {
                    "team": team,
                    "driver": driver,
                    "position": position_with_suffix,
                    "avgPlace": avgPlace
                }

                raw_template = layout_text.get("1.0", tk.END).strip()

                if not show_team.get():
                    raw_template = raw_template.replace("{team}", "")
                if not show_driver.get():
                    raw_template = raw_template.replace("{driver}", "")
                if not show_position.get():
                    raw_template = raw_template.replace("{position}", "")
                if not show_avgPlace.get():
                    raw_template = raw_template.replace("{avgPlace}", "")

                output = raw_template.format(**context)

                output_path = "overlay.txt"

                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(output.strip())

                result_label.config(
                    text=f"Found: {driver}\nSaved to: {output_path}"
                )
                found = True
                break

        if not found:
            result_label.config(text=f"'{search_name}' not found")
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")

def start_search():
    global search_name
    input_name = entry.get().strip().lower()
    if not input_name:
        messagebox.showwarning("Input Error", "Please enter a name to search for.")
        return

    search_name = input_name
    update_overlay()

def auto_update_loop():
    while not stop_event.is_set():
        time.sleep(300)
        update_overlay()

def on_quit():
    stop_event.set()
    root.destroy()

threading.Thread(target=auto_update_loop, daemon=True).start()

root = tk.Tk()
root.title("F1 Standing Overlay")
root.geometry("400x300")
root.resizable(False, False)

tk.Label(root, text="Enter name to search for:", font=("Segoe UI", 12)).pack(pady=10)
entry = tk.Entry(root, font=("Segoe UI", 12), width=30)
entry.pack(pady=5)

tk.Button(root, text="Search", font=("Segoe UI", 10), command=start_search).pack(pady=10)

tk.Label(root, text="Select fields to include:", font=("Segoe UI", 11)).pack(pady=4)
show_team = tk.BooleanVar(value=True)
show_driver = tk.BooleanVar(value=True)
show_position = tk.BooleanVar(value=True)
show_avgPlace = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Team", variable=show_team, font=("Segoe UI", 10)).pack(anchor='w', padx=40)
tk.Checkbutton(root, text="Driver", variable=show_driver, font=("Segoe UI", 10)).pack(anchor='w', padx=40)
tk.Checkbutton(root, text="Position", variable=show_position, font=("Segoe UI", 10)).pack(anchor='w', padx=40)
tk.Checkbutton(root, text="Average Place", variable=show_avgPlace, font=("Segoe UI", 10)).pack(anchor='w', padx=40)

layout_text = tk.Text(root, height=4, width=50, font=("Segoe UI", 10))
layout_text.insert("1.0", "{team} | {driver} | {position} | {avgPlace}")
layout_text.pack()

result_label = tk.Label(root, text="", font=("Segoe UI", 10), wraplength=400, justify="left")
result_label.pack(pady=10)

tk.Label(root, text="Auto-updates every 5 minutes", font=("Segoe UI", 9), fg="gray").pack(pady=5)

tk.Button(root, text="Quit", font=("Segoe UI", 11), fg="white", bg="red", command=on_quit).pack(pady=10)

root.protocol("WM_DELETE_WINDOW", on_quit)
root.bind("<Return>", lambda event: start_search())

root.mainloop()