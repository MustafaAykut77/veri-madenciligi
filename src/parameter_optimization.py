# Hiperparametre optimizasyonu için gerekli kütüphaneler içe aktarılıyor
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, RandomizedSearchCV, GridSearchCV
from sklearn.preprocessing import LabelEncoder
import warnings

# Gereksiz uyarı mesajlarını bastır
warnings.filterwarnings("ignore")  

def load_data():
    """
    Veri setini yükler, temizler ve makine öğrenmesi için hazır hale getirir.
    
    Returns:
        tuple: Özellik matrisi (X) ve kodlanmış hedef değişken (y_encoded)
    """
    try:
        # Performans için veri setinin sadece %10'unu rastgele olarak al
        df = pd.read_csv("./IoT-DH Dataset/Dataset/dataset.csv")
        df = df.sample(frac=0.1, random_state=42)

        # Model performansına katkı sağlamayan sütunları kaldır
        df.drop(columns=["src", "dst", "Protocol"], inplace=True)

        # Eksik değerlere sahip satırları sil
        df.dropna(inplace=True)

        # Özellikleri (X) ve hedef değişkeni (y) ayır
        X = df.drop(columns=["label"])
        y = df["label"]

        # Kategorik sütunları sayısal değerlere dönüştür (label encoding)
        for col in X.select_dtypes(include="object").columns:
            X[col] = LabelEncoder().fit_transform(X[col])
        y_encoded = LabelEncoder().fit_transform(y)

        return X, y_encoded
    except Exception as e:
        print(f"Veri hazırlanırken hata oluştu: {e}")
        return None, None

def randomized_search_optimization(X_train, y_train):
    """
    RandomizedSearchCV kullanarak hiperparametre optimizasyonu yapar.
    Geniş parametre aralığında rastgele arama yaparak en iyi kombinasyonu bulur.
    
    Args:
        X_train: Eğitim veri özellikleri
        y_train: Eğitim veri etiketleri
        
    Returns:
        dict: En iyi hiperparametreler
    """
    print("\nRandomizedSearchCV başlatılıyor...")

    # Aranacak hiperparametre aralıklarını tanımla
    param_dist = {
        'n_estimators': [100, 200, 300, 400, 500],        # ağaç sayısı seçenekleri
        'max_depth': [10, 15, 20, 25, 30, None],          # maksimum derinlik seçenekleri
        'min_samples_split': [2, 5, 10, 16],              # bölme için minimum örnek sayısı
        'min_samples_leaf': [1, 2, 4],                    # yaprak düğümde minimum örnek sayısı
        'max_features': ['sqrt', 'log2'],                 # her bölmede kullanılacak özellik sayısı
        'bootstrap': [True],                              # örneklem yeniden yerleştirme
        'criterion': ['gini', 'entropy'],                # bölme kriteri seçenekleri
        'class_weight': ['balanced']                      # sınıf ağırlıklandırma
    }

    # Random Forest modelini oluştur
    model = RandomForestClassifier(random_state=42, n_jobs=-1)

    # RandomizedSearchCV yapılandırması
    random_search = RandomizedSearchCV(
        model,
        param_distributions=param_dist,
        n_iter=50,            # 50 farklı parametre kombinasyonu dene
        cv=5,                 # 5 katlı çapraz doğrulama kullan
        scoring='f1',         # f1 skoru ile değerlendirme yap
        verbose=1,            # ilerleme durumunu göster
        random_state=42,      # tekrarlanabilirlik için rastgele tohum
        n_jobs=-1             # tüm işlemci çekirdeğini kullan
    )

    # Optimizasyonu başlat ve en iyi parametreleri bul
    random_search.fit(X_train, y_train)
    best_params = random_search.best_params_
    print("\nEn iyi parametreler (RandomizedSearch):")
    print(best_params)
    return best_params

