from tkinter import *
import math


# Функция для поворота пушки
def rotate_gun(angle):
    # Точка, откуда начинается пушка (в центре танка)
    x0, y0 = 250, 375  # Центр круга (позиция ствола)
    length = 125

    # Вычисление новых координат конца линии в зависимости от угла
    x1 = x0 + length * math.cos(math.radians(angle))
    y1 = y0 - length * math.sin(math.radians(angle))

    # Обновление координат
    canvas.coords("gun", x0, y0, x1, y1)


# Функция для обработки нажатий клавиш
def KeyPressed(event):
    global gun_angle
    if event.keysym == 'w':
        gun_angle += 10  # Поворот против часовой стрелки
    elif event.keysym == 's':
        gun_angle -= 10  # Поворот по часовой стрелке
    elif event.keysym == 'f':
        fire_bullet()  # Вызываем функцию стрельбы при нажатии клавиши 'f'

    # Ограничиваем угол поворота в пределах 360 градусов
    gun_angle %= 360

    # Поворачиваем пушку на новый угол
    rotate_gun(gun_angle)


# Функция для стрельбы
def fire_bullet():
    # Вычисляем начальные координаты пули на конце пушки
    x0, y0 = 250, 375  # Центр пушки
    length = 125
    x1 = x0 + length * math.cos(math.radians(gun_angle))
    y1 = y0 - length * math.sin(math.radians(gun_angle))

    # Создаем пулю в виде маленького круга (oval)
    bullet = canvas.create_oval(x1 - 5, y1 - 5, x1 + 5, y1 + 5, fill="yellow", tags="bullet")

    # Анимация пули
    move_bullet(bullet, x1, y1, gun_angle)


# Функция для перемещения пули
def move_bullet(bullet, x, y, angle):
    # Скорость пули
    speed = 10

    # Вычисляем новые координаты для перемещения
    x += speed * math.cos(math.radians(angle))
    y -= speed * math.sin(math.radians(angle))

    # Обновляем положение пули
    canvas.coords(bullet, x - 5, y - 5, x + 5, y + 5)

    # Условие для остановки пули (например, когда она выйдет за пределы окна)
    if 0 < x < 500 and 0 < y < 500:
        # Продолжаем перемещение пули
        root.after(50, move_bullet, bullet, x, y, angle)
    else:
        # Удаляем пулю, если она выходит за пределы
        canvas.delete(bullet)


root = Tk()
root.title("Мото-мото")
root.geometry("500x500")

canvas = Canvas(root, height=500, width=500)
canvas.pack()

# Создаем объекты танка (корпус, ствол, колеса)
# Корпус танка теперь расположен немного выше
rectangle = canvas.create_rectangle(200, 300, 300, 490, fill="white")
# Ствол, исходящий из центра корпуса
line = canvas.create_line(250, 375, 250, 250, fill="green", width=10, tags="gun")
# Колеса (круги)
circle = canvas.create_oval(200, 325, 300, 425, fill="black")

# Начальный угол для пушки
gun_angle = 90

# Обработка клавиш
root.bind('<Key>', KeyPressed)

root.mainloop()
