#  YOLOv8 ile Nesne Tespiti ve Masaüstü Arayüzü (GUI)

Bu proje, **YOLOv8** (You Only Look Once) mimarisi kullanılarak geliştirilmiş bir nesne tespiti modelini ve bu modeli kullanmak için tasarlanmış kullanıcı dostu bir masaüstü arayüzünü içerir.

##  Proje İçeriği ve Dosyalar

Bu depo (repository) temel olarak 3 ana bileşenden oluşmaktadır:

### 1.  Eğitim Süreci (`YoloV8_Nesne_Tespiti.ipynb`)
Google Colab üzerinde çalıştırılan bu Jupyter Notebook dosyası, modelin eğitim sürecini kapsar.
* **Veri Seti Hazırlığı:** Verilerin düzenlenmesi ve YOLO formatına uygun hale getirilmesi.
* **Eğitim (Training):** YOLOv8 nano/small/medium modellerinden biri kullanılarak yapılan eğitim adımları.
* **Değerlendirme (Evaluation):** Confusion Matrix, F1-Score ve mAP değerlerinin analizi.
* Bu dosya, modelin nasıl eğitildiğini incelemek isteyenler için teknik bir rehber niteliğindedir.

### 2.  Eğitilmiş Model (`best.pt`)
Eğitim sonucunda elde edilen ağırlık dosyasıdır.
* Eğitim süresince doğrulama (validation) setinde **en yüksek başarıyı** gösteren modeldir.
* `gui_app.py` uygulaması, nesne tespiti yapmak için bu dosyayı referans alır.
* YOLOv8 formatındadır ve doğrudan kullanılabilir.

### 3.  Kullanıcı Arayüzü (`gui_app.py`)
Python ve **PyQt5** kütüphanesi kullanılarak geliştirilmiş masaüstü uygulamasıdır.
* Kullanıcıların kod yazmadan modeli test etmesini sağlar.
* **Özellikler:** Resim yükleme, web kamerasından canlı tespit yapma veya video üzerinde tahmin yürütme.
* Tespit edilen nesneleri çerçeve içine alır ve güven skorunu (confidence score) ekranda gösterir.

---

##  Kurulum (Installation)

Projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin.

### Gereksinimler
Projenin çalışması için Python kurulu olmalıdır. Gerekli kütüphaneleri yüklemek için terminale şu komutu yazın:

```bash
pip install ultralytics PyQt5 opencv-python
