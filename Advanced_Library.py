from datetime import datetime, timedelta
import smtplib

class Library:
    def __init__(self):
        self.booklist = []
        self.borrowed_books_log = []  # Log to track borrowed books
        self.reserved_books = {}  # Dictionary to track reserved books
        self.users = []  # List to store users
        self.categories = {}  # Dictionary to store books by category

    def add_user(self, username, role, email=None):
        username = username.lower()  # Ensure username is stored in lowercase
        new_user = User(username, role, email)
        self.users.append(new_user)
        print(f"User '{username}' with role '{role}' has been added successfully.")

    def login(self):
        username = input("Enter your username: ").lower()
        for user in self.users:
            if user.username == username:
                print(f"Welcome, {user.username} ({user.role})!")
                return user
        print("User not found. Please register first.")
        return None

    def addbook(self, user):
        if user.role != "librarian":
            print("Only librarians can add books.")
            return
        self.unit = int(input("How many books will you register? : "))
        for _ in range(self.unit):
            book_name = input("Please enter the book's name: ")
            authors_name = input("Please enter the author's name: ")
            category = input("Enter the book category: ").lower()
            new_book = Book(book_name, authors_name, category)
            self.booklist.append(new_book)
            if category not in self.categories:
                self.categories[category] = []
            self.categories[category].append(new_book)
            print("Book registered successfully")

    def list_books(self):
        if len(self.booklist) != 0:
            print("Available Books in the Library:")
            for book in self.booklist:
                status = "Available" if not book.borrowed else "Borrowed"
                print(f"{book.book_name} by {book.authors_name} - [{status}] - Category: {book.category.capitalize()}")
        else:
            print("Sorry, there are no books available.")

    def borrow_book(self, user):
        if user.role != "member":
            print("Only members can borrow books.")
            return
        borrowed_book_name = input("Which book would you like to borrow? ").lower()
        for book in self.booklist:
            if book.book_name.lower() == borrowed_book_name:
                if not book.borrowed:
                    book.borrowed = True
                    book.borrow_date = datetime.now()
                    book.borrowed_by = user.username
                    self.borrowed_books_log.append((book.book_name, book.authors_name, book.borrow_date, user.username))
                    print(f"You have successfully borrowed '{book.book_name}'.")
                else:
                    print(f"Sorry, '{book.book_name}' is already borrowed.")
                    reserve = input("Would you like to reserve this book? (yes/no): ").lower()
                    if reserve == "yes":
                        if book.book_name not in self.reserved_books:
                            self.reserved_books[book.book_name] = []
                        self.reserved_books[book.book_name].append(user.username)
                        print(f"You have successfully reserved '{book.book_name}'.")
                return
        print(f"Sorry, '{borrowed_book_name}' is not available in the library.")

    def return_book(self, user):
        if user.role != "member":
            print("Only members can return books.")
            return
        returned_book_name = input("Which book would you like to return? ").lower()
        for book in self.booklist:
            if book.book_name.lower() == returned_book_name:
                if book.borrowed and book.borrowed_by == user.username:
                    borrow_duration = (datetime.now() - book.borrow_date).days
                    if borrow_duration > 15:
                        overdue_days = borrow_duration - 15
                        fee = overdue_days * 2
                        print(f"The book is overdue by {overdue_days} days. The fee is {fee} TL.")
                        paid = input("Have you paid the fee? (yes/no): ").lower()
                        if paid != "yes":
                            print("You must pay the overdue fee before returning the book.")
                            return
                    book.borrowed = False
                    book.borrow_date = None
                    book.borrowed_by = None
                    self.borrowed_books_log = [log for log in self.borrowed_books_log if log[0].lower() != returned_book_name]
                    print(f"You have successfully returned '{book.book_name}'.")
                    rating = input(f"Please rate the book '{book.book_name}' from 1 to 5: ")
                    try:
                        rating = int(rating)
                        if 1 <= rating <= 5:
                            book.ratings.append(rating)
                            print(f"Thank you for rating '{book.book_name}'. Current average rating: {book.get_average_rating()}.")
                        else:
                            print("Invalid rating. Please provide a rating between 1 and 5.")
                    except ValueError:
                        print("Invalid input. Please enter a number between 1 and 5.")
                    if book.book_name in self.reserved_books and len(self.reserved_books[book.book_name]) > 0:
                        next_user = self.reserved_books[book.book_name].pop(0)
                        print(f"Notification: '{book.book_name}' is now available for {next_user}.")
                else:
                    print(f"'{book.book_name}' is already in the library or not borrowed by you.")
                return
        print(f"Sorry, '{returned_book_name}' is not part of our library collection.")

    def search_book(self):
        search_query = input("Enter the book name, author, or category to search: ").lower()
        found_books = []
        for book in self.booklist:
            if (search_query in book.book_name.lower() or
                search_query in book.authors_name.lower() or
                search_query in book.category.lower()):
                found_books.append(book)

        if found_books:
            print("Search Results:")
            for book in found_books:
                status = "Available" if not book.borrowed else "Borrowed"
                print(f"{book.book_name} by {book.authors_name} - [{status}] - Category: {book.category.capitalize()} - Average Rating: {book.get_average_rating()}")
        else:
            print("No books found matching your search criteria.")

    def remove_book(self, user):
        if user.role != "librarian":
            print("Only librarians can remove books.")
            return
        book_to_remove = input("Enter the name of the book to remove: ").lower()
        for book in self.booklist:
            if book.book_name.lower() == book_to_remove:
                if book.borrowed:
                    print(f"Cannot remove '{book.book_name}' as it is currently borrowed.")
                else:
                    self.booklist.remove(book)
                    if book.category in self.categories:
                        self.categories[book.category].remove(book)
                    print(f"'{book.book_name}' has been removed from the library.")
                return
        print(f"Sorry, '{book_to_remove}' is not in the library.")

    def list_borrowed_books(self):
        if len(self.borrowed_books_log) != 0:
            print("Borrowed Books Log:")
            for book_name, author_name, borrow_date, borrowed_by in self.borrowed_books_log:
                overdue = ""
                borrow_duration = (datetime.now() - borrow_date).days
                if borrow_duration > 15:
                    overdue_days = borrow_duration - 15
                    overdue = f" - Overdue by {overdue_days} days"
                print(f"{book_name} by {author_name}, Borrowed on: {borrow_date.strftime('%Y-%m-%d %H:%M:%S')} by {borrowed_by}{overdue}")
        else:
            print("No books are currently borrowed.")

    def send_due_reminders(self):
        for book_name, author_name, borrow_date, borrowed_by in self.borrowed_books_log:
            borrow_duration = (datetime.now() - borrow_date).days
            if borrow_duration > 12:
                user = next((u for u in self.users if u.username == borrowed_by), None)
                if user and user.email:
                    print(f"Sending reminder email to {user.email}: '{book_name}' is due in {15 - borrow_duration} days.")

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

# Example usage
if __name__ == "__main__":
    library = Library()
    current_user = None
    while True:
        if current_user is None:
            print("\nLibrary Menu:")
            print("1. Add User")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                username = input("Enter username: ")
                role = input("Enter role (librarian/member): ").lower()
                email = input("Enter email (optional): ")
                if role in ["librarian", "member"]:
                    library.add_user(username, role, email)
                else:
                    print("Invalid role. Please enter 'librarian' or 'member'.")
            elif choice == "2":
                current_user = library.login()
            elif choice == "3":
                print("Exiting the library system. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 3.")
        else:
            print("\nUser Menu:")
            if current_user.role == "librarian":
                print("1. Add Book")
                print("2. List Books")
                print("3. Remove Book")
                print("4. List Borrowed Books")
                print("5. Logout")
            elif current_user.role == "member":
                print("1. List Books")
                print("2. Borrow Book")
                print("3. Return Book")
                print("4. Search Book")
                print("5. Logout")
            user_choice = input("Enter your choice: ")

            if current_user.role == "librarian":
                if user_choice == "1":
                    library.addbook(current_user)
                elif user_choice == "2":
                    library.list_books()
                elif user_choice == "3":
                    library.remove_book(current_user)
                elif user_choice == "4":
                    library.list_borrowed_books()
                elif user_choice == "5":
                    current_user = None
                else:
                    print("Invalid choice. Please enter a number between 1 and 5.")
            elif current_user.role == "member":
                if user_choice == "1":
                    library.list_books()
                elif user_choice == "2":
                    library.borrow_book(current_user)
                elif user_choice == "3":
                    library.return_book(current_user)
                elif user_choice == "4":
                    library.search_book()
                elif user_choice == "5":
                    current_user = None
                else:
                    print("Invalid choice. Please enter a number between 1 and 5.")



