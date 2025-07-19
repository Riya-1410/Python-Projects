from data import basket

def update_fruit():
    if not basket:
        print("Basket is empty. Nothing to update.")
        return

    print("\nCurrent Basket Contents:")
    for fruit, qty in basket.items():
        print(f"- {fruit}: {qty}")

    fruit = input("\nEnter fruit name to update: ").strip().capitalize()
    if fruit in basket:
        try:
            qty = int(input(f"Enter new quantity for {fruit}: "))
            basket[fruit] = qty
            print(f"{fruit} updated to {qty}.")
        except ValueError:
            print("Quantity must be a number.")
    else:
        print(f"{fruit} is not in the basket.")
