import requests

URL = "http://127.0.0.1:5000"

def main_menu():
    while True:
        print("\n=== INVENTORY MANAGEMENT SYSTEM ===")
        print("1. View All Items")
        print("2. Add New Product (Manual)")
        print("3. Fetch & Add Product from Open Food Facts API")
        print("4. Delete Item")
        print("5. Exit")
        
        choice = input("Select an option (1-5): ")

        if choice == "1":
            res = requests.get(f"{URL}/inventory")
            print("\n--- Current Inventory ---")
            print(res.json())

        elif choice == "2":
            name = input("Enter product name: ")
            price = float(input("Enter price: "))
            stock = int(input("Enter stock: "))
            res = requests.post(f"{URL}/inventory", json={"name": name, "price": price, "stock": stock})
            
            if res.status_code == 201:
                print("\nItem added successfully:", res.json())
            else:
                print(f"\nFailed to add item (Status {res.status_code}):", res.text)

        elif choice == "3":
            identifier = input("Enter product barcode or query name: ")
            res = requests.post(f"{URL}/inventory/fetch-external/{identifier}")
            if res.status_code == 201:
                print("\nProduct successfully fetched & added:", res.json())
            else:
                print("\nError:", res.text)

        elif choice == "4":
            item_id = input("Enter item ID to delete: ")
            res = requests.delete(f"{URL}/inventory/{item_id}")
            print("\nResponse:", res.json() if res.status_code == 200 else res.text)

        elif choice == "5":
            print("Exiting CLI. Goodbye!")
            break

        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main_menu()