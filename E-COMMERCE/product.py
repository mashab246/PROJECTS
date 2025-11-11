from category import Category

class Product:
    def __init__(self, name, description, price, available_stock, brand, vendor, category:Category):
        self.__id = ""
        self.name = name
        self.description = description
        self.price = price
        self.__available_stock =available_stock
        self.brand = brand
        self.vendor = vendor
        self.category =category
        
    def set_id(self, id):
        self.__id = id
        
        return self.__id
        
    @property
    def id(self):
        return self.__id
    
    @property
    def available_stock(self):
        return self.__available_stock
    
    def update_available_stock(self, quantity_added):
        self.__available_stock += quantity_added
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
        return f"Product(ID:{self.id}, Name: {self.name}, Price: {self.price}, Vendor : {self.vendor.name})"


class Electronics(Product):
    def __init__(self, name, description, price, available_stock, brand, vendor, category, watts, voltage, guarantee_period):
        super().__init__(name, description, price, available_stock, brand, vendor, category)
  
        self.watts = watts
        self.voltage = voltage
        self.guarantee_period = guarantee_period
        
    def get_details(self):
        details = super().get_details()
        details["watts"] = self.watts
        details["voltage"] = self.voltage
        details["guarantee_period"] = self.guarantee_period
        
        return details

        
class Clothes(Product):
    def __init__(self, name, description, price, available_stock, brand, vendor, category, size, material,color,):
        super().__init__(name, description, price, available_stock, brand, vendor, category)
        
        self.size = size
        self.material = material
        self.color = color
        
    def get_details(self):
        details = super().get_details()
        details["size"] = self.size
        details["material"] = self.material
        details["color"] = self.color
        
        return details
    
        
        
class Shoes(Product):
    def __init__(self, name, description, price, available_stock, brand, vendor, category, size, type, color):
        super().__init__(name, description, price, available_stock, brand, vendor, category)
        
        self.size = size
        self.type = type
        self.color = color
        
    def get_details(self):
        details = super().get_details()
        details["size"] = self.size
        details["type"] = self.type
        details["color"] = self.color
        
        return details
    
    