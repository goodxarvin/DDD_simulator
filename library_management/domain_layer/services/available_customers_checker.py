class AvailableCustomersService:
    def customer_existing(self, customer, customer_list):
        return customer in customer_list
