from shopping_cart_item import Shopping_cart_item
from product import Product
from customer import Customer

p1 = Product('date', 'eats', 2000, 5, 'kiiki', 'musa', 'fruit')
p1.set_id('100')

c1 = Customer('adnan', 'musa', 'adnanmusa@gmail.com', '0700000000', 'nairobi')
c1.set_id('500')

cart_item = Shopping_cart_item(c1)
cart_item.add_item(p1, 3)


total = cart_item.calculate_total() 
print(f"Total cart amount: {total}")




