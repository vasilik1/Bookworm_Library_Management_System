from datetime import datetime, timedelta

class LibrarySystem:
    def __init__(self):
        self.books = []
        self.customers = {}
        self.borrowed_books = {}
        self.late_return_penalty = 2           # Penalty for late book return in days.
        self.reward_points = {}

    def add_book(self, book_title, author, copies):
        book = {'title': book_title, 'author': author, 'copies': copies, 'available': copies}
        self.books.append(book)
        print(f"Book '{book_title}' by {author} added to the library with {copies} copies.")

    def add_customer(self, customer_id, name, surname, max_books):
        if not all ([customer_id, name, surname, max_books]):
            print("Error: Customer information cannot be empty.")  # Additional error handling to control invalid entries regarding customer details.
            return
        
        try:
            customer_id = int(customer_id)
            max_books = int(max_books)
            if customer_id <= 0 or max_books <= 0:
                   print( "Error: Customer ID and maximum number of books must be integers.")
                   return
        except ValueError:
            print("Error: Customer ID and limitations in max book number must be integers!")
        
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
                    due_date = current_date + timedelta(days=14)  # Assuming a 14-day borrowing period.
                    due_date = due_date.replace(second=0, microsecond=0)  
                    self.customers[customer_id]['borrowed_books'].append({'title': book_title, 'due_date': due_date})
                    print(f"Book '{book_title}' borrowed by {self.customers[customer_id]['name']}. Due Date: {due_date}.")
                elif book['available'] == 0:
                    print(f"Book '{book_title}' is not available for borrowing.")
                else:
                    print(f"Maximum books limit reached for {self.customers[customer_id]['name']}. You cannot borrow more.")
            else:
                print(f"Book '{book_title}' not found in the library.")
        else:
            print(f"Customer with ID {customer_id} not found, please speak with a library staff member.")

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
                    print(f"Book '{book_title}' returned by {self.customers[customer_id]['name']} {days_late} days late. 
                          Late book return penalty applied: {penalty} points.")
                    # Log late book return.
                    print(f"Late book return log: Customer {self.customers[customer_id]['name']} (ID: {customer_id}) returned '{book_title}' {days_late} days late.")
                else:
                    print(f"Book '{book_title}' returned by {self.customers[customer_id]['name']} on time.")
                    # Reward points for on-time book return.
                    self.reward_points[customer_id] += 1
            else:
                print(f"Book '{book_title}' not borrowed by {self.customers[customer_id]['name']}.")
        else:
            print(f"Customer with ID {customer_id} not found, please speak with a staff member.")

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


# Example Usage
library = LibrarySystem()

library.add_book("The Great Gatsby", "F.Scott. Fitzgerald", 5)
library.add_book("Animal Farm", "George Orwell", 3)

library.add_customer(101, "Susie", "Brown", 2)
library.add_customer(102, "Nicolas", "Jones", 3)

library.display_books()
library.display_customers()

current_date = datetime.now().replace(second=0, microsecond=0)  

library.borrow_book(101, "The Great Gatsby", current_date)
library.borrow_book(102, "Animal Farm", current_date)

library.display_books()
library.display_customers()

return_date_1 = current_date + timedelta(days=15)
return_date_2 = current_date + timedelta(days=12)

library.return_book(101, "The Great Gatsby", return_date_1)
library.return_book(102, "Animal Farm", return_date_2)

library.display_books()
library.display_customers()
