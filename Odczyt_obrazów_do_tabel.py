import tkinter as tk
from tkinter import filedialog, messagebox
import text_to_table
import platform


def select_source_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        source_folder_var.set(folder_selected)


def select_output_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        output_folder_var.set(folder_selected)


def run_script():
    source = source_folder_var.get()
    output = output_folder_var.get()
    if not source or not output:
        messagebox.showerror("Błąd", "Wybierz oba foldery przed rozpoczęciem")
        return
    try:
        text_to_table.main_multi(source, output)
        messagebox.showinfo("Sukces", "Przetwarzanie zakończone!")
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił problem: {e}")

# if platform.system() == "Windows":
#     icon_path = "icon.ico"
# else:
#     icon_path = "icon.png" 


root = tk.Tk()
# if platform.system() == "Windows":
#     root.iconbitmap(icon_path)
# else:
#     icon_image = tk.PhotoImage(file=icon_path)
#     root.iconphoto(True, icon_image)

root.title("Konwersja Obrazów na Tabele")

source_folder_var = tk.StringVar()
output_folder_var = tk.StringVar()

tk.Label(root, text="Folder źródłowy:").grid(row=0, column=0)
tk.Entry(root, textvariable=source_folder_var, width=40).grid(row=0, column=1)
tk.Button(root, text="Wybierz", command=select_source_folder).grid(row=0, column=2)

tk.Label(root, text="Folder wynikowy:").grid(row=1, column=0)
tk.Entry(root, textvariable=output_folder_var, width=40).grid(row=1, column=1)
tk.Button(root, text="Wybierz", command=select_output_folder).grid(row=1, column=2)

tk.Button(root, text="Rozpocznij", command=run_script).grid(row=2, column=1)

root.mainloop()
