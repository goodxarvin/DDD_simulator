# domain_layer/entities/books.py:

class Book:
    def __init__(self, title, writer, ISBN):
        self.title = title
        self.writer = writer
        self.ISBN = ISBN

    def __eq__(self, value):
        if isinstance(value, Book):
            return all((self.title == value.title, self.writer == value.writer, self.ISBN == value.ISBN))

        return False

# domain_layer/entities/customers.py:

class Customer:
    def __init__(self, name, register_id):
        self.name = name
        self.register_id = register_id
        self.books_rented = []

    def __eq__(self, value):
        if isinstance(value, Customer):
            return self.register_id == value.register_id
        return False
    
# domain_layer/interface/infrastructure_interface.py:

from abc import ABC, abstractmethod


class RepoInterface(ABC):
    @abstractmethod
    def add_book(self, book_obj):
        pass

    @abstractmethod
    def add_library_member(self, customer_obj):
        pass

    @abstractmethod
    def rent_book(self):
        pass

    @abstractmethod
    def show_all_info(self):
        pass


# domain_layer/services/available_books_checker.py:

class AvailableBooksService:
    def book_availabality(self, book, book_list):
        return book in book_list
    
# domain_layer/services/available_customers_checker.py:

class AvailableCustomersService:
    def customer_existing(self, customer, customer_list):
        return customer in customer_list


# domain_layer/services/rented_books_checker.py:

class RentedBooksService:
    def is_book_rented(self, book, customer_list):
        for customer in customer_list:
            for book_rents in customer.books_rented:
                if book_rents == book:
                    return False
        return True

# application_layer/book_use_cases.py:

from library_management.infrastructure_layer.book_infrastructure import BookRepoInfrastructure
from library_management.domain_layer.entities.books import Book
from library_management.domain_layer.entities.customers import Customer
from library_management.domain_layer.services.rented_books_checker import RentedBooksService
from library_management.domain_layer.services.available_books_checker import AvailableBooksService
from library_management.domain_layer.services.available_customers_checker import AvailableCustomersService


class AddBook:
    def __init__(self, infras_repo: BookRepoInfrastructure):
        self.infras_repo = infras_repo

    def execute(self, title, writer, ISBN):
        self.infras_repo.add_book(Book(title, writer, ISBN))
        print("book added to database successfully\n")


class AddCustomer:
    def __init__(self, infras_repo: BookRepoInfrastructure):
        self.infras_repo = infras_repo

    def execute(self, name, register_id):
        self.infras_repo.add_library_member(Customer(name, register_id))
        print("customer added to database successfully\n")


class RentBooks:
    def __init__(self, infras_repo: BookRepoInfrastructure):
        self.infras_repo = infras_repo

    def execute(self, customer_register_id, book_title, book_writer, book_ISBN):
        customer = Customer("", customer_register_id)
        wanted_book = Book(book_title, book_writer, book_ISBN)
        books, customers = self.infras_repo.rent_book()
        is_book_available = AvailableBooksService().book_availabality(wanted_book, books)
        is_customer_exist = AvailableCustomersService(
        ).customer_existing(customer, customers)
        is_book_rented = RentedBooksService().is_book_rented(wanted_book, customers)
        conditions_for_renting = all(
            (is_book_available, is_customer_exist, is_book_rented))
        if conditions_for_renting:
            for data_base_customer in customers:
                if customer == data_base_customer:
                    data_base_customer.books_rented.append(wanted_book)
                    print(
                        f"""book info:
book title: {wanted_book.title}
book writer: {wanted_book.writer}
book ISBN: {wanted_book.ISBN}
got rented by the customer: {data_base_customer.name} and register id: {data_base_customer.register_id}
""")
        elif not is_book_available:
            print("book is not available in database\n")

        elif not is_book_rented:
            print("book is rented\n")

        else:
            print("customer is not exist in database\n")


class ShowAllIinfo:
    def __init__(self, infras_repo: BookRepoInfrastructure):
        self.infras_repo = infras_repo

    def execute(self):
        raw_customers, raw_books, raw_renting_info = self.infras_repo.show_all_info()
        all_customers = f"all customers: {[[cus.name, cus.register_id] for cus in raw_customers]}\n"
        all_books = f"all books: {[[book.title, book.writer, book.ISBN] for book in raw_books]}\n"
        rented_books_details = [{"renter_name": renter_info["renter"],
                                 "renter_id": renter_info["renter_id"],
                                 "title": book.title,
                                 "writer": book.writer,
                                 "ISBN": book.ISBN}
                                for renter_info in raw_renting_info if renter_info["books_rented"] for book in renter_info["books_rented"]]
        books_renting_info = f"rentings info:\n{rented_books_details}"
        return all_books + all_customers + books_renting_info


# infrastructure_layer/book_infrastructure.py:

from library_management.domain_layer.interface.inrfastructure_interface import RepoInterface
from library_management.domain_layer.entities.books import Book
from library_management.domain_layer.entities.customers import Customer


class BookRepoInfrastructure(RepoInterface):
    def __init__(self):
        self.books_data = []
        self.customers_data = []

    def add_book(self, book_obj):
        self.books_data.append(book_obj)

    def add_library_member(self, customer_obj):
        self.customers_data.append(customer_obj)

    def rent_book(self):
        return self.books_data, self.customers_data

    def show_all_info(self):
        rented_books = [{"renter": customer.name,
                         "renter_id": customer.register_id,
                         "books_rented": customer.books_rented} for customer in self.customers_data]
        return self.customers_data, self.books_data, rented_books


# presentation_layer/main.py:

from library_management.application_layer.book_use_cases import AddBook, AddCustomer, RentBooks, ShowAllIinfo
from library_management.infrastructure_layer.book_infrastructure import BookRepoInfrastructure


if __name__ == "__main__":
    infrastructure = BookRepoInfrastructure()
    add_book = AddBook(infrastructure)
    add_customer = AddCustomer(infrastructure)
    cus1_rent_book = RentBooks(infrastructure)
    cus2_rent_book = RentBooks(infrastructure)
    cus3_rent_book = RentBooks(infrastructure)
    show_all = ShowAllIinfo(infrastructure)

    books = [("book1", "book1", "10"),
             ("book2", "book2", "20"),
             ("book3", "book3", "30"),
             ("book4", "book4", "40")]
    customers = [("cus1", "1"),
                 ("cus2", "2"),
                 ("cus3", "3"),
                 ("cus4", "4")]
    for book, customer in zip(books, customers):
        add_book.execute(book[0], book[1], book[2])
        add_customer.execute(customer[0], customer[1])

    cus1_rent_book.execute("1", "book1", "book1", "10")
    cus1_rent_book.execute("1", "book1", "book1", "10")
    cus2_rent_book.execute("2", "book2", "book2", "20")
    cus2_rent_book.execute("2", "book3", "book3", "30")
    cus1_rent_book.execute("3", "book30", "book3", "30")
    cus3_rent_book.execute("5", "book4", "book4", "40")
    cus3_rent_book.execute("3", "book4", "book4", "40")

    print(show_all.execute())
