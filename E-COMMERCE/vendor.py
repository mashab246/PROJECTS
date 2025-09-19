class Vendor:
    def __init__(self, name, contact, address):
        self.name = name
        self.contact = contact
        self.address = address
        self.__id = self.set_id(id)
           
    def __str__(self):
        return f"Vendor Name: {self.name}, Contact: {self.contact}, Address: {self.address}"
    
    def set_id(self, id):
        self.__id = id
    
    @property
    def id(self):
        return self.__id
    
    def update_info(self, new_name, new_contact, new_address):
        self.name = new_name
        self.contact = new_contact
        self.address = new_address
        
        