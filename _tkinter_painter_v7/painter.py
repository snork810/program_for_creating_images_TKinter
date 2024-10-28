import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, simpledialog
from PIL import Image, ImageDraw, ImageFont


class DrawingApp:
    def __init__(self, root):
        """Инициализация приложения рисования."""
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        # Изначальные параметры холста
        self.canvas_width = 600
        self.canvas_height = 400

        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'
        self.last_pen_color = self.pen_color
        self.background_color_mode = False

        # Поле цвета
        self.color_label = tk.Label(root, text="Текущий цвет", fg='black')
        self.color_label.place(x=550, y=10)

        self.color_box = tk.Label(root, width=5, height=2, bg=self.pen_color)
        self.update_color_box_position()  # Установка положения сразу
        self.color_box.place(x=550, y=30)

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-3>', self.pick_color)
        self.canvas.bind('<Button-1>', self.place_text)

        # Привязка горячих клавиш
        self.root.bind('<Control-s>', self.save_image)
        self.root.bind('<Control-c>', self.choose_color)

    def setup_ui(self):
        """Создание пользовательского интерфейса с кнопками управления."""
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(fill=tk.X)

        self.new_canvas_button = tk.Button(self.control_frame, text="Новый холст", command=self.new_canvas)
        self.new_canvas_button.pack(side=tk.LEFT)

        self.clear_button = tk.Button(self.control_frame, text="Очистить", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT)

        self.color_button = tk.Button(self.control_frame, text="Выбрать цвет", command=self.choose_color)
        self.color_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(self.control_frame, text="Сохранить", command=self.save_image)
        self.save_button.pack(side=tk.LEFT)

        self.background_color_button = tk.Button(self.control_frame, text="Ластик", command=self.eraser)
        self.background_color_button.pack(side=tk.LEFT)

        self.text_button = tk.Button(self.control_frame, text="Текст", command=self.enable_text_mode)
        self.text_button.pack(side=tk.LEFT)

        self.change_background_button = tk.Button(self.control_frame, text="Изменить фон",
                                                  command=self.change_background)
        self.change_background_button.pack(side=tk.LEFT)

        self.brush_size_var = tk.IntVar(value=1)
        brush_sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.brush_size_menu = tk.OptionMenu(self.control_frame, self.brush_size_var, *brush_sizes)
        self.brush_size_menu.pack(side=tk.LEFT)

    def update_color_box_position(self):
        """Обновить позицию поля цвета в правом верхнем углу."""
        self.color_box.place(x=self.canvas.winfo_width() - 55, y=30)  # Сдвиг, чтобы не выходить за пределы

    def new_canvas(self):
        """Создать новый холст с пользовательскими размерами."""
        width = simpledialog.askinteger("Ширина", "Введите ширину холста:", minvalue=100)
        height = simpledialog.askinteger("Высота", "Введите высоту холста:", minvalue=100)

        if width and height:
            self.canvas_width = width
            self.canvas_height = height

            self.canvas.config(width=self.canvas_width, height=self.canvas_height)
            self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
            self.draw = ImageDraw.Draw(self.image)
            self.clear_canvas()  # Очистка холста

            # Обновление позиции поля цвета
            self.update_color_box_position()

    def paint(self, event):
        """Рисование на холсте при перемещении мыши с нажатой левой кнопкой."""
        if self.last_x and self.last_y:
            brush_size = self.brush_size_var.get()
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=brush_size, fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=brush_size)

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        """Сбросить координаты последней точки."""
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        """Очистить холст и создать новый белый холст."""
        self.canvas.delete("all")
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.update_color_display()

    def choose_color(self, event=None):
        """Выбрать цвет для рисования с помощью диалогового окна цветового выбора."""
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        self.update_color_display()  # Обновляем цвет панели после выбора

    def update_color_display(self):
        """Обновить отображение текущего цвета на поле цвета."""
        self.color_box.config(bg=self.pen_color)  # Изменяем цвет панели

    def eraser(self):
        """Переключение режима "ластик" для очистки холста."""
        if self.background_color_mode:
            self.pen_color = self.last_pen_color
            self.background_color_button.config(relief=tk.RAISED)
        else:
            self.last_pen_color = self.pen_color
            self.pen_color = self.canvas['bg']
            self.background_color_button.config(relief=tk.SUNKEN)

        self.background_color_mode = not self.background_color_mode
        self.update_color_display()  # Обновляем панель цвета при смене режима

    def save_image(self, event=None):
        """Сохранить текущее изображение в файл PNG."""
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    def pick_color(self, event):
        """Выбрать цвет из пикселей на холсте при щелчке правой кнопкой мыши."""
        x = event.x
        y = event.y
        if (0 < x < self.canvas.winfo_width()) and (0 < y < self.canvas.winfo_height()):
            pixel_color = self.image.getpixel((x, y))
            self.pen_color = f'#{pixel_color[0]:02x}{pixel_color[1]:02x}{pixel_color[2]:02x}'
            self.update_color_display()  # Обновляем панель цвета после выбора

    def enable_text_mode(self):
        """Включить режим ввода текста."""
        self.is_text_mode = True
        text = simpledialog.askstring("Введите текст", "Введите текст для рисования:")
        if text:
            self.text_to_draw = text

    def place_text(self, event):
        """Отобразить текст на холсте по координатам мыши."""
        if self.is_text_mode and hasattr(self, 'text_to_draw'):
            x, y = event.x, event.y
            font = ImageFont.load_default()
            self.draw.text((x, y), self.text_to_draw, fill=self.pen_color, font=font)
            self.image = self.image  # Это обновление необходимо, чтобы увидеть текст в холсте
            self.canvas.create_text(x, y, text=self.text_to_draw, fill=self.pen_color, anchor='nw')
            self.is_text_mode = False  # Отключить режим текста после размещения текста

    def change_background(self):
        """Изменить цвет фона холста."""
        new_color = colorchooser.askcolor()[1]  # Выбор нового цвета
        if new_color:
            self.background_color = new_color
            self.canvas.config(bg=new_color)  # Изменяем цвет фона холста
            self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), self.background_color)
            self.draw = ImageDraw.Draw(self.image)


def main():
    """Запуск приложения рисования."""
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
