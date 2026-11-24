import os
import tkinter as tk
from tkinter import messagebox, simpledialog

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "studentMarks.txt")

# LOAD STUDENT RECORDS FROM THE TEXT FILE
def loadStudents():
    students = []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as data_file:
            lines = data_file.readlines()
        for line in lines[1:]:
            parts = line.strip().split(",")
            if len(parts) == 6:
                try:
                    student = {
                        "code": parts[0],
                        "name": parts[1],
                        "course1": int(parts[2]),
                        "course2": int(parts[3]),
                        "course3": int(parts[4]),
                        "exam": int(parts[5])
                    }
                    students.append(student)
                except ValueError:
                    continue

    # DISPLAY AN ERROR IF THE FILE DOES NOT EXIST
    except FileNotFoundError:
        messagebox.showerror("Missing file", "studentMarks.txt was not found.")
    return students

# SAVE ALL STUDENT RECORDS TO THE TEXT FILE
def saveStudents():
    with open(DATA_FILE, "w", encoding="utf-8") as data_file:
        data_file.write(str(len(students)) + "\n")

        # WRITE EACH STUDENT'S DETAILS INTO THE FILE
        for student in students:
            data_file.write(
                f"{student['code']},{student['name']},"
                f"{student['course1']},{student['course2']},"
                f"{student['course3']},{student['exam']}\n"
            )

# CALCULATE COURSEWORK TOTAL, OVERALL MARK, PERCENTAGE AND GRADE
def getResults(student):
    coursework = student["course1"] + student["course2"] + student["course3"]
    total = coursework + student["exam"]
    percentage = (total / 160) * 100
    if percentage >= 70:
        grade = "A"
    elif percentage >= 60:
        grade = "B"
    elif percentage >= 50:
        grade = "C"
    elif percentage >= 40:
        grade = "D"
    else:
        grade = "F"
    return coursework, total, percentage, grade

# FORMAT STUDENT DETAILS AND RESULTS FOR DISPLAY
def formatStudent(student):
    coursework, total, percentage, grade = getResults(student)

    # RETURN STUDENT INFORMATION IN A READABLE FORMAT
    return (
        f"Name: {student['name']}\n"
        f"Student number: {student['code']}\n"
        f"Coursework total: {coursework}/60\n"
        f"Exam mark: {student['exam']}/100\n"
        f"Overall: {total}/160 ({percentage:.2f}%)\n"
        f"Grade: {grade}\n"
        f"{'-' * 42}\n"
    )

# DISPLAY TEXT IN THE OUTPUT TEXT BOX
def showText(content):
    output.config(state="normal")
    output.delete("1.0", tk.END)
    output.insert(tk.END, content)
    output.config(state="disabled")

# DISPLAY ALL STUDENT RECORDS AND CALCULATE THE CLASS AVERAGE
def viewAll():
    if not students:
        showText("No student records are available.")
        return
    content = ""
    percentage_total = 0

    # DISPLAY EACH STUDENT'S DETAILS AND ADD THEIR PERCENTAGES
    for student in students:
        content += formatStudent(student)
        percentage_total += getResults(student)[2]

    # CALCULATE THE CLASS AVERAGE PERCENTAGE
    average = percentage_total / len(students)

    # DISPLAY THE NUMBER OF STUDENTS AND CLASS AVERAGE
    content += f"\nNumber of students: {len(students)}"
    content += f"\nClass average: {average:.2f}%"
    showText(content)

# SEARCH FOR A STUDENT USING THEIR CODE OR FULL NAME
def findStudent():
    search_value = simpledialog.askstring(
        "Find student", "Enter the student's code or full name:"
    )

    # STOP IF THE USER CANCELS OR ENTERS NOTHING
    if not search_value:
        return

    # REMOVE EXTRA SPACES AND CONVERT THE SEARCH VALUE TO LOWERCASE
    search_value = search_value.strip().lower()

    # FIND STUDENTS MATCHING THE ENTERED CODE OR NAME
    matches = [
        student for student in students
        if student["code"].lower() == search_value
        or student["name"].lower() == search_value
    ]

    if matches:
        showText("".join(formatStudent(student) for student in matches))
    else:
        messagebox.showinfo("Not found", "No matching student was found.")

