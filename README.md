CMPP 3000 – E-Commerce Order Management System
[Simulation file is the final project]
By Group 7, CMPP 3000 BSA, Fall 2025 – BTech
Drew, Mihir, Joanna, Samia, Muqadas, Muhammad

⸻

Overview

This project is an E-Commerce Order Management System designed to reduce food waste by allowing customers to buy perishable goods at discounted prices from local sellers such as grocers, farmers, and restaurants.

The system distinguishes between three roles — Buyer, Seller, and Admin — each with unique functionalities. The simulation, developed in Python, demonstrates live inventory updates, order validation, cart operations, and report generation.

⸻

Part A: Problem Definition & Requirements

The goal of our e-commerce system is to create a digital platform that connects sellers with surplus perishable goods and buyers looking for affordable fresh items.

Functional Features:
	•	Buyer Role: View available products, search/filter items, add to cart, and checkout.
	•	Seller Role: Add, update, or remove products from their inventory.
	•	Admin Role: Monitor seller inventories, check for duplicate orders, and generate alerts/reports.

Non-Functional Requirements:
	•	Data Encryption – Protects user credentials and payment data.
	•	Usability – Simple, intuitive, and responsive interface.
	•	Portability – Runs on multiple devices/platforms.
	•	Compliance – Follows local food safety and transaction rules.

⸻

Part B: Data Structures & Logic

The system’s backend is implemented using Python dictionaries and lists to manage users, inventories, and customer carts.
	•	User Structure: Holds credentials and user roles (Customer, Seller, Admin).
	•	Inventory Structure: Stores items with name, quantity, price, category, and expiry date.
	•	Cart Structure: Tracks items selected for checkout and calculates total cost.

Boolean logic ensures an order is successful only if:
	•	The user is logged in
	•	The item is in stock
	•	Payment is completed
	•	Delivery is available

Expression:
Order = LoggedIn ∧ InStock ∧ PaymentSuccessful ∧ DeliveryAvailable

⸻

Part C: System Simulation (Python)

This part contains the Python simulation that models real-world e-commerce operations for each role:

Buyer Workflow
	•	Log in as Buyer
	•	Browse and filter items
	•	Add products to cart
	•	Proceed to checkout and confirm purchase

Seller Workflow
	•	Log in as Seller
	•	View and manage inventory
	•	Add, modify, or delete items
	•	View customer orders

Admin Workflow
	•	Log in as Admin
	•	Monitor low stock alerts
	•	Check for duplicate orders
	•	Generate reports

⸻

Part D: Model and Design

A UML Activity Diagram models the logical flow of the system, including login, purchasing, inventory updates, and report generation.

For a complete view, refer to the UML Activity Diagram.vsdx file located in the repository.
