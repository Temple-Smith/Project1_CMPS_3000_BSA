import random

# Sample user data
users = [
    {"username": "john", "password": "password123", "role": "Customer"},
    {"username": "fresh_farmfoods", "password": "freshfood321", "role": "Seller"},
    {"username": "the_admin", "password": "securepass321", "role": "Admin"}
]

# Sample inventory data
inventory = {
    "fresh_farmfoods": [
        {"item_name": "apples", "quantity": 10, "price": 4.50, "category": "fruits", "expiry_date": "2025-10-29"},
        {"item_name": "milk", "quantity": 5, "price": 10.00, "category": "dairy", "expiry_date": "2025-11-29"}
    ],
    "abbeysbakery": [
        {"item_name": "4pc pack butter rolls", "quantity": 8, "price": 4.25, "category": "bakery", "expiry_date": "2026-01-20"}
    ]
}

# Cart structure
cart = {"customer_name": "", "items": [], "total": 0.0}

# Helper functions
def generate_order_id():
    return f"O-{random.randint(1000, 9999)}"

def generate_payment_id():
    return f"P-{random.randint(5000, 9999)}"

# Login function
def login():
    attempts = 3
    while attempts > 0:
        username = input("Username: ")
        password = input("Password: ")
        for user in users:
            if user["username"] == username and user["password"] == password:
                print(f"Login successful. Role: {user['role']}")
                return user
        attempts -= 1
        print(f"Invalid credentials. Attempts left: {attempts}")
    print("Login failed. Exiting system.")
    return None

# Display inventory
def display_inventory():
    print("\n--- Product Catalog ---")
    for seller, items in inventory.items():
        for item in items:
            print(f"{seller:<15} | {item['item_name']:<25} | ${item['price']} | qty={item['quantity']} | {item['category']} | exp={item['expiry_date']}")
    print("="*50)

# Buyer workflow
def buyer_menu(user):
    cart["customer_name"] = user["username"]
    while True:
        print("\n[Buyer Menu]\n1) View all items\n2) Search/filter items\n3) Add item to cart\n4) View cart\n5) Checkout\n0) Back to main")
        choice = input("Choose: ")
        if choice == "1":
            display_inventory()
        elif choice == "2":
            keyword = input("Enter keyword to search: ")
            print("Search Results:")
            for seller, items in inventory.items():
                for item in items:
                    if keyword.lower() in item["item_name"].lower():
                        print(f"{seller} | {item['item_name']} | ${item['price']} | qty={item['quantity']}")
        elif choice == "3":
            seller_name = input("Seller name: ")
            item_name = input("Item name: ")
            qty = int(input("Quantity: "))
            if seller_name in inventory:
                for item in inventory[seller_name]:
                    if item["item_name"] == item_name:
                        if item["quantity"] >= qty:
                            cart["items"].append({"item_name": item_name, "quantity": qty, "price": item["price"], "seller": seller_name})
                            cart["total"] += item["price"] * qty
                            item["quantity"] -= qty
                            print("Added to cart.")
                        else:
                            print("Not enough stock.")
        elif choice == "4":
            print("\n-- Cart --")
            for item in cart["items"]:
                print(f"{item['seller']} | {item['item_name']} x {item['quantity']} @ ${item['price']}")
            print(f"Total: ${cart['total']:.2f}")
        elif choice == "5":
            simulate = input("Simulate payment success? (y/n): ")
            if simulate.lower() == "y":
                order_id = generate_order_id()
                payment_id = generate_payment_id()
                print(f"Order confirmed! Order ID: {order_id}, Payment ID: {payment_id}, Total: ${cart['total']:.2f}")
                print(f"[Email → {user['username']}] Order Confirmed: Your order {order_id} has been placed.")
                cart["items"] = []
                cart["total"] = 0.0
            else:
                print("Payment failed.")
        elif choice == "0":
            break

# Seller workflow
def seller_menu(user):
    while True:
        print("\n[Seller Menu]\n1) View inventory\n2) Add item\n0) Back to main")
        choice = input("Choose: ")
        if choice == "1":
            print("Current Inventory:")
            for item in inventory[user["username"]]:
                print(item)
        elif choice == "2":
            name = input("Item name: ")
            qty = int(input("Quantity: "))
            price = float(input("Price: "))
            category = input("Category: ")
            expiry = input("Expiry date (YYYY-MM-DD): ")
            inventory[user["username"]].append({"item_name": name, "quantity": qty, "price": price, "category": category, "expiry_date": expiry})
            print("Item added successfully.")
        elif choice == "0":
            break

# Admin workflow
def admin_menu():
    print("\n[Admin Dashboard]")
    print("Monitoring inventory thresholds...")
    for seller, items in inventory.items():
        for item in items:
            if item["quantity"] < 5:
                print(f"Alert: Low stock for {item['item_name']} from {seller}")
    print("Checking for duplicate orders... (Simulation)")
    print("No duplicate orders detected.")

# Main system loop
def main():
    print("=== E-Commerce Order Management System (Perishables) ===")
    user = login()
    if not user:
        return
    while True:
        print("\n[Main Menu]\n1) Buyer actions\n2) Seller actions\n3) Admin actions\n9) Logout")
        choice = input("Choose: ")
        if choice == "1" and user["role"] == "Customer":
            buyer_menu(user)
        elif choice == "2" and user["role"] == "Seller":
            seller_menu(user)
        elif choice == "3" and user["role"] == "Admin":
            admin_menu()
        elif choice == "9":
            print("You have been logged out.")
            break
        else:
            print("Invalid choice or insufficient permissions.")

# Run the system
if __name__ == "__main__":
    main()