from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox

class Library:
    def __init__(self):
        self.booklist = []
        self.borrowed_books_log = []  # Log to track borrowed books
        self.reserved_books = {}  # Dictionary to track reserved books
        self.users = []  # List to store users
        self.categories = {}  # Dictionary to store books by category
        self.current_user = None

    def add_user(self, username, role, email=None):
        username = username.lower()  # Ensure username is stored in lowercase
        new_user = User(username, role, email)
        self.users.append(new_user)
        messagebox.showinfo("Success", f"User '{username}' with role '{role}' has been added successfully.")

    def login(self, username):
        username = username.lower()
        for user in self.users:
            if user.username == username:
                self.current_user = user
                messagebox.showinfo("Success", f"Welcome, {user.username} ({user.role})!")
                return
        messagebox.showerror("Error", "User not found. Please register first.")

    def add_book(self, book_name, authors_name, category):
        if self.current_user is None or self.current_user.role != "librarian":
            messagebox.showerror("Error", "Only librarians can add books.")
            return
        new_book = Book(book_name, authors_name, category)
        self.booklist.append(new_book)
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(new_book)
        messagebox.showinfo("Success", "Book registered successfully")

    def list_books(self):
        if len(self.booklist) != 0:
            books = "Available Books in the Library:\n"
            for book in self.booklist:
                status = "Available" if not book.borrowed else "Borrowed"
                books += f"{book.book_name} by {book.authors_name} - [{status}] - Category: {book.category.capitalize()}\n"
            messagebox.showinfo("Book List", books)
        else:
            messagebox.showinfo("Book List", "Sorry, there are no books available.")

    def borrow_book(self, borrowed_book_name):
        if self.current_user is None or self.current_user.role != "member":
            messagebox.showerror("Error", "Only members can borrow books.")
            return
        borrowed_book_name = borrowed_book_name.lower()
        for book in self.booklist:
            if book.book_name.lower() == borrowed_book_name:
                if not book.borrowed:
                    book.borrowed = True
                    book.borrow_date = datetime.now()
                    book.borrowed_by = self.current_user.username
                    self.borrowed_books_log.append((book.book_name, book.authors_name, book.borrow_date, self.current_user.username))
                    messagebox.showinfo("Success", f"You have successfully borrowed '{book.book_name}'.")
                else:
                    messagebox.showinfo("Info", f"Sorry, '{book.book_name}' is already borrowed.")
                return
        messagebox.showerror("Error", f"Sorry, '{borrowed_book_name}' is not available in the library.")

    def return_book(self, returned_book_name):
        if self.current_user is None or self.current_user.role != "member":
            messagebox.showerror("Error", "Only members can return books.")
            return
        returned_book_name = returned_book_name.lower()
        for book in self.booklist:
            if book.book_name.lower() == returned_book_name:
                if book.borrowed and book.borrowed_by == self.current_user.username:
                    borrow_duration = (datetime.now() - book.borrow_date).days
                    if borrow_duration > 15:
                        overdue_days = borrow_duration - 15
                        fee = overdue_days * 2
                        paid = messagebox.askyesno("Overdue Fee", f"The book is overdue by {overdue_days} days. The fee is {fee} TL. Have you paid the fee?")
                        if not paid:
                            messagebox.showerror("Error", "You must pay the overdue fee before returning the book.")
                            return
                    book.borrowed = False
                    book.borrow_date = None
                    book.borrowed_by = None
                    self.borrowed_books_log = [log for log in self.borrowed_books_log if log[0].lower() != returned_book_name]
                    messagebox.showinfo("Success", f"You have successfully returned '{book.book_name}'.")
                    return
                else:
                    messagebox.showerror("Error", f"'{book.book_name}' is already in the library or not borrowed by you.")
                return
        messagebox.showerror("Error", f"Sorry, '{returned_book_name}' is not part of our library collection.")

class Book:
    def __init__(self, book_name, authors_name, category):
        self.book_name = book_name
        self.authors_name = authors_name
        self.category = category
        self.borrowed = False
        self.borrow_date = None
        self.borrowed_by = None
        self.ratings = []

    def get_average_rating(self):
        if self.ratings:
            return round(sum(self.ratings) / len(self.ratings), 2)
        return "No ratings yet"

