import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image

class Library:
    def __init__(self):
        # Open the file for appending
        self.file = open("books.txt", "a+")

    def __del__(self):
        # Close the file when the instance is deleted
        self.file.close()

    def list_books(self):
        # Function to list all the books in the file
        self.file.seek(0)
        books = self.file.readlines()
        if not books:
            # If no books are available, show a message
            messagebox.showinfo("List Books", "No books available.")
        else:
            # If books are available, create a list of book information
            book_list = ""
            for book in books:
                book_info = book.strip().split(',')
                book_list += f"Book: {book_info[0]}, Author: {book_info[1]}\n"
            # Show the list of books in a message box
            messagebox.showinfo("List Books", book_list)

    def add_book(self, title, author, release_year, num_pages):
        # Function to add a book to the file
        # Check if there's a trailing space at the end of the file
        self.file.seek(0)  # Go to the beginning of the file

        # Check if the first character is empty
        first_char = self.file.read(1)
        if not first_char:
            # If the file is empty, we can directly add the book
            book_info = f"{title},{author},{release_year},{num_pages}"
            self.file.write(book_info)
        else:
            # Read the first line and then go back
            self.file.seek(0, 0)

            # Read the last character of the file
            last_char = self.file.read()[-1:]
            if last_char != '\n':  # If the last character doesn't indicate a newline
                self.file.write("\n")  # Add a new line

            # Add the new book information to the file
            book_info = f"{title},{author},{release_year},{num_pages}"
            self.file.write(book_info)

        self.file.close()
        self.file = open("books.txt", "a+")
        self.file.seek(0, 0)
        # Show a message indicating the book has been added
        messagebox.showinfo("Add Book", f"Book '{title}' added successfully.")

    def remove_book(self, title):
        # Function to remove a book from the file
        self.file.seek(0)
        books = self.file.readlines()
        removed = False
        with open("books.txt", "w") as f:
            for book in books:
                book_info = book.strip().split(',')
                if title.lower() != book_info[0].lower():
                    f.write(book)
                else:
                    removed = True
        if removed:
            messagebox.showinfo("Remove Book", f"Book '{title}' removed successfully.")
        else:
            messagebox.showinfo("Remove Book", "Book not found.")

class LibraryGUI:
    def __init__(self, master):
        # Constructor for the GUI
        self.master = master
        master.title("Library Management System")
        master.geometry("500x250")

        # Load background image
        background_image = Image.open("picture.jpg")
        background_image = background_image.resize((500, 250), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(background_image)
        self.background_label = tk.Label(master, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)
        
        self.lib = Library()  # Create an instance of the Library class
        self.label = tk.Label(master, text="Welcome to Library Management System", bg='sky blue')
        self.label.pack(pady=15)

        self.label = tk.Label(master, text="Please select an option from the menu (1/2/3/q)", bg='yellow')
        self.label.pack(pady=8)

        self.label = tk.Label(master, text="********* MENU *********\n(1) List Books\n(2) Add Book\n(3) Remove Book\n(q) Quit", bg='white')
        self.label.pack(pady=8)

        # Bind key events for menu options
        self.master.bind('1', self.list_books)
        self.master.bind('2', self.add_book_window)
        self.master.bind('3', self.remove_book_window)
        self.master.bind('<KeyPress>', lambda event: self.master.quit() if event.char.lower() == 'q' else None)

    def list_books(self, event=None):
        # Function to handle listing books
        self.lib.list_books()

    def add_book_window(self, event=None):
        # Function to create the window for adding a book
        self.add_window = tk.Toplevel(self.master)
        self.add_window.title("Add Book")

        # Labels and Entry widgets for book information
        self.title_label = tk.Label(self.add_window, text="Title:")
        self.title_label.grid(row=0, column=0)
        self.title_entry = tk.Entry(self.add_window)
        self.title_entry.grid(row=0, column=1)

        self.author_label = tk.Label(self.add_window, text="Author:")
        self.author_label.grid(row=1, column=0)
        self.author_entry = tk.Entry(self.add_window)
        self.author_entry.grid(row=1, column=1)

        self.release_label = tk.Label(self.add_window, text="Release Year:")
        self.release_label.grid(row=2, column=0)
        self.release_entry = tk.Entry(self.add_window)
        self.release_entry.grid(row=2, column=1)

        self.pages_label = tk.Label(self.add_window, text="Number of Pages:")
        self.pages_label.grid(row=3, column=0)
        self.pages_entry = tk.Entry(self.add_window)
        self.pages_entry.grid(row=3, column=1)

        self.add_button = tk.Button(self.add_window, text="Add", command=self.add_book)
        self.add_button.grid(row=4, columnspan=2)

    def add_book(self, event=None):
        # Function to add a book
        title = self.title_entry.get()
        author = self.author_entry.get()
        release_year = self.release_entry.get()
        num_pages = self.pages_entry.get()
        self.lib.add_book(title, author, release_year, num_pages)
        self.add_window.destroy()

    def remove_book_window(self, event=None):
        # Function to create the window for removing a book
        self.remove_window = tk.Toplevel(self.master)
        self.remove_window.title("Remove Book")

        self.title_label = tk.Label(self.remove_window, text="Title:")
        self.title_label.grid(row=0, column=0)
        self.title_entry = tk.Entry(self.remove_window)
        self.title_entry.grid(row=0, column=1)

        self.remove_button = tk.Button(self.remove_window, text="Remove", command=self.remove_book)
        self.remove_button.grid(row=1, columnspan=2)

    def remove_book(self, event=None):
        # Function to remove a book
        title = self.title_entry.get()
        self.lib.remove_book(title)
        self.remove_window.destroy()

root = tk.Tk()
my_gui = LibraryGUI(root)
root.mainloop()