import re
import shutil
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinterdnd2 import DND_FILES, TkinterDnD


def on_drop(event, file_var, valid_file_name, entry_widget):
    file_path = event.data.strip('{}')
    filename = os.path.basename(file_path)

    if filename == valid_file_name:
        file_var.set(file_path)
        entry_widget.config(highlightbackground="green", highlightcolor="green",
                            highlightthickness=2)
    else:
        messagebox.showerror("Error", f"Invalid file. Please drop a '{valid_file_name}' file.")
        entry_widget.config(highlightbackground="red", highlightcolor="red", highlightthickness=2)


def clean_prefs():
    lua_path = lua_file_path.get()
    prefs_path = prefs_file_path.get()

    if not lua_path or not prefs_path:
        messagebox.showerror("Error", "Please select both files.")
        return

    try:
        backup_path = prefs_path + ".backup"
        shutil.copyfile(prefs_path, backup_path)
        log.insert(tk.END, f"Backup created at: {backup_path}\n")

        keys_to_remove = []
        pattern_key = r'key\s*=\s*[\'"](.+?)[\'"]'

        with open(lua_path, 'r', encoding='utf-8') as lua_file:
            for line in lua_file:
                match = re.search(pattern_key, line)
                if match:
                    keys_to_remove.append(f"LobbyOpt_{match.group(1)}")

        pattern_prefs = re.compile(r"^\s*(LobbyOpt_\w+)\s*=")
        with open(prefs_path, "r", encoding="utf-8") as prefs_file:
            lines = prefs_file.readlines()

        removed_lines = 0
        with open(prefs_path, "w", encoding="utf-8") as prefs_file:
            for line in lines:
                match = pattern_prefs.search(line)
                if match:
                    key = match.group(1)
                    if key in keys_to_remove:
                        removed_lines += 1
                        log.insert(tk.END, f"Removing line with key: {key}\n")
                        continue
                prefs_file.write(line)

        log.insert(tk.END, f"Finished cleaning. Removed {removed_lines} lines.\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))


root = TkinterDnD.Tk()
root.title("Prefs Cleaner - AI Wave Survival")

bg_color = "#2E2E2E"
fg_color = "#FFFFFF"

root.configure(bg=bg_color)

lua_file_path = tk.StringVar()
prefs_file_path = tk.StringVar()

lua_frame = tk.Frame(root, bg=bg_color)
lua_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")


tk.Label(lua_frame, text="1. Start FAF Client (If you have removed the mod AI Wave Survival already, install it again)",
         bg=bg_color, fg=fg_color, anchor="w").pack(side=tk.TOP, padx=5, anchor='w', pady=(0, 5))

tk.Label(lua_frame, text="2. Drop 'mod_options.lua' File from AI Wave Survival:",
         bg=bg_color, fg=fg_color, anchor="w").pack(side=tk.TOP, padx=5, anchor='w', pady=(0, 5))

lua_entry = tk.Entry(lua_frame, textvariable=lua_file_path, width=40, bg="#4E4E4E",
                     fg=fg_color, insertbackground=fg_color, highlightthickness=2)
lua_entry.pack(side=tk.TOP, padx=5, anchor='w', pady=(0, 5))
lua_entry.drop_target_register(DND_FILES)
lua_entry.dnd_bind('<<Drop>>', lambda e: on_drop(e, lua_file_path, "mod_options.lua", lua_entry))

prefs_frame = tk.Frame(root, bg=bg_color)
prefs_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

tk.Label(prefs_frame, text="3. Drop 'Game.prefs' from FAF Client:",
         bg=bg_color, fg=fg_color, anchor="w").pack(side=tk.TOP, padx=5, anchor='w', pady=(0, 5))

prefs_entry = tk.Entry(prefs_frame, textvariable=prefs_file_path, width=40, bg="#4E4E4E",
                       fg=fg_color, insertbackground=fg_color, highlightthickness=2)
prefs_entry.pack(side=tk.TOP, padx=5, anchor='w', pady=(0, 5))
prefs_entry.drop_target_register(DND_FILES)
prefs_entry.dnd_bind('<<Drop>>', lambda e: on_drop(e, prefs_file_path, "Game.prefs", prefs_entry))

clean_button = tk.Button(root, text="4. Hit this button to remove all lobby settings from AI Wave Survival", command=clean_prefs,
                         bg="#4E4E4E", fg=fg_color)
clean_button.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="w")

tk.Label(root, text="5. Uninstall the mod 'AI Wave Survival via FAF Client in the Mods tab",
          bg=bg_color, fg=fg_color, anchor="w").grid(row=3, column=0, padx=10, pady=(0, 5), sticky="w")

log = scrolledtext.ScrolledText(root, width=90, height=15, bg="#4E4E4E", fg=fg_color)
log.grid(row=5, column=0, padx=10, pady=10)

tutorial_text = (
    "A backup will be made before any changes are applied (Game.prefs.backup).\n"
)
log.insert(tk.END, tutorial_text)

root.grid_columnconfigure(0, weight=1)
root.mainloop()