class User:
    def __init__(self, username, role, email=None):
        self.username = username
        self.role = role
        self.email = email

# GUI Implementation using Tkinter
class LibraryGUI:
    def __init__(self, root, library):
        self.library = library
        self.root = root
        self.root.title("Library Management System")

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.label = tk.Label(self.frame, text="Library Management System", font=("Arial", 16))
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        self.username_label = tk.Label(self.frame, text="Username:")
        self.username_label.grid(row=1, column=0, sticky=tk.E)
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=1, column=1)

        self.role_label = tk.Label(self.frame, text="Role (librarian/member):")
        self.role_label.grid(row=2, column=0, sticky=tk.E)
        self.role_entry = tk.Entry(self.frame)
        self.role_entry.grid(row=2, column=1)

        self.email_label = tk.Label(self.frame, text="Email (optional):")
        self.email_label.grid(row=3, column=0, sticky=tk.E)
        self.email_entry = tk.Entry(self.frame)
        self.email_entry.grid(row=3, column=1)

        self.add_user_button = tk.Button(self.frame, text="Add User", command=self.add_user)
        self.add_user_button.grid(row=4, column=0, columnspan=2, pady=5)

        self.login_button = tk.Button(self.frame, text="Login", command=self.login)
        self.login_button.grid(row=5, column=0, columnspan=2, pady=5)

        self.book_name_label = tk.Label(self.frame, text="Book Name:")
        self.book_name_label.grid(row=6, column=0, sticky=tk.E)
        self.book_name_entry = tk.Entry(self.frame)
        self.book_name_entry.grid(row=6, column=1)

        self.authors_name_label = tk.Label(self.frame, text="Author's Name:")
        self.authors_name_label.grid(row=7, column=0, sticky=tk.E)
        self.authors_name_entry = tk.Entry(self.frame)
        self.authors_name_entry.grid(row=7, column=1)

        self.category_label = tk.Label(self.frame, text="Category:")
        self.category_label.grid(row=8, column=0, sticky=tk.E)
        self.category_entry = tk.Entry(self.frame)
        self.category_entry.grid(row=8, column=1)

        self.add_book_button = tk.Button(self.frame, text="Add Book", command=self.add_book)
        self.add_book_button.grid(row=9, column=0, columnspan=2, pady=5)

        self.list_books_button = tk.Button(self.frame, text="List Books", command=self.list_books)
        self.list_books_button.grid(row=10, column=0, columnspan=2, pady=5)

        self.borrow_book_button = tk.Button(self.frame, text="Borrow Book", command=self.borrow_book)
        self.borrow_book_button.grid(row=11, column=0, columnspan=2, pady=5)

        self.return_book_button = tk.Button(self.frame, text="Return Book", command=self.return_book)
        self.return_book_button.grid(row=12, column=0, columnspan=2, pady=5)

    def add_user(self):
        username = self.username_entry.get()
        role = self.role_entry.get().lower()
        email = self.email_entry.get()
        if role in ["librarian", "member"]:
            self.library.add_user(username, role, email)
        else:
            messagebox.showerror("Error", "Invalid role. Please enter 'librarian' or 'member'.")

    def login(self):
        username = self.username_entry.get()
        self.library.login(username)

    def add_book(self):
        if self.library.current_user is None:
            messagebox.showerror("Error", "Please login first.")
            return
        book_name = self.book_name_entry.get()
        authors_name = self.authors_name_entry.get()
        category = self.category_entry.get()
        self.library.add_book(book_name, authors_name, category)

    def list_books(self):
        if self.library.current_user is None:
            messagebox.showerror("Error", "Please login first.")
            return
        self.library.list_books()

    def borrow_book(self):
        if self.library.current_user is None:
            messagebox.showerror("Error", "Please login first.")
            return
        book_name = self.book_name_entry.get()
        self.library.borrow_book(book_name)

    def return_book(self):
        if self.library.current_user is None:
            messagebox.showerror("Error", "Please login first.")
            return
        book_name = self.book_name_entry.get()
        self.library.return_book(book_name)

if __name__ == "__main__":
    root = tk.Tk()
    library = Library()
    app = LibraryGUI(root, library)
    root.mainloop()
