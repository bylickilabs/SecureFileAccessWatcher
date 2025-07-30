import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from watcher import FileEventHandler, start_watching
import pandas as pd

class LogStore:
    def __init__(self):
        self.log = []

    def add(self, event):
        self.log.append(event)

    def get_df(self):
        return pd.DataFrame(self.log, columns=["Zeit", "Aktion", "Pfad", "Prozess"])

def start_gui():
    store = LogStore()
    root = tk.Tk()
    root.title("Secure File Access Watcher")

    frame = ttk.Frame(root, padding=16)
    frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(frame, columns=("Zeit", "Aktion", "Pfad", "Prozess"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=200, anchor="center")
    tree.pack(fill="both", expand=True)

    def update_view():
        df = store.get_df()
        for i in tree.get_children():
            tree.delete(i)
        for _, row in df.iterrows():
            tree.insert("", "end", values=tuple(row))
        root.after(2000, update_view)

    def choose_folder():
        folder = filedialog.askdirectory(title="Überwachten Ordner auswählen")
        if not folder:
            return
        messagebox.showinfo("Info", f"Überwache: {folder}")
        threading.Thread(target=start_watching, args=(folder, store), daemon=True).start()

    btn = ttk.Button(frame, text="Ordner auswählen & Überwachung starten", command=choose_folder)
    btn.pack(pady=12)

    update_view()
    root.mainloop()
