class Book:
    def __init__(self, title, writer, ISBN):
        self.title = title
        self.writer = writer
        self.ISBN = ISBN

    def __eq__(self, value):
        if isinstance(value, Book):
            return all((self.title == value.title, self.writer == value.writer, self.ISBN == value.ISBN))

        return False
