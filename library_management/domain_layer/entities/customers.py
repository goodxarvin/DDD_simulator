class Customer:
    def __init__(self, name, register_id):
        self.name = name
        self.register_id = register_id
        self.books_rented = []

    def __eq__(self, value):
        if isinstance(value, Customer):
            return self.register_id == value.register_id
        return False
