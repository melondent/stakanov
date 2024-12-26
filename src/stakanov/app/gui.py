from stakanov import Indiana
import tkinter as tk
from tkinter import filedialog, messagebox, Text, ttk

class stakanovApp:
    """Class to create the stakanov app, which allows scanning files in the
    specified directory, retrieving information about them, and displaying the
    results in the graphical interface.

    Attributes:
        master (tk.Tk): The main window of the application.
    """
    
    def __init__(self, master):
        """Initialize the application."""
        
        self.master = master
        master.title("stakanov")

        self.info_label = tk.Label(master, text="Добро пожаловать в stakanov!\n"
                                                 "Это приложение расскажет все о твоих файлах! (-:", 
                                     font=("Arial", 16, "bold"))
        self.info_label.pack(pady=10)

        self.instructions_label = tk.Label(master, text="Необходимо указать путь к папке для сканирования и имя выходного файла.\n"
                                                         "Нажми 'Начать', чтобы продолжить!", 
                                            font=("Arial", 14))
        self.instructions_label.pack(pady=5)

        self.start_button = tk.Button(master, text="Начать", command=self.show_controls)
        self.start_button.pack(pady=10)

        self.path_label = tk.Label(master, text="Путь к папке:")
        self.path_entry = tk.Entry(master, width=50)
        self.browse_button = tk.Button(master, text="Обзор", command=self.browse_directory)

        self.output_label = tk.Label(master, text="Имя выходного файла:")
        self.output_entry = tk.Entry(master, width=50)

        self.scan_button = tk.Button(master, text="Сканировать", command=self.start_scan)

        self.results_area = Text(master, wrap='word', height=15, width=70)

        self.progress_bar = ttk.Progressbar(master, orient='horizontal', mode='determinate', length=200)
        self.progress_bar.pack(pady=30)

        self.hide_controls()

    def hide_controls(self):
        """Hides control elements."""
        self.path_label.pack_forget()
        self.path_entry.pack_forget()
        self.browse_button.pack_forget()
        self.output_label.pack_forget()
        self.output_entry.pack_forget()
        self.scan_button.pack_forget()
        self.results_area.pack_forget()
        self.progress_bar.pack_forget()

    def show_controls(self):
        """Displays control elements."""
        self.path_label.pack()
        self.path_entry.pack()
        self.browse_button.pack()
        self.output_label.pack()
        self.output_entry.pack()
        self.scan_button.pack()
        self.results_area.pack()
        self.progress_bar.pack()  
        
        self.info_label.pack_forget()
        self.instructions_label.pack_forget()

        self.start_button.pack_forget()

    def browse_directory(self):
        """Opens a dialog window to select a directory and displays the
        selected path in the input field.

        If no directory is selected, the path remains empty.
        """
        folder_selected = filedialog.askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, folder_selected)

    def start_scan(self):
        """Starts the process of scanning files in the specified directory,
        collecting information about the files, and displaying the results in
        the output area.

        If the specified path or output file name is empty, an error
        message will be shown.
        """
        path = self.path_entry.get()
        output_file = self.output_entry.get()

        if not path or not output_file:
            messagebox.showerror("Ошибка", "Пожалуйста, укажите путь к директории и имя выходного файла.")
            return

        try:
            indi = Indiana(path, output_file)

            self.progress_bar['value'] = 0
            self.progress_bar['maximum'] = len(list(indi.guide.files()))
                
            def update_progress(count, total_files):
                """Updates the progress bar based on the number of processed
                files."""
                progress = int(count / total_files * 100)
                self.progress_bar['value'] = progress
                self.master.update_idletasks()

            indi.find_loot(update_progress)
            indi.save_results()
            indi.viewer.display(self.results_area)
            indi.viewer.display_top_size_files(indi.data, self.results_area)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
        finally:
            self.progress_bar['value'] = 0