# DISPLAY THE STUDENT WITH THE HIGHEST OVERALL PERCENTAGE
def showHighest():
    if students:
        highest = max(students, key=lambda item: getResults(item)[2])
        showText("Highest overall mark\n\n" + formatStudent(highest))
    else:
        showText("No student records are available.")

# DISPLAY THE STUDENT WITH THE LOWEST OVERALL PERCENTAGE
def showLowest():
    if students:
        lowest = min(students, key=lambda item: getResults(item)[2])
        showText("Lowest overall mark\n\n" + formatStudent(lowest))
    else:
        showText("No student records are available.")

# COLLECT AND VALIDATE DETAILS FOR A NEW STUDENT
def readNewStudent():
    # ASK THE USER TO ENTER THE STUDENT CODE
    code = simpledialog.askstring("New student", "Student code (4 digits):")
    if code is None:
        return None

    # ASK THE USER TO ENTER THE STUDENT NAME
    name = simpledialog.askstring("New student", "Student name:")
    if name is None:
        return None
    marks = []

    # DEFINE THE MARK ENTRY PROMPTS AND THEIR MAXIMUM VALUES
    prompts = ["Coursework mark 1 (0-20):", "Coursework mark 2 (0-20):",
               "Coursework mark 3 (0-20):", "Exam mark (0-100):"]
    limits = [20, 20, 20, 100]

    # COLLECT EACH MARK WITH ITS ALLOWED MINIMUM AND MAXIMUM
    for prompt, limit in zip(prompts, limits):
        value = simpledialog.askinteger("New student", prompt, minvalue=0,
                                         maxvalue=limit)
        if value is None:
            return None
        marks.append(value)

    # VALIDATE THAT THE STUDENT CODE CONTAINS EXACTLY FOUR DIGITS
    if not code.isdigit() or len(code) != 4:
        messagebox.showerror("Invalid code", "Student code must contain 4 digits.")
        return None

    # CHECK THAT THE NAME IS NOT EMPTY AND DOES NOT CONTAIN COMMAS
    if not name.strip() or "," in name:
        messagebox.showerror("Invalid name", "Enter a name without commas.")
        return None

    # CHECK THAT THE STUDENT CODE IS NOT ALREADY IN USE
    if any(student["code"] == code for student in students):
        messagebox.showerror("Duplicate code", "That student code already exists.")
        return None

    # RETURN THE NEW STUDENT'S DETAILS AS A DICTIONARY
    return {
        "code": code, "name": name.strip(),
        "course1": marks[0], "course2": marks[1],
        "course3": marks[2], "exam": marks[3]
    }

# ADD A NEW STUDENT RECORD TO THE SYSTEM
def addStudent():
    student = readNewStudent()
    if student:
        students.append(student)
        saveStudents()
        messagebox.showinfo("Saved", "Student record added.")
        viewAll()

# SELECT A STUDENT USING THEIR CODE OR NAME
def selectStudent():
    value = simpledialog.askstring("Select student", "Enter student code or name:")

    # STOP IF THE USER CANCELS OR ENTERS NOTHING
    if not value:
        return None

    # REMOVE EXTRA SPACES AND CONVERT THE VALUE TO LOWERCASE
    value = value.strip().lower()

    # SEARCH FOR A MATCHING STUDENT
    for student in students:
        if student["code"].lower() == value or student["name"].lower() == value:
            return student

    # DISPLAY A MESSAGE IF NO MATCHING STUDENT IS FOUND
    messagebox.showinfo("Not found", "No matching student was found.")
    return None

# DELETE A SELECTED STUDENT RECORD
def deleteStudent():
    student = selectStudent()

    # ASK FOR CONFIRMATION BEFORE DELETING THE STUDENT
    if student and messagebox.askyesno(
        "Confirm deletion", f"Delete {student['name']}?"
    ):
        students.remove(student)
        saveStudents()
        viewAll()

