import sys
import random
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QMessageBox
from PyQt5.QtMultimedia import QSound

class MouseHandling(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(300, 300, 700, 600)
        self.setWindowTitle('Task Week 3 - (F1D022145 - Muhammad Fiqri Jordy Ardianto)')

        self.skor = 0
        self.waktu_tersisa = 30
        self.kecepatan = 5
        self.target_x = 0
        self.target_y = 0
        self.suara = QSound("click.wav")

        self.skor_label = QLabel(f'Skor: {self.skor}', self)
        self.skor_label.move(10, 10)
        self.skor_label.setFixedWidth(150)
        self.skor_label.setStyleSheet("font-weight: bold; font-size: 20px;")

        self.timer_label = QLabel(f'Waktu: {self.waktu_tersisa}s', self)
        self.timer_label.move(500, 10)
        self.timer_label.setStyleSheet("font-weight: bold; font-size: 20px;")

        self.catch_button = QPushButton('Tangkap Saya!', self)
        self.catch_button.setStyleSheet(
            """
            background-color: #6495ED;
            padding: 10px;
            font-weight: bold;
            font-size: 16px;
            color: white;
            border-radius: 25px;
            """
        )
        self.catch_button.setFixedSize(150, 60)
        self.tataLetakTombol()

        self.catch_button.clicked.connect(self.tangkapTombol)

        self.timer_gerak = QTimer()
        self.timer_gerak.timeout.connect(self.gerakTombol)
        self.timer_gerak.start(10)

        self.timer_waktu = QTimer()
        self.timer_waktu.timeout.connect(self.updateWaktu)
        self.timer_waktu.start(1000)

        self.setMouseTracking(True)

    def tataLetakTombol(self):
        posisi_x = (self.width() - self.catch_button.width()) // 2
        posisi_y = (self.height() - self.catch_button.height()) // 2
        self.catch_button.move(posisi_x, posisi_y)
        self.target_x, self.target_y = posisi_x, posisi_y

    def mouseMoveEvent(self, event):
        x, y = event.x(), event.y()
        posisi_x, posisi_y = self.catch_button.x(), self.catch_button.y()
        lebar_button, tinggi_button = self.catch_button.width(), self.catch_button.height()

        gerak_x = self.kecepatan if x > posisi_x else -self.kecepatan
        gerak_y = self.kecepatan if y > posisi_y else -self.kecepatan

        self.target_x = max(0, min(self.width() - lebar_button, posisi_x - gerak_x))
        self.target_y = max(0, min(self.height() - tinggi_button, posisi_y - gerak_y))

        batas = 10
        if (posisi_x <= batas or posisi_x + lebar_button >= self.width() - batas or
            posisi_y <= batas or posisi_y + tinggi_button >= self.height() - batas):
            self.pindahkanTombol()

    def tangkapTombol(self):
        self.skor += 1
        self.skor_label.setText(f'Skor: {self.skor}')
        self.suara.play()
        self.kecepatan += 0.5
        self.pindahkanTombol()

    def pindahkanTombol(self):
        new_x = random.randint(50, self.width() - 100)
        new_y = random.randint(50, self.height() - 100)
        self.catch_button.move(new_x, new_y)
        self.target_x, self.target_y = new_x, new_y

    def gerakTombol(self):
        posisi_sekarang_x = self.catch_button.x()
        posisi_sekarang_y = self.catch_button.y()
        langkah_x = (self.target_x - posisi_sekarang_x) * 0.3
        langkah_y = (self.target_y - posisi_sekarang_y) * 0.3

        if abs(langkah_x) < 1:
            langkah_x = 0
        if abs(langkah_y) < 1:
            langkah_y = 0

        self.catch_button.move(int(posisi_sekarang_x + langkah_x), int(posisi_sekarang_y + langkah_y))

    def updateWaktu(self):
        self.waktu_tersisa -= 1
        self.timer_label.setText(f'Waktu: {self.waktu_tersisa}s')

        if self.waktu_tersisa == 0:
            self.timer_gerak.stop()
            self.timer_waktu.stop()
            self.skor_label.setText(f'Skor: {self.skor}')
            QMessageBox.information(self, 'Game Over', f'Permainan selesai! Skor Kamu: {self.skor}')
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MouseHandling()
    window.show()
    sys.exit(app.exec_())
