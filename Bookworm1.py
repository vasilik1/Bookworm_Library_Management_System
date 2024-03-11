from datetime import datetime, timedelta

class LibrarySystem:
    def __init__(self):
        self.books = []
        self.customers = {}
        self.borrowed_books = {}
        self.late_return_penalty = 2  # Penalty for late book return in days
        self.reward_points = {}

    def add_book(self, book_title, author, copies):
        book = {'title': book_title, 'author': author, 'copies': copies, 'available': copies}
        self.books.append(book)
        print(f"Book '{book_title}' by {author} added to the library with {copies} copies.")

    def add_customer(self, customer_id, name, surname, max_books):
        full_name = f"{name} {surname}"
        if customer_id not in self.customers:
            self.customers[customer_id] = {'name': full_name, 'max_books': max_books, 'borrowed_books': []}
            self.reward_points[customer_id] = 0
            print(f"Customer '{full_name}' with ID {customer_id} added. Maximum allowed books: {max_books}.")
        else:
            print(f"Customer with ID {customer_id} already exists.")

    def calculate_penalty(self, due_date, return_date):
        days_late = max(0, (return_date - due_date).days)
        return days_late * self.late_return_penalty

    def borrow_book(self, customer_id, book_title, current_date):
        if customer_id in self.customers:
            if book_title in [book['title'] for book in self.books]:
                book = next(item for item in self.books if item['title'] == book_title)
                if book['available'] > 0 and len(self.customers[customer_id]['borrowed_books']) < self.customers[customer_id]['max_books']:
                    book['available'] -= 1
                    due_date = current_date + timedelta(days=14)  # Assuming a 14-day borrowing period
                    due_date = due_date.replace(second=0, microsecond=0)  # Remove seconds and microseconds
                    self.customers[customer_id]['borrowed_books'].append({'title': book_title, 'due_date': due_date})
                    print(f"Book '{book_title}' borrowed by {self.customers[customer_id]['name']}. Due Date: {due_date}.")
                elif book['available'] == 0:
                    print(f"Book '{book_title}' is not available for borrowing.")
                else:
                    print(f"Maximum books limit reached for {self.customers[customer_id]['name']}. Cannot borrow more.")
            else:
                print(f"Book '{book_title}' not found in the library.")
        else:
            print(f"Customer with ID {customer_id} not found.")

    def return_book(self, customer_id, book_title, return_date):
        if customer_id in self.customers:
            if any(item['title'] == book_title for item in self.customers[customer_id]['borrowed_books']):
                borrowed_book = next(item for item in self.customers[customer_id]['borrowed_books'] if item['title'] == book_title)
                self.customers[customer_id]['borrowed_books'].remove(borrowed_book)

                book = next(item for item in self.books if item['title'] == book_title)
                book['available'] += 1

                due_date = borrowed_book['due_date']
                days_late = max(0, (return_date - due_date).days)
                if days_late > 0:
                    penalty = self.calculate_penalty(due_date, return_date)
                    print(f"Book '{book_title}' returned by {self.customers[customer_id]['name']} {days_late} days late. Late return penalty applied: {penalty} points.")
                    # Log late return
                    print(f"Late return log: Customer {self.customers[customer_id]['name']} (ID: {customer_id}) returned '{book_title}' {days_late} days late.")
                else:
                    print(f"Book '{book_title}' returned by {self.customers[customer_id]['name']} on time.")
                    # Reward points for on-time return
                    self.reward_points[customer_id] += 1
            else:
                print(f"Book '{book_title}' not borrowed by {self.customers[customer_id]['name']}.")
        else:
            print(f"Customer with ID {customer_id} not found.")

    def display_books(self):
        print("\nLibrary Books:")
        for book in self.books:
            availability = f"{book['available']} available out of {book['copies']}"
            print(f"Title: {book['title']}, Author: {book['author']}, Status: {availability}")

    def display_customers(self):
        print("\nLibrary Customers:")
        for customer_id, info in self.customers.items():
            borrowed_books = ', '.join([book['title'] for book in info['borrowed_books']])
            print(f"ID: {customer_id}, Name: {info['name']}, Borrowed Books: {borrowed_books}, Reward Points: {self.reward_points[customer_id]}")

# Welcome Message and program operations menu.
print("Welcome to Bookworm our library Management System!")
print("Here are the available operations of our program: ")
print("1. Add a book")
print("2. Add a customer")
print("3.Borrow a book")
print("4. Return a book")
print("5.Display all books")
print("6. Dispaly all customers")
print("Exit")


# Example Usage
library = LibrarySystem()

while True:
    choice = input("Enter your choice: ")

    if choice == "1":
        title = input("Enter the title of the book: ")
        author = input("Enter the author of the book; ")
        copies = input("Enter the number of copies available: ")
        library.add_book(title, author, copies)
    
    elif choice == "2":
        customer_id = input("Enter the customer ID: ")
        name = input("Enter the customer's first name: ")
        surname = input("Enter the customer's last name: ")
        max_books = input("Enter the maximum number of books allowed to borrow: ")
        library.add_customer(customer_id, name, surname, max_books)

    elif choice == "3":
        customer_id = input("Enter the customer ID:  ")
        book_title = input ("Enter the title of the book to borrow: ")
        current_date = datetime.now().replace(seconds =0, microsecond =0)
        library.borrow_book(customer_id,book_title, current_date)

    elif choice == "4":
        customer_id = input("Enter the customer ID: ")
        book_title = input ("Enter the title of the book to return: ")
        return_date = datetime.now().replace(second =0, microsecond =0)
        library.return_book(customer_id, book_title, return_date)

    elif choice == "5":
        library.display_books()
    elif choice == "6":
        library.display_customers()
    elif choice == "7":
        print( "Exiting the program. Thank you!")
        break
    else:
        print(" Invalid choice.Please enter a number between 1 and 7.")



