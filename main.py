import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from tkcalendar import DateEntry
from datetime import datetime, timedelta

# IMPORT THE OTHER FILES
from database import TaskManager
from notifications import ReminderSystem

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TO_Do - Ultimate Task Manager")
        
        self.root.minsize(850, 600) 
        self.root.geometry("900x700")
        self.root.configure(bg="#2d3436")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(3, weight=1)

        # --- LOAD DATABASE ---
        self.db = TaskManager() # Initialize the separate database file
        self.check_streak()

        # --- LOAD NOTIFICATIONS ---
        # We pass 'self.db' so it can see tasks, and 'self.update_ui_safe' to refresh screen
        self.notifier = ReminderSystem(self.db, self.update_ui_safe)
        self.notifier.start()

        self.filters = {"category": "All", "priority": "All"}

        # --- Styles ---
        self.setup_styles()

        # --- UI Construction ---
        self.create_header()
        self.create_input_area()
        self.create_filter_bar()
        self.create_task_list()

    def update_ui_safe(self):
        """Helper to update UI from background thread"""
        self.root.after(0, self.update_listbox)

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28, background="white", fieldbackground="white")
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#0984e3", foreground="white")
        style.map('Treeview', background=[('selected', '#6c5ce7')])

    def create_header(self):
        header = tk.Frame(self.root, bg="#2d3436")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=15)
        header.columnconfigure(1, weight=1)

        tk.Label(header, text="My Command Center", font=("Segoe UI", 20, "bold"), bg="#2d3436", fg="white").grid(row=0, column=0, sticky="w")
        
        streak_text = f"🔥 Streak: {self.db.user_stats['streak']} Days"
        self.streak_lbl = tk.Label(header, text=streak_text, font=("Segoe UI", 14, "bold"), bg="#2d3436", fg="#fab1a0")
        self.streak_lbl.grid(row=0, column=2, sticky="e")

    def create_input_area(self):
        frame = tk.LabelFrame(self.root, text="New Task", font=("Segoe UI", 11, "bold"), bg="#2d3436", fg="white", padx=10, pady=10)
        frame.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        
        frame.columnconfigure(1, weight=1) 
        frame.columnconfigure(3, weight=1)
        frame.columnconfigure(5, weight=1)

        # Task Name
        tk.Label(frame, text="Task:", bg="#2d3436", fg="white").grid(row=0, column=0, sticky="w", padx=5)
        self.task_entry = tk.Entry(frame, font=("Segoe UI", 10))
        self.task_entry.grid(row=0, column=1, columnspan=6, sticky="ew", padx=5, pady=(0, 10))
        self.task_entry.bind('<Return>', lambda event: self.add_task())

        # Category
        tk.Label(frame, text="Category:", bg="#2d3436", fg="white").grid(row=1, column=0, sticky="w", padx=5)
        self.category_var = tk.StringVar(value="Work")
        ttk.Combobox(frame, textvariable=self.category_var, values=["Work", "Study", "Personal", "Health", "Coding"], state="readonly", width=10).grid(row=1, column=1, sticky="ew", padx=5)

        # Priority
        tk.Label(frame, text="Priority:", bg="#2d3436", fg="white").grid(row=1, column=2, sticky="w", padx=5)
        self.priority_var = tk.StringVar(value="Normal")
        ttk.Combobox(frame, textvariable=self.priority_var, values=["High", "Normal", "Low"], state="readonly", width=8).grid(row=1, column=3, sticky="ew", padx=5)

        # Date
        tk.Label(frame, text="Due:", bg="#2d3436", fg="white").grid(row=1, column=4, sticky="w", padx=5)
        self.date_entry = DateEntry(frame, width=10, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.grid(row=1, column=5, sticky="ew", padx=5)

        # Time
        time_frame = tk.Frame(frame, bg="#2d3436")
        time_frame.grid(row=1, column=6, sticky="w", padx=5)
        self.hour_var = tk.StringVar(value="09")
        self.minute_var = tk.StringVar(value="00")
        self.ampm_var = tk.StringVar(value="AM")
        ttk.Combobox(time_frame, textvariable=self.hour_var, values=[f"{i:02d}" for i in range(1,13)], width=3, state="readonly").pack(side=tk.LEFT)
        ttk.Combobox(time_frame, textvariable=self.minute_var, values=[f"{i:02d}" for i in range(0,60,5)], width=3, state="readonly").pack(side=tk.LEFT)
        ttk.Combobox(time_frame, textvariable=self.ampm_var, values=["AM", "PM"], width=4, state="readonly").pack(side=tk.LEFT)

        # Add Button
        tk.Button(frame, text="➕ Add", bg="#00b894", fg="white", font=("Segoe UI", 9, "bold"), command=self.add_task, width=10).grid(row=1, column=7, padx=10, sticky="e")

    def create_filter_bar(self):
        frame = tk.Frame(self.root, bg="#2d3436")
        frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        
        tk.Label(frame, text="🔍 Filter:", bg="#2d3436", fg="white", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT)

        def apply_filter(event=None):
            self.filters['category'] = self.filter_cat.get()
            self.filters['priority'] = self.filter_pri.get()
            self.update_listbox()

        self.filter_cat = ttk.Combobox(frame, values=["All", "Work", "Study", "Personal", "Health", "Coding"], state="readonly", width=10)
        self.filter_cat.set("All")
        self.filter_cat.pack(side=tk.LEFT, padx=5)
        self.filter_cat.bind("<<ComboboxSelected>>", apply_filter)

        self.filter_pri = ttk.Combobox(frame, values=["All", "High", "Normal", "Low"], state="readonly", width=10)
        self.filter_pri.set("All")
        self.filter_pri.pack(side=tk.LEFT, padx=5)
        self.filter_pri.bind("<<ComboboxSelected>>", apply_filter)

        tk.Button(frame, text="💾 Export CSV", bg="#636e72", fg="white", font=("Segoe UI", 8), command=self.export_csv).pack(side=tk.RIGHT)

    def create_task_list(self):
        list_frame = tk.Frame(self.root)
        list_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 10)) 

        cols = ("Priority", "Task", "Category", "Due Date", "Status")
        self.tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=12)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.tree.heading("Priority", text="Pri")
        self.tree.heading("Task", text="Task")
        self.tree.heading("Category", text="Cat")
        self.tree.heading("Due Date", text="Due")
        self.tree.heading("Status", text="Stat")

        self.tree.column("Priority", width=50, anchor="center")
        self.tree.column("Task", width=350) 
        self.tree.column("Category", width=80, anchor="center")
        self.tree.column("Due Date", width=120, anchor="center")
        self.tree.column("Status", width=80, anchor="center")

        self.tree.bind("<Double-1>", self.open_task_dashboard)

        self.tree.tag_configure('High', foreground='#d63031', font=("Segoe UI", 10, "bold"))
        self.tree.tag_configure('Completed', foreground='#00b894') 
        self.tree.tag_configure('Overdue', foreground='#e17055', font=("Segoe UI", 10, "bold")) 

        # Footer Area
        btn_frame = tk.Frame(self.root, bg="#2d3436")
        btn_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=10)
        
        tk.Button(btn_frame, text="📜 View History", bg="#6c5ce7", fg="white", font=("Segoe UI", 11, "bold"), 
                 command=self.show_history, width=20).pack(side=tk.LEFT)
        
        tk.Label(btn_frame, text="(Double-click task for actions)", bg="#2d3436", fg="#b2bec3", font=("Segoe UI", 9)).pack(side=tk.RIGHT)

    # --- LOGIC ---

    def add_task(self):
        task_text = self.task_entry.get()
        if not task_text: return
        date_str = self.date_entry.get_date().strftime("%Y-%m-%d")
        time_str = f"{self.hour_var.get()}:{self.minute_var.get()} {self.ampm_var.get()}"
        try:
            dt_obj = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %I:%M %p")
        except ValueError:
            messagebox.showerror("Error", "Invalid Time")
            return

        new_task = {
            "task": task_text,
            "category": self.category_var.get(),
            "priority": self.priority_var.get(),
            "datetime": dt_obj.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Pending",
            "last_reminded": None
        }
        
        # Access self.db instead of self.tasks
        self.db.tasks.append(new_task)
        self.db.save_data()
        self.update_listbox()
        self.task_entry.delete(0, tk.END)

    def mark_done(self, task_to_complete=None):
        target_task = task_to_complete
        
        if not target_task:
            selected = self.tree.selection()
            if selected:
                vals = self.tree.item(selected[0])['values']
                # Search in self.db.tasks
                target_task = next((t for t in self.db.tasks if t['task'] == vals[1] and t['datetime'] == str(vals[3])), None)

        if target_task:
            target_task['status'] = "Completed"
            self.db.user_stats["total_completed"] += 1
            self.check_streak(increment=True)
            self.db.save_data()
            self.update_listbox()
            self.notifier.play_sound("success")

    def open_task_dashboard(self, event):
        item = self.tree.selection()
        if not item: return
        vals = self.tree.item(item[0])['values']
        # Search in self.db.tasks
        target = next((t for t in self.db.tasks if t['task'] == vals[1] and t['datetime'] == str(vals[3])), None)
        if not target: return

        top = tk.Toplevel(self.root)
        top.title("Task Dashboard")
        top.geometry("400x350")
        top.configure(bg="white")
        top.resizable(False, False)

        tk.Label(top, text="Task Details", font=("Segoe UI", 10), bg="white", fg="gray").pack(pady=(10,0))
        tk.Label(top, text=target['task'], font=("Segoe UI", 16, "bold"), bg="white", wraplength=380).pack(pady=5)

        badge_frame = tk.Frame(top, bg="white")
        badge_frame.pack(pady=5)
        pri_color = "#d63031" if target['priority'] == "High" else "#0984e3"
        tk.Label(badge_frame, text=f" {target['priority']} Priority ", bg=pri_color, fg="white", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Label(badge_frame, text=f" {target['category']} ", bg="#636e72", fg="white", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)

        time_lbl = tk.Label(top, text="", font=("Segoe UI", 14), bg="white", fg="#2d3436")
        time_lbl.pack(pady=20)

        def update_timer():
            try:
                dt_obj = datetime.strptime(target['datetime'], "%Y-%m-%d %H:%M:%S")
                now = datetime.now()
                if target['status'] == "Completed":
                    time_lbl.config(text="✅ Task Completed", fg="green")
                elif now > dt_obj:
                    diff = now - dt_obj
                    time_lbl.config(text=f"⚠️ Overdue by: {str(diff).split('.')[0]}", fg="#d63031")
                else:
                    diff = dt_obj - now
                    days = diff.days
                    hours, _ = divmod(diff.seconds, 3600)
                    minutes, _ = divmod(_, 60)
                    time_str = f"{days}d, {hours}h, {minutes}m"
                    time_lbl.config(text=f"⏳ Due in: {time_str}")
            except:
                time_lbl.config(text="Invalid Time Data")
        update_timer()

        btn_frame = tk.Frame(top, bg="white")
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20, padx=20)

        tk.Button(btn_frame, text="✓ Complete", bg="#00b894", fg="white", font=("Segoe UI", 10, "bold"), 
                  height=2, command=lambda: [self.mark_done(target), top.destroy()]).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        tk.Button(btn_frame, text="🗑 Delete", bg="#d63031", fg="white", font=("Segoe UI", 10, "bold"), 
                  height=2, command=lambda: [self.delete_task(target), top.destroy()]).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        snooze_mb = tk.Menubutton(btn_frame, text="💤 Snooze ▾", bg="#f39c12", fg="white", font=("Segoe UI", 10, "bold"), height=2, relief="raised")
        snooze_menu = tk.Menu(snooze_mb, tearoff=0)
        snooze_mb.config(menu=snooze_menu)

        def do_snooze(mins):
            try:
                new_time = datetime.strptime(target['datetime'], "%Y-%m-%d %H:%M:%S") + timedelta(minutes=mins)
                target['datetime'] = new_time.strftime("%Y-%m-%d %H:%M:%S")
                target['last_reminded'] = None
                self.db.save_data()
                self.update_listbox()
                top.destroy()
                messagebox.showinfo("Snoozed", f"Task snoozed for {mins} minutes.")
            except:
                pass

        for m in [5, 10, 30, 60]:
            snooze_menu.add_command(label=f"{m} Mins", command=lambda x=m: do_snooze(x))
        snooze_mb.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

    def delete_task(self, task_to_delete=None):
        target = task_to_delete
        if not target:
            selected = self.tree.selection()
            if selected:
                vals = self.tree.item(selected[0])['values']
                target = next((t for t in self.db.tasks if t['task'] == vals[1] and t['datetime'] == str(vals[3])), None)
        
        if target:
            target['status'] = "Deleted" 
            self.db.save_data()
            self.update_listbox()

    def show_history(self):
        hist_win = tk.Toplevel(self.root)
        hist_win.title("📜 Task History")
        hist_win.geometry("600x400")
        hist_win.configure(bg="#2d3436")

        tk.Label(hist_win, text="Completed & Deleted Tasks", font=("Segoe UI", 14, "bold"), bg="#2d3436", fg="white").pack(pady=10, side=tk.TOP)

        btn_frame = tk.Frame(hist_win, bg="#2d3436")
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        def clear_history():
            if messagebox.askyesno("Confirm", "Permanently delete history?"):
                # Filter self.db.tasks
                self.db.tasks = [t for t in self.db.tasks if t['status'] == "Pending"]
                self.db.save_data()
                hist_win.destroy()
                self.update_listbox()

        tk.Button(btn_frame, text="🗑 Clear All History", bg="#d63031", fg="white", command=clear_history).pack()

        cols = ("Task", "Date", "Status")
        h_tree = ttk.Treeview(hist_win, columns=cols, show="headings")
        h_tree.heading("Task", text="Task")
        h_tree.heading("Date", text="Original Due Date")
        h_tree.heading("Status", text="Final Status")
        
        h_tree.column("Task", width=300)
        h_tree.column("Date", width=150)
        h_tree.column("Status", width=100)
        
        h_tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10)

        h_tree.tag_configure('Completed', foreground='green')
        h_tree.tag_configure('Deleted', foreground='red')

        # Read from self.db.tasks
        history_items = [t for t in self.db.tasks if t['status'] in ["Completed", "Deleted"]]
        history_items.sort(key=lambda x: x['datetime'], reverse=True)

        for t in history_items:
            h_tree.insert("", "end", values=(t['task'], t['datetime'], t['status']), tags=(t['status'],))

    def update_listbox(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        
        # Read from self.db.tasks
        active_tasks = [t for t in self.db.tasks if t['status'] != "Deleted"]
        active_tasks.sort(key=lambda x: (x['status'] == "Completed", x['datetime']))

        for t in active_tasks:
            if self.filters['category'] != "All" and t['category'] != self.filters['category']: continue
            if self.filters['priority'] != "All" and t['priority'] != self.filters['priority']: continue
            
            tag = t['priority']
            try:
                if t['status'] == "Completed": tag = "Completed"
                elif datetime.now() > datetime.strptime(t['datetime'], "%Y-%m-%d %H:%M:%S"): tag = "Overdue"
            except:
                pass
            
            self.tree.insert("", "end", values=(t['priority'], t['task'], t['category'], t['datetime'], t['status']), tags=(tag,))

    def check_streak(self, increment=False):
        today = datetime.now().strftime("%Y-%m-%d")
        # Access self.db.user_stats
        if increment and self.db.user_stats.get("last_active_date") != today:
            self.db.user_stats['streak'] += 1
            self.db.user_stats['last_active_date'] = today
            # Update the Label (defined in create_header) if it exists
            if hasattr(self, 'streak_lbl'):
                self.streak_lbl.config(text=f"🔥 Streak: {self.db.user_stats['streak']} Days")

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv")
        if self.db.export_csv(path):
            messagebox.showinfo("Done", "Exported!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()