def grid_search_optimization(X_train, y_train, best_params):
    """
    GridSearchCV kullanarak RandomizedSearch sonuçlarının çevresinde
    daha detaylı arama yaparak parametreleri ince ayar yapar.
    
    Args:
        X_train: Eğitim veri özellikleri
        y_train: Eğitim veri etiketleri
        best_params: RandomizedSearch'ten gelen en iyi parametreler
        
    Returns:
        dict: İnce ayar yapılmış en iyi hiperparametreler
    """
    print("\nGridSearchCV başlatılıyor...")

    # RandomizedSearch sonuçlarına göre daraltılmış parametre aralığı
    param_grid = {
        'n_estimators': [best_params['n_estimators'] - 50, best_params['n_estimators'], best_params['n_estimators'] + 50],
        'max_depth': [best_params['max_depth']] if best_params['max_depth'] else [None],
        'min_samples_split': [best_params['min_samples_split'], best_params['min_samples_split'] + 4],
        'min_samples_leaf': [best_params['min_samples_leaf'], best_params['min_samples_leaf'] + 1],
        'max_features': [best_params['max_features']],
        'bootstrap': [best_params['bootstrap']],
        'criterion': [best_params['criterion']],
        'class_weight': [best_params['class_weight']]
    }

    # Yeni Random Forest modeli oluştur
    model = RandomForestClassifier(random_state=42, n_jobs=-1)

    # GridSearchCV yapılandırması
    grid_search = GridSearchCV(
        model,
        param_grid=param_grid,
        cv=5,                 # 5 katlı çapraz doğrulama
        scoring='f1',         # f1 skoru ile değerlendirme
        verbose=1,            # ilerleme durumunu göster
        n_jobs=-1             # tüm işlemci çekirdeğini kullan
    )

    # Grid search'ü başlat ve en iyi parametreleri bul
    grid_search.fit(X_train, y_train)
    best_params = grid_search.best_params_
    print("\nEn iyi parametreler (GridSearch):")
    print(best_params)
    return best_params

def save_optimized_parameters(params):
    """
    Bulunan en iyi hiperparametreleri metin dosyasına kaydeder.
    Bu parametreler daha sonra ana modelde kullanılabilir.
    
    Args:
        params: Kaydedilecek hiperparametreler dictionary'si
    """
    with open("optimize_rf_parametreleri.txt", "w", encoding='utf-8') as f:
        f.write("# Optimizasyon sonucu bulunan en iyi Random Forest parametreleri\n")
        f.write("# Bu parametreler main.py dosyasında kullanılabilir\n\n")
        f.write("RandomForestClassifier(\n")
        for key, value in params.items():
            val_str = f"'{value}'" if isinstance(value, str) else str(value)
            f.write(f"    {key}={val_str},\n")
        f.write("    random_state=42,\n")
        f.write("    n_jobs=-1\n")
        f.write(")\n")

def main():
    """
    Ana fonksiyon - hiperparametre optimizasyon sürecini yönetir.
    Kullanıcıdan optimizasyon yöntemini seçmesini ister ve süreci başlatır.
    """
    # Veri setini yükle ve hazırla
    X, y = load_data()
    if X is None:
        print("Veri yüklenemedi, program sonlandırılıyor.")
        return

    # Veriyi eğitim ve test olarak ayır, sınıf dağılımını koru
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # Kullanıcıdan optimizasyon yöntemi seçimini al
    print("\nHiperparametre Optimizasyon Yöntemleri:")
    print("1. RandomizedSearchCV - Geniş aralıkta hızlı arama")
    print("2. GridSearchCV - Dar aralıkta detaylı arama (önceden belirlenen parametrelerle)")
    choice = input("Seçiminiz (1 ya da 2): ").strip()

    if choice == '1':
        # Rastgele arama ile hiperparametre optimizasyonu
        best_params = randomized_search_optimization(X_train, y_train)
        save_optimized_parameters(best_params)

    elif choice == '2':
        print("Önceki RandomizedSearch çıktısındaki en iyi değerler kullanılarak GridSearch yapılacak...")
        
        # Önceki optimizasyon sonuçlarından en iyi parametreler
        # Bu değerler gerçek bir RandomizedSearch çıktısından gelir
        initial_best_params = {
            'n_estimators': 400,
            'max_depth': 20,
            'min_samples_split': 2,
            'min_samples_leaf': 1,
            'max_features': 'log2',
            'bootstrap': True,
            'criterion': 'entropy',
            'class_weight': 'balanced'
        }
        
        # Grid search ile ince ayar yap
        refined_params = grid_search_optimization(X_train, y_train, initial_best_params)
        save_optimized_parameters(refined_params)

    else:
        print("Geçersiz seçim. Lütfen 1 veya 2 seçin.")
        return

    print("\n✓ Optimizasyon tamamlandı!")
    print("✓ 'optimize_rf_parametreleri.txt' dosyası oluşturuldu.")
    print("✓ Bu parametreleri main.py dosyasında kullanabilirsiniz.")

# Program başlangıç noktası
if __name__ == "__main__":
    main()