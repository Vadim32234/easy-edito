#создай тут фоторедактор Easy Editor!
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter, ImageOps
import random

app = QApplication([])
main_win = QWidget()
main_win.resize(600, 300)
main_win.setWindowTitle("Easy Editor-простой редактор")

# Стиль для сглаживания и цветных кнопок
main_win.setStyleSheet("""
    QWidget {
        background-color: #2b2b2b;
    }
    QPushButton {
        border: none;
        color: white;
        padding: 8px 12px;
        font-size: 12px;
        font-weight: bold;
        border-radius: 5px;
    }
    QPushButton:hover {
        opacity: 0.8;
    }
    QPushButton:pressed {
        transform: scale(0.95);
    }
    QListWidget {
        background-color: #3c3c3c;
        border: 1px solid #555;
        border-radius: 5px;
        color: white;
        padding: 5px;
    }
    QListWidget::item:selected {
        background-color: #0078d7;
    }
    QLabel {
        background-color: #3c3c3c;
        border: 2px solid #555;
        border-radius: 5px;
        color: white;
        padding: 10px;
    }
""")

label = QLabel("Картинка")
label.setAlignment(Qt.AlignCenter)
list_widget = QListWidget()

btn1 = QPushButton("📁 Папка")
btn2 = QPushButton("↩️ Лево")
btn3 = QPushButton("↪️ Право")
btn4 = QPushButton("🪞 Зеркало")
btn5 = QPushButton("✨ Резкость")
btn6 = QPushButton("⚫ Ч/Б")
btn7 = QPushButton("💾 Сохранить")
btn8 = QPushButton("🎨 Инверсия")
btn9 = QPushButton("🌀 Размытие")
btn10 = QPushButton("📺 Шум")
btn11 = QPushButton("🔄 Сбросить")

# Цвета для кнопок
btn1.setStyleSheet("background-color: #2196F3;")  # Синий - папка
btn2.setStyleSheet("background-color: #9C27B0;")  # Фиолетовый - лево
btn3.setStyleSheet("background-color: #9C27B0;")  # Фиолетовый - право
btn4.setStyleSheet("background-color: #00BCD4;")  # Голубой - зеркало
btn5.setStyleSheet("background-color: #FF9800;")  # Оранжевый - резкость
btn6.setStyleSheet("background-color: #607D8B;")  # Серый - ч/б
btn7.setStyleSheet("background-color: #4CAF50;")  # Зеленый - сохранить
btn8.setStyleSheet("background-color: #E91E63;")  # Розовый - инверсия
btn9.setStyleSheet("background-color: #3F51B5;")  # Индиго - размытие
btn10.setStyleSheet("background-color: #FF5722;") # Оранжево-красный - шум
btn11.setStyleSheet("background-color: #F44336;") # Красный - сброс

line1 = QVBoxLayout()
line1.addWidget(btn1)
line1.addWidget(list_widget)
line2 = QHBoxLayout()
line2.addWidget(btn2)
line2.addWidget(btn3)
line2.addWidget(btn4)
line2.addWidget(btn5)
line2.addWidget(btn6)
line2.addWidget(btn7)
line2.addWidget(btn8)
line2.addWidget(btn9)
line2.addWidget(btn10)
line2.addWidget(btn11)
line3 = QVBoxLayout()
line3.addWidget(label)
line3.addLayout(line2)
line4 = QHBoxLayout()
line4.addLayout(line1)
line4.addLayout(line3)
main_win.setLayout(line4)

workdir = ''

