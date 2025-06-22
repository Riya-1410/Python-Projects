from data import basket

def show_fruits():
    if not basket:
        print("Basket is empty.")
        return
    print("\nCurrent Fruits in Basket:")
    for fruit, qty in basket.items():
        print(f"- {fruit}: {qty}")