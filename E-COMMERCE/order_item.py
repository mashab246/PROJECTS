from product import Product

class Order_item:
    def __init__(self, quantity, price, order, amount):
        self.product = Product()
        self.quantity = quantity
        self.price = price
        self.order = order
        self.__amount = amount
        
    @property
    def amount(self):
        return self.__amount
    
    
    def calculate_amount(self):
        self.__amount = self.price * self.quantity
        
        return self.__amount