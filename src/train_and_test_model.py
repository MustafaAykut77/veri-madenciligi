# Makine öğrenmesi ve veri görselleştirme için gerekli kütüphaneler içe aktarılıyor
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
import os
from sklearn.model_selection import train_test_split, cross_val_score, learning_curve
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    classification_report, confusion_matrix,
    roc_curve, auc, precision_score, recall_score
)
import warnings

# Matplotlib'i sunucu ortamları için etkileşimsiz modda yapılandır
matplotlib.use('Agg')  # sunucu ortamları için etkileşimsiz backend kullan
plt.ioff()  # etkileşimli çizim modunu kapat
warnings.filterwarnings('ignore')  # uyarı mesajlarını bastır

def main():
    """
    Tüm makine öğrenmesi sürecini yöneten ana fonksiyon.
    Veriyi yükler, ön işler, Random Forest modeli eğitir ve görselleştirmeler oluşturur.
    """
    try:
        # Model sonuçlarının kaydedileceği klasörü oluştur
        os.makedirs("Sonuçlar", exist_ok=True)

        # Veri setinin rastgele %10'luk kısmını al (performans için)
        df = pd.read_csv("./IoT-DH Dataset/Dataset/dataset.csv").sample(frac=0.1, random_state=19)
        
        # Model başarısına katkı sağlamayacak kaynak, hedef ve protokol sütunlarını sil
        df = df.drop(columns=["src", "dst", "Protocol"]).dropna()

        # Özellikler X değişkeninde, hedef değişken y değişkeninde tutulur
        X = df.drop(columns=["label"])
        y = df["label"]

        # Kategorik verileri sayısal veriye dönüştür (label encoding)
        for col in X.select_dtypes(include="object").columns:
            X[col] = LabelEncoder().fit_transform(X[col])

        # Hedef değişkeni sayısal forma dönüştür
        label_encoder = LabelEncoder()
        y_encoded = label_encoder.fit_transform(y)

        # Veriyi eğitim (%80) ve test (%20) olarak ayır, sınıf dağılımını koru
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=13, stratify=y_encoded
        )

        # Kullanıcıya ilerleme bilgisi ver
        print("Eğitim/Test bölmesi tamamlandı.")
        print("Eğitim sınıf dağılımı:", np.bincount(y_train))
        print("Test sınıf dağılımı:", np.bincount(y_test))

        # RANDOM FOREST MODEL PARAMETRELERİ
        # Bu parametreler hiperparametre optimizasyonu ile belirlenmiştir
        rf = RandomForestClassifier(
            bootstrap=True,          # örneklem yeniden yerleştirme kullan
            class_weight='balanced', # dengesiz sınıflar için ağırlık ayarla
            criterion='entropy',     # bölme kriteri olarak entropi kullan
            max_depth=25,            # ağaçların maksimum derinliği
            max_features='sqrt',     # her bölmede kullanılacak özellik sayısı
            min_samples_leaf=1,      # yaprak düğümde minimum örnek sayısı
            min_samples_split=10,    # bölme için minimum örnek sayısı
            n_estimators=350,        # ağaç sayısı
            random_state=42,         # tekrarlanabilirlik için rastgele tohum
            n_jobs=-1                # tüm işlemci çekirdeklerini kullan
        )

        # Modeli eğit ve test verileri üzerinde tahmin yap
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_test)
        y_prob = rf.predict_proba(X_test)[:, 1]  # roc eğrisi için pozitif sınıf olasılıkları

        # Detaylı sınıflandırma raporunu yazdır
        print("\nSınıflandırma raporu:")
        target_names = [str(cls) for cls in label_encoder.classes_]
        print(classification_report(y_test, y_pred, digits=4, target_names=target_names))

        # Karışıklık matrisinden ek performans metriklerini hesapla
        cm = confusion_matrix(y_test, y_pred)
        tn, fp, fn, tp = cm.ravel()  # true negative, false positive, false negative, true positive
        specificity = tn / (tn + fp) if (tn + fp) else 0  # gerçek negatif oranı
        precision = precision_score(y_test, y_pred)  # kesinlik
        recall = recall_score(y_test, y_pred)  # duyarlılık

        print(f"- Precision     : {precision:.4f}")
        print(f"- Recall        : {recall:.4f}")
        print(f"- Specificity   : {specificity:.4f}")

        # Veri görselleştirme fonksiyonunu çalıştır
        create_plots(y_test, y_pred, y_prob, target_names, rf, X, y_encoded)

        # 5 katlı çapraz doğrulama ile model performansını değerlendir
        cv_scores = cross_val_score(rf, X, y_encoded, cv=5, scoring='f1')
        print(f"\n-Çapraz Doğrulama F1 Skorları: {cv_scores}")
        print(f"Ortalama: {cv_scores.mean():.4f}, Std: {cv_scores.std():.4f}")

        # Öğrenme eğrisini çiz ve kaydet
        create_learning_curve(rf, X, y_encoded)

    except Exception as e:
        print(f"Hata oluştu: {e}")
    finally:
        # Bellek temizliği için tüm matplotlib grafiklerini kapat
        plt.close('all')

