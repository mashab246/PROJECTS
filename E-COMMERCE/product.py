class Product:
    def __init__(self, name, description, price, available_stock, brand, vendor, category):
        self.__id = self.set_id(id)
        self.name = name
        self.description = description
        self.price = price
        self.__available_stock =available_stock
        self.brand = brand
        self.vendor = vendor
        self.category =category
        
    def set_id(self, id):
        self.__id = id
        
    @property
    def id(self):
        return self.__id
    
    @property
    def available_stock(self):
        return self.__available_stock
    
    
    def get_details(self):
        details = {
            "id" : self.id,
            "name" : self.name,
            "description" : self.description,
            "price" : self.price,
            "brand" : self.brand,
            "available_stock" : self.__available_stock,
            "vendor" : self.vendor,
            "category" : self.category
        }
        return details
        
        
    def __str__(self):
        return f"Product(ID:{self.id}, Name: {self.name}, Price: {self.price})"