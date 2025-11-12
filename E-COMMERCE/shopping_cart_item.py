from datetime import datetime

class Shopping_cart_item:
    def __init__(self, customer=None):
        self.__items = {}  # product_id -> {'product': Product, 'quantity': int}
        self.customer = customer        # The customer who owns the cart
        self.created_at = datetime.now() # Automatically record when cart was created
        self.updated_at = None          # Updated whenever cart changes
        self.discount = 0.0             # Any discount applied to the cart
        self.currency = "UGX"           # Currency for price display
        self.status = "Active"           # Could be "Active", "Checked Out", "Abandoned"


    def add_item(self, product, quantity):
        pid = product.id
        
        if pid in self.__items:
            self.__items[pid]['quantity'] += quantity
            
            message = f"Updated {product.name} quantity to {self.__items[pid]['quantity']}."
            
        else:
            self.__items[pid] = {
                'product': product,
                'quantity': quantity
            }
            
            message = f"Added {product.name} to cart."
        
        self.updated_at = datetime.now()
        return f"{message} on {self.updated_at}"

    @property
    def items(self):
        return self.__items

    def remove_item(self, product_id):
        if product_id in self.__items:
            
            removed = self.__items.pop(product_id)
            
            self.updated_at = datetime.now()
            
            return f"Removed {removed['product'].name} from cart."
        
        else:
            return "Item not found in cart."

    def calculate_total(self):
        total = 0
        
        for entry in self.__items.values():
            total += entry['product'].price * entry['quantity']
        return total