def create_plots(y_test, y_pred, y_prob, target_names, rf, X, y_encoded):
    """
    Model performansını değerlendirmek için çeşitli grafikler oluşturur.
    
    Args:
        y_test: Test verisi gerçek etiketleri
        y_pred: Modelin tahmin ettiği etiketler
        y_prob: Pozitif sınıf için tahmin olasılıkları
        target_names: Sınıf isimlerinin listesi
        rf: Eğitilmiş Random Forest modeli
        X: Özellik matrisi
        y_encoded: Kodlanmış hedef değişken
    """

    # 1. Karışıklık matrisi - modelin hangi sınıfları karıştırdığını gösterir
    plt.figure(figsize=(6, 5))
    sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues',
                xticklabels=target_names, yticklabels=target_names)
    plt.title("Karışıklık Matrisi")
    plt.xlabel("Tahmin")
    plt.ylabel("Gerçek")
    plt.tight_layout()
    plt.savefig('./Sonuçlar/karmasiklik_matrisi.png', dpi=300)

    # 2. ROC eğrisi - model performansını farklı eşik değerlerinde gösterir
    fpr, tpr, thresholds = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)  # eğri altında kalan alan

    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='blue', lw=2, label=f'ROC Curve (AUC = {roc_auc:.4f})')
    plt.plot([0, 1], [0, 1], color='gray', linestyle='--', label='Random Guess')
    plt.xlabel('Yanlış Pozitif Oranı')
    plt.ylabel('Doğru Pozitif Oranı')
    plt.title('ROC Eğrisi')
    plt.legend(loc='lower right')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('./Sonuçlar/roc_egrisi.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 3. Özellik önem grafiği - hangi özelliklerin daha önemli olduğunu gösterir
    importances = rf.feature_importances_
    indices = np.argsort(importances)[::-1]  # önem sırasına göre sırala
    plt.figure(figsize=(10, 6))
    plt.barh(range(len(indices)), importances[indices])
    plt.yticks(range(len(indices)), [X.columns[i] for i in indices])
    plt.title("Özellik Önem Skoru")
    plt.xlabel("Önem")
    plt.tight_layout()
    plt.grid(axis='x')
    plt.savefig('./Sonuçlar/ozellik_onem_grafigi.png', dpi=300)

    # 4. Sınıf dağılımı grafiği - veri setindeki sınıf dengesini gösterir
    plt.figure(figsize=(6, 4))
    plt.bar(["Normal", "Saldırı"], np.bincount(y_encoded))
    plt.title("Sınıf Dağılımı")
    plt.xlabel("Sınıf")
    plt.ylabel("Örnek Sayısı")
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig('./Sonuçlar/sinif_dagilimi.png', dpi=300)

    print("\nGrafikler başarıyla kaydedildi:\n- karmasiklik_matrisi.png\n- roc_egrisi.png"
          "\n- ozellik_onem_grafigi.png\n- sinif_dagilimi.png")

def create_learning_curve(rf, X, y_encoded):
    """
    Modelin farklı eğitim veri boyutlarındaki performansını gösteren öğrenme eğrisini oluşturur.
    Bu grafik overfitting veya underfitting durumlarını tespit etmek için kullanılır.
    
    Args:
        rf: Random Forest modeli
        X: Özellik matrisi
        y_encoded: Kodlanmış hedef değişken
    """
    try:
        # Farklı eğitim boyutlarında modelin performansını hesapla
        train_sizes, train_scores, test_scores = learning_curve(
            rf, X, y_encoded, cv=5, n_jobs=-1,
            train_sizes=np.linspace(0.1, 1.0, 10), scoring='f1'
        )
        
        # Öğrenme eğrisini çiz
        plt.figure(figsize=(8, 6))
        plt.plot(train_sizes, train_scores.mean(axis=1), label='Eğitim Skoru', color='blue')
        plt.plot(train_sizes, test_scores.mean(axis=1), label='Test Skoru', color='orange')
        plt.title('Öğrenme Eğrisi')
        plt.xlabel('Eğitim Verisi Sayısı')
        plt.ylabel('F1 Skoru')
        plt.legend(loc='best')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('./Sonuçlar/ogrenme_egrisi.png', dpi=300)
        print("- ogrenme_egrisi.png")
    except Exception as e:
        print(f"Öğrenme eğrisi çizilemedi: {e}")

# Program başlangıç noktası
if __name__ == "__main__":
    main()