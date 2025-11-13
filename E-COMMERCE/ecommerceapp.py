import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from inventory_manager import InventoryManager
from product import Product, Category
from shopping_cart_item import Shopping_cart_item
from order import Order


class ECommerceApp:
    def __init__(self, window, inventory_manager, cart):
        self.window = window
        self.window.title("🛍️ Customer E-Commerce Portal")
        self.window.geometry("950x600")
        self.window.configure(bg="#f9f9f9")

        self.inventory = inventory_manager
        self.cart = cart
        self.orders = []  # Store completed orders

        # ---- Header ----
        header_frame = tk.Frame(window, bg="#0078D4")
        header_frame.pack(fill=tk.X)
        tk.Label(
            header_frame,
            text=f"🛍️ Welcome to the E-Commerce Portal, {self.cart.customer}!",
            bg="#0078D4",
            fg="white",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        # ---- Top Buttons ----
        top_frame = tk.Frame(window, bg="#f9f9f9")
        top_frame.pack(pady=10)

        tk.Label(top_frame, text="Search Product:", bg="#f9f9f9", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(top_frame, width=40, font=("Arial", 12))
        
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(top_frame, text="Search", command=self.search_product,
                  bg="#0078D4", fg="white", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(top_frame, text="Show All", command=self.show_all_products,
                  bg="#666", fg="white", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(top_frame, text="🛒 View Cart", command=self.show_cart_window,
                  bg="#00A36C", fg="white", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=10)
        
        tk.Button(top_frame, text="📦 View Orders", command=self.show_orders_window,
                  bg="#FFB100", fg="white", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=10)

        # ---- Product Table ----
        columns = ("ID", "Name", "Description", "Brand", "Category", "Price", "Stock")
        self.tree = ttk.Treeview(window, columns=columns, show="headings", height=15)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=120)

        self.tree.bind("<Double-1>", self.show_product_details)
        self.load_products()

    # ---------------------------------------------------------
    # Product Management
    # ---------------------------------------------------------
    def load_products(self):
        """Load only available products (stock > 0) — customer-facing view."""
        self.tree.delete(*self.tree.get_children())
        for data in self.inventory.products_stock.values():
            product = data["product"]
            stock = data["stock"]
            if stock <= 0:
                continue  # hide out-of-stock items from customer view
            self.tree.insert(
                "",
                "end",
                values=(
                    product.id,
                    product.name,
                    product.description[:40] + "..." if len(product.description) > 40 else product.description,
                    product.brand,
                    getattr(product.category, "name", str(product.category)),
                    f"${product.price:.2f}",
                    stock,
                ),
            )

    def load_all_products(self):
        """Load all products including out-of-stock (admin/explicit view)."""
        self.tree.delete(*self.tree.get_children())
        for data in self.inventory.products_stock.values():
            product = data["product"]
            stock = data["stock"]
            self.tree.insert(
                "",
                "end",
                values=(
                    product.id,
                    product.name,
                    product.description[:40] + "..." if len(product.description) > 40 else product.description,
                    product.brand,
                    getattr(product.category, "name", str(product.category)),
                    f"${product.price:.2f}",
                    stock,
                ),
            )

    def search_product(self):
        keyword = self.search_entry.get().lower()
        if not keyword:
            messagebox.showinfo("Search", "Please enter a product name or brand.")
            return

        self.tree.delete(*self.tree.get_children())
        found = False
        for data in self.inventory.products_stock.values():
            product = data["product"]
            stock = data["stock"]
            if keyword in product.name.lower() or keyword in product.brand.lower():
                found = True
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        product.id,
                        product.name,
                        product.description[:40] + "..." if len(product.description) > 40 else product.description,
                        product.brand,
                        getattr(product.category, "name", str(product.category)),
                        f"${product.price:.2f}",
                        stock,
                    ),
                )
        if not found:
            messagebox.showinfo("Search", f"No products found matching '{keyword}'.")

    def show_all_products(self):
        self.search_entry.delete(0, tk.END)
        self.load_all_products()

    # ---------------------------------------------------------
    # Product Details + Add to Cart
    # ---------------------------------------------------------
    def show_product_details(self, event):
        selected = self.tree.focus()
        if not selected:
            return

        values = self.tree.item(selected, "values")
        product_id = values[0]

        # Robust lookup: compare IDs as strings in case of type differences
        product_entry = None
        for key, entry in self.inventory.products_stock.items():
            if str(key) == str(product_id) or str(entry.get("product").id) == str(product_id):
                product_entry = entry
                break

        if not product_entry:
            messagebox.showerror("Error", "Product not found in inventory.")
            return

        product = product_entry["product"]
        stock = product_entry["stock"]

        detail_window = tk.Toplevel(self.window)
        detail_window.title(f"Product Details — {product.name}")
        detail_window.geometry("400x400")
        detail_window.configure(bg="#ffffff")

        tk.Label(detail_window, text=product.name, font=("Arial", 16, "bold"),
                 bg="#ffffff", fg="#0078D4").pack(pady=10)
        tk.Label(detail_window, text=f"Product ID: {product.id}", bg="#ffffff", font=("Arial", 11)).pack(pady=2)
        tk.Label(detail_window, text=f"Brand: {product.brand}", bg="#ffffff", font=("Arial", 11)).pack(pady=2)
        tk.Label(detail_window, text=f"Category: {getattr(product.category, 'name', product.category)}",
                 bg="#ffffff", font=("Arial", 11)).pack(pady=2)
        tk.Label(detail_window, text=f"Price: ${product.price:.2f}", bg="#ffffff", font=("Arial", 11)).pack(pady=2)
        tk.Label(detail_window, text=f"Available Stock: {stock}", bg="#ffffff", font=("Arial", 11)).pack(pady=2)

        tk.Label(detail_window, text="Description:", bg="#ffffff", font=("Arial", 12, "bold")).pack(pady=(10, 0))
        desc_box = tk.Text(detail_window, wrap=tk.WORD, height=5, width=45, bg="#f5f5f5", font=("Arial", 10))
        desc_box.insert(tk.END, product.description)
        desc_box.config(state=tk.DISABLED)
        desc_box.pack(pady=5)

        qty_frame = tk.Frame(detail_window, bg="#ffffff")
        qty_frame.pack(pady=10)
        tk.Label(qty_frame, text="Quantity:", bg="#ffffff", font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
        qty_var = tk.IntVar(value=1)
        tk.Entry(qty_frame, textvariable=qty_var, width=5, font=("Arial", 11)).pack(side=tk.LEFT)

        def add_to_cart():
            qty = qty_var.get()
            if qty <= 0:
                messagebox.showerror("Invalid Quantity", "Enter a positive quantity.")
                return
            if qty > stock:
                messagebox.showerror("Stock Error", f"Only {stock} units available.")
                return
            msg = self.cart.add_item(product, qty)
            messagebox.showinfo("Cart", msg)
            detail_window.destroy()

        tk.Button(detail_window, text="Add to Cart", command=add_to_cart,
                  bg="#0078D4", fg="white", font=("Arial", 11, "bold")).pack(pady=10)
        tk.Button(detail_window, text="Close", command=detail_window.destroy,
                  bg="#999", fg="white", font=("Arial", 10, "bold")).pack(pady=5)

    # ---------------------------------------------------------
    # Shopping Cart Window
    # ---------------------------------------------------------
    def show_cart_window(self):
        cart_window = tk.Toplevel(self.window)
        cart_window.title("🛒 Shopping Cart")
        cart_window.geometry("700x400")
        cart_window.configure(bg="#ffffff")

        tk.Label(cart_window, text=f"{self.cart.customer}'s Shopping Cart",
                 font=("Arial", 16, "bold"), bg="#ffffff", fg="#0078D4").pack(pady=10)

        columns = ("Product", "Price", "Quantity", "Subtotal")
        cart_table = ttk.Treeview(cart_window, columns=columns, show="headings", height=10)
        cart_table.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        for col in columns:
            cart_table.heading(col, text=col)
            cart_table.column(col, anchor=tk.CENTER, width=150)
            
        total_label = tk.Label(cart_window, text=f"Total: ${self.cart.calculate_total():.2f}",
                                font=("Arial", 14, "bold"), bg="#ffffff", fg="#333")
        total_label.pack(pady=5)
            
        def refresh_cart():
            cart_table.delete(*cart_table.get_children())
            total = 0
            for entry in self.cart.items.values():
                product = entry["product"]
                quantity = entry["quantity"]
                subtotal = product.price * quantity
                total += subtotal
                cart_table.insert("", "end", values=(product.name, f"${product.price:.2f}", quantity, f"${subtotal:.2f}"))
            total_label.config(text=f"Total: ${total:.2f}")

           

        button_frame = tk.Frame(cart_window, bg="#ffffff")
        button_frame.pack(pady=10)
        
        def remove_selected():
            selected = cart_table.focus()
            if not selected:
                messagebox.showwarning("Select Item", "Please select an item to remove.")
                return

            values = cart_table.item(selected, "values")
            product_name = values[0]

            # Find matching product in cart and remove it
            for pid, entry in list(self.cart.items.items()):
                if entry["product"].name == product_name:
                    self.cart.remove_item(pid)
                    messagebox.showinfo("Removed", f"Removed {product_name} from cart.")
                    refresh_cart
                    break
                
        def checkout():
            if not self.cart.items:
                messagebox.showwarning("Empty Cart", "Your cart is empty.")
                return
            else:
                order_no = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                order = Order(order_no, self.cart.customer, "Processing")
                order.purchased_items = []

            for entry in self.cart.items.values():
                product = entry["product"]
                qty = entry["quantity"]
                self.inventory.update_stock(product.id, qty, "subtract", )
                order.purchased_items.append((product, qty, product.price))

            total_cost = self.cart.calculate_total()
            order.total_amount = total_cost
            order.date_created = datetime.now()
            self.orders.append(order)

            self.cart = Shopping_cart_item(customer=order.customer)
            self.load_products()
            messagebox.showinfo("Checkout Complete", f"Order {order_no} placed successfully!\nTotal: ${total_cost:.2f}")
            cart_window.destroy()
            
        tk.Button(button_frame, text="Remove Selected", command=remove_selected,
              bg="#FF5C5C", fg="white", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="Checkout", command=checkout,
                bg="#00A36C", fg="white", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Close", command=cart_window.destroy,
                bg="#999", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)
        
        refresh_cart()

    # ---------------------------------------------------------
    # Orders Window
    # ---------------------------------------------------------
    def show_orders_window(self):
        orders_window = tk.Toplevel(self.window)
        orders_window.title("📦 My Orders")
        orders_window.geometry("700x400")
        orders_window.configure(bg="#ffffff")

        tk.Label(orders_window, text=f"{self.cart.customer}'s Order History",
                 font=("Arial", 16, "bold"), bg="#ffffff", fg="#FFB100").pack(pady=10)

        columns = ("Order No", "Date", "Total", "Status")
        order_table = ttk.Treeview(orders_window, columns=columns, show="headings", height=10)
        order_table.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        for col in columns:
            order_table.heading(col, text=col)
            order_table.column(col, anchor=tk.CENTER, width=150)

        for order in self.orders:
            date_str = order.date_created.strftime("%Y-%m-%d %H:%M:%S") if hasattr(order, "date_created") else "N/A"
            order_table.insert("", "end",
                               values=(order.order_no, date_str, f"${order.total_amount:.2f}", order.status))


# ---------------------------------------------------------
# Example Run
# ---------------------------------------------------------
if __name__ == "__main__":
    category1 = Category("Electronics", "elec products")
    category2 = Category("Clothing", "cloth products")

    inventory = InventoryManager()
    cart = Shopping_cart_item(customer="Musa Adnan")

    p1 = Product("Laptop", "High-end gaming laptop.", 1200, 10, "Asus", "VendorX", category1)
    p1.set_id("P001")
    inventory.add_product(p1, 10, p1.name)

    p2 = Product("Headphones", "Noise-cancelling wireless headphones.", 150, 15, "Sony", "VendorY", category1)
    p2.set_id("P002")
    inventory.add_product(p2, 15, p1.name)

    p3 = Product("T-Shirt", "Soft cotton T-shirt, unisex design.", 25, 30, "Nike", "VendorZ", category2)
    p3.set_id("P003")
    inventory.add_product(p3, 30, p1.name)

    window = tk.Tk()
    app = ECommerceApp(window, inventory, cart)
    window.mainloop()
