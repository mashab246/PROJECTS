class Order:
    def __init__(self, order_no, customer, status, total_amount):
        self.order_no = order_no
        self.customer = customer
        self.status = status
        self.total_amount = total_amount
        
        
    def calculate_total(self, discount_type = None, discount_value = 0):
        total = 0
        
        for item in self.__items.values():
            total += item.get_total_price()
        
        if discount_type == "percentage":
            total -= total * (discount_value / 100) 
        elif discount_type == "fixed":
            total -= discount_value
        else:
            print("Invalid discount type")
            
        # Ensure total is not negative
        if total < 0:
            total = 0
        
        self.total_amount = total
        return total
       


        
    def update_status(self, new_status):
        valid_statuses = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]
        
        if new_status not in valid_statuses:
            print(f"Invalid status: {new_status}. Valid statuses are: {valid_statuses}")
            return False
        
        if self.status == "Cancelled":
            print("Cannot update status of a cancelled order.")
            return False
        
        if self.status == "Delivered" and new_status != "Cancelled":
            print("Cannot update status of a delivered order unless cancelling.") # Prevents updating the status of a delivered order unless it’s being canceled.
            return False
        
        if new_status in valid_statuses:
            self.status = new_status
            print(f"Order status updated to {new_status}")
            return True
    