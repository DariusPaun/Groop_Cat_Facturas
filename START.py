import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import fitz
import re
import sys
sys.path.append("Data\Project")
from main import main
from functions import check_veracity
from to_excel import excelCreat

class MyApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Forest Theme App")
        self.geometry("1300x500")
        self.option_add("*tearOff", False)
        self.data = [[]]
        self.path = r"Data\Facturi\1-3.pdf"

        # Make the app responsive
        for i in range(9):
            self.columnconfigure(i, weight=1)
            self.rowconfigure(0, weight=1)

        # Create a style
        style = ttk.Style(self)
        self.tk.call("source", "forest-light.tcl")
        style.theme_use("forest-light")

        # Create the main container frame
        container = ttk.Frame(self)
        container.grid(row=0, column=0, columnspan=9, sticky="nsew", padx=10, pady=10)

        # Create UI elements for Page 1
        label_page1 = ttk.Label(container, text="PDF :", font=("Arial", 18))
        label_page1.grid(row=0, column=0, pady=10, padx=10)

        choose_file_button = ttk.Button(
            container, text="Choose File", command=self.choose_file
        )
        choose_file_button.grid(row=1, column=0, pady=10)

        # Create UI elements for dynamic content
        self.dynamic_label = ttk.Label(container, text="", font=("Arial", 18))
        self.dynamic_label.grid(row=0, column=2, pady=10, padx=10)

        columns = ("Prices", "Cost Center", "ID / Page")
        self.treeview = ttk.Treeview(
            container, columns=columns, show="headings", selectmode="browse"
        )

        for col in columns:
            self.treeview.heading(col, text=col)

        # Pack the Treeview
        self.treeview.grid(row=1, column=7, padx=10, pady=10)

        # Bind double click event to the edit function
        self.treeview.bind("<Double-1>", self.edit_cell)

        # Button to save the edit
        save_button = ttk.Button(container, text="Commit", command=self.save_changes)
        save_button.grid(row=3, column=0, pady=10)

    def save_changes(self):
        new_data=check_veracity(self.data)

        if new_data == -2:
            edit_window = tk.Toplevel(self)
            edit_window.title("Sad")
            edit_window.geometry("200x70")
            # Button to save the edit
            OK_button = ttk.Button(edit_window, text="Numbers don't add up", command=lambda:edit_window.destroy())
            OK_button.grid( padx=20 , pady=10)
        else:
            excelCreat(self.data)

            

    def choose_file(self):
        file_path = filedialog.askopenfilename(
            title="Choose a PDF file", filetypes=[("PDF files", "*.pdf")]
        )
        if file_path:
            self.path = file_path
            self.data = main(self.path)
            self.show_preview(file_path)

    def show_preview(self, pdf_path):
        # Load a low-res preview image from the PDF
        preview_image = self.generate_preview(pdf_path)

        # Display the image in a label
        preview_label = ttk.Label(self, image=preview_image)
        preview_label.image = preview_image
        preview_label.grid(row=0, column=8, pady=10)

        # Update the table data
        self.update_table_data()

    def generate_preview(self, pdf_path):
        # Use PyMuPDF to extract a low-res preview image from the PDF
        pdf_document = fitz.open(pdf_path)
        first_page = pdf_document[0]

        # Calculate the zoom factor based on the physical size of the page
        zoom_factor = 500.0 / max(first_page.rect.width, first_page.rect.height)

        # Apply the zoom factor to the image matrix
        image_matrix = fitz.Matrix(zoom_factor, zoom_factor)

        image = first_page.get_pixmap(matrix=image_matrix)

        # Convert the PyMuPDF image to a Tkinter PhotoImage
        image = Image.frombytes("RGB", (image.width, image.height), image.samples)
        image = ImageTk.PhotoImage(image)

        return image

    def update_table_data(self):
        # Clear existing data in the treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        # Insert the updated data into the treeview
        for i, row in enumerate(self.data):
            item_tags = () if i % 2 == 0 else ("odd_row",)
            self.treeview.insert("", "end", values=row, tags=item_tags)

    def edit_cell(self, event):
        # Identify the selected item and column
        item = self.treeview.selection()[0]
        column = self.treeview.identify_column(event.x)

        # Extract the numeric part of the item identifier
        item_numeric_part = self.treeview.index(item)

        # Check if the numeric part is not empty
        if item_numeric_part:
            # Enable cell editing using a separate Toplevel window
            self.edit_window = tk.Toplevel(self)
            self.edit_window.title("Edit Cell")

            # Get the event coordinates
            x, y, _, _ = self.treeview.bbox(item, column)

            # Create an entry widget in the Toplevel window
            entry = ttk.Entry(self.edit_window, justify="center", font=("Arial", 12))
            entry.grid(row=0, column=0, padx=10, pady=10)

            # Save the entry and event as attributes
            self.entry = entry
            self.edit_event = event

            # Set the current cell value to the entry
            cell_value = self.treeview.item(item, "values")[int(column[-1]) - 1]
            entry.insert(0, cell_value)

            # Button to save the edit
            save_button = ttk.Button(self.edit_window, text="Save", command=lambda: self.save_edit(event))
            save_button.grid(row=1, column=0, pady=10)
        else:
            print(f"Invalid item identifier: {item}")

    def save_edit(self, event):
        # Get the new value from the entry
        edited_value = self.entry.get()

        # Identify the selected item and column
        item = self.treeview.selection()[0]
        column = self.treeview.identify_column(self.edit_event.x)

        # Get the numeric part of the item identifier
        item_numeric_part = self.treeview.index(item)

        # Update the treeview and data list
        values = list(self.treeview.item(item, "values"))
        values[int(column[-1]) - 1] = edited_value
        self.treeview.item(item, values=values, tags=())
        self.data[item_numeric_part] = values

        # Destroy the entry widget
        self.entry.destroy()
        # Destroy the Toplevel window
        self.edit_window.destroy()

if __name__ == "__main__":
    app = MyApp()
    # Center the app on the screen
    app.update_idletasks()
    width = app.winfo_reqwidth()
    height = app.winfo_reqheight()
    x = (app.winfo_screenwidth() // 2) - (width // 2)
    y = (app.winfo_screenheight() // 2) - (height // 2)
    app.geometry("{}x{}+{}+{}".format(width, height, x, y))
    app.mainloop()
