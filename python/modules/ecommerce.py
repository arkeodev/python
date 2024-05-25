class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Cart:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def total(self):
        return sum(product.price for product in self.products)

    def apply_discount(self, discount):
        total = self.total()
        return total - (total * discount / 100)

class PaymentProcessor:
    def process_payment(self, amount):
        # Simulate payment processing
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")
        return True