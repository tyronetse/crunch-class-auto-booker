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

Verify your installation:

```bash
python3 --version
```

---

### 2. Install Google Chrome

Make sure Chrome is installed on your system:  
[https://www.google.com/chrome/](https://www.google.com/chrome/)

Install **ChromeDriver** (must match your Chrome version):

#### On macOS (with Homebrew):

```bash
brew install chromedriver
```

#### Or download manually:

[https://sites.google.com/a/chromium.org/chromedriver/downloads](https://sites.google.com/a/chromium.org/chromedriver/downloads)

---

### 3. Install Python Dependencies

In the folder where your script is saved, run:

```bash
pip install -r requirements.txt
```

This installs Selenium, which automates the browser.

---

### ✅ `requirements.txt` (should be in the same folder)

```
selenium
```

---

## 🔐 Edit `credentials.json`

A sample `credentials.json` file is included. Open it and **edit it with your Crunch login details**:

```json
{
  "username": "your@email.com",
  "password": "YourPassword"
}
```

> ⚠️ Never share this file publicly.

---

## 📅 Edit `classes.json`

A sample `classes.json` file is also included. Edit it to list the classes you want to book:

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

- `name`: Must exactly match the class name shown on Crunch
- `time`: Class start time (e.g., `"5:30 pm"`)
- `day`: Day of the week the class occurs (e.g., `"Wednesday"`)

---

## 🏃‍♂️ Run the Script

Use the following command:

```bash
python book_crunch_classes.py
```

You’ll see logs like:

```
📅 Class to book: BuildHIIT(HIITZone) at 6:00 pm on Tuesday
⏳ Booking will happen at Monday 08:00 PM
🚀 Launching browser...
🔐 Logging in...
🎉 Class reserved successfully!
```

---

## ⛔ Stop the Script

Press `Ctrl + C` in the terminal to stop it manually.

---

## 🛠 Troubleshooting

- **Login timed out**: Double-check `credentials.json` and your internet.
- **Class not found**: The class name or time might not match what Crunch displays.
- **Chromedriver version mismatch**: Make sure ChromeDriver matches your installed Chrome browser version.
