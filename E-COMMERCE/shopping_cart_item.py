from  order_item import Order_item
class Shopping_cart_item:
    def __init__(self, customer):
        self.__items = {}
        self.customer = customer
        
    def add_item(self, product, quantity):
        if product.id in self.__items:
            self.__items[product.id]['quantity'] += quantity
            return f"Updated {product.name} quantity to {self.__items[product.id]['quantity']}."
        else:
            new_item = Order_item(product, quantity, product.price)
            self.__items[product.id] = new_item
            return f"Added {product.name} to cart."
    
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
            
            