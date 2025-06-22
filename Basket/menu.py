from add import add_fruit
from show import show_fruits
from update import update_fruit
from delete import delete_fruit

def menu():
    while True:
        print("\n--- Basket Management ---")
        print("1. Add Fruit")
        print("2. Show Fruits")
        print("3. Update Fruit")
        print("4. Delete Fruit")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            add_fruit()
        elif choice == '2':
            show_fruits()
        elif choice == '3':
            update_fruit()
        elif choice == '4':
            delete_fruit()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

menu()
