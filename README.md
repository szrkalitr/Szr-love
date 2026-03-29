#Szr-love
# 🚀 Asenkron & Paralel SMS Gönderici (v0.1)

Bu proje, Python'un **asenkron (`asyncio`)** yapısını kullanarak, birden fazla servis üzerinden yüksek hızda ve paralel bir şekilde doğrulama SMS'i gönderilmesini sağlayan bir CLI aracıdır. **SZR-KALI** tarafından asenkron mimariyle yeniden tasarlanmıştır.

## ✨ Öne Çıkan Özellikler

* **SZR-KALI Özel Banner:** Şık ve profesyonel terminal açılışı.
* **Tam Asenkron Altyapı:** `httpx` kütüphanesi sayesinde ağ istekleri sırasında donma yaşanmaz.
* **Paralel İşleme:** `asyncio.Semaphore` ile aynı anda çalışan kanal sayısını kullanıcı belirler.
* **Dinamik Servis Algılama:** `sms.py` içine eklediğiniz fonksiyonlar otomatik olarak tanınır.


---

## 🛠️ Kurulum

Bilgisayarınızda Python yüklü olduğundan emin olun. Gerekli kütüphaneleri şu komutla yükleyebilirsiniz:

```bash
pip install httpx colorama
git clone https://github.com/szrkalitr/Szr-love
cd Szr-love
python Bm.py
'''
