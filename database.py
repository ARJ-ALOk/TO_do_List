import json
import os
import csv

DATA_FILE = "ultimate_tasks.json"

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.user_stats = {"streak": 0, "last_active_date": "", "total_completed": 0}
        self.load_data()

    def save_data(self):
        """Saves tasks and stats to JSON file."""
        try:
            with open(DATA_FILE, "w") as f:
                json.dump({"tasks": self.tasks, "stats": self.user_stats}, f)
        except Exception as e:
            print(f"Error saving data: {e}")

    def load_data(self):
        """Loads tasks from JSON file."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    d = json.load(f)
                    self.tasks = d.get("tasks", [])
                    self.user_stats = d.get("stats", {"streak": 0, "last_active_date": "", "total_completed": 0})
            except:
                self.tasks = []
                self.user_stats = {"streak": 0, "last_active_date": "", "total_completed": 0}

    def export_csv(self, path):
        """Exports data to a CSV file."""
        if path:
            try:
                with open(path, 'w', newline='', encoding='utf-8') as f:
                    w = csv.writer(f)
                    w.writerow(["Task", "Category", "Priority", "Date", "Status"])
                    for t in self.tasks:
                        w.writerow([t['task'], t['category'], t['priority'], t['datetime'], t['status']])
                return True
            except Exception as e:
                print(f"Export error: {e}")
                return False
        return False