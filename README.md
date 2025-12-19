# EDISU News Page Monitor

A background script that monitors the EDISU news page and notifies the user when changes occur. Runs once every hour after the first execution.

## 📌 Features

- Periodically checks the EDISU news page
- Detects content changes using SHA-256 hashing
- Filters out dynamic elements (dates, times, whitespace)
- Sends Windows toast notifications on changes
- Plays a system sound alert
- Logs all checks and events
- Designed to run silently in the background on Windows

## 🛠️ How It Works

1. Downloads the EDISU news page  
2. Extracts only the relevant news section  
3. Normalizes the content (removes dates, times, extra spaces)  
4. Generates a SHA-256 hash of the cleaned content  
5. Compares it with the previously saved hash  
6. Notifies the user if a change is detected  

## 📂 File Structure
```
.
├── edisu_checker.py
├── edisu_hash.txt # Stores last known page hash
├── edisu.log # Log file for checks and events
├── news.txt # Extracted text (debug purposes) 
└── start.bat # Optional startup launcher
```
> **Note:** Delete the relative code pieces for news.txt to avoid oversized news.txt file in normal use.
## 🚀 Usage

### Install dependencies
```
pip install requests winotify beautifulsoup4
```
### Run manually
```
python edisu_checker.py
```
### Run on startup (recommended)

1. Keep the project folder anywhere on your system.
2. Open the Startup folder (`Win + R` → `shell:startup`).
3. Create a shortcut to `edisu_checker_starter.bat` inside the Startup folder.

## ⚙️ Configuration

Edit these variables in the script:
```
CHECK_INTERVAL = 3600 # Time interval between each execution. Lower values may cause connection issues or be interpreted as bot traffic.
URL = "https://www.edisu.piemonte.it/en/news" # Change this URL to use the bot for other pages. May need additional changes in code.
```
## 🧠 Notes

- The script stores only hashes, not full page content
- Hash comparison is used to detect changes, not restore content
- `news.txt` is intended for debugging and diff purposes. Delete the related code pieces for long-term use.

## 📜 License

MIT License


