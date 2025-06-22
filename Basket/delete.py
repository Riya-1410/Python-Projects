from data import basket

def delete_fruit():
    fruit = input("Enter fruit name to delete: ").strip().capitalize()
    if fruit in basket:
        del basket[fruit]
        print(f"{fruit} removed from basket.")
    else:
        print(f"{fruit} is not in the basket.")
        