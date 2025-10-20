from library_management.domain_layer.interface.inrfastructure_interface import RepoInterface
from library_management.domain_layer.entities.books import Book
from library_management.domain_layer.entities.customers import Customer


class BookRepoInfrastructure(RepoInterface):
    def __init__(self):
        self.books_data = []
        self.customers_data = []

    def add_book(self, title, writer, ISBN):
        self.books_data.append(Book(title, writer, ISBN))

    def add_library_member(self, name, register_id):
        self.customers_data.append(Customer(name, register_id))

    def rent_book(self, customer_register_id, book_title, book_writer, book_ISBN):
        wanted_book = Book(book_title, book_writer, book_ISBN)
        if self.__check_if_book_not_rented(wanted_book):
            renting_customer = None
            for customer in self.customers_data:
                if customer.register_id == customer_register_id:
                    renting_customer = customer

            if renting_customer:

                for available_book in self.books_data:
                    if wanted_book == available_book:
                        renting_customer.books_rented.append(available_book)
                        return available_book
                return "book existing error"
            return "customer error"
        return "book renting error"

    def __check_if_book_not_rented(self, wanted_book: Book):
        for customer in self.customers_data:
            if wanted_book in customer.books_rented:
                return False

        return True
