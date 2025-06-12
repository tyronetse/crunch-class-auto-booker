# Crunch Class Auto Booker

This Python script automatically books your classes on [https://members.crunch.com](https://members.crunch.com). It logs in 5 minutes before class booking opens (22 hours before class time) and clicks "Reserve" exactly on time.

---

## ✅ Features

- Logs in early and waits for booking to open
- Supports multiple classes listed in a JSON file
- Detects and handles booking errors automatically
- Runs continuously in the background until stopped

---

## 🚀 Getting Started

### 1. Install Python 3

Install Python 3.7 or higher from [https://www.python.org/downloads/](https://www.python.org/downloads/)

Verify installation:

```bash
python3 --version
```

---

### 2. Install Google Chrome

Make sure Chrome is installed:  
[https://www.google.com/chrome/](https://www.google.com/chrome/)

Install **ChromeDriver** (version must match your Chrome browser):

#### On macOS (with Homebrew):
```bash
brew install chromedriver
```

#### Or download manually:
[https://sites.google.com/a/chromium.org/chromedriver/downloads](https://sites.google.com/a/chromium.org/chromedriver/downloads)

---

### 3. Create and Activate a Virtual Environment

In the root project folder:

```bash
python3 -m venv venv
source venv/bin/activate
```

Then install all dependencies:

```bash
pip install -r requirements.txt
```

---

## 📄 `requirements.txt`

```
selenium
pytz
```

---

## 🔐 Edit `credentials.json`

```json
{
  "username": "your@email.com",
  "password": "YourPassword"
}
```

> ⚠️ Never commit or share this file publicly.

---

## 📅 Edit `classes.json`

```json
[
  {
    "name": "The Ride",
    "time": "6:15 pm",
    "day": "Monday"
  },
  {
    "name": "BuildHIIT(HIITZone)",
    "time": "6:00 pm",
    "day": "Tuesday"
  }
]
```

- `name`: Must match the Crunch class title exactly
- `time`: Use the same format shown on Crunch (e.g., `"5:30 pm"`)
- `day`: Day of the week (e.g., `"Wednesday"`)

---

## 🏃 Run the Script

With the virtual environment active:

```bash
python book_crunch_classes.py
```

Example output:

```
📅 Class to book: BuildHIIT(HIITZone) at 6:00 pm on Tuesday
⏳ Booking will happen at Monday 08:00 PM
🔐 Logging in...
🎉 Class reserved successfully!
```

---


---

### 🖥 Run with Shell Script (Recommended)

You can automate script startup using the provided shell script:

1. **Create the file** `run_crunch_booker.sh` in the root directory:

```bash
#!/bin/bash

# Activate virtual environment
source ~/venvs/selenium-env/bin/activate

# Run the booking script
python book_crunch_classes.py
```

2. **Make it executable**:

```bash
chmod +x run_crunch_booker.sh
```

3. **Run the script**:

```bash
./run_crunch_booker.sh
```

This will activate the Python environment and launch the booking script automatically.


## ⛔ Stop the Script

Use `Ctrl + C` in the terminal.

---

## 🛠 Troubleshooting

- **Login timed out**: Check `credentials.json` and internet
- **Class not found**: Double-check class name, time, and day
- **Chromedriver issues**: Ensure it matches your Chrome version
