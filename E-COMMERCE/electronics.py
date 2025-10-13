from product import Product

class Electronics(Product):
    def __init__(self, name, description, price, available_stock, brand, vendor, category, watts):
        super().__init__(name, description, price, available_stock, brand, vendor, category)
  
        self.watts = watts
        
        
        
