# Практическая работа №20 #

### Тема: Составление игровых программ с использованием звука ###

### Цель: Совершенствование навыков составления программ на основе графики ###

#### Вариант №12 ####

#### Задача: ####

> Написать игру "Таблица умножения"

##### Контрольный пример: #####

> Получаю:![prim1.gif](prim1.gif)

##### Системный анализ: #####

> Входные данные: `None`  
> Промежуточные
>
данные: `root`, `canvas`, `int gun_angle`, `int length`, `int x0`, `int y0`, `int x1`, `int y1`, `int speed`, `int score`, `list square_coords`, `list square_answers`, `list square_texts`
> Выходные данные: `canvas`, `int score`

##### Блок схема: #####

![dimm1_2.png](dimm1_2.png)

##### Код программы: #####

```python
from tkinter import *
import random
import math
import simpleaudio as sa


# Поворот пушки
def rotate_gun(angle):
    x0, y0 = 250, 375
    length = 125
    x1 = x0 + length * math.cos(math.radians(angle))
    y1 = y0 - length * math.sin(math.radians(angle))
    canvas.coords("gun", x0, y0, x1, y1)


# Нажатие клавиш
def KeyPressed(event):
    global gun_angle
    if event.keysym == 'w':
        gun_angle += 10
    elif event.keysym == 's':
        gun_angle -= 10
    elif event.keysym == 'f':
        fire_bullet()
    gun_angle %= 360
    rotate_gun(gun_angle)


# Стрельба
def fire_bullet():
    x0, y0 = 250, 375
    length = 125
    x1 = x0 + length * math.cos(math.radians(gun_angle))
    y1 = y0 - length * math.sin(math.radians(gun_angle))
    bullet = canvas.create_oval(x1 - 5, y1 - 5, x1 + 5, y1 + 5, fill="yellow", tags="bullet")
    play_sound("tankovyiy-vyistrel.wav")
    move_bullet(bullet, x1, y1, gun_angle)


def play_sound(filename):
    track = sa.WaveObject.from_wave_file(filename)
    track.play()


# Перемещение пули
def move_bullet(bullet, x, y, angle):
    speed = 10
    x += speed * math.cos(math.radians(angle))
    y -= speed * math.sin(math.radians(angle))
    canvas.coords(bullet, x - 5, y - 5, x + 5, y + 5)

    # Проверка попадания пули в квадраты
    if check_collision(x, y):
        canvas.delete(bullet)
    elif 0 < x < 500 and 0 < y < 600:
        root.after(50, move_bullet, bullet, x, y, angle)
    else:
        canvas.delete(bullet)


# Проверка попадания пули в квадраты
def check_collision(bullet_x, bullet_y):
    i = 0
    for coords in square_coords:
        if coords[0] <= bullet_x <= coords[2] and coords[1] <= bullet_y <= coords[3]:
            check_answer(i)
            return True
        i += 1
    return False


# Обновление вопроса
def update_question():
    global num1, num2, correct_answer
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)
    correct_answer = num1 * num2

    question_label.config(text=f"{num1} x {num2} = ?")

    # Генерируем случайные ответы для квадратов
    answers = [correct_answer]
    while len(answers) < 3:
        wrong_answer = random.randint(1, 81)
        if wrong_answer not in answers:
            answers.append(wrong_answer)

    random.shuffle(answers)

    # Обновляем текст в квадратах
    for i in range(3):
        canvas.itemconfig(square_texts[i], text=answers[i])
        square_answers[i] = answers[i]


# Проверка правильного ответа
def check_answer(index):
    global score
    if square_answers[index] == correct_answer:
        score += 1
        score_label.config(text=f"Score: {score}")
        play_sound("inecraft_levelu.wav")
    else:
        play_sound("inecraft_death.wav")
    update_question()


# Настройки окна
root = Tk()
root.title("Мото-мото")
root.geometry("500x600")

canvas = Canvas(root, height=500, width=500)
canvas.pack()

# Создаем объекты танка (корпус, ствол, колеса)
rectangle = canvas.create_rectangle(200, 300, 300, 490, fill="white")
line = canvas.create_line(250, 375, 250, 250, fill="green", width=10, tags="gun")
circle = canvas.create_oval(200, 325, 300, 425, fill="black")

# Начальный угол для пушки
gun_angle = 90

# Обработка клавиш
root.bind('<Key>', KeyPressed)

# Надпись с вопросом
question_label = Label(root, text="", font=("Arial", 20))
question_label.pack()

# Отображаем счет
score = 0
score_label = Label(root, text=f"Score: {score}", font=("Arial", 16))
score_label.pack()

# Создаем 3 квадрата с ответами
square_coords = [(50, 50, 150, 150), (200, 50, 300, 150), (350, 50, 450, 150)]
square_answers = [0, 0, 0]  # Массив для хранения ответов в квадратах
square_texts = []

# Создание квадратов и текстов для ответов
for i in range(3):
    coords = square_coords[i]
    square = canvas.create_rectangle(*coords, fill="lightblue")
    text = canvas.create_text((coords[0] + coords[2]) // 2, (coords[1] + coords[3]) // 2, text="", font=("Arial", 16))
    square_texts.append(text)

# Инициализация первого вопроса
update_question()

root.mainloop()


```

##### Результат работы программы: #####

> Оконное:
![prim1.gif](prim1.gif)

##### Контрольные вопросы: #####

1. Модули для работы программы:  
   `tkinter`: для создания графического интерфейса (окно, кнопки, текст, графические объекты).  
   `random`: для генерации случайных чисел (вопросы и ответы).  
   `math`: для математических расчетов (углы, тригонометрия для движения пули и поворота пушки).  
   `simpleaudio`: для воспроизведения звуков (звук выстрела, попадания и других событий).


2. Функции для работы программы:
   `rotate_gun(angle)`: поворачивает пушку на указанный угол.  
   `KeyPressed(event)`: обрабатывает нажатие клавиш для поворота пушки или стрельбы.  
   `fire_bullet()`: создаёт пулю и инициирует её движение.  
   `play_sound(filename)`: воспроизводит звуковой файл.  
   `move_bullet(bullet, x, y, angle)`: перемещает пулю по экрану.  
   `check_collision(bullet_x, bullet_y)`: проверяет, попала ли пуля в один из квадратов.  
   `update_question()`: обновляет вопрос и случайные ответы в квадрате.  
   `check_answer(index)`: проверяет, правильный ли ответ был выбран, обновляет счёт и задаёт новый вопрос.

##### Вывод по проделанной работе: #####

> Я совершенствовал навыки работы с графикой, создав игру по мотивам таблицы умножения со звуком