class Category:
    def __init__(self, name):
        self.__id = ""
        self.name = name
        # self.decription = description
        
    def set_id(self, id):
        self.__id = id
        
        return self.__id
        
    @property
    def id(self):   
        return self.__id
        
    def __str__(self):
        return f"Category(ID:{self.id}, Name: {self.name})"