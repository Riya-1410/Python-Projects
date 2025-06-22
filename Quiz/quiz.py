import random
from string import ascii_lowercase 
from data import Question_bank

def start_quiz():
    count = 0
    for num, (que, ans) in enumerate(Question_bank.items(), start = 1):
        print(f"\n{num} {que}?")
    
    
        correct = ans[0]
        shuffled_option = ans[:]
        random.shuffle(shuffled_option)
        
        
        option_label = dict(zip(ascii_lowercase, shuffled_option))
        for label, option in option_label.items():
            print(f"{label} {option}")
        
        
        while True:
            option = input("\nYour Option __").lower()
            if option in option_label:
                break
            print(f"Please enter from the following {', '.join(option_label)}")
        
            
        correct_option = option_label.get(option)
        if correct_option == correct:
            count += 1
            print(":) Correct")
        else:
            print(f":( The correct answer was {correct}, not {option_label.get(option)}")
            
        print(f"You've scored {count} out of {num}") 

    print(f"\nQuiz complete Final score: {count} out of {len(Question_bank)}")
