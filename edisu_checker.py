import requests
import hashlib
import os
import sched
import time
import re
from winotify import Notification
import winsound
from bs4 import BeautifulSoup



"""
EDISU News Page Controller – Background Script

- Checks EDISU news page at regular intervals
- Detects changes using SHA-256 hashes
- Sends Windows toast notifications via winotify
- Plays a system sound on change
- Logs every check
- Designed to run in background using pythonw + .bat in Startup
"""

CHECK_INTERVAL=3600 #interval between each check in seconds
URL = "https://www.edisu.piemonte.it/en/news"

#Creates the paths for hash file and log file next to the python file. Otherwise, the bat file will create these files in the Startup file.
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
HASH_FILE = os.path.join(BASE_DIR, "edisu_hash.txt") 
LOG_FILE = os.path.join(BASE_DIR, "edisu.log")
CONTENT_FILE=os.path.join(BASE_DIR, "news.txt")

HEADERS = {
    "User-Agent": "EDISU-Checker/1.0"
}

#Turns web page into a hash
def get_page_hash():
    r = requests.get(URL,headers=HEADERS, timeout=10)
    r.raise_for_status()
    return hashlib.sha256(normalize_text(extract_news_section(r.text)).encode("utf-8")).hexdigest()


#Checks the internet connection of pc via trying to connect google.com
def check_connection(timeout=3):
    try:
        r = requests.head("https://www.google.com", timeout=timeout)
        return r.status_code < 500
    except requests.RequestException:
        return False

#To get rid of date, time, and extra spaces in the website 
def normalize_text(text):
    text = text.lower()
    text = re.sub(r"\d{1,2}/\d{1,2}/\d{2,4}", "", text)
    text = re.sub(r"\d{1,2}:\d{2}", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

#To get only the spesific content for comparison
def extract_news_section(html):
    soup = BeautifulSoup(html, "html.parser")

    #spesific div for news section
    news_div = soup.find("div", class_="view-content")
    if not news_div:
        return ""
    
    return news_div.get_text(separator=" ", strip=True)

#Old version with only prints instead of toast notifications
#def edisu_check():
#   if check_connection():
#       new_hash = get_page_hash()
#    
#       if os.path.exists(HASH_FILE):
#           with open(HASH_FILE, "r") as f:
#               old_hash = f.read().strip()
#
#           if new_hash != old_hash:
#               print("⚠️ EDISU page changed!")
#               print('\007', end="")
#           else:
#               print("✓ No change.")
#       else:
#           print("First run — hash saved.")
#   
#       with open(HASH_FILE, "w") as f:
#           f.write(new_hash)
#   else:
#       print("No internet connection, the check skipped")

#Alerting user when there is a change in Edisu page using winotify
def alert_user(text):
    winsound.MessageBeep()

    toast = Notification(
        app_id="EDISU Checker",
        title="EDISU Uyarı",
        msg=text,
        duration="short"
    )

    toast.add_actions(
        "Siteyi Aç",
        "https://www.edisu.piemonte.it/en/news"
    )

    toast.show()

#Logging each check into a log file
def info(msg):
    print(msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{time.ctime()} | {msg}\n")

#main function that checks the website
def check_site(sc):
    if check_connection():
        try:
            new_hash = get_page_hash()

            if os.path.exists(HASH_FILE):
                with open(HASH_FILE, "r") as f:
                    old_hash = f.read().strip()

                if new_hash != old_hash:
                    alert_user("Change in news page!")
                    info(f"Change, new_hash: {new_hash}")

                    with open(HASH_FILE, "w") as f:
                        f.write(new_hash)

                else:
                    info("No change detected")
            else:
                info(f"First run — hash saved. Hash: {new_hash}")
                with open(HASH_FILE, "w") as f:
                    f.write(new_hash)

        except Exception as e:
            alert_user(f"Error: {e}")
            info(f"Error: {e}")
        
    else:
        info("No internet connection, the check skipped")

    # ⏱️ Plans the next check using sched
    sc.enter(CHECK_INTERVAL, 1, check_site, (sc,))

# =========================
# START OF PROGRAM 
# =========================
if __name__ == "__main__":
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(0, 1, check_site, (scheduler,))
    scheduler.run()

    
