from product import Product

class Clothes(Product):
    def __init__(self, name, description, price, available_stock, brand, vendor, category, size, material):
        super().__init__(name, description, price, available_stock, brand, vendor, category)
        
        self.size = size
        self.material = material
        