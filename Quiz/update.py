from data import Question_bank

def update_questions():
    question = list(Question_bank.keys())  
    
    for num, que in enumerate(question):
        print(f"\n{num} {que}?") 
    
    try:
        no = int(input("Select question number to update "))
        que_update = question[no]
        opt_update = Question_bank[que_update]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return
    
     
    def q():
        new = input(f"Write question >>").strip().capitalize()
        
        Question_bank[new] = opt_update
        del Question_bank[que_update]
        print("Question updated")
        
    def o():
        new = []
        for i in range(1,5):
            choices = input(f"Enter option {i}:  ").strip().capitalize()
            new.append(choices)
            
        correct = input(f"Add correct answer from the {new} ").strip().capitalize()
        if correct not in new:
            print(f"Add from the options {new} ")
            return

        new.remove(correct)
        new.insert(0, correct)
        Question_bank[que_update] = new
        print("Options updated")
            
    def b():
        o()
        q()
    
    
    def menu():
        while True:
            print("1. update question")
            print("2. Update option")
            print("3. Update both")
            print("4. Exit")
            ch = input("Choose from 1, 2, 3: ").strip()
            if ch == '1':
                q()
            elif ch == '2':
                o()
            elif ch == '3':
                b()
            elif ch == '4':
                break
            else:
                print(f"Choose from {1, 2, 3, 4} to get the results")
    menu()
    