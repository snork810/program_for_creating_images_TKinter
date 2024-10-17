import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        """
        Инициализация главного окна и создание элементов интерфейса.

        :param root: Объект корневого окна Tkinter.
        """
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'  # Текущий цвет кисти
        self.last_pen_color = self.pen_color  # Последний использованный цвет кисти
        self.background_color_mode = False  # Режим цвета фона

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

        self.canvas.bind('<Button-3>', self.pick_color)

        self.root.bind('<Control-s>', self.save_image)

        self.root.bind('<Control-c>', self.choose_color)

    def setup_ui(self):
        """
        Настройка пользовательского интерфейса, создание кнопок и выпадающего меню.
        """
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(fill=tk.X)

        self.clear_button = tk.Button(self.control_frame, text="Очистить", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT)

        self.color_button = tk.Button(self.control_frame, text="Выбрать цвет", command=self.choose_color)
        self.color_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(self.control_frame, text="Сохранить", command=self.save_image)
        self.save_button.pack(side=tk.LEFT)

        # Переключаемая кнопка для установки цвета кисти в цвет фона
        self.background_color_button = tk.Button(self.control_frame, text="Ластик",
                                                 command=self.eraser)
        self.background_color_button.pack(side=tk.LEFT)

        # Список толщин кисти как целые числа
        self.brush_size_var = tk.IntVar(value=1)  # Устанавливаем значение по умолчанию

        # Создаем выпадающее меню для выбора толщины кисти
        brush_sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.brush_size_menu = tk.OptionMenu(self.control_frame, self.brush_size_var, *brush_sizes)
        self.brush_size_menu.pack(side=tk.LEFT)

    def paint(self, event):
        """
        Рисование линии на холсте при перемещении мыши с зажатой кнопкой.

        :param event: Событие мыши с координатами x и y.
        """
        if self.last_x and self.last_y:
            brush_size = self.brush_size_var.get()  # Получаем размер кисти
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=brush_size, fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=brush_size)

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        """
        Сбрасывает координаты последней точки после отпускания кнопки мыши.

        :param event: Событие отпускания кнопки мыши.
        """
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        """
        Очищает холст и сбрасывает изображение.
        """
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self, event=None):
        """
        Открывает диалог выбора цвета для кисти.
        """
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]

    def eraser(self):
        """
        Переключает режим ластика. При активации цвет кисти равен цвету фона,
        при деактивации возвращается последний использованный цвет кисти.
        """
        if self.background_color_mode:
            self.pen_color = self.last_pen_color  # Возвращаем последний цвет кисти
            self.background_color_button.config(relief=tk.RAISED)  # Изменяем стиль кнопки
        else:
            self.last_pen_color = self.pen_color  # Сохраняем текущий цвет кисти
            self.pen_color = self.canvas['bg']  # Устанавливаем цвет кисти в цвет фона
            self.background_color_button.config(relief=tk.SUNKEN)  # Изменяем стиль кнопки

        self.background_color_mode = not self.background_color_mode

    def save_image(self, event=None):
        """
        Сохраняет текущее изображение в формате PNG.

        Вызывает диалог выбора места сохранения.
        """
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    def pick_color(self, event):
        x = event.x
        y = event.y
        if (0 < x < self.canvas.winfo_width()) and (
                0 < y < self.canvas.winfo_height()):  # Проверка, что щелчок был в пределах холста
            pixel_color = self.image.getpixel((x, y))  # Получаем цвет пикселя из изображения
            self.pen_color = f'#{pixel_color[0]:02x}{pixel_color[1]:02x}{pixel_color[2]:02x}'


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
