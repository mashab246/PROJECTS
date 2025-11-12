class InventoryManager:
    def __init__(self):
        self.products_stock = {}

    def add_product(self, product, stock, name):
        self.products_stock[product.id] = {"product": product, "stock": stock, "name": name}
        
       

        return f"Product '{product.name}' added to inventory with {stock} units."

    def update_stock(self, product_id, quantity, operation):
        if product_id not in self.products_stock:
            return f"Error: Product with ID {product_id} not found in inventory."

        # Sync the Product's available stock to match the inventory
        # Adjust only if there’s a difference
        # stock_difference = stock - product.available_stock
        
        # if stock_difference != 0:
        #     product.update_available_stock(stock_difference)
        
        product_entry = self.products_stock[product_id]
        product = product_entry["product"]
        current_stock = product_entry["stock"]

        if operation == "add":
            new_stock = current_stock + quantity
            product_entry["stock"] = new_stock
            product.update_available_stock(quantity)
            
            return f"Stock increased by {quantity}. New stock: {new_stock}."
        
        elif operation == "subtract":
            if quantity > current_stock:
                return f"Error: Insufficient stock to subtract the requested quantity. Current stock: {current_stock}."
            
            new_stock = current_stock - quantity
            product_entry["stock"] = new_stock
            product.update_available_stock(-quantity)
            
            return f"Stock decreased by {quantity}. New stock: {new_stock}."
        
        else:
            return "Error: Invalid operation. Use 'add' or 'subtract'."

    def get_stock(self, product_id):
        if product_id in self.products_stock:
            return f"Product {self.products_stock[product_id]["name"]} has quantity of {self.products_stock[product_id]["stock"]}"
        return f"Error: Product with ID {product_id} not found in inventory."