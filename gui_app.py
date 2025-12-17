import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget, QHBoxLayout, QTextEdit, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer
from ultralytics import YOLO

class UnoTespitUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UNO Kart Tespit Sistemi - FİNAL PROJE")
        self.setGeometry(100, 100, 1200, 750)
        
        # --- Değişkenler ---
        self.model = None
        self.cap = None             # Kamera nesnesi
        self.timer = QTimer()       # Zamanlayıcı (FPS için)
        self.timer.timeout.connect(self.goruntuyu_guncelle)
        self.kamera_acik_mi = False
        self.secilen_resim_yolu = None

        # Arayüzü Kur
        self.initUI()

    def initUI(self):
        # --- Ana Düzen ---
        ana_widget = QWidget()
        self.setCentralWidget(ana_widget)
        ana_layout = QVBoxLayout()
        ana_widget.setLayout(ana_layout)

        # --- Başlık ---
        baslik = QLabel("UNO KART TESPİT VE SINIFLANDIRMA SİSTEMİ")
        baslik.setAlignment(Qt.AlignCenter)
        baslik.setStyleSheet("font-size: 24px; font-weight: bold; color: #333; margin-bottom: 10px;")
        ana_layout.addWidget(baslik)

        # --- Resim Panelleri ---
        resim_layout = QHBoxLayout()
        
        # Sol Panel (Kaynak)
        self.label_orijinal = QLabel("Kamera / Kaynak Görüntü")
        self.label_orijinal.setAlignment(Qt.AlignCenter)
        self.label_orijinal.setStyleSheet("border: 3px dashed #aaa; background-color: #f0f0f0; border-radius: 10px;")
        self.label_orijinal.setFixedSize(550, 450)
        
        # Sağ Panel (Sonuç)
        self.label_sonuc = QLabel("Yapay Zeka Tespiti")
        self.label_sonuc.setAlignment(Qt.AlignCenter)
        self.label_sonuc.setStyleSheet("border: 3px solid #4CAF50; background-color: #f0f0f0; border-radius: 10px;")
        self.label_sonuc.setFixedSize(550, 450)

        resim_layout.addWidget(self.label_orijinal)
        resim_layout.addWidget(self.label_sonuc)
        ana_layout.addLayout(resim_layout)

        # --- Bilgi Ekranı ---
        self.sonuc_kutusu = QTextEdit()
        self.sonuc_kutusu.setReadOnly(True)
        self.sonuc_kutusu.setMaximumHeight(100)
        self.sonuc_kutusu.setStyleSheet("font-size: 14px; border: 1px solid #ccc;")
        self.sonuc_kutusu.setPlaceholderText("Tespit sonuçları burada anlık olarak akacak...")
        ana_layout.addWidget(self.sonuc_kutusu)

        # --- Butonlar ---
        buton_layout = QHBoxLayout()

        # Model Butonu
        self.btn_model_sec = QPushButton("1. ADIM: Model Yükle (.pt)")
        self.btn_model_sec.clicked.connect(self.model_yukle)
        self.btn_model_sec.setStyleSheet("padding: 12px; font-weight: bold; font-size: 14px;")

        # Resim Modu Butonları
        self.btn_resim_yukle = QPushButton("Resim Seç")
        self.btn_resim_yukle.clicked.connect(self.resim_yukle)
        self.btn_resim_yukle.setStyleSheet("padding: 12px;")

        self.btn_test_et = QPushButton("Resmi Analiz Et")
        self.btn_test_et.clicked.connect(self.fotograf_test_et)
        self.btn_test_et.setStyleSheet("padding: 12px;")

        # --- KAMERA BUTONU ---
        self.btn_kamera = QPushButton(" CANLI KAMERA BAŞLAT")
        self.btn_kamera.clicked.connect(self.kamera_islem)
        self.btn_kamera.setStyleSheet("background-color: #d32f2f; color: white; padding: 12px; font-weight: bold; font-size: 14px; border-radius: 5px;")
        
        buton_layout.addWidget(self.btn_model_sec)
        buton_layout.addWidget(self.btn_resim_yukle)
        buton_layout.addWidget(self.btn_test_et)
        buton_layout.addWidget(self.btn_kamera)
        ana_layout.addLayout(buton_layout)

    def model_yukle(self):
        dosya_yolu, _ = QFileDialog.getOpenFileName(self, "Model Dosyası Seç", "", "Model Files (*.pt)")
        if dosya_yolu:
            try:
                self.model = YOLO(dosya_yolu)
                QMessageBox.information(self, "Başarılı", f"Model yüklendi!\n{dosya_yolu.split('/')[-1]}")
                self.sonuc_kutusu.setText(f" Model Hazır: {dosya_yolu}")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Model yüklenemedi: {str(e)}")

    def resim_yukle(self):
        if self.kamera_acik_mi:
            self.kamera_kapat()

        dosya_yolu, _ = QFileDialog.getOpenFileName(self, "Resim Seç", "", "Image Files (*.png *.jpg *.jpeg)")
        if dosya_yolu:
            self.secilen_resim_yolu = dosya_yolu
            pixmap = QPixmap(dosya_yolu)
            self.label_orijinal.setPixmap(pixmap.scaled(550, 450, Qt.KeepAspectRatio))
            self.label_sonuc.clear()
            self.label_sonuc.setText("Analiz Bekleniyor...")

    def fotograf_test_et(self):
        if self.model is None:
            QMessageBox.warning(self, "Uyarı", "Önce modeli yüklemelisin!")
            return
        if self.secilen_resim_yolu is None:
            QMessageBox.warning(self, "Uyarı", "Önce bir resim seçmelisin!")
            return

        # Fotoğraf için güven eşiği (conf=0.25 normaldir, istersen artırabilirsin)
        results = self.model(self.secilen_resim_yolu, conf=0.50)
        self.sonuc_goster(results[0])

    # --- KAMERA FONKSİYONLARI ---
    def kamera_islem(self):
        if not self.kamera_acik_mi:
            self.kamera_baslat()
        else:
            self.kamera_kapat()

    def kamera_baslat(self):
        if self.model is None:
            QMessageBox.warning(self, "Uyarı", "Kamerayı açmadan önce lütfen 'Model Yükle' butonuna basıp best.pt dosyasını seç.")
            return

       
        self.cap = cv2.VideoCapture(1) 
        
        if not self.cap.isOpened():
            # Eğer 1 numara açılmazsa otomatik 0'ı dene
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                QMessageBox.critical(self, "Hata", "Kameraya erişilemedi!")
                return

        self.timer.start(30)
        self.kamera_acik_mi = True
        self.btn_kamera.setText("⏹ KAMERAYI DURDUR")
        self.btn_kamera.setStyleSheet("background-color: #333; color: white; padding: 12px; font-weight: bold;")
        self.label_orijinal.setText("Kamera Aktif...")
        self.sonuc_kutusu.setText("Canlı analiz başlatıldı...")

    def kamera_kapat(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
        self.kamera_acik_mi = False
        self.btn_kamera.setText(" CANLI KAMERA BAŞLAT")
        self.btn_kamera.setStyleSheet("background-color: #d32f2f; color: white; padding: 12px; font-weight: bold;")
        self.label_orijinal.clear()
        self.label_sonuc.clear()
        self.label_sonuc.setText("Kamera Durduruldu")

    def goruntuyu_guncelle(self):
        ret, frame = self.cap.read()
        if ret:
            
            results = self.model(frame, verbose=False, conf=0.75) 
            
            res_plotted = results[0].plot()

            rgb_img = cv2.cvtColor(res_plotted, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_img.shape
            bytes_per_line = ch * w
            q_img = QImage(rgb_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.label_sonuc.setPixmap(QPixmap.fromImage(q_img).scaled(550, 450, Qt.KeepAspectRatio))

            tespitler = []
            for box in results[0].boxes:
                sinif = self.model.names[int(box.cls[0])]
                guven = float(box.conf[0])
                tespitler.append(f"{sinif} (%{guven*100:.0f})")
            
            if tespitler:
                self.sonuc_kutusu.setText(" | ".join(tespitler))
            else:
                self.sonuc_kutusu.setText("Kart aranıyor...")

    def sonuc_goster(self, result):
        res_plotted = result.plot()
        rgb_img = cv2.cvtColor(res_plotted, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_img.shape
        bytes_per_line = ch * w
        q_img = QImage(rgb_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.label_sonuc.setPixmap(QPixmap.fromImage(q_img).scaled(550, 450, Qt.KeepAspectRatio))
        
        metin = "FOTOĞRAF ANALİZ SONUCU:\n"
        sayac = {}
        for box in result.boxes:
            ad = self.model.names[int(box.cls[0])]
            sayac[ad] = sayac.get(ad, 0) + 1
        for k, v in sayac.items():
            metin += f"• {k}: {v} adet\n"
        self.sonuc_kutusu.setText(metin)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = UnoTespitUygulamasi()
    win.show()
    sys.exit(app.exec_())