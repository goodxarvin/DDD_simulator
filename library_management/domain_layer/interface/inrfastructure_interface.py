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