def filter_files(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
               result.append(filename)
    return result

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
    extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir()
    if workdir:
        filenames = filter_files(os.listdir(workdir), extensions)
        list_widget.clear()
        for filename in filenames:
            list_widget.addItem(filename)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"
        self.original_image = None

    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
        self.original_image = self.image.copy()
        
    def showImage(self, path):
        pixmapimage = QPixmap(path)
        label_width, label_height = label.width(), label.height()
        # Сглаживание при масштабировании
        scaled_pixmap = pixmapimage.scaled(label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(scaled_pixmap)
        label.setVisible(True)
        
    def save_image(self):
        if self.image:
            path = os.path.join(workdir, self.save_dir)
            if not(os.path.exists(path) or os.path.isdir(path)):
                os.mkdir(path)
            image_path = os.path.join(path, self.filename)
            # Сохраняем с высоким качеством
            if self.filename.lower().endswith('.jpg') or self.filename.lower().endswith('.jpeg'):
                self.image.save(image_path, quality=95)
            else:
                self.image.save(image_path)
            return image_path
        return None
        
    def do_bw(self):
        if self.image:
            self.image = self.image.convert("L")
            image_path = self.save_image()
            if image_path:
                self.showImage(image_path)
        
    def do_left(self):
        if self.image:
            self.image = self.image.transpose(Image.ROTATE_90)
            image_path = self.save_image()
            if image_path:
                self.showImage(image_path)

    def do_right(self):
        if self.image:
            self.image = self.image.transpose(Image.ROTATE_270)
            image_path = self.save_image()
            if image_path:
                self.showImage(image_path)

    def do_mirror(self):
        if self.image:
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            image_path = self.save_image()
            if image_path:
                self.showImage(image_path)

    def do_sharped(self):
        if self.image:
            self.image = self.image.filter(ImageFilter.SHARPEN)
            image_path = self.save_image()
            if image_path:
                self.showImage(image_path)

    def do_invert(self):
        if self.image:
            if self.image.mode == 'RGB':
                self.image = ImageOps.invert(self.image)
            elif self.image.mode == 'L':
                self.image = ImageOps.invert(self.image)
            else:
                self.image = self.image.convert('RGB')
                self.image = ImageOps.invert(self.image)
            image_path = self.save_image()
            if image_path:
                self.showImage(image_path)

    def do_blur(self):
        if self.image:
            self.image = self.image.filter(ImageFilter.GaussianBlur(radius=3))
            image_path = self.save_image()
            if image_path:
                self.showImage(image_path)

    def do_noise(self):
        if self.image:
            if self.image.mode != 'RGB':
                self.image = self.image.convert('RGB')
            
            width, height = self.image.size
            pixels = self.image.load()
            noise_level = 30
            
            for x in range(width):
                for y in range(height):
                    r, g, b = pixels[x, y]
                    r = r + random.randint(-noise_level, noise_level)
                    g = g + random.randint(-noise_level, noise_level)
                    b = b + random.randint(-noise_level, noise_level)
                    r = max(0, min(255, r))
                    g = max(0, min(255, g))
                    b = max(0, min(255, b))
                    pixels[x, y] = (r, g, b)
            
            image_path = self.save_image()
            if image_path:
                self.showImage(image_path)

    def reset_filter(self):
        if self.image and self.original_image:
            self.image = self.original_image.copy()
            image_path = self.save_image()
            if image_path:
                self.showImage(image_path)

def save_current_image():
    if workimage.image is None:
        QMessageBox.warning(main_win, "Предупреждение", "Нет изображения для сохранения!\nСначала выберите изображение.")
        return
    
    try:
        image_path = workimage.save_image()
        if image_path:
            QMessageBox.information(main_win, "Успех", f"Изображение успешно сохранено!\nПуть: {image_path}")
            label.setText(f"Сохранено: {workimage.filename}")
        else:
            QMessageBox.warning(main_win, "Предупреждение", "Нечего сохранять!")
    except Exception as e:
        QMessageBox.critical(main_win, "Ошибка", f"Не удалось сохранить изображение!\nОшибка: {str(e)}")

def showChoseImage():
    if list_widget.currentRow() >= 0:
        filename = list_widget.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workdir, filename)
        workimage.showImage(image_path)
            
workimage = ImageProcessor()         
list_widget.currentRowChanged.connect(showChoseImage)
btn1.clicked.connect(showFilenamesList)
btn2.clicked.connect(workimage.do_left)
btn3.clicked.connect(workimage.do_right)
btn4.clicked.connect(workimage.do_mirror)
btn5.clicked.connect(workimage.do_sharped)
btn6.clicked.connect(workimage.do_bw)
btn7.clicked.connect(save_current_image)
btn8.clicked.connect(workimage.do_invert)
btn9.clicked.connect(workimage.do_blur)
btn10.clicked.connect(workimage.do_noise)
btn11.clicked.connect(workimage.reset_filter)

main_win.show()
app.exec_()
