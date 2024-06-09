import tkinter as tk

class Order:
    def __init__(self, order_id, customer_name, items):
        # Initialize order attributes
        self.order_id = order_id
        self.customer_name = customer_name
        self.items = items
        self.status = 'Pending'

    def update_status(self, status):
        # Update the status of the order
        self.status = status

    def __str__(self):
        # Return a string representation of the order
        return f"Order ID: {self.order_id}, Customer: {self.customer_name}, Items: {', '.join(self.items)}, Status: {self.status}"

def send_notification(order):
    # Function to display a notification window for the given order
    if not hasattr(RestaurantOrderSystem, 'notification_window') or not RestaurantOrderSystem.notification_window:
        # If no notification window exists, create a new one
        RestaurantOrderSystem.notification_window = tk.Toplevel()
        RestaurantOrderSystem.notification_window.title("Order Notification")
        RestaurantOrderSystem.notification_window.geometry("450x150")

        notification_label = tk.Label(RestaurantOrderSystem.notification_window, wraplength=400)
        notification_label.pack(expand=True, fill='both', padx=20, pady=20)

        close_button = tk.Button(RestaurantOrderSystem.notification_window, text="Close", command=lambda: destroy_notification_window(RestaurantOrderSystem.notification_window))
        close_button.pack(pady=10)
    else:
        # If a notification window already exists, update its content
        notification_label = tk.Label(RestaurantOrderSystem.notification_window, wraplength=400)
        notification_label.pack(expand=True, fill='both', padx=20, pady=20)

    notification_label.config(text=str(order))

def destroy_notification_window(window):
    # Function to destroy the notification window
    window.destroy()
    del RestaurantOrderSystem.notification_window

class RestaurantOrderSystem:
    def __init__(self, root):
        # Initialize the restaurant order system
        self.orders = []
        self.next_order_id = 1
        self.current_order = None

        self.root = root
        self.root.title("Restaurant Order System")
        self.root.geometry("400x300")

        self.customer_name_label = tk.Label(root, text="Customer name:")
        self.customer_name_label.pack()
        self.customer_name_entry = tk.Entry(root)
        self.customer_name_entry.pack()

        self.items_label = tk.Label(root, text="Enter items (comma separated):")
        self.items_label.pack()
        self.items_entry = tk.Entry(root)
        self.items_entry.pack()

        self.order_button = tk.Button(root, text="Order", command=self.receive_order)
        self.order_button.pack(pady=(10, 5))

        self.update_order_button = tk.Button(root, text="Update Order", command=self.update_order_status)
        self.update_order_button.pack(pady=5)

        self.mark_completed_button = tk.Button(root, text="Mark as Completed", command=self.mark_as_completed)
        self.mark_completed_button.pack(pady=5)

    def receive_order(self):
        # Function to receive a new order
        customer_name = self.customer_name_entry.get()
        items = [item.strip() for item in self.items_entry.get().split(',')]
        order = Order(self.next_order_id, customer_name, items)
        self.orders.append(order)
        self.next_order_id += 1
        self.current_order = order
        self.display_order(order)

    def update_order_status(self):
        # Function to update the status of the current order
        if self.current_order:
            if self.current_order.status == 'Pending':
                self.current_order.update_status('Preparing')
                self.display_order(self.current_order)
            elif self.current_order.status == 'Preparing':
                self.current_order.update_status('Complete')
                self.display_order(self.current_order)
                send_notification(self.current_order)

    def mark_as_completed(self):
        # Function to mark the current order as completed
        if self.current_order and self.current_order.status == 'Complete':
            send_notification(self.current_order)

    def destroy_order_window(self):
        # Function to destroy the order window
        if hasattr(self, 'order_window'):
            self.order_window.destroy()
            del self.order_window

    def display_order(self, order):
        # Function to display the details of the current order
        if not hasattr(self, 'order_window') or not self.order_window:
            self.order_window = tk.Toplevel()
            self.order_window.title("Order Received")
            self.order_window.geometry("450x150")

            self.order_label = tk.Label(self.order_window, wraplength=400)
            self.order_label.pack(expand=True, fill='both', padx=20, pady=20)

            close_button = tk.Button(self.order_window, text="Close", command=self.destroy_order_window)
            close_button.pack(pady=10)

        self.order_label.config(text=str(order))

def main():
    # Main function to initialize the GUI
    root = tk.Tk()
    app = RestaurantOrderSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()
