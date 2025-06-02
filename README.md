# IoT DDoS Saldırı Tespit Sistemi

Bu proje, Nesnelerin İnterneti (IoT) ağlarında Dağıtılmış Hizmet Reddi (DDoS) saldırılarını tespit etmek için Random Forest algoritması kullanan bir makine öğrenmesi uygulamasıdır.

## 📋 Proje Hakkında

IoT cihazları günümüzde yaygın olarak kullanılmakta ve birbirleriyle sürekli iletişim halindedir. Bu durum beraberinde güvenlik risklerini de getirmektedir. DDoS saldırıları bu riskler arasında en ciddi olanlardan biridir. Bu proje, IoT ağ trafiğini analiz ederek normal trafik ile saldırı trafiğini ayırt edebilen bir sınıflandırma modeli geliştirmeyi amaçlamaktadır.

## ✨ Özellikler

- **Yüksek Doğruluk**: %99 doğruluk oranı ile DDoS saldırılarını tespit eder
- **Random Forest Algoritması**: Stabil ve güvenilir sonuçlar için ensemble learning kullanır
- **Gerçek Zamanlı Analiz**: IoT ağ trafiğini gerçek zamanlı olarak analiz edebilir
- **Detaylı Görselleştirme**: ROC eğrisi, özellik önem skorları ve öğrenme eğrileri ile model performansını görselleştirir

## 📊 Veri Seti

Projede **IoT-DH veri seti** kullanılmıştır. Bu veri seti aşağıdaki özellikleri içermektedir:

| Özellik | Açıklama |
|---------|----------|
| `dt` | Ardışık paketler arasındaki zaman farkı |
| `dur` | Ardışık paketler arasındaki süre |
| `dur_nsec` | Geçen zamanın nano saniye kısmı |
| `tot_dur` | Yakalanan paketlerin toplam süresi |
| `pktrate` | Saniye başına gelen paket sayısı |
| `protocol` | Paket protokolü |
| `port_no` | Port numarası |
| `tx_kbps` | Saniye başına iletilen kilobit |
| `rx_kbps` | Saniye başına alınan kilobit |
| `tot_kbps` | Saniye başına toplam kilobit |
| `label` | Normal trafik (0) veya saldırı trafiği (1) |

## 🚀 Kurulum

### Projeyi Çalıştırma

1. Kaynak dosyalarını indirin ve projenin çalışacağı dizine yerleştirin

2. Veri setini indirin ve proje dizinine yerleştirin

3. Modeli eğitin ve test edin:
```bash
python train_and_test_model.py
```

## 📈 Model Performansı

### Sınıflandırma Raporu

| Sınıf | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| Normal (0) | 0.9984 | 0.9961 | 0.9972 | 1269 |
| DDoS (1) | 0.9937 | 0.9975 | 0.9956 | 790 |

### Karmaşıklık Matrisi

|  | Gerçek Normal (0) | Gerçek DDoS (1) |
|--|-------------------|-----------------|
| **Tahmin Normal (0)** | 788 | 5 |
| **Tahmin DDoS (1)** | 2 | 1264 |

**Genel Doğruluk: %99**

## 🔧 Metodoloji

1. **Veri Ön İşleme**:
   - Veri setinin rastgele %10'u kullanılarak model ezberlenmesi önlendi
   - Gereksiz sütunlar (src, dst, protocol) kaldırıldı
   - Kategorik veriler sayısal veriye dönüştürüldü

2. **Model Eğitimi**:
   - Random Forest Classifier kullanıldı
   - GridSearchCV ile hiperparametre optimizasyonu yapıldı
   - %80 eğitim, %20 test verisi ayrımı

3. **Değerlendirme**:
   - Precision, Recall, F1-Score metrikleri
   - ROC eğrisi analizi
   - Özellik önem skorları

## 📊 Görselleştirmeler

Proje aşağıdaki görselleştirmeleri içermektedir:

- **ROC Eğrisi**: Model performansının görsel analizi
- **Özellik Önem Skorları**: En etkili özelliklerin belirlenmesi
- **Sınıf Dağılımı**: Veri setindeki dengesizlik analizi
- **Öğrenme Eğrileri**: Model performansının eğitim verisi boyutuna göre değişimi

## 🎯 Kullanım Alanları

- IoT ağ güvenliği
- Siber güvenlik sistemleri
- Ağ trafiği analizi
- Gerçek zamanlı tehdit tespiti

## 📚 Kaynaklar

- [IoT-DH Veri Seti (Mendeley)](https://data.mendeley.com/datasets/8dns3xbckv/1)
- [Scikit-learn Random Forest Dokumentasyonu](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)
- [Random Forest Hiperparametreleri](https://www.geeksforgeeks.org/hyperparameters-of-random-forest-classifier/)

## 📝 Lisans

Bu proje GPLv3 lisansı altında lisanslanmıştır.

## 👨‍💻 Geliştirici

**Mustafa AYKUT**  
Öğrenci No: 22360859028




## 📞 İletişim

Proje hakkında sorularınız için issue açabilir veya e-posta ile iletişim kurabilirsiniz.

---

**Not**: Bu proje veri madenciliği dersi kapsamında hazırlanmış bir ödev projesidir.
