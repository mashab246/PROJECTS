class InventoryManager:
    def __init__(self):
        self.products_stock = {}

    def add_product(self, product, stock):
        self.products_stock[product.id] = {"product": product, "stock": stock}

    def update_stock(self, product_id, quantity, operation):
        if product_id not in self.products_stock:
            return f"Error: Product with ID {product_id} not found in inventory."

        current_stock = self.products_stock[product_id]["stock"]

        if operation == "add":
            self.products_stock[product_id]["stock"] += quantity
            return f"Stock increased by {quantity}. New stock: {self.products_stock[product_id]['stock']}."
        elif operation == "subtract":
            if quantity > current_stock:
                return f"Error: Insufficient stock to subtract the requested quantity. Current stock: {current_stock}."
            self.products_stock[product_id]["stock"] -= quantity
            return f"Stock decreased by {quantity}. New stock: {self.products_stock[product_id]['stock']}."
        else:
            return "Error: Invalid operation. Use 'add' or 'subtract'."

    def get_stock(self, product_id):
        if product_id in self.products_stock:
            return self.products_stock[product_id]["stock"]
        return f"Error: Product with ID {product_id} not found in inventory."