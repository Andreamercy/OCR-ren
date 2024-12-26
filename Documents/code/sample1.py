'''
import random
a=random.randint(1,10)
print(a)
while True:
    b=int(input("Guess the number:"))
    if a==b:
        print("you are correct")
        break
    elif a>b:
        print("too low")
    else:
        print("too high")
from tkinter import *
 
root = Tk()
root.geometry("300x300")
root.title(" Q&A ")
 
def Take_input():
    import random
    a=random.randint(1,5)
    print(a)
    
    INPUT = inputtxt.get("1.0", "end-1c")
    print(INPUT)
    if(int(INPUT) == int(a)):
        Output.insert(END, 'Correct \n')
    elif(int(INPUT) <= int(a)):
        Output.insert(END, 'Too Low \n')
    else:
        Output.insert(END, "Too high\n")
     
l = Label(text = "GUSSE THE NUMBER")
inputtxt = Text(root, height = 10,
                width = 25,
                bg = "black")
 
Output = Text(root, height = 5, 
              width = 25, 
              bg = "black")
 
Display = Button(root, height = 2,
                 width = 20, 
                 text ="Show",
                 command = lambda:Take_input())
 
l.pack()
inputtxt.pack()
Display.pack()
Output.pack()
'''
import tkinter as tk
import random

class NumberGuessingGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Number Guessing Game")
        self.master.geometry("300x150")
        
        self.secret_number = random.randint(1, 10)
        self.guess_label = tk.Label(self.master, text="Enter your guess:")
        self.guess_label.pack()
        
        self.guess_entry = tk.Entry(self.master)
        self.guess_entry.pack()
        
        self.submit_button = tk.Button(self.master, text="Submit", command=self.check_guess)
        self.submit_button.pack()
        
        self.result_label = tk.Label(self.master, text="")
        self.result_label.pack()
        
        self.remaining_guesses = 5
        
    def check_guess(self):
        guess = self.guess_entry.get()
        try:
            guess = int(guess)
        except ValueError:
            self.result_label.config(text="Invalid input. Please enter a number.")
        if guess == self.secret_number:
            self.result_label.config(text=f"Congratulations! You guessed the number {self.secret_number}.")
            self.submit_button.config(state="disabled")
        elif guess < self.secret_number:
            self.result_label.config(text="Too low! Try again.")
        else:
            self.result_label.config(text="Too high! Try again.")
if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGuessingGame(root)
    root.mainloop()
'''
import tkinter as tk
import random

secret_number = random.randint(1, 10)
remaining_guesses = 5
def check_guess(self):
    guess = self.guess_entry.get()
    try:
            guess = int(guess)
    except ValueError:
            self.result_label.config(text="Invalid input. Please enter a number.")
            return
        
    if guess == self.secret_number:
            self.result_label.config(text=f"Congratulations! You guessed the number {self.secret_number}.")
            self.submit_button.config(state="disabled")
    elif guess < self.secret_number:
            self.result_label.config(text="Too low! Try again.")
    else:
            self.result_label.config(text="Too high! Try again.")
    
    guess = int(guess_entry.get())
    msg = ["Too low! Try again.", "Too high! Try again.", f"Congratulations! You guessed the number {secret_number}.", f"Game over! The number was {secret_number}."][min(2, (guess - secret_number) // 0)] if guess != secret_number else ''
    result_label.config(text=msg)
    remaining_guesses -= 1
    submit_button.config(state="disabled") if msg else None

root = tk.Tk()
root.title("Number Guessing Game")
root.geometry("300x150")

guess_label = tk.Label(root, text="Enter your guess:")
guess_label.pack()

guess_entry = tk.Entry(root)
guess_entry.pack()

submit_button = tk.Button(root, text="Submit", command=check_guess)
submit_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
'''
