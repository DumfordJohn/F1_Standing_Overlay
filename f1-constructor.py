import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
import threading
import time
import os

search_name = ""
stop_event = threading.Event()

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
                team = cells[1].get_text(strip=True)
                avgPlace = cells[3].get_text(strip=True)
                safe_path = os.path.join(os.path.expanduser("~"), "Documents", "overlay.txt")

                with open(safe_path, "w", encoding="utf-8") as f:
                    f.write(f"Team: {team}\n")
                    f.write(f"Drivers: {driver}\n")
                    f.write(f"Position: {position}\n")
                    f.write(f"Average place: {avgPlace}\n")

                result_label.config(
                    text=f"Found: {driver}\nTeam: {team} | Position: {position} | Average place: {avgPlace}"
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
result_label = tk.Label(root, text="", font=("Segoe UI", 10), wraplength=400, justify="left")
result_label.pack(pady=10)

tk.Label(root, text="Auto-updates every 5 minutes", font=("Segoe UI", 9), fg="gray").pack(pady=5)

tk.Button(root, text="Quit", font=("Segoe UI", 11), fg="white", bg="red", command=on_quit).pack(pady=10)

root.protocol("WM_DELETE_WINDOW", on_quit)
root.bind("<Return>", lambda event: start_search())

root.mainloop()