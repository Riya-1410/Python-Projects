from quiz import start_quiz
from data import Question_bank
from add import add_questions
from update import update_questions

def menu():
    while True:
        print("1. Start Quiz")
        print("2. Add Questions")
        print("3. Update Questions")
        print("4. Exit")
        
        ch = input("Choice __")
        if ch == '1':
            start_quiz()
        elif ch == '2':
            add_questions()
        elif ch == '3':
            update_questions()
        elif ch == '4':
            break
        else:
            print(f"Choose from {1, 2, 3, 4} to get the results")
            
menu()
        
    