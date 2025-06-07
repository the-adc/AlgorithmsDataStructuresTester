from abc import ABC, abstractmethod
import random
import math

class RecurrenceQuestion(ABC):
    def __init__(self):
        self.question = ""
        self.options = []
        self.correct_answer = ""
        self.difficulty = 1  # 1-5 scale
        self.generate_question()
    
    @abstractmethod
    def generate_question(self):
        pass
    
    def shuffle_options(self):
        random.shuffle(self.options)
        return self.options
    
    def get_question(self):
        return {
            "question": self.question,
            "options": self.options,
            "answer": self.correct_answer
        }

class MasterTheoremQuestion(RecurrenceQuestion):
    def generate_question(self):
        # Randomly generate recurrence parameters
        a = random.choice([1, 2, 3, 4, 7, 8])
        b = random.choice([2, 3, 4])
        k = random.randint(0, 2)
        
        # Generate different f(n) based on cases
        case = random.choice([1, 2, 3])
        
        if case == 1:  # Case 1: f(n) = O(n^log_b(a-ε))
            f_exp = math.log(a, b) - random.uniform(0.1, 0.5)
            f_n = f"n^{f_exp:.1f}"
            complexity = f"Θ(n^{math.log(a, b):.3f})"
        elif case == 2:  # Case 2: f(n) = Θ(n^log_b(a))
            f_n = f"n^{math.log(a, b):.1f} log n"
            complexity = f"Θ(n^{math.log(a, b):.3f} log n)"
        else:  # Case 3: f(n) = Ω(n^log_b(a+ε))
            f_exp = math.log(a, b) + random.uniform(0.1, 0.5)
            f_n = f"n^{f_exp:.1f}"
            complexity = f"Θ({f_n})"
        
        self.question = f"""Consider the recurrence relation:
T(n) = {a}T(n/{b}) + {f_n}
        
Which case of the Master Theorem applies and what is the solution?"""
        
        # Generate options
        self.options = [
            f"Case 1: Θ(n^{math.log(a, b):.3f})",
            f"Case 2: Θ(n^{math.log(a, b):.3f} log n)",
            f"Case 3: Θ({f_n})",
            "Master Theorem does not apply",
            f"Case {case}: {complexity}"
        ]
        self.correct_answer = f"Case {case}: {complexity}"

class RecursionTreeQuestion(RecurrenceQuestion):
    def generate_question(self):
        a = random.randint(2, 4)
        b = random.randint(2, 3)
        k = random.randint(0, 2)
        
        # Generate question text
        self.question = f"""Draw the recursion tree for:
T(n) = {a}T(n/{b}) + Θ(n^{k})
        
What is the total work at each level and the number of levels?"""
        
        # Calculate correct values
        levels = math.log(1, b)  # Simplified for example
        work_per_level = f"a^i * (n/b^i)^{k}"
        total_work = f"Θ(n^{k} log n)" if k == math.log(a, b) else f"Θ(n^{max(k, math.log(a, b))})"
        
        # Generate options
        self.options = [
            f"{levels:.1f} levels, {work_per_level} work per level, {total_work} total",
            f"{levels:.1f} levels, constant work, Θ(log n) total",
            f"n levels, n work per level, Θ(n²) total",
            "Cannot be determined",
            f"{levels:.1f} levels, {work_per_level} work per level, Θ(n) total"
        ]
        self.correct_answer = self.options[0]

class DivideConquerQuestion(RecurrenceQuestion):
    def generate_question(self):
        parts = random.randint(2, 5)
        work = random.choice(["n", "n²", "n log n", "1"])
        
        self.question = f"""A divide-and-conquer algorithm divides a problem into {parts} 
subproblems each of size n/2 and spends {work} time on the divide/combine steps.
        
What is the recurrence relation and its solution?"""
        
        # Calculate solution
        if work == "n":
            solution = "Θ(n log n)" if parts == 2 else f"Θ(n^{math.log(parts, 2)})"
        elif work == "n²":
            solution = "Θ(n²)"
        else:
            solution = f"Θ({work} log n)" if parts == 2 else "Varies"
        
        self.options = [
            f"T(n) = {parts}T(n/2) + Θ({work}); {solution}",
            f"T(n) = T(n/{parts}) + Θ({work}); Θ(log n)",
            f"T(n) = {parts}T(n/2) + Θ(1); Θ(n^{math.log(parts, 2)})",
            f"T(n) = {parts}T(n-1) + Θ({work}); Θ({parts}^n)",
            "Cannot be determined from given information"
        ]
        self.correct_answer = self.options[0]

class RecurrenceQuestionFactory:
    @staticmethod
    def create_question():
        question_type = random.choice([
            MasterTheoremQuestion,
            RecursionTreeQuestion,
            DivideConquerQuestion
            # Could add more types here
        ])
        return question_type()