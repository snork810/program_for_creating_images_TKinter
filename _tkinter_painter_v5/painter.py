import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'
        self.last_pen_color = self.pen_color
        self.background_color_mode = False

        # Поле цвета
        self.color_display_frame = tk.Frame(root, width=100, height=100)
        self.color_label = tk.Label(self.color_display_frame, text="Текущий цвет", fg='black')
        self.color_label.pack()

        self.color_box = tk.Label(self.color_display_frame, width=4, height=2, bg=self.pen_color)
        self.color_box.pack()

        self.color_display_frame.place(x=520, y=10)  # Позиция в правом верхнем углу

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-3>', self.pick_color)

        # Привязка горячих клавиш
        self.root.bind('<Control-s>', self.save_image)
        self.root.bind('<Control-c>', self.choose_color)

    def setup_ui(self):
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(fill=tk.X)

        self.clear_button = tk.Button(self.control_frame, text="Очистить", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT)

        self.color_button = tk.Button(self.control_frame, text="Выбрать цвет", command=self.choose_color)
        self.color_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(self.control_frame, text="Сохранить", command=self.save_image)
        self.save_button.pack(side=tk.LEFT)

        self.background_color_button = tk.Button(self.control_frame, text="Ластик", command=self.eraser)
        self.background_color_button.pack(side=tk.LEFT)

        self.brush_size_var = tk.IntVar(value=1)
        brush_sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.brush_size_menu = tk.OptionMenu(self.control_frame, self.brush_size_var, *brush_sizes)
        self.brush_size_menu.pack(side=tk.LEFT)

    def paint(self, event):
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
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.update_color_display()

    def choose_color(self, event=None):
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        self.update_color_display()  # Обновляем цвет панели после выбора

    def update_color_display(self):
        self.color_box.config(bg=self.pen_color)  # Изменяем цвет панели

    def eraser(self):
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
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    def pick_color(self, event):
        x = event.x
        y = event.y
        if (0 < x < self.canvas.winfo_width()) and (0 < y < self.canvas.winfo_height()):
            pixel_color = self.image.getpixel((x, y))
            self.pen_color = f'#{pixel_color[0]:02x}{pixel_color[1]:02x}{pixel_color[2]:02x}'
            self.update_color_display()  # Обновляем панель цвета после выбора

def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
