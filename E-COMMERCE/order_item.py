class Order_item:
    def __init__(self, product, quantity, rate):
        self.__product = product
        self.__quantity = quantity
        self.rate = rate
        
    @property
    def product(self):
        return self.__product
    
    @property
    def quantity(self):
        return self.__quantity
    
    def get_total_price(self):
        return self.rate * self.quantity
            