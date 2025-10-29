# simulation.py
import itertools
from datetime import date

# ----- Seed Data -----
users = [
    {"username": "john", "password": "password123", "role": "Customer"},
    {"username": "fresh_farmfoods", "password": "freshfood321", "role": "Seller"},
    {"username": "the_admin", "password": "securepass321", "role": "Admin"},
]

inventory = {
    "fresh_farmfoods": [
        {"item_name": "apples", "quantity": 10, "price": 4.50, "category": "fruits", "expiry_date": "2025-10-29"},
        {"item_name": "milk",   "quantity": 5,  "price": 10.00, "category": "dairy",  "expiry_date": "2025-11-29"},
    ],
    "abbeysbakery": [
        {"item_name": "4pc pack butter rolls", "quantity": 8, "price": 4.25, "category": "bakery", "expiry_date": "2026-01-20"}
    ],
}

orders = []

DELIVERY_AVAILABLE = True
LOW_STOCK_THRESHOLD = 5
order_counter = itertools.count(start=1002)
payment_counter = itertools.count(start=5002)

# ----- Utilities -----
def find_user(username, password):
    for u in users:
        if u["username"] == username and u["password"] == password:
            return u
    return None

def list_all_items():
    print("\n--- Product Catalog ---")
    for seller, items in inventory.items():
        for itm in items:
            print(f"{seller:16} | {itm['item_name']:24} | ${itm['price']:5.2f} | qty={itm['quantity']:3} | {itm['category']} | exp={itm['expiry_date']}")
    print("------------------------")

def filter_items_by_text(text):
    text = text.lower().strip()
    matches = []
    for seller, items in inventory.items():
        for itm in items:
            hay = f"{seller} {itm['item_name']} {itm['category']}".lower()
            if text in hay:
                matches.append((seller, itm))
    return matches

def select_item(seller_name, item_name):
    items = inventory.get(seller_name, [])
    for itm in items:
        if itm["item_name"].lower() == item_name.lower():
            return itm
    return None

def simulate_payment():
    ans = input("Simulate payment success? (y/n): ").strip().lower()
    return ans == "y"

def simulate_delivery():
    return DELIVERY_AVAILABLE

def generate_ids():
    oid = f"O-{next(order_counter)}"
    pid = f"P-{next(payment_counter)}"
    return oid, pid

def send_email(to_user, subject, body):
    print(f"[Email → {to_user}] {subject}: {body}")

def check_duplicates(new_order_id, new_payment_id):
    for o in orders:
        if o["order_id"] == new_order_id or o["payment_id"] == new_payment_id:
            return True
    return False

# ----- Role Flows -----
def buyer_flow(current_user):
    cart = []  # {"seller":..., "item_name":..., "qty":..., "unit_price":...}

    while True:
        print("\n[Buyer Menu]")
        print("1) View all items")
        print("2) Search/filter items")
        print("3) Add item to cart")
        print("4) View cart")
        print("5) Checkout")
        print("0) Back to main")
        choice = input("Choose: ").strip()

        if choice == "1":
            list_all_items()

        elif choice == "2":
            q = input("Search text (item/seller/category): ")
            matches = filter_items_by_text(q)
            if not matches:
                print("No matches.")
            else:
                for seller, itm in matches:
                    print(f"- {seller} | {itm['item_name']} | ${itm['price']:.2f} | qty={itm['quantity']} | {itm['category']}")

        elif choice == "3":
            seller = input("Seller name: ").strip()
            item = input("Item name: ").strip()
            try:
                qty  = int(input("Quantity: ").strip())
            except ValueError:
                print("Quantity must be a number.")
                continue
            sel_itm = select_item(seller, item)
            if not sel_itm:
                print("Item not found.")
                continue
            if qty <= 0:
                print("Quantity must be > 0.")
                continue
            if qty > sel_itm["quantity"]:
                print("Insufficient stock.")
                continue
            cart.append({"seller": seller, "item_name": item, "qty": qty, "unit_price": sel_itm["price"]})
            print("Added to cart.")

        elif choice == "4":
            if not cart:
                print("Cart is empty.")
            else:
                total = sum(line["qty"] * line["unit_price"] for line in cart)
                print("\n-- Cart --")
                for line in cart:
                    print(f"{line['seller']} | {line['item_name']} x {line['qty']} @ ${line['unit_price']:.2f}")
                print(f"Total: ${total:.2f}")

        elif choice == "5":
            if not cart:
                print("Cart is empty.")
                continue

            # L ∧ S ∧ P ∧ D
            L = True  # already logged in
            S = all(select_item(line["seller"], line["item_name"]) and
                    select_item(line["seller"], line["item_name"])["quantity"] >= line["qty"]
                    for line in cart)
            P = simulate_payment()
            D = simulate_delivery()

            if L and S and P and D:
                order_id, payment_id = generate_ids()
                if check_duplicates(order_id, payment_id):
                    print("Duplicate detected. Rejecting order.")
                    return
                # Decrement inventory
                for line in cart:
                    sel_itm = select_item(line["seller"], line["item_name"])
                    sel_itm["quantity"] -= line["qty"]

                total = sum(line["qty"] * line["unit_price"] for line in cart)
                orders.append({
                    "order_id": order_id,
                    "payment_id": payment_id,
                    "buyer": current_user["username"],
                    "items": cart,
                    "total": total,
                    "status": "CONFIRMED",
                    "order_date": str(date.today())
                })
                print(f"Order confirmed! Order ID: {order_id}, Payment ID: {payment_id}, Total: ${total:.2f}")
                send_email(current_user["username"], "Order Confirmed", f"Your order {order_id} has been placed.")
                cart.clear()
            else:
                reason = []
                if not S: reason.append("out of stock")
                if not P: reason.append("payment failed")
                if not D: reason.append("delivery unavailable")
                print("Order failed: " + ", ".join(reason) if reason else "Order failed.")

        elif choice == "0":
            break
        else:
            print("Invalid choice.")

