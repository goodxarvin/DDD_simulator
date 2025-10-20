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
