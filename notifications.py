import threading
import time
import winsound
from datetime import datetime

# Check for notification support
try:
    from plyer import notification
    NOTIFICATION_AVAILABLE = True
except ImportError:
    NOTIFICATION_AVAILABLE = False

class ReminderSystem:
    def __init__(self, task_manager, update_ui_callback):
        self.db = task_manager        # Access to the data
        self.update_ui = update_ui_callback # Function to refresh UI
        self.stop_thread = False

    def start(self):
        """Starts the background checker thread."""
        self.reminder_thread = threading.Thread(target=self.checker, daemon=True)
        self.reminder_thread.start()

    def checker(self):
        """Loop that checks for due tasks."""
        while not self.stop_thread:
            now = datetime.now()
            changed = False
            
            # We iterate over the tasks list located in database.py
            for t in self.db.tasks:
                if t['status'] in ["Completed", "Deleted"]: 
                    continue
                
                try:
                    dt = datetime.strptime(t['datetime'], "%Y-%m-%d %H:%M:%S")
                    
                    if now >= dt:
                        notify = False
                        
                        # Logic: Notify if never reminded OR if interval passed
                        if t['last_reminded'] is None: 
                            notify = True
                        else:
                            last = datetime.strptime(t['last_reminded'], "%Y-%m-%d %H:%M:%S")
                            interval = 300 if t['priority'] == "High" else 900
                            if (now - last).total_seconds() > interval: 
                                notify = True
                        
                        if notify:
                            self.play_sound("alert")
                            if NOTIFICATION_AVAILABLE:
                                notification.notify(
                                    title=f"Due: {t['task']}", 
                                    message="Task is due!", 
                                    timeout=5
                                )
                            t['last_reminded'] = now.strftime("%Y-%m-%d %H:%M:%S")
                            changed = True
                except ValueError:
                    continue # Skip tasks with broken date formats

            if changed: 
                self.db.save_data()
                self.update_ui() # Safe UI update callback
            
            time.sleep(2)

    def play_sound(self, sound_type):
        """Plays a system beep."""
        try: 
            freq = 2000 if sound_type == "success" else 1000
            winsound.Beep(freq, 300)
        except: 
            pass