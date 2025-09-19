class Product:
    def __init__(self, name, description, price, stock_quantity, brand, vendor, category):
        self.__id = self.set_id(id)
        self.name = name
        self.description = description
        self.price = price
        self.stock_quantity = stock_quantity
        self.brand = brand
        self.vendor = vendor
        self.category =category
        
    def set_id(self, id):
        self.__id = id
        
    @property
    def id(self):
        return self.__id
    
    def get_details(self):
        details = {
            "id" : self.id,
            "name" : self.name,
            "description" : self.description,
            "price" : self.price,
            "brand" : self.brand,
            "stock_quantity" : self.stock_quantity,
            "vendor" : self.vendor,
            "category" : self.category
        }
        return details
    
    def update_stock(self, quantity,operation):
        if operation == "add":
            self.stock_quantity += quantity
            return f"Stock increased by {quantity}. New stock: {self.stock_quantity}."
        elif operation == "subtract":
            if quantity > self.stock_quantity:
                return f"Error: Insufficient stock to subtract the requested quantity. Current stock: {self.stock_quantity}."
            self.stock_quantity -= quantity
            return f"Stock decreased by {quantity}. New stock: {self.stock_quantity}."
        else:
            return "Error: Invalid operation. Use 'add' or 'subtract'."
        
        
    def __str__(self):
        return f"Product(ID:{self.id}, Name: {self.name}, Price: {self.price}, Stock: {self.stock_quantity})"