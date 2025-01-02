file_path = 'netflix_list.csv'

# 1. Зчитування даних із файлу
with open(file_path, 'r', encoding='utf-8') as file:
    rows = file.readlines()

# 2. Обробка заголовків (припускаємо, що заголовок — це перший рядок)
headers = [header.strip(' "') for header in rows[0].strip().split(',')]
data = []

# 3. Обробка кожного рядка CSV з урахуванням можливих лапок
for row in rows[1:]:
    values, current_value, in_quotes = [], '', False
    for char in row:
        if char == '"':
            in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            values.append(current_value.strip(' "'))
            current_value = ''
        else:
            current_value += char
    # Додаємо останнє поле
    values.append(current_value.strip(' "'))
    data.append(values)

# 4. Фільтрація за рейтингом > 7.5 (приклад із вашого початкового коду)
rating_index = headers.index('rating')
filtered_by_rating = [
    row for row in data
    if len(row) > rating_index 
    and row[rating_index].replace('.', '', 1).isdigit() 
    and float(row[rating_index]) > 7.5
]
filtered_top_columns = [row[:5] for row in filtered_by_rating]

# 5. Генератор Netflix (приклад із вашого початкового коду)
def netflix_generator(data, headers):
    indices = {
        'language': headers.index('language'),
        'type': headers.index('type'),
        'endYear': headers.index('endYear')
    }
    for row in data:
        if (
            len(row) > max(indices.values()) and
            row[indices['language']] == 'English' and
            row[indices['type']] in ['tvSeries', 'movie'] and
            row[indices['endYear']].isdigit() and int(row[indices['endYear']]) > 2015
        ):
            yield row

# 6. Використання генератора (виводимо перші 5 рядків, як у прикладі)
netflix_gen = netflix_generator(data, headers)
generated_rows = [next(netflix_gen) for _ in range(5)]

# --------------------------------------------------------------------------------
# ДОДАТКОВІ ВИМОГИ
# --------------------------------------------------------------------------------

# (A) ІТЕРАТОР для поля cast, якщо довжина значення > 50 символів
class CastIterator:
    def __init__(self, data, headers):
        self.data = data
        self.headers = headers
        self.cast_index = headers.index('cast')  # визначаємо індекс колонки 'cast'
        self.position = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        while self.position < len(self.data):
            row = self.data[self.position]
            self.position += 1
            # Перевіряємо, чи поле 'cast' є достатньо довгим
            if len(row) > self.cast_index and len(row[self.cast_index]) > 50:
                return row[self.cast_index]
        raise StopIteration

cast_iter = CastIterator(data, headers)

print("Перші 10 полів 'cast' (довжина > 50 символів):")
count_printed = 0
for cast_value in cast_iter:
    print(cast_value)
    count_printed += 1
    if count_printed >= 10:
        break

# (B) ФУНКЦІЯ для підрахунку:
#     (a) скільки дорослих шоу (isAdult == 1),
#     (b) середній рейтинг для фільмів/шоу з понад 1000 голосів (numVotes > 1000).
def adult_and_average_rating(data, headers):
    # Індекси потрібних полів
    is_adult_idx = headers.index('isAdult')
    rating_idx = headers.index('rating')
    num_votes_idx = headers.index('numVotes')
    
    adult_count = 0
    rating_sum = 0.0
    rating_count = 0
    
    for row in data:
        # (a) Підрахунок дорослих шоу (isAdult == 1)
        if len(row) > is_adult_idx and row[is_adult_idx].isdigit():
            if int(row[is_adult_idx]) == 1:
                adult_count += 1
        
        # (b) Середній рейтинг шоу/фільмів з понад 1000 голосів
        if (
            len(row) > max(rating_idx, num_votes_idx)
            and row[rating_idx].replace('.', '', 1).isdigit()
            and row[num_votes_idx].isdigit()
        ):
            if int(row[num_votes_idx]) > 1000:
                rating_sum += float(row[rating_idx])
                rating_count += 1
    
    average_rating = rating_sum / rating_count if rating_count > 0 else 0
    return adult_count, average_rating

adult_count, avg_rating_1000 = adult_and_average_rating(data, headers)
print("\nКількість шоу/фільмів для дорослих (isAdult == 1):", adult_count)
print("Середній рейтинг шоу/фільмів із >1000 голосів:", avg_rating_1000)

# (C) СПИСОК ЗАГОЛОВКІВ, які:
#     (a) мають більше 10 епізодів
#     (b) мають рейтинг вище середнього
# Використаємо comprehension + генератор для обчислення середнього рейтингу

# Спочатку порахуємо середній рейтинг по всьому датасету
all_ratings = []
for row in data:
    if len(row) > rating_index and row[rating_index].replace('.', '', 1).isdigit():
        all_ratings.append(float(row[rating_index]))

dataset_avg_rating = sum(all_ratings) / len(all_ratings) if len(all_ratings) > 0 else 0

# Тепер створимо список заголовків з умовами:
#     1) episodes > 10
#     2) rating > dataset_avg_rating

# Перевіримо, чи в нас існують колонки episodes та title
# (у вихідних даних CSV вони можуть називатися по-різному, уточніть за потреби)
try:
    episodes_index = headers.index('episodes')
    title_index = headers.index('title')
except ValueError:
    # Якщо таких полів немає, виведемо попередження
    print("\nУвага! У файлі немає полів 'episodes' або 'title'. Неможливо створити потрібний список.")
    episodes_index = None
    title_index = None

if episodes_index is not None and title_index is not None:
    titles_above_avg = [
        row[title_index] 
        for row in data
        if (
            len(row) > max(episodes_index, rating_index) 
            and row[episodes_index].isdigit() 
            and int(row[episodes_index]) > 10
            and row[rating_index].replace('.', '', 1).isdigit()
            and float(row[rating_index]) > dataset_avg_rating
        )
    ]

    print("\nCписок заголовків з >10 епізодами та рейтингом вище середнього:")
    for t in titles_above_avg:
        print(" -", t)

# --------------------------------------------------------------------------------
# Приклад виводу (залежить від даних у 'netflix_list.csv'):
# --------------------------------------------------------------------------------

print("\nВідфільтровані дані (перші 6 рядків, рейтинг > 7.5):")
for row in filtered_top_columns[:6]:
    print(row)

print("\nРезультати генератора (перші 5 рядків):")
for row in generated_rows:
    print(row)
