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
