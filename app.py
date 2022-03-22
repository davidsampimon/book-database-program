from models import (Base, session, 
                    Book, engine)
import datetime
import csv
import re

fmt = '%d/%m/%Y' # format string for datetime
price_regex = r"[\d]+.\d{2}" # regex for price validation

def menu():
    while True:
        print('''
                \nPROGRAMMING BOOKS
                \r1) Add book
                \r2) View all books
                \r3) Search for book
                \r4) Analysis
                \r5) Exit''')

        choice = input('What would you like to do? ')

        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            input("Please choose one of the options above. Press 'enter' to try again")


# add books
def add_books():
    title = input('What is the title? ')
    author = input('Who is the author? ')
    
    # Ensure published date input is correct formatted
    date_check = True
    while date_check:
        # ensure that input can be converted to datetime object
        try:
            published_date = datetime.datetime.strptime(input('When was the book published? Please use dd/mm/yyyy '), fmt)
        except ValueError:
            input('''The published date is in the incorrect format. Make sure to use dd/mm/yyyy. E.g. 31/01/1996. 
                     \rPress Enter to continue''')
        else:
            date_check = False

    # Ensure price input is correct formatted
    price_check = True
    while price_check:
        raw_price = input('What is the price of the book? Format eg. 12.34 ')
        if re.match(price_regex, raw_price ):
            price = float(raw_price) * 100
            price_check = False

    add_book(title, author, published_date, price)

# add book
def add_book(title, author, published_date, price):
    # Create new book and add to db
    book = Book(title = title, author = author, published_date = published_date, price = price)
    session.add(book)
    session.commit()

# edit books
def edit_books(book):
    # Print book
    print(f'EDIT: {book}')
    book.title = input('What is the new title? ')
    book.author = input('Who is the new author? ')
    
    # Ensure published date input is correct formatted
    date_check = True
    while date_check:
        # ensure that input can be converted to datetime object
        try:
            book.published_date = datetime.datetime.strptime(input('When was the book published? Please use dd/mm/yyyy '), fmt)
        except ValueError:
            input('''The published date is in the incorrect format. Make sure to use dd/mm/yyyy. E.g. 31/01/1996. 
                     \rPress Enter to continue''')
        else:
            date_check = False

    # Ensure price input is correct formatted
    price_check = True
    while price_check:
        raw_price = input('What is the new price of the book? Format eg. 12.34 ')
        if re.match(price_regex, raw_price ):
            book.price = float(raw_price) * 100
            price_check = False

    session.add(book)
    session.commit()

    





# delete books
def delete_books(book):
    choice = input(f'Delete {book}. Are you sure? y/n ').upper()
    if choice == 'N':
        return
    if choice == 'Y':
        session.delete(book)
        session.commit()
    else:
        input('Invalid choice, pree Enter to try again')
        delete_books(book)


# search books
def search(column, search_term):
    return session.query(Book).filter(getattr(Book, column).like(f'%{search_term}%')).all()

# data cleaning

# loop runs program

def add_csv():
    with open ('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            book_in_db = session.query(Book).filter(Book.title == row[0]).one_or_none()
            if book_in_db == None:
                title = row[0]
                author = row[1]
                date = datetime.datetime.strptime(row[2], "%B %d, %Y")
                price = round(float(row[3]) * 100)
                add_book(title, author, date, price)


def app():
    app_running = True
    add_csv()
    while app_running:
        choice = menu()
        if choice == '1':
            # add book
            add_books()
        elif choice == '2':
            # View all books
            # get all books
            books = session.query(Book)
            for book in books:
                print(f'ID: {book.id}, {book}')
            # select book
            # ensure book exists in db
            book_check = True
            while book_check:
                id = int(input('Select book by ID: ')) - 1
                if books[id] in books:
                    book = books[id]
                    book_check = False
                else:
                    input('Book not found. Press enter to try again')
            
            print(book)
            print('''
                    \rBOOK OPTIONS:
                    \r1) Edit book
                    \r2) Delete book''')
            choice = input('What do you want to do with this book? ')

            if choice not in ['1', '2']:
                input("Please choose one of the options above. Press 'enter' to try again")
            else:
                if choice == '1':
                    edit_books(book)
                else:
                    delete_books(book)

        elif choice == '3':
            # Search for book
            print('''
                  \rSearch options:
                  \r1) Search by title
                  \r2) Search by Author
                  \r3) Search by published date.
                    ''')
            choice = input("How do you want to search? ")
            query = input("Enter you search term ")
            if choice not in ['1', '2', '3']:
                input("Please choose one of the options above. Press 'enter' to try again")
            else:
                if choice == '1':
                    print(search('title', query))
                elif choice == '2':
                    print(search('author', query))
                else:
                    print(search('published_date', query))
                    
        elif choice == '4':
            # Analysis
            pass
        else:
            print('Goodbye')
            app_running = False
        



if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app()