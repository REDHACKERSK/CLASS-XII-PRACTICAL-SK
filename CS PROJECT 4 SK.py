import csv
import random

# ---------------- INPUT ----------------
subjects = []
teachers = []

print("Enter 8 subjects and their teacher names:\n")

for i in range(1, 9):
    sub = input(f"Enter subject {i}: ")
    teacher = input(f"Enter teacher for {sub}: ")
    subjects.append(sub)
    teachers.append(teacher)

subject_teacher = {}
for i in range(len(subjects)):
    subject_teacher[subjects[i]] = teachers[i]

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
periods = ["P1", "P2", "P3", "P4", "LUNCH", "P5", "P6", "P7", "P8"]

open("Timetables/dummy.txt", "w").close()


# -------------- GENERATE DAY TIMETABLE --------------
def generate_day_timetable():

    class_day = {}
    for c in range(1, 9):
        class_day[c] = [""] * 9

    teacher_busy = {}
    for p in range(9):
        teacher_busy[p] = []

    for c in range(1, 9):
        available_subjects = subjects[:]

        for p in range(9):
            if p == 4:
                class_day[c][p] = "LUNCH"
                continue

            assigned = False

            used = []
            while len(used) < len(available_subjects):
                i = random.randint(0, len(available_subjects) - 1)
                if i in used:
                    continue
                used.append(i)

                sub = available_subjects[i]
                t = subject_teacher[sub]

                if t not in teacher_busy[p]:
                    class_day[c][p] = f"{sub} ({t})"
                    teacher_busy[p].append(t)
                    available_subjects.remove(sub)
                    assigned = True
                    break

            if not assigned:
                return None

    return class_day


# -------------- GENERATE WEEK TIMETABLES --------------
class_tables = {}
for c in range(1, 9):
    class_tables[c] = {}

for day in days:
    valid = None
    while valid is None:
        valid = generate_day_timetable()

    for c in range(1, 9):
        class_tables[c][day] = valid[c]


# -------------- SAVE CLASS TIMETABLES --------------
for c in range(1, 9):
    with open(f"Timetables/Class_{c}_Timetable.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Day/Period"] + periods)

        for day in days:
            writer.writerow([day] + class_tables[c][day])


# -------------- GENERATE TEACHER TIMETABLES --------------
def generate_teacher_tt(tname):
    tt = {}
    for day in days:
        tt[day] = ["FREE"] * 9

    for c in range(1, 9):
        for day in days:
            for p in range(9):
                cell = class_tables[c][day][p]
                if cell != "LUNCH" and tname in cell:
                    tt[day][p] = f"Class {c}"

    return tt


# -------------- SAVE TEACHER TIMETABLES --------------
for t in teachers:
    t_tt = generate_teacher_tt(t)

    with open(f"Timetables/{t}_Teacher_Timetable.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Day/Period"] + periods)

        for day in days:
            writer.writerow([day] + t_tt[day])


print("\nTimetables successfully created!")
