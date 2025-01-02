import os

required_files = ['math.txt', 'statistics.txt', 'physics.txt', 'student_names.txt'] # необхідні документи

files_in_directory = os.listdir()

for file in required_files:
    if file not in files_in_directory:                                 #перевірка на наявність
        raise FileNotFoundError(f"Файл {file} не знайдено в поточній директорії.")

with open('math.txt', 'r') as math_file, \
     open('statistics.txt', 'r') as stats_file, \
     open('physics.txt', 'r') as physics_file, \
     open('student_names.txt', 'r') as names_file:

    math_scores = [int(line.strip()) for line in math_file]
    stats_scores = [int(line.strip()) for line in stats_file]
    physics_scores = [int(line.strip()) for line in physics_file]
    student_names = [line.strip() for line in names_file]       #читання оцінок з видаленням зайвих пробілів


    if not (len(student_names) == len(math_scores) == len(stats_scores) == len(physics_scores)):    #перевірка на кількість
        raise ValueError("Кількість студентів не відповідає кількості оцінок у файлах.")

    students_data = {}
    for i in range(len(student_names)):
        name = student_names[i]
        students_data[name] = {
            'math': math_scores[i],
            'statistics': stats_scores[i],
            'physics': physics_scores[i]           #створення словника в словнику, з ключом у вигляді ім'я студента та значенням цього "іншого" словника
        }

print("Статистика по студентам:")
average_scores = {}
for name, grades in students_data.items():
    average = sum(grades.values()) / len(grades)
    average_scores[name] = average
    print(f"Студент: {name}, середня оцінка: {average:.3f}\n")  #знаходження середнього балу


top_students = sorted(average_scores.items(), key=lambda x: x[1], reverse=True)[:3]     #сортування на спад з виводом найкращих
print("Топ 3 студенти з найвищими середніми оцінками:")
for student in top_students:
    print (student[0])

total_students = len(student_names)
subjects = ['math', 'statistics', 'physics']
subject_stats = {}

for subject in subjects:
    subject_grades = [students_data[name][subject] for name in student_names]       #пошук мінімальної, максимальної та середньої оцінок відповідно до кожного з предметів
    average = sum(subject_grades) / total_students
    min_score = min(subject_grades)
    max_score = max(subject_grades)
    subject_stats[subject] = {      
        'average': average,
        'min': min_score,
        'max': max_score
    }       

print(f"Загальна кількість студентів: {total_students}\n")
for subject, stats in subject_stats.items():
    print(f"Предмет: {subject}, середня оцінка: {stats['average']:.2f}, min оцінка: {stats['min']}, max оцінка: {stats['max']}\n")

print("Найвищі бали по кожному предмету:")
for subject in subjects:
    max_score = subject_stats[subject]['max']
    top_students_subject = [name for name in student_names if students_data[name][subject] == max_score]       #Пошук найкращого студента відповідно по кожному предмету
    for student in top_students_subject:
        print(f"Предмет: {subject} | Студент: {student}, оцінка: {max_score}\n")

low_score_students = [name for name, avg in average_scores.items() if avg < 50]
print(f"Кількість студентів з середньою оцінкою нижче 50: {len(low_score_students)}")   #пошук студентів з оцінкою меншою 50
for student in low_score_students:
    print(student)