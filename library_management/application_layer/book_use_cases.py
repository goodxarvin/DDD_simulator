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
