from PyQt5.QtGui import QPalette, QBrush, QPixmap
image_path = "C:/Project/background.jpg"
pixmap = QPixmap(image_path)
if pixmap.isNull():
    print("Image failed to load.")
else:
    print("Image loaded successfully.")
