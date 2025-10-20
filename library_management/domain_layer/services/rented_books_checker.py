class RentedBooksService:
    def is_book_rented(self, book, customer_list):
        for customer in customer_list:
            for book_rents in customer.books_rented:
                if book_rents == book:
                    return False
        return True