def seller_flow(current_user):
    seller_name = current_user["username"]
    inventory.setdefault(seller_name, [])

    while True:
        print("\n[Seller Menu]")
        print("1) View my inventory")
        print("2) Add item")
        print("3) Update item quantity/price")
        print("4) Remove item")
        print("0) Back to main")
        choice = input("Choose: ").strip()

        if choice == "1":
            items = inventory.get(seller_name, [])
            if not items:
                print("No items yet.")
            else:
                for itm in items:
                    print(itm)

        elif choice == "2":
            name = input("Item name: ").strip()
            if any(i["item_name"].lower() == name.lower() for i in inventory[seller_name]):
                print("Item already exists.")
                continue
            try:
                qty = int(input("Quantity: ").strip())
                price = float(input("Price: ").strip())
            except ValueError:
                print("Invalid number.")
                continue
            cat = input("Category: ").strip()
            exp = input("Expiry (YYYY-MM-DD): ").strip()
            inventory[seller_name].append({
                "item_name": name, "quantity": qty, "price": price,
                "category": cat, "expiry_date": exp
            })
            print("Item added.")

        elif choice == "3":
            name = input("Item name to update: ").strip()
            itm = next((i for i in inventory[seller_name] if i["item_name"].lower() == name.lower()), None)
            if not itm:
                print("Item not found.")
                continue
            new_qty = input(f"New quantity (enter to skip, current {itm['quantity']}): ").strip()
            new_price = input(f"New price (enter to skip, current {itm['price']}): ").strip()
            if new_qty:
                try: itm["quantity"] = int(new_qty)
                except ValueError: print("Invalid number.")
            if new_price:
                try: itm["price"] = float(new_price)
                except ValueError: print("Invalid number.")
            print("Item updated.")

        elif choice == "4":
            name = input("Item name to remove: ").strip()
            before = len(inventory[seller_name])
            inventory[seller_name] = [i for i in inventory[seller_name] if i["item_name"].lower() != name.lower()]
            print("Removed." if len(inventory[seller_name]) < before else "Item not found.")

        elif choice == "0":
            break
        else:
            print("Invalid choice.")

def admin_flow(current_user):
    while True:
        print("\n[Admin Menu]")
        print("1) Low stock alerts")
        print("2) Check duplicate orders")
        print("3) Reports")
        print("0) Back to main")
        choice = input("Choose: ").strip()

        if choice == "1":
            print(f"Threshold = {LOW_STOCK_THRESHOLD}")
            alerts = []
            for seller, items in inventory.items():
                for itm in items:
                    if itm["quantity"] < LOW_STOCK_THRESHOLD:
                        alerts.append((seller, itm["item_name"], itm["quantity"]))
            if alerts:
                print("Low stock alerts:")
                for a in alerts:
                    print(f"- {a[0]} | {a[1]} | qty={a[2]}")
            else:
                print("No low stock items.")

        elif choice == "2":
            seen_o, seen_p = set(), set()
            duplicates = []
            for o in orders:
                oid, pid = o["order_id"], o["payment_id"]
                if oid in seen_o or pid in seen_p:
                    o["status"] = "REJECTED_DUPLICATE"
                    duplicates.append((oid, pid))
                seen_o.add(oid); seen_p.add(pid)
            if duplicates:
                for d in duplicates:
                    print(f"Duplicate order detected: order_id={d[0]}, payment_id={d[1]} (marked rejected)")
            else:
                print("No duplicates found.")

        elif choice == "3":
            total_orders = len(orders)
            confirmed = sum(1 for o in orders if o.get("status") == "CONFIRMED")
            rejected = total_orders - confirmed
            revenue = sum(o["total"] for o in orders if o.get("status") == "CONFIRMED")
            print(f"Orders: {total_orders}, Confirmed: {confirmed}, Rejected: {rejected}, Revenue: ${revenue:.2f}")

        elif choice == "0":
            break
        else:
            print("Invalid choice.")

# ----- App Shell -----
def main():
    print("=== E‑Commerce Order Management System (Perishables) ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    user = find_user(username, password)
    if not user:
        print("Invalid login. Try again.")
        return

    print(f"Login successful. Role: {user['role']}")
    while True:
        print("\n[Main Menu]")
        if user["role"] == "Customer": print("1) Buyer actions")
        if user["role"] == "Seller":   print("2) Seller actions")
        if user["role"] == "Admin":    print("3) Admin actions")
        print("9) Logout")
        choice = input("Choose: ").strip()

        if choice == "1" and user["role"] == "Customer":
            buyer_flow(user)
        elif choice == "2" and user["role"] == "Seller":
            seller_flow(user)
        elif choice == "3" and user["role"] == "Admin":
            admin_flow(user)
        elif choice == "9":
            print("You have been logged out.")
            break
        else:
            print("Invalid choice or not permitted for your role.")

if __name__ == "__main__":
    main()
# simulation.py