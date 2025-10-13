from product import Product

class Shopping_cart_item:
    def __init__(self, customer):
        self.__items = {}
        self.customer = customer
        
    def add_item(self, product , quantity):
        if product.id in self.__items:
            self.__items[Product.id]['quantity'] += quantity
            return f"Updated {Product.name} quantity to {self.__items[product.id]['quantity']}."
        else:
            
            self.__items[Product.id] = {
            'id': Product.id,
            'name': Product.name,
            'price': Product.price,
            'quantity': quantity
        }
        return f"Added {Product.name} to cart."
    
        
    @property
    def items(self):
        return self.__items
    
    def remove_item(self, product_id,):
        if product_id in self.__items:
            removed_item = self.__items.pop(product_id)
            return f"Removed {removed_item.product.name} from cart."
        else:
            return "Item not found in cart."
    
    def calculate_total(self):
        total = 0
        for item in self.__items.values():
            total += item.product.price * item.quantity
        return total
            
            