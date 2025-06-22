from data import basket

def add_fruit():
    fruit = input("Enter fruit name to add: ").strip().capitalize()
    qty = int(input(f"Enter quantity of {fruit}: "))
    if fruit in basket:
        basket[fruit] += qty
    else:
        basket[fruit] = qty
    print(f"{qty} {fruit}(s) added to basket.")