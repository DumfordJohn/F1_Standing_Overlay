import requests
from bs4 import BeautifulSoup
import time

url = "https://mcsocko.com/f1standings"
driver_name = "naudu"


def update_overlay():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find_all("tr")
    found = False
    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 4:
            continue

        driver = cells[2].get_text(strip=True)
        if driver_name in driver.lower():
            position = cells[0].get_text(strip=True)
            team = cells[1].get_text(strip=True)
            avgPlace = cells[3].get_text(strip=True)

            with open("overlay.txt", "w", encoding="utf-8") as f:
                f.write(f"Team: {team}\n")
                f.write(f"Drivers: {driver}\n")
                f.write(f"Position: {position}\n")
                f.write(f"Average Place: {avgPlace}\n")

            print(f"Found: {driver} ({team} | P{position} | {avgPlace})")
            found = True
            break
    if not found:
        print("Naudu not found in any driver name")

while True:
    update_overlay()
    time.sleep(300)
