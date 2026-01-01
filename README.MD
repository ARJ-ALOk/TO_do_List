# 🔥 Ultimate Productivity Suite

A robust, feature-rich desktop To-Do application built with Python and Tkinter. This application goes beyond simple lists by integrating gamification (streaks), persistent data storage, and smart notifications.

## APP SCREENSHOT
![App Screenshot](https://github.com/ARJ-ALOk/TO_do_List/blob/main/TO_DO.png)

## 🚀 Features

* **Command Center Dashboard:** Clean UI to manage tasks, priorities, and deadlines.
* **Gamification:** Tracks your daily streak to keep you motivated.
* **Smart Notifications:** Background thread checks for due tasks and plays sound alerts.
* **History Vault:** view completed and deleted tasks without cluttering the main view.
* **Data Persistence:** Automatically saves all data to a local JSON database.
* **Export:** One-click export to CSV for external backups.
* **Task Logic:**
    * **Double-click** for detailed dashboard (Snooze, Delete, Complete).
    * **Enter key** support for quick adding.
    * **Soft Deletion** keeps records in history.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **GUI:** Tkinter (Standard Lib), Ttk
* **Date Handling:** tkcalendar
* **Notifications:** Plyer, Winsound (Windows)
* **Data:** JSON (Local Storage)

## 📦 Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/ARJ-ALOk/TO_do_List.git](https://github.com/ARJ-ALOk/TO_do_List.git)
    cd TO_do_List
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App**
    ```bash
    python main.py
    ```

## 📂 File Structure

* `main.py` - The entry point and GUI logic.
* `database.py` - Handles JSON saving/loading and CSV export.
* `notifications.py` - Manages background threads and alert sounds.

## 🤝 Contributing

Feel free to fork this project and submit pull requests. Suggestions for new features (like Dark Mode toggles or Cloud Sync) are welcome!

## 📄 License

This project is open-source and available under the MIT License.
