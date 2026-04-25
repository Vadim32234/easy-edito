#создай тут фоторедактор Easy Editor!
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter

app = QApplication([])
main_win = QWidget()
main_win.resize(600, 300)
main_win.setWindowTitle("Easy Editor")
label = QLabel("Картинка")
list_widget = QListWidget()  # Переименовал, чтобы не конфликтовало с функцией list()

btn1 = QPushButton("Папка")
btn2 = QPushButton("Лево")
btn3 = QPushButton("право")
btn4 = QPushButton("Зеркало")
btn5 = QPushButton("Резкость")
btn6 = QPushButton("Ч/Б")
btn7 = QPushButton("Сохранить")
btn8 = QPushButton("Сбросить фильтры")

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
        self.original_image = None  # Для хранения оригинала

    def loadImage(self, dir, filename):
        ''' при загрузке запоминаем путь и имя файла '''
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
        self.original_image = self.image.copy()  # Сохраняем копию оригинала
        
    def showImage(self, path):
        pixmapimage = QPixmap(path)
        label_width, label_height = label.width(), label.height()
        scaled_pixmap = pixmapimage.scaled(label_width, label_height, Qt.KeepAspectRatio)
        label.setPixmap(scaled_pixmap)
        label.setVisible(True)
        
    def save_image(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
        return image_path
        
    def do_bw(self):
        if self.image:
            self.image = self.image.convert("L")
            image_path = self.save_image()
            self.showImage(image_path)
        
    def do_left(self):
        if self.image:
            self.image = self.image.transpose(Image.ROTATE_90)  # Исправлено
            image_path = self.save_image()
            self.showImage(image_path)

    def do_right(self):
        if self.image:
            self.image = self.image.transpose(Image.ROTATE_270)  # Исправлено
            image_path = self.save_image()
            self.showImage(image_path)

    def do_mirror(self):
        if self.image:
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)  # Исправлено
            image_path = self.save_image()
            self.showImage(image_path)

    def do_sharped(self):
        if self.image:
            self.image = self.image.filter(ImageFilter.SHARPEN)  # Исправлено
            image_path = self.save_image()
            self.showImage(image_path)

    def reset_filter(self):
        if self.image and self.original_image:
            self.image = self.original_image.copy()  # Восстанавливаем оригинал
            image_path = self.save_image()
            self.showImage(image_path)

def showChoseImage():
    if list_widget.currentRow() >= 0:
        filename = list_widget.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workdir, filename)
        workimage.showImage(image_path)
            
workimage = ImageProcessor()         
list_widget.currentRowChanged.connect(showChoseImage)
btn1.clicked.connect(showFilenamesList)
btn6.clicked.connect(workimage.do_bw)
btn2.clicked.connect(workimage.do_left)
btn3.clicked.connect(workimage.do_right)
btn4.clicked.connect(workimage.do_mirror)
btn5.clicked.connect(workimage.do_sharped)
btn8.clicked.connect(workimage.reset_filter)

main_win.show()
app.exec_()


