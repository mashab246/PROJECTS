class Order_item:
    def __init__(self, quantity, product):
        self.product = product
        self.quantity = quantity
        self.__amount = 0
               
    @property
    def amount(self):
        return self.__amount
    
    
    def calculate_amount(self):
        self.__amount = self.product.price * self.quantity
        
        return self.__amount