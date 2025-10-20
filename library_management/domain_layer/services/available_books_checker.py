class AvailableBooksService:
    def book_availabality(self, book, book_list):
        return book in book_list