# IoT DDoS Attack Detection System

This project is a machine learning application that uses the Random Forest algorithm to detect Distributed Denial of Service (DDoS) attacks in Internet of Things (IoT) networks.

## 📋 About the Project

IoT devices are widely used today and are in constant communication with each other. This brings security risks along with it. DDoS attacks are among the most serious of these risks. This project aims to develop a classification model that can distinguish between normal traffic and attack traffic by analyzing IoT network traffic.

## ✨ Features

- **High Accuracy**: Detects DDoS attacks with 99% accuracy rate
- **Random Forest Algorithm**: Uses ensemble learning for stable and reliable results
- **Real-Time Analysis**: Can analyze IoT network traffic in real-time
- **Detailed Visualization**: Visualizes model performance with ROC curve, feature importance scores, and learning curves

## 📊 Dataset

The **IoT-DH dataset** is used in the project. This dataset includes the following features:

| Feature | Description |
|---------|-------------|
| `dt` | Time difference between consecutive packets |
| `dur` | Duration between consecutive packets |
| `dur_nsec` | Nanosecond part of elapsed time |
| `tot_dur` | Total duration of captured packets |
| `pktrate` | Number of packets per second |
| `protocol` | Packet protocol |
| `port_no` | Port number |
| `tx_kbps` | Kilobits transmitted per second |
| `rx_kbps` | Kilobits received per second |
| `tot_kbps` | Total kilobits per second |
| `label` | Normal traffic (0) or attack traffic (1) |

## 🚀 Installation

### Running the Project

1. Download the project source files and place them in the directory where the project will run

2. Download the dataset by clicking "Download All 695 MB" button from the link in the references section, extract from zip and place in the project directory

3. The dataset path should be ./IoT-DH Dataset/Dataset/IoT-DH Dataset.csv

4. Train and test the model:
```bash
python train_and_test_model.py
```

## 📈 Model Performance

### Classification Report

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| Normal (0) | 0.9984 | 0.9961 | 0.9972 | 1269 |
| DDoS (1) | 0.9937 | 0.9975 | 0.9956 | 790 |

### Confusion Matrix

|  | Actual Normal (0) | Actual DDoS (1) |
|--|-------------------|-----------------|
| **Predicted Normal (0)** | 788 | 5 |
| **Predicted DDoS (1)** | 2 | 1264 |

**Overall Accuracy: 99%**

## 🔧 Methodology

1. **Data Preprocessing**:
   - 10% of the dataset was used randomly to prevent model overfitting
   - Unnecessary columns (src, dst, protocol) were removed
   - Categorical data was converted to numerical data

2. **Model Training**:
   - Random Forest Classifier was used
   - Hyperparameter optimization was performed with GridSearchCV
   - 80% training, 20% test data split

3. **Evaluation**:
   - Precision, Recall, F1-Score metrics
   - ROC curve analysis
   - Feature importance scores

## 📊 Visualizations

The project includes the following visualizations:

- **ROC Curve**: Visual analysis of model performance
- **Feature Importance Scores**: Identification of the most effective features
- **Class Distribution**: Analysis of imbalance in the dataset
- **Learning Curves**: Change in model performance according to training data size

## 🎯 Use Cases

- IoT network security
- Cybersecurity systems
- Network traffic analysis
- Real-time threat detection

## 📚 References

- [IoT-DH Dataset (Mendeley)](https://data.mendeley.com/datasets/8dns3xbckv/1)
- [Scikit-learn Random Forest Documentation](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)
- [Random Forest Hyperparameters](https://www.geeksforgeeks.org/hyperparameters-of-random-forest-classifier/)

## 📝 License

This project is licensed under the GPLv3 license.

## 👨‍💻 Developer

**Mustafa AYKUT**  
Student No: 22360859028

## 📞 Contact

For questions about the project, you can open an issue or contact via email.

---

**Note**: This project is a homework project prepared within the scope of the data mining course.
