class Order_item:
    def __init__(self, quantity, order, product):
        self.product = product
        self.quantity = quantity
        self.order = order
        self.__amount = 0
        
    def __str__(self):
        return f"order owner : {self.order.customer} - order number : {self.order.order_no} - status : {self.order.status}"
        
    @property
    def amount(self):
        return self.__amount
    
    
    def calculate_amount(self):
        self.__amount = self.product.price * self.quantity
        
        return self.__amount