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
        self.window.title("🛍️  Customer E-Commerce Portal") 
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
            text=f"🛍️ Welcome to the E-Commerce Shop, {self.cart.customer}!",
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
        
          
        tk.Button(top_frame, text="Add Product", command=self.open_add_product_window, fg="white", bg="navy blue", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=5)
        
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

        self.tree.bind("<Double-1>", self.show_product_details) # bind double-click to show details
        self.load_products()
        
   
        
    def open_add_product_window(self):
        # Use self.window instead of self.root
        win = tk.Toplevel(self.window)
        win.title("Add New Product")
        win.geometry("350x450")

        tk.Label(win, text="Add New Product", font=("Arial", 16, "bold")).pack(pady=10)

        # ---- Labels and Entry Widgets ----
        tk.Label(win, text="Product Name:").pack()
        name_entry = tk.Entry(win, width=30)
        name_entry.pack()

        tk.Label(win, text="Price:").pack()
        price_entry = tk.Entry(win, width=30)
        price_entry.pack()

        tk.Label(win, text="Quantity:").pack()
        qty_entry = tk.Entry(win, width=30)
        qty_entry.pack()

        tk.Label(win, text="Description:").pack()
        desc_entry = tk.Entry(win, width=30)
        desc_entry.pack()

        tk.Label(win, text="Brand:").pack()
        brand_entry = tk.Entry(win, width=30)
        brand_entry.pack()

        tk.Label(win, text="Category:").pack()
        category_entry = tk.Entry(win, width=30)
        category_entry.pack()

        tk.Label(win, text="Vendor:").pack()
        vendor_entry = tk.Entry(win, width=30)
        vendor_entry.pack()
        
      


        # ---- Save Button ----
        def save_product():
            name = name_entry.get()
            price = price_entry.get()
            qty = qty_entry.get()
            desc = desc_entry.get()
            brand = brand_entry.get()
            category_name = category_entry.get()
            vendor = vendor_entry.get()

            # Validation
            if not name or not price or not qty:
                messagebox.showerror("Error", "Name, Price and Quantity are required.")
                return

            try:
                price = float(price)
                qty = int(qty)
            except:
                messagebox.showerror("Error", "Price must be a number and Quantity must be an integer.")
                return

            # Create Category object
            category = Category(category_name)

            # Create Product object
            product = Product(
                name=name,
                description=desc,
                price=price,
                available_stock=qty,
                brand=brand,
                vendor=vendor,
                category=category
            )

            # Generate ID
            pid = self.inventory.generate_product_id()
            product.set_id(pid)

            # Add to inventory
            self.inventory.add_product(product, qty)

            messagebox.showinfo("Success", f"{name} added to inventory!")
            self.load_products()   # Refresh table
            win.destroy()          # Close window
        
        tk.Button(win, text="Save Product", command=save_product,
            bg="#0078D4", fg="white", font=("Arial", 12, "bold")).pack(pady=20)
            
   


        


    # ---------------------------------------------------------
    # Product Management
    # ---------------------------------------------------------
    def load_products(self):
        """Load only available products (stock > 0) — customer-facing view."""
        self.tree.delete(*self.tree.get_children())  #clear existing rows in the treeview
        for data in self.inventory.products_stock.values():
            product = data["product"]
            stock = data["stock"]
            if stock <= 0:
                continue  # hide out-of-stock items from customer view
            self.tree.insert(  # insert a row for each in-stock product
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
        self.tree.delete(*self.tree.get_children()) # clear treeview
        for data in self.inventory.products_stock.values(): #iterate through all inventory entries
            product = data["product"]
            stock = data["stock"]
            self.tree.insert(   # insert row regardless of stock level
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
        keyword = self.search_entry.get().lower()   # read search entry and lower-case it
        if not keyword:
            messagebox.showinfo("Search", "Please enter a product name or brand.")
            return

        self.tree.delete(*self.tree.get_children()) # clear treeview
        found = False
        for data in self.inventory.products_stock.values(): #iterate inventory and check name/brand
            product = data["product"]
            stock = data["stock"]
            if keyword in product.name.lower() or keyword in product.brand.lower():
                found = True
                self.tree.insert(   # insert matching rows
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
        self.search_entry.delete(0, tk.END)   # clear search box
        self.load_all_products()

    # ---------------------------------------------------------
    # Product Details + Add to Cart
    # ---------------------------------------------------------
    def show_product_details(self, event):
        selected = self.tree.focus()   # get currently selected item id in treeview
        if not selected:
            return

        values = self.tree.item(selected, "values")  #get row values
        product_id = values[0]  #first column is product id

        # Robust lookup: compare IDs as strings in case of type differences
        product_entry = None
        for key, entry in self.inventory.products_stock.items():   #search inventory for matching id
            if str(key) == str(product_id) or str(entry.get("product").id) == str(product_id):
                product_entry = entry
                break

        if not product_entry:
            messagebox.showerror("Error", "Product not found in inventory.")
            return

        product = product_entry["product"]   #retrieve product
        stock = product_entry["stock"]  # retrieve stock count

        detail_window = tk.Toplevel(self.window)  #open a top-level window for details
        detail_window.title(f"Product Details — {product.name}")
        detail_window.geometry("400x400")
        detail_window.configure(bg="#ffffff")

        tk.Label(detail_window, text=product.name, font=("Arial", 16, "bold"), bg="#ffffff", fg="#0078D4").pack(pady=10)
        
        tk.Label(detail_window, text=f"Product ID: {product.id}", bg="#ffffff", font=("Arial", 11)).pack(pady=2)
        
        tk.Label(detail_window, text=f"Brand: {product.brand}", bg="#ffffff", font=("Arial", 11)).pack(pady=2)
        
        tk.Label(detail_window, text=f"Category: {getattr(product.category, 'name', product.category)}", bg="#ffffff", font=("Arial", 11)).pack(pady=2)
        
        tk.Label(detail_window, text=f"Price: ${product.price:.2f}", bg="#ffffff", font=("Arial", 11)).pack(pady=2)
        
        tk.Label(detail_window, text=f"Available Stock: {stock}", bg="#ffffff", font=("Arial", 11)).pack(pady=2)

        tk.Label(detail_window, text="Description:", bg="#ffffff", font=("Arial", 12, "bold")).pack(pady=(10, 0))
        
        desc_box = tk.Text(detail_window, wrap=tk.WORD, height=5, width=45, bg="#f5f5f5", font=("Arial", 10)) #text widget for description
        
        desc_box.insert(tk.END, product.description) #fill description
        
        desc_box.config(state=tk.DISABLED)  #make it read-only
        
        desc_box.pack(pady=5)

        qty_frame = tk.Frame(detail_window, bg="#ffffff")
        qty_frame.pack(pady=10) # frame for quantity controls
        
        tk.Label(qty_frame, text="Quantity:", bg="#ffffff", font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
        
        qty_var = tk.IntVar(value=1) #variable to hold chosen quantity set to 1
        tk.Entry(qty_frame, textvariable=qty_var, width=5, font=("Arial", 11)).pack(side=tk.LEFT)

        def add_to_cart():
            qty = qty_var.get()   #read selected quantity
            if qty <= 0:
                messagebox.showerror("Invalid Quantity", "Enter a positive quantity.")  #validate positive
                return
            if qty > stock:
                messagebox.showerror("Stock Error", f"Only {stock} units available.")  #validate stock
                return
            msg = self.cart.add_item(product, qty)  
            messagebox.showinfo("Cart", msg)  #show result message
            detail_window.destroy()

        tk.Button(detail_window, text="Add to Cart", command=add_to_cart,
                  bg="#0078D4", fg="white", font=("Arial", 11, "bold")).pack(pady=10)
        
        tk.Button(detail_window, text="Close", command=detail_window.destroy,
                  bg="#999", fg="white", font=("Arial", 10, "bold")).pack(pady=5)

    # ---------------------------------------------------------
    # Shopping Cart Window
    # ---------------------------------------------------------
    def show_cart_window(self):
        cart_window = tk.Toplevel(self.window)  #open cart top-level window
        cart_window.title("🛒 Shopping Cart")
        cart_window.geometry("700x400")
        cart_window.configure(bg="#ffffff")

        tk.Label(cart_window, text=f"{self.cart.customer}'s Shopping Cart",
                 font=("Arial", 16, "bold"), bg="#ffffff", fg="#0078D4").pack(pady=10)

        columns = ("Product", "Price", "Quantity", "Subtotal")  #columns for cart items
        cart_table = ttk.Treeview(cart_window, columns=columns, show="headings", height=10)
        cart_table.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        for col in columns:
            cart_table.heading(col, text=col)
            cart_table.column(col, anchor=tk.CENTER, width=150)
            
        total_label = tk.Label(cart_window, text=f"Total: ${self.cart.calculate_total():.2f}",
                                font=("Arial", 14, "bold"), bg="#ffffff", fg="#333")  # label showing total
        total_label.pack(pady=5)
            
        def refresh_cart():
            cart_table.delete(*cart_table.get_children()) #clear cart display
            total = 0
            for entry in self.cart.items.values():  #iterate items in cart
                product = entry["product"]
                quantity = entry["quantity"]
                subtotal = product.price * quantity
                total += subtotal
                cart_table.insert("", "end", values=(product.name, f"${product.price:.2f}", quantity, f"${subtotal:.2f}"))
            total_label.config(text=f"Total: ${total:.2f}") #update total label

           

        button_frame = tk.Frame(cart_window, bg="#ffffff")
        button_frame.pack(pady=10)
        
        def remove_selected():
            selected = cart_table.focus()  #get selected row in cart table
            if not selected:
                messagebox.showwarning("Select Item", "Please select an item to remove.")
                return

            values = cart_table.item(selected, "values")
            product_name = values[0]  #product name column

            # Find matching product in cart and remove it
            for pid, entry in list(self.cart.items.items()):
                if entry["product"].name == product_name:
                    self.cart.remove_item(pid)
                    messagebox.showinfo("Removed", f"Removed {product_name} from cart.")
                    refresh_cart()
                    break
                
        def checkout():
            if not self.cart.items:
                messagebox.showwarning("Empty Cart", "Your cart is empty.")
                return
            else:
                order_no = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}" #generate order number
                order = Order(order_no, self.cart.customer, "Processing")  #create order instance
                order.purchased_items = []   #initialize list for purchased items

            for entry in self.cart.items.values():   #iterate cart to update inventory and fill order
                product = entry["product"]
                qty = entry["quantity"]
                self.inventory.update_stock(product.id, qty, "subtract", )
                order.purchased_items.append((product, qty, product.price))  #add to order items

            total_cost = self.cart.calculate_total()
            order.total_amount = total_cost
            order.date_created = datetime.now()
            self.orders.append(order)

            self.cart = Shopping_cart_item(customer=order.customer)  #rest cart for same customer
            self.load_products()
            messagebox.showinfo("Checkout Complete", f"Order {order_no} placed successfully!\nTotal: ${total_cost:.2f}")
            cart_window.destroy()
            
        tk.Button(button_frame, text="Remove Selected", command=remove_selected,
              bg="#FF5C5C", fg="white", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="Checkout", command=checkout,
                bg="#00A36C", fg="white", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Close", command=cart_window.destroy,
                bg="#999", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)
        
        refresh_cart()  #initial populate of cart table

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

        for order in self.orders:  #populate table from stored orders
            date_str = order.date_created.strftime("%Y-%m-%d %H:%M:%S") if hasattr(order, "date_created") else "N/A"
            order_table.insert("", "end",
                               values=(order.order_no, date_str, f"${order.total_amount:.2f}", order.status))


# ---------------------------------------------------------
# Example Run
# ---------------------------------------------------------
if __name__ == "__main__":
    # category1 = Category("Electronics")
    # category2 = Category("Clothing")

    inventory = InventoryManager()
    cart = Shopping_cart_item(customer="Musa Adnan Rahmah")

    # p1 = Product("Laptop", "High-end gaming laptop.", 1200, 10, "Asus", "VendorX", category1)
    # p1.set_id("P001")
    # inventory.add_product(p1, 10)

    # p2 = Product("Headphones", "Noise-cancelling wireless headphones.", 150, 15, "Sony", "VendorY", category1)
    # p2.set_id("P002")
    # inventory.add_product(p2, 15)

    # p3 = Product("T-Shirt", "Soft cotton T-shirt, unisex design.", 25, 30, "Nike", "VendorZ", category2)
    # p3.set_id("P003")
    # inventory.add_product(p3, 30)

    window = tk.Tk()
    app = ECommerceApp(window, inventory, cart)  #instantiate app with inventory and cart
    window.mainloop()
