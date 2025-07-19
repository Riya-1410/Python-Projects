from data import Question_bank

def add_questions():
    question = input(f"Write question >> ").strip().capitalize()
    
    if question in Question_bank:
        print("This question already exists.")
        return 
    
    options = []
    for i in range(1,5):
        choices = input(f"Enter option {i}: ").strip().capitalize()
        options.append(choices)
        
    if len(set(options)) != 4:
        print("Options must be unique.")
        return

        
    correct = input(f"Add correct answer from the {options} ").strip().capitalize()
    if correct not in options:
        print(f"Add from the options {options}")
        return

    options.remove(correct)
    options.insert(0, correct)
    
    Question_bank[question] = options
    