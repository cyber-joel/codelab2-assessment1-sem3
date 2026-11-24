import random
import tkinter as tk
from tkinter import messagebox 

# QUIZ RULES
TOTAL_QUESTIONS = 10
POINTS_FIRST_TRY = 10
POINTS_SECOND_TRY = 5

# DEFINES NUMBER RANGES FOR EACH DIFFICULTY LEVEL
LEVELS = {
    "Easy": (1, 9),            
    "Moderate": (10, 99),      
    "Advanced": (1000, 9999),  
}

# COLOUR AND FONT 
BG = "#1e2235"
CARD = "#2a2f4a"
ACCENT = "#00FFF7"
GOOD = "#15FF00"
BAD = "#FF0000"
WARN = "#FFC100"
TEXT = "#FFFFFF"
MUTED = "#FFFFFF"
FONT = "Times New Roman"
 
# GENERATES A RANDOM NUMBER BASED ON THE SELECTED LEVEL
def randomInt(level):
    low, high = LEVELS[level]
    return random.randint(low, high)
 
# RANDOMLY SELECT ADDITION OR SUBTRACTION 
def decideOperation():
    return random.choice(["+", "-"])
 
# CHECKS THE USER'S ANSWER AND CALCULATE THE POINTS 
def isCorrect(user_answer, correct_answer, attempt):
    if user_answer == correct_answer:
        if attempt == 1:
            return True, POINTS_FIRST_TRY, "Correct! +10 points"
        return True, POINTS_SECOND_TRY, "Correct on the second try! +5 points"
 
    if attempt == 1:
        return False, 0, "Not quite - you get one more chance."
    return False, 0, f"Wrong again. The answer was {correct_answer}."
 
# CALCULATES THE GRADE BASED ON THE FINAL SCORE 
def getGrade(score):
    if score >= 90:
        return "A+", "Outstanding! You're a maths machine."
    if score >= 80:
        return "A", "Excellent work!"
    if score >= 70:
        return "B", "Good job, keep it up."
    if score >= 60:
        return "C", "Decent, a bit more practice will help."
    if score >= 50:
        return "D", "You passed, but revise your basics."
    return "F", "Don't give up - try again!"
 
# CREATES A REUSABLE LABEL FOR THE PROGRAM
def _label(parent, text, size=12, bold=False, colour=TEXT, bg=BG):
    weight = "bold" if bold else "normal"
    return tk.Label(parent, text=text, bg=bg, fg=colour, font=(FONT, size, weight))

# CREATES A REUSABLE BUTTON FOR THE PROGRAM
def _button(parent, text, command, colour=ACCENT, width=18):
    return tk.Button(
        parent, text=text, command=command, width=width,
        bg=colour, fg="#10131f", activebackground=TEXT,
        font=(FONT, 12, "bold"), relief="flat", cursor="hand2", pady=6,
    )

# DISPLAYS THE MAIN MENU AND DIFFICULTY OPTIONS
def displayMenu(parent, on_select):
    frame = tk.Frame(parent, bg=BG)
    _label(frame, "ARITHMETIC QUIZ", 24, True, ACCENT).pack(pady=(40, 5))
    _label(frame, "DIFFICULTY LEVEL", 14, True, MUTED).pack(pady=(0, 25))

    # DIFFICULTY DESCRIPTIONS
    descriptions = {
        "Easy": "1.  Easy       (1-digit numbers)",
        "Moderate": "2.  Moderate   (2-digit numbers)",
        "Advanced": "3.  Advanced   (4-digit numbers)",
    }
    # SET A DIFFERENT COLOUR FOR EACH DIFFICULTY
    colours = {"Easy": GOOD, "Moderate": WARN, "Advanced": BAD}
    # CREATE A BUTTON FOR EACH DIFFICULTY LEVEL
    for level, text in descriptions.items():
        _button(frame, text, lambda lv=level: on_select(lv),
                colours[level], width=30).pack(pady=7)
        
    # DISPLAYS QUIZ INFORMATION
    _label(frame, f"{TOTAL_QUESTIONS} questions per round  |  "
                  "10 points first try, 5 points second try", 10, False, MUTED).pack(pady=(30, 0))
    return frame

# CREATES THE QUESTION SCREEN
def displayProblem(parent, on_submit):
    frame = tk.Frame(parent, bg=BG)
    w = {}
    
    # DISPLAYS QUESTION AND CURRENT SCORE
    top = tk.Frame(frame, bg=BG)
    top.pack(fill="x", padx=30, pady=(25, 0))
    w["progress"] = _label(top, "", 12, True, MUTED)
    w["progress"].pack(side="left")
    w["score"] = _label(top, "", 12, True, ACCENT)
    w["score"].pack(side="right")
    
    # CREATE THE QUESTION DISPLAY CARD
    card = tk.Frame(frame, bg=CARD, padx=30, pady=30)
    card.pack(padx=30, pady=30, fill="x")
    w["level"] = _label(card, "", 11, False, MUTED, CARD)
    w["level"].pack()
    w["question"] = _label(card, "", 36, True, TEXT, CARD)
    w["question"].pack(pady=15)
    w["attempt"] = _label(card, "", 11, False, WARN, CARD)
    w["attempt"].pack()

    # ENTRY BOX FOR THE USER'S ANSWER
    w["entry"] = tk.Entry(card, font=(FONT, 22), justify="center", width=10,
                          bg=BG, fg=TEXT, insertbackground=TEXT, relief="flat")
    w["entry"].pack(pady=15, ipady=6)

    # ALLOW THE USER TO SUBMIT AN ANSWER USING THE ENTER KEY
    w["entry"].bind("<Return>", lambda event: on_submit())

    # CREATE THE SUBMIT BUTTON
    w["button"] = _button(card, "Submit", on_submit)
    w["button"].pack(pady=5)

    # DISPLAY FEEDBACK AFTER SUBMITTING AN ANSWER
    w["feedback"] = _label(frame, "", 14, True, TEXT)
    w["feedback"].pack()
    return frame, w

# DISPLAYS THE FINAL SCORE, GRADE AND REPLAY OPTIONS
def displayResults(parent, score, on_replay, on_quit):
    grade, remark = getGrade(score)
    frame = tk.Frame(parent, bg=BG)
    _label(frame, "QUIZ COMPLETE", 24, True, ACCENT).pack(pady=(40, 20))

    # DISPLAY THE FINAL RESULTS
    card = tk.Frame(frame, bg=CARD, padx=40, pady=25)
    card.pack(pady=10)
    _label(card, "Your score", 12, False, MUTED, CARD).pack()
    _label(card, f"{score} / 100", 34, True, TEXT, CARD).pack(pady=5)
    _label(card, f"Grade: {grade}", 26, True, GOOD if score >= 50 else BAD, CARD).pack()
    _label(card, remark, 12, False, MUTED, CARD).pack(pady=(8, 0))

    # ASK THE USER WHETHER THEY WANT TO PLAY AGAIN
    _label(frame, "Would you like to play again?", 13, True, TEXT).pack(pady=(30, 10))
    _button(frame, "Yes, play again", on_replay, GOOD).pack(pady=5)
    _button(frame, "No, quit", on_quit, BAD).pack(pady=5)
    return frame

# MAIN CLASS THAT CONTROLS THE QUIZ
class QuizApp:

    # INITIALISE THE PROGRAM
    def __init__(self, root):
        self.root = root
        root.title("Arithmetic Quiz")
        root.geometry("520x620")
        root.configure(bg=BG)
        root.resizable(False, False)

        # CREATES THE MAIN CONTAINER
        self.container = tk.Frame(root, bg=BG)
        self.container.pack(fill="both", expand=True)
        self.current_frame = None
        self.show_menu()

    # SWITCH BETWEEN DIFFERENT PROGRAM
    def _switch(self, frame):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frame
        frame.pack(fill="both", expand=True)

    # DISPLAYS THE MAIN MENU
    def show_menu(self):
        self._switch(displayMenu(self.container, self.start_quiz))

    # START A NEW QUIZ WITH THE SELECTED DIFFICULTY
    def start_quiz(self, level):
        self.level = level
        self.score = 0
        self.question_no = 0
        self.locked = False
        frame, self.w = displayProblem(self.container, self.check_answer)
        self._switch(frame)
        self.w["level"].config(text=f"Level: {level}")
        self.next_question()

    # DISPLAYS THE NEXT QUESTION
    def next_question(self):
    
        # CHECK WHETHER ALL QUESTIONS ARE COMPLETED
        if self.question_no >= TOTAL_QUESTIONS:
            self.finish_quiz()
            return
        self.question_no += 1
        self.attempt = 1
        self.locked = False

        # GENERATE RANDOM NUMBERS
        self.num1 = randomInt(self.level)
        self.num2 = randomInt(self.level)
        self.op = decideOperation()

        # CALCULATES THE CORRECT ANSWER
        self.answer = self.num1 + self.num2 if self.op == "+" else self.num1 - self.num2
        self.w["progress"].config(text=f"Question {self.question_no} of {TOTAL_QUESTIONS}")
        self.w["score"].config(text=f"Score: {self.score}")
        self.w["question"].config(text=f"{self.num1} {self.op} {self.num2} =")
        self.w["attempt"].config(text="Attempt 1 of 2")
        self.w["feedback"].config(text="")
        self.w["entry"].config(state="normal")
        self.w["entry"].delete(0, tk.END)
        self.w["entry"].focus_set()
        self.w["button"].config(state="normal")

    # CHECKS THE ANSWER
    def check_answer(self):
    
        # PREVENTS MULTIPLE SUBMISSIONS WHILE MOVING TO THE NEXT QUESTION
        if self.locked:
            return
        raw = self.w["entry"].get().strip()

        # VALIDATE THAT THE INPUT IS A WHOLE NUMBER
        try:
            user_answer = int(raw)
        except ValueError:
            self.w["feedback"].config(text="Please enter a whole number.", fg=WARN)
            return

        # CHECKS THE ANSWER AND CALCULATE POINTS
        right, points, message = isCorrect(user_answer, self.answer, self.attempt)
        self.score += points
        self.w["score"].config(text=f"Score: {self.score}")
        if right:
            self.w["feedback"].config(text=message, fg=GOOD)
            self._lock_and_advance()
        elif self.attempt == 1:

            # GIVE THE USER ONE MORE CHANCE
            self.attempt = 2
            self.w["attempt"].config(text="Attempt 2 of 2")
            self.w["feedback"].config(text=message, fg=WARN)
            self.w["entry"].delete(0, tk.END)
            self.w["entry"].focus_set()

        else:
                    
            # DISPLAYS THE CORRECT ANSWER AFTER THE SECOND WRONG ATTEMPT
            self.w["feedback"].config(text=message, fg=BAD)
            self._lock_and_advance(delay=1800)

    # DISABLE INPUTS AND MOVE TO THE NEXT QUESTIONS
    def _lock_and_advance(self, delay=1000):
        self.locked = True
        self.w["entry"].config(state="disabled")
        self.w["button"].config(state="disabled")
        self.root.after(delay, self.next_question)

    # FINISH THE QUIZ AND DISPLAY THE RESULTS
    def finish_quiz(self):
        frame = displayResults(self.container, self.score, self.show_menu, self.quit_app)
        self._switch(frame)

    # ASK FOR CONFIRMATION BEFORE CLOSING THE PROGRAM
    def quit_app(self):
        if messagebox.askyesno("Quit", "Are you sure you want to exit?"):
            self.root.destroy()


# RUN THE PROGRAM
if __name__ == "__main__":
    root = tk.Tk()
    QuizApp(root)
    root.mainloop()