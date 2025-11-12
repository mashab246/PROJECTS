from shopping_cart_item import Shopping_cart_item
from product import Product
from customer import Customer
from order_item import Order_item
from order import Order
from vendor import Vendor
from inventory_manager import InventoryManager

vendor_1 = Vendor('ADNAN', '0753194495', 'makindye')

p1 = Product('date', 'eats', 2000, 5, 'kiiki', vendor_1, 'fruit')
p1.set_id('100')
# print(p1.id)
# print(p1.__str__())

order_1 = Order('100', 'Musa', 'Processing')

order_item_1 = Order_item(2, p1)

# print(order_1.add_item(p1, 4))


# p2 = Product('mango', 'eats', 3000, 10, 'kiiki', 'musa', 'fruit')
# p2.set_id('200')

c1 = Customer('adnan', 'musa', 'adnanmusa@gmail.com', '0700000000', 'nairobi')
c1.set_id('500')

cart_item = Shopping_cart_item(c1)
# print(cart_item.add_item(p1, 3))
# cart_item.add_item(p2, 2)

# Product.update_available_stock(p1, 3, 'subtract')
# Product.update_available_stock(p2, 2, 'subtract')

# cart_item.add_item(p2, 4)
# Product.update_available_stock(p2, 4, 'subtract')

# cart_item.add_item(p2, 6)
# Product.update_available_stock(p2, 6, 'subtract')

store = InventoryManager()

print(store.add_product(p1, p1.available_stock, p1.name))

print(store.update_stock(p1.id, 5, "add" ))

print(store.update_stock(p1.id, 2, "subtract" ))

print(store.update_stock(p1.id, 5, "ad" ))

print(store.get_stock(p1.id))





