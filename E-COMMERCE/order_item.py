class Order_item:
    def __init__(self, product, quantity, price, order, amount):
        self.product = product
        self.quantity = quantity
        self.price = price
        self.order = order
        self.__amount = amount
        
    @property
    def amount(self):
        return self.__amount
    
    
    def calculate_amount(self, amount):
        amount = self.price * self.quantity
        self.__amount = amount
        
        return amount