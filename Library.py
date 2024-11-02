class Book:
    def __init__(self,book_name,authors_name):
        self.book_name=book_name
        self.authors_name=authors_name
        self.barrowed=False

    def __str__(self):
        return f"Book Name: {self.book_name}, Author: {self.authors_name}"

class Library:
    def __init__(self):
        self.booklist=[]

    def addbook(self):
        self.unit= int(input("How many books will you register? : "))
        i=0
        while i<self.unit:
            book_name =input("Please enter the books name: ").lower()
            authors_name = input("Please enter the authors name: ").lower()
            new_book = Book(book_name, authors_name)
            self.booklist.append(new_book)
            i+=1
            print("Books registered successfully")
    
    def list_books(self):
        if len(self.booklist) != 0:
            print("Available Books in the Library:")
            for book in self.booklist:
                status = "Available" if not book.borrowed else "Borrowed"
                print(f"{book.book_name} by {book.authors_name} - [{status}]")
        else: 
            print("Sorry, There is no book avaliable.")

    def borrow_book(self):
        borrowed_book_name=input("Which book would you like to borrow? ").lower()
        for book in self.booklist:
            if book.book_name.lower() ==borrowed_book_name:
                if not book.borrowed:
                    book.borrowed = True
                    print(f"You have successfully borrowed '{book.book_name}'")
                else:
                    print(f"Sorry, '{book.book_name}' is already borrowed.")
                return

        else:
            print(f"Sorry, '{borrowed_book_name}' is not available in the library.")
             

    def return_book(self):
        returned_book_name = input("Which book would you like to return? ").lower()

        for book in self.booklist:
            if book.book_name.lower() == returned_book_name:
                if book.borrowed:
                    book.borrowed = False
                    print(f"You have successfully returned '{book.book_name}'")
                else:
                    print(f"'{book.book_name}' is already in the library.")
                return
        else:
            print(f"Sorry, '{returned_book_name}' is not part of our library collection.")