# UPDATE THE DETAILS AND MARKS OF AN EXISTING STUDENT
def updateStudent():
    student = selectStudent()

    # STOP IF NO STUDENT IS SELECTED
    if not student:
        return

    # ASK THE USER TO ENTER THE UPDATED STUDENT NAME
    name = simpledialog.askstring("Update student", "New name:",
                                  initialvalue=student["name"])
    if name is None:
        return

    # VALIDATE THE UPDATED NAME
    if not name.strip() or "," in name:
        messagebox.showerror("Invalid name", "Enter a name without commas.")
        return

    # DEFINE THE MARK FIELDS AND THEIR MAXIMUM VALUES
    prompts = [("Coursework mark 1", "course1", 20),
               ("Coursework mark 2", "course2", 20),
               ("Coursework mark 3", "course3", 20),
               ("Exam mark", "exam", 100)]
    new_values = {}

    # COLLECT THE UPDATED MARKS FROM THE USER
    for label, key, limit in prompts:
        value = simpledialog.askinteger(
            "Update student", f"{label} (0-{limit}):",
            initialvalue=student[key], minvalue=0, maxvalue=limit
        )
        if value is None:
            return
        new_values[key] = value

    # UPDATE THE STUDENT NAME AND MARKS
    student["name"] = name.strip()
    student.update(new_values)
    saveStudents()

    # INFORM THE USER THAT THE UPDATE WAS SUCCESSFUL
    messagebox.showinfo("Updated", "Student record updated.")
    viewAll()

# SORT STUDENT RECORDS BY OVERALL PERCENTAGE
def sortStudents():
    direction = simpledialog.askstring(
        "Sort records", "Enter A for ascending or D for descending:"
    )

    # STOP IF THE USER CANCELS OR ENTERS NOTHING
    if not direction:
        return

    # CONVERT THE USER'S CHOICE TO UPPERCASE
    direction = direction.strip().upper()

    # VALIDATE THE SORTING DIRECTION
    if direction not in ("A", "D"):
        messagebox.showwarning("Invalid choice", "Enter A or D.")
        return

    # SORT STUDENTS BY PERCENTAGE IN THE SELECTED DIRECTION
    students.sort(key=lambda item: getResults(item)[2],
                  reverse=(direction == "D"))
    viewAll()

# LOAD STUDENT RECORDS
students = loadStudents()

# CREATE THE MAIN WINDOW
root = tk.Tk()
root.title("Student Manager")
root.geometry("760x620")
root.minsize(480, 380)
root.resizable(False, False)

# DISPLAY THE HEADING
tk.Label(root, text="STUDENT MANAGER", font=("Arial", 20, "bold")).pack(pady=10)

# CREATE A FRAME TO HOLD THE MENU BUTTONS
menu = tk.Frame(root)
menu.pack(pady=5)

# DEFINES THE BUTTONS AND THEIR FUNCTIONS
buttons = [
    ("View all records", viewAll),
    ("Find individual", findStudent),
    ("Highest mark", showHighest),
    ("Lowest mark", showLowest),
    ("Sort records", sortStudents),
    ("Add student", addStudent),
    ("Delete student", deleteStudent),
    ("Update student", updateStudent)
]

# CREATE AND ARRANGE THE MENU BUTTONS IN FOUR COLUMNS
for index, (label, action) in enumerate(buttons):
    tk.Button(menu, text=label, width=17, command=action).grid(
        row=index // 4, column=index % 4, padx=5, pady=5
    )

# CREATE THE TEXT BOX TO DISPLAY STUDENT INFORMATION
output = tk.Text(root, height=22, width=88, wrap="word")
output.pack(padx=12, pady=12, fill="both", expand=True)
output.config(state="disabled")

# CREATES THE QUIT BUTTON TO CLOSE
def quitApp():
    if messagebox.askyesno("Quit", "Are you sure you want to exit?"):
        root.destroy()
tk.Button(root, text="Quit", width=15, command=quitApp).pack(pady=8)

root.mainloop()