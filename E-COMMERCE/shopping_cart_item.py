class Shopping_cart_item:
    def __init__(self):
        self.__items = {}  # product_id -> {'product': Product, 'quantity': int}


    def add_item(self, product, quantity):
        pid = product.id
        if pid in self.__items:
            self.__items[pid]['quantity'] += quantity
            return f"Updated {product.name} quantity to {self.__items[pid]['quantity']}."
        else:
            self.__items[pid] = {
                'product': product,
                'quantity': quantity
            }
            return f"Added {product.name} to cart."

    @property
    def items(self):
        return self.__items

    def remove_item(self, product_id):
        if product_id in self.__items:
            removed = self.__items.pop(product_id)
            return f"Removed {removed['product'].name} from cart."
        else:
            return "Item not found in cart."

    def calculate_total(self):
        total = 0
        for entry in self.__items.values():
            total += entry['product'].price * entry['quantity']
        return total

