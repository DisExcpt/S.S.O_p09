import threading
import tkinter as tk
import time

class ReaderWriter:
    def __init__(self):
        self.writer_semaphore = threading.Semaphore(1)
        self.edit_lock = threading.Lock()
        self.file = "archivo.txt"
        self.reading_count = 0
        self.edit_allowed = True

    def read_from_file(self, text_widget):
        with open(self.file, "r") as f:
            data = f.read()
            text_widget.insert(tk.END, data)

    def write_to_file(self, new_data):
        with open(self.file, "w") as f:
            f.write(new_data)

    def read_with_typing_effect(self, text_widget, data):
        def display_text(i=0):
            if i < len(data):
                text_widget.insert(tk.END, data[i])
                text_widget.see(tk.END)
                text_widget.update_idletasks()
                time.sleep(0.05)
                display_text(i + 1)
        
        display_text()

    def read(self, text_widget, btn_list, window):
        text_widget.delete("1.0", tk.END)
        for btn in btn_list:
            if btn.cget("text").startswith("Escribir"):
                btn.config(state=tk.DISABLED)
        with open(self.file, "r") as f:
            data = f.read()
        text_widget.config(state=tk.NORMAL)
        self.read_with_typing_effect(text_widget, data)
        text_widget.config(state=tk.DISABLED)

    def edit_and_save(self, text_widget, btn_list):
        if self.edit_allowed:
            text_widget.config(state=tk.NORMAL)
            for btn in btn_list:
                btn.config(state=tk.DISABLED)

def on_hover(event):
    event.widget.config(bg="#555555")

def on_leave(event):
    event.widget.config(bg="#333333")

def create_window(reader_writer, action, root, btn_list):
    window = tk.Toplevel(root)
    window.title(action)
    
    text_widget = tk.Text(window, height=15, width=50, wrap=tk.WORD)
    text_widget.pack(padx=10, pady=10)

    if action.startswith("Leer"):
        thread = threading.Thread(target=reader_writer.read, args=(text_widget, btn_list, window))
        thread.start()
        save_button = tk.Button(window, text="Cerrar", width=15, command=lambda: save_changes(reader_writer, text_widget, btn_list, window))
        save_button.pack(pady=10)
    elif action.startswith("Escribir"):
        reader_writer.edit_and_save(text_widget, btn_list)
        reader_writer.read_from_file(text_widget)
        save_button = tk.Button(window, text="Guardar", width=15, command=lambda: save_changes(reader_writer, text_widget, btn_list, window))
        save_button.pack(pady=10)

    window.protocol("WM_DELETE_WINDOW", lambda: on_closing(window, reader_writer, root, btn_list))
    window.bind("<Enter>", on_hover)
    window.bind("<Leave>", on_leave)
    return window

def save_changes(reader_writer, text_widget, btn_list, window):
    new_data = text_widget.get("1.0", tk.END)
    reader_writer.write_to_file(new_data)
    for btn in btn_list:
        btn.config(state=tk.NORMAL)
    window.destroy()

def on_closing(window, reader_writer, root, btn_list):
    window.destroy()
    if window.title().startswith("Leer"):
        with reader_writer.edit_lock:
            reader_writer.reading_count -= 1
            if reader_writer.reading_count == 0:
                reader_writer.edit_allowed = True
    for btn in btn_list:
        btn.config(state=tk.NORMAL)
    root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Editor de Archivos")
    root.geometry("800x600")
    root.configure(bg="#333333")

    rw = ReaderWriter()

    group1_frame = tk.Frame(root, bg="#333333")
    group1_frame.pack(pady=10)
    group1_label = tk.Label(group1_frame, text="Grupo 1", fg="white", bg="#333333")
    group1_label.pack(side=tk.TOP, pady=5)

    btn_read1 = tk.Button(group1_frame, text="Leer 1", width=15, command=lambda: create_window(rw, "Leer 1", root, [btn_edit1, btn_edit2, btn_edit3, btn_read1, btn_read2, btn_read3]))
    btn_read1.pack(side=tk.LEFT, padx=10)
    btn_read1.bind("<Enter>", on_hover)
    btn_read1.bind("<Leave>", on_leave)

    btn_edit1 = tk.Button(group1_frame, text="Escribir 1", width=15, command=lambda: create_window(rw, "Escribir 1", root, [btn_edit2, btn_edit3, btn_read1, btn_read2, btn_read3]))
    btn_edit1.pack(side=tk.LEFT, padx=10)
    btn_edit1.bind("<Enter>", on_hover)
    btn_edit1.bind("<Leave>", on_leave)

    group2_frame = tk.Frame(root, bg="#333333")
    group2_frame.pack(pady=10)
    group2_label = tk.Label(group2_frame, text="Grupo 2", fg="white", bg="#333333")
    group2_label.pack(side=tk.TOP, pady=5)

    btn_read2 = tk.Button(group2_frame, text="Leer 2", width=15, command=lambda: create_window(rw, "Leer 2", root, [btn_edit1, btn_edit2, btn_edit3, btn_read1, btn_read2, btn_read3]))
    btn_read2.pack(side=tk.LEFT, padx=10)
    btn_read2.bind("<Enter>", on_hover)
    btn_read2.bind("<Leave>", on_leave)

    btn_edit2 = tk.Button(group2_frame, text="Escribir 2", width=15, command=lambda: create_window(rw, "Escribir 2", root, [btn_edit1, btn_edit3, btn_read1, btn_read2, btn_read3]))
    btn_edit2.pack(side=tk.LEFT, padx=10)
    btn_edit2.bind("<Enter>", on_hover)
    btn_edit2.bind("<Leave>", on_leave)

    group3_frame = tk.Frame(root, bg="#333333")
    group3_frame.pack(pady=10)
    group3_label = tk.Label(group3_frame, text="Grupo 3", fg="white", bg="#333333")
    group3_label.pack(side=tk.TOP, pady=5)

    btn_read3 = tk.Button(group3_frame, text="Leer 3", width=15, command=lambda: create_window(rw, "Leer 3", root, [btn_edit1, btn_edit2, btn_edit3, btn_read1, btn_read2, btn_read3]))
    btn_read3.pack(side=tk.LEFT, padx=10)
    btn_read3.bind("<Enter>", on_hover)
    btn_read3.bind("<Leave>", on_leave)

    btn_edit3 = tk.Button(group3_frame, text="Escribir 3", width=15, command=lambda: create_window(rw, "Escribir 3", root, [btn_edit1, btn_edit2, btn_read1, btn_read2, btn_read3]))
    btn_edit3.pack(side=tk.LEFT, padx=10)
    btn_edit3.bind("<Enter>", on_hover)
    btn_edit3.bind("<Leave>", on_leave)

    root.mainloop()
