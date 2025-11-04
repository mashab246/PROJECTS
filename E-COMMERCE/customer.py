class Customer:
    def __init__(self, first_name, last_name, email, contact, address, cart):
        self.__id = self.set_id(id)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.contact = contact
        self.address = address
        self.cart = cart
        
        
    def set_id(self, id):
        self.__id = id
        return self.__id
        
    @property
    def id(self):
        return self.__id
    
    def add_to_cart(self, product, quantity):
        return self.cart.add_item(product, quantity)
    
    def remove_from_cart(self, product_id):
        return self.cart.remove_item(product_id)
        
    def update_info(self, new_first_name, new_last_name, new_email, new_contact, new_address):
        self.first_name = new_first_name
        self.last_name = new_last_name
        self.email = new_email
        self.contact = new_contact
        self.address = new_address
        
    
    def __str__(self):
        return f"Customer(ID:{self.id}, Name: {self.first_name} {self.last_name})"