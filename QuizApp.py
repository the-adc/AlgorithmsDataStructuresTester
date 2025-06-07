import tkinter as tk
from tkinter import messagebox
import random

from RecurrenceQuestion import RecurrenceQuestionFactory

class Question:
    def __init__(self, question_text, options, correct_answer):
        self.question = question_text
        self.options = options
        self.correct_answer = correct_answer
    
    def shuffle_options(self):
        random.shuffle(self.options)
        return self.options
    
    def __str__(self):
        return self.question
    
    def __getitem__(self, index):
        return self.options[index]

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("eAssistant")
        self.root.geometry("900x700")  # Increased window size
        
        # Quiz variables
        self.questions = self.load_questions()
        self.current_question = 0
        self.score = 0
        self.time_left = 15
        self.timer_running = False
        
        # GUI elements
        self.setup_welcome_screen()
    
    def load_questions(self):
        # Create question objects
        questions = [
            Question(
                "Which of the following sorting algorithms runs in linear time when executed on an already sorted array (assuming that it is an array of distinct integers)?",
                ["Selection Sort", "Merge Sort", "Heapsort", "Insertion Sort"],
                "Insertion Sort"
            ),
            Question(
                "For a sequence of n integers in range [0 … n^3], and considering worst-case time complexity, which sorting algorithm(s) can be optimally implemented to guarantee a linear time to sort this sequence?",
                ["Counting Sort", "Quick Sort", "Radix Sort", "None of the answers"],
                "Radix Sort"
            ),
            Question(
                "Which of the following statements are true about the Median of Median algorithm?",
                ["Median of medians is not an in-place algorithm",
                 "Median of medians is a recursive algorithm that would partition the list into 4 regions.",
                 "Median of medians will always obtain the median as the pivot in O(N) time.",
                 "Median of medians will require the list have the number of items be in multiples of 5 as it would need to break into smaller lists of size 5."],
                "Median of medians is not an in-place algorithm"
            ),
            Question(
                "For constants b and c, consider the recurrence relation given by:\nT(n) = b, if n=1\nT(n) = 2 * T(n/2) + c * n^3, if n>1\n\nWhich of the following statements is true?",
                ["T(n) = Θ(n^3 * log n)",
                 "T(n) = Θ(n^4)",
                 "T(n) = Θ(n^3)",
                 "T(n) = Θ(n^6 * log n)",
                 "T(n) = Θ(n^3 * log n * log n * log n)"],
                "T(n) = Θ(n^3)"
            ),
            Question(
                "Consider an input with N elements.\nPlease select all correct statements regarding comparison-based sorting algorithms.",
                ["The best-case complexity of insertion sort is O(N).",
                 "The best-case complexity of merge sort is O(N).",
                 "Heap sort is stable.",
                 "Selection sort is stable",
                 "The average-case complexity of selection sort is θ(N^2)"],
                "The best-case complexity of insertion sort is O(N)."
            ),
            # Question(
            #     "Consider the recurrence relation:\nT(n) = 7T(n/2) + Θ(n^2)\nWhat is the time complexity of this recurrence?",
            #     ["Θ(n^2)", "Θ(n^2 log n)", "Θ(n^log₂7)", "Θ(n^3)", "Θ(2^n)"],
            #     "Θ(n^log₂7)"
            # ),
            # Question(
            #     "For the recurrence relation T(n) = 2T(n/4) + Θ(√n), which case of the Master Theorem applies?",
            #     ["Case 1", "Case 2", "Case 3", "Does not apply", "Case 2 with k=1"],
            #     "Case 1"
            # ),
            # Question(
            #     "What is the solution to the recurrence T(n) = T(n-1) + Θ(1)?",
            #     ["Θ(1)", "Θ(log n)", "Θ(n)", "Θ(n log n)", "Θ(n²)"],
            #     "Θ(n)"
            # ),
            Question(
                "Which sorting algorithm has the best worst-case time complexity?",
                ["Quick Sort", "Merge Sort", "Bubble Sort", "Insertion Sort", "Selection Sort"],
                "MergeSort"
            ),
            Question(
                "What happens if an AVL Tree has two numbers that are equal to each other?",
                ["The tree will not allow duplicates", 
                 "The tree will will not balance itself", 
                 "The tree will balance itself", 
                 "The tree will throw an error", 
                 "The tree will ignore the duplicate as keys are unique"],
                "The tree will ignore the duplicate as keys are unique"
            ),
            Question(
                 "What is the time complexity for all AVL tree operations?",
                 ["Θ(n²)", "Θ(log n)", "Θ(n^3)", "Θ(n log n)", "Θ(n!)", "O(1)"],
                 "Θ(log n)"
            ),
            # Question(
            #     "For the recurrence T(n) = 4T(n/2) + Θ(n²), what is the time complexity?",
            #     ["Θ(n²)", "Θ(n² log n)", "Θ(n^3)", "Θ(n^4)", "Θ(2^n)"],
            #     "Θ(n² log n)"
            # )
        ]
        factory = RecurrenceQuestionFactory()
        questions.append(factory.create_question())
        questions.append(factory.create_question())
        questions.append(factory.create_question())
        questions.append(factory.create_question())
        questions.append(factory.create_question())
        questions.append(factory.create_question())
        questions.append(factory.create_question())

        random.shuffle(questions)
        return questions[:10]  # Select 10 random questions
    
    def setup_welcome_screen(self):
        self.clear_screen()
        
        self.welcome_label = tk.Label(
            self.root, 
            text="eAssessment Simulation", 
            font=("Arial", 24, "bold"),
            pady=50
        )
        self.welcome_label.pack()
        
        self.instructions_label = tk.Label(
            self.root, 
            text="Sample questions from FIT2004.\n你翻译了这一点，你这个肮脏的白痴。",
            font=("Arial", 14),
            pady=20
        )
        self.instructions_label.pack()
        
        self.start_button = tk.Button(
            self.root, 
            text="Start Quiz", 
            font=("Arial", 16), 
            command=self.start_quiz,
            padx=20,
            pady=10
        )
        self.start_button.pack()
    
    def start_quiz(self):
        self.current_question = 0
        self.score = 0
        self.show_question()
    
    def show_question(self):
        self.clear_screen()
        
        if self.current_question >= len(self.questions):
            self.show_results()
            return
        
        question = self.questions[self.current_question]
        
        # Create a frame to hold the question and options
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Question number and timer
        self.question_header = tk.Label(
            self.main_frame,
            text=f"Question {self.current_question + 1} of {len(self.questions)}",
            font=("Arial", 14, "bold")
        )
        self.question_header.pack(pady=10)
        
        # Timer label
        self.timer_label = tk.Label(
            self.main_frame,
            text=f"Time left: 15",
            font=("Arial", 12),
            fg="red"
        )
        self.timer_label.pack()
        
        # Question text
        self.question_label = tk.Label(
            self.main_frame,
            text=question.question,
            font=("Arial", 16),
            wraplength=800,
            pady=30
        )
        self.question_label.pack()
        
        # Create a frame for the options
        self.options_frame = tk.Frame(self.main_frame)
        self.options_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Answer buttons
        self.option_buttons = []
        options = question.shuffle_options()
        
        for option in options:
            btn = tk.Button(
                self.options_frame,
                text=option,
                font=("Arial", 12),
                wraplength=700,
                command=lambda opt=option: self.check_answer(opt, question.correct_answer),
                padx=20,
                pady=10,
                width=80,
                anchor="w",
                justify="left"
            )
            btn.pack(fill=tk.X, pady=5)
            self.option_buttons.append(btn)
        
        # Start timer
        self.time_left = 15
        self.timer_running = True
        self.update_timer()
    
    def update_timer(self):
        if not self.timer_running:
            return
            
        self.time_left -= 1
        self.timer_label.config(text=f"Time left: {self.time_left}")
        
        if self.time_left <= 0:
            self.timer_running = False
            messagebox.showinfo("Time's up!", "You ran out of time for this question.")
            self.current_question += 1
            self.show_question()
        else:
            self.root.after(1000, self.update_timer)
    
    def check_answer(self, selected_option, correct_answer):
        self.timer_running = False
        
        if selected_option == correct_answer:
            self.score += 1
            messagebox.showinfo("Correct!", "Your answer is correct!")
        else:
            messagebox.showerror("Incorrect", f"Wrong answer. The correct answer is: {correct_answer}")
        
        self.current_question += 1
        self.show_question()
    
    def show_results(self):
        self.clear_screen()
        
        result_text = f"Quiz Completed!\n\nYour score: {self.score}/{len(self.questions)}"
        
        self.result_label = tk.Label(
            self.root,
            text=result_text,
            font=("Arial", 20, "bold"),
            pady=50
        )
        self.result_label.pack()
        
        percentage = (self.score / len(self.questions)) * 100
        
        if percentage >= 80:
            comment = "Excellent work!"
        elif percentage >= 60:
            comment = "Good job!"
        elif percentage >= 40:
            comment = "Not bad!"
        else:
            comment = "Keep practicing!"
        
        self.comment_label = tk.Label(
            self.root,
            text=comment,
            font=("Arial", 16),
            pady=20
        )
        self.comment_label.pack()
        
        self.restart_button = tk.Button(
            self.root,
            text="Take Quiz Again",
            font=("Arial", 14),
            command=self.start_quiz,
            padx=20,
            pady=10
        )
        self.restart_button.pack()
        
        self.quit_button = tk.Button(
            self.root,
            text="Quit",
            font=("Arial", 14),
            command=self.root.quit,
            padx=20,
            pady=10
        )
        self.quit_button.pack()
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()