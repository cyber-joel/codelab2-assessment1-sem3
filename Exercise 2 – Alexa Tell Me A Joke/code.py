import os
import random
import tkinter as tk
from tkinter import messagebox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JOKES_FILE = os.path.join(BASE_DIR, "randomJokes.txt")

BG = "#1e2235"
CARD = "#2a2f4a"
FG = "#FFFFFF"
ACCENT = "#00FFF7"
BAD = "#FF0000"

# DEFINE A FUNCTION TO LOAD AND ORGANIZE JOKES FROM THE TEXT FILE
def load_jokes(path):
    jokes = []
    # OPEN THE TEXT FILE USING UTF-8 ENCODING
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if "?" not in line:
                continue
            # SPLIT THE JOKE INTO SETUP AND PUNCHLINE USING THE QUESTION MARK
            setup, _, punchline = line.partition("?")
            setup, punchline = setup.strip(), punchline.strip()
            if setup and punchline:
                jokes.append((setup + "?", punchline))
    return jokes

# DEFINE THE JOKE ASSISTANT CLASS
class JokeAssistant:
    def __init__(self, root, jokes):
        self.root = root
        self.jokes = jokes
        self.deck = []
        self.current = None
        root.title("Joke Assistant")
        root.geometry("760x620")
        root.minsize(480, 380)
        root.resizable(False, False)
        root.configure(bg=BG)
        self._build_widgets()
        self._bind_keys()
        self._set_state("idle")
        
    # CREATES AND ARRANGES THE PROGRAM
    def _build_widgets(self):
        tk.Label(self.root, text="Alexa Tell Me A Joke", font=("Times New Roman", 20, "bold"),
                 bg=BG, fg=ACCENT).pack(pady=(18, 6))
        card = tk.Frame(self.root, bg=CARD, padx=16, pady=16)
        card.pack(fill="both", expand=True, padx=24, pady=14)
        self.setup_var = tk.StringVar(value="Press the button and I'll tell you a joke...")
        self.punch_var = tk.StringVar()
        self.setup_label = tk.Label(card, textvariable=self.setup_var, wraplength=460,
                                    justify="center", font=("Helvetica", 14),
                                    bg=CARD, fg=FG)
        self.setup_label.pack(expand=True, fill="both")
        self.punch_label = tk.Label(card, textvariable=self.punch_var, wraplength=460,
                                    justify="center", font=("Helvetica", 14, "bold italic"),
                                    bg=CARD, fg=BAD)
        self.punch_label.pack(expand=True, fill="both")
        bar = tk.Frame(self.root, bg=BG)
        bar.pack(pady=(0, 16))
        self.start_btn = tk.Button(bar, text="Alexa tell me a Joke", command=self.tell_joke)
        self.punch_btn = tk.Button(bar, text="Show Punchline", command=self.show_punchline)
        self.next_btn = tk.Button(bar, text="Next Joke", command=self.tell_joke)
        self.quit_btn = tk.Button(bar, text="Quit", command=self.quit_app)
        for col, btn in enumerate((self.start_btn, self.punch_btn, self.next_btn, self.quit_btn)):
            btn.grid(row=0, column=col, padx=5, ipadx=4, ipady=3)

    def _bind_keys(self):
        self.root.bind("<space>", lambda e: self.show_punchline()
                       if self.punch_btn["state"] == "normal" else None)
        self.root.bind("<Return>", lambda e: self.tell_joke())
        self.root.bind("<Escape>", lambda e: self.root.destroy())

    # DEFINE WHICH BUTTONS ARE ENABLED IN EACH ORDER
    def _set_state(self, state):
        
        states = {
            "idle":      ("normal",   "disabled", "disabled"),
            "setup":     ("disabled", "normal",   "normal"),
            "punchline": ("disabled", "disabled", "normal"),
        }
        start, punch, nxt = states[state]
        self.start_btn.config(state=start)
        self.punch_btn.config(state=punch)
        self.next_btn.config(state=nxt)

    # REFILL AND SHUFFLE THE DECK WHEN IT IS EMPTY
    def _draw_joke(self):
        if not self.deck:
            self.deck = self.jokes[:]
            random.shuffle(self.deck)
        return self.deck.pop()
    
    def tell_joke(self):
        self.current = self._draw_joke()
        self.setup_var.set(self.current[0])
        self.punch_var.set("")
        self._set_state("setup")

    # DISPLAYS THE PUNCHLINE IF A JOKE IS SELECTED
    def show_punchline(self):
        if self.current:
            self.punch_var.set(self.current[1])
            self._set_state("punchline")

    # ASK FOR CONFIRMATION BEFORE CLOSING THE PROGRAM
    def quit_app(self):
        if messagebox.askyesno("Quit", "Are you sure you want to exit?"):
            self.root.destroy()

# CREATE THE MAIN WINDOW
def main():
    root = tk.Tk()
    try:
        # LOAD JOKES FROM THE TEXT FILE
        jokes = load_jokes(JOKES_FILE)
    except FileNotFoundError:
        # SHOWS AN ERROR IF THE JOKES FILE IS MISSING
        messagebox.showerror("File not found", f"Could not find:\n{JOKES_FILE}")
        root.destroy()
        return

    # CHECK WHETHER THE JOKES FILE CONTAINS VALID JOKES
    if not jokes:
        messagebox.showerror("No jokes", "The jokes file is empty or badly formatted.")
        root.destroy()
        return

    JokeAssistant(root, jokes)
    root.mainloop()


# RUNS THE MAIN FUNCTION
if __name__ == "__main__":
    main()