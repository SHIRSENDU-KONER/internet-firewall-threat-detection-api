# Threat and Anomaly Detection System Report

## 1. Exploratory Data Analysis (EDA)

### Action Distribution

The dataset contains four types of actions:

- **allow**: 37,439
- **drop**: 11,635
- **deny**: 8,042
- **reset-both**: 54

### Null Values

- No null values found in the dataset.
- Duplicate values dropped.

### Packet-related Columns (`packets`, `pkts_sent`, `pkts_received`)

- These columns exhibit a long-tail / right-skewed distribution.
- Statistics for `packets`:
  - **Mean**: 118
  - **Std**: 5,495
  - **Min**: 1
  - **25%**: 1
  - **50%**: 2
  - **75%**: 10
  - **Max**: 1,036,116
- Similar behavior observed in `pkts_sent` and `pkts_received`.
- Over 75% of traffic involves very few packets, while a small number of flows involve extremely high packet volumes.

### Bytes

- **Mean**: 111,315
- **Std**: 6,015,189
- **Min**: 60
- **25%**: 70
- **50% (Median)**: 193
- **75%**: 1,139
- **Max**: 1,269,359,015
- **Insights**:
  - Nearly 55% of the entries have total bytes (sent + received) below 200.
  - The median is under 200 bytes, and 75% of data is below 800 bytes.
  - Indicates most traffic consists of small packets; few entries show unusually high byte volumes (potential anomalies).

### Top Destination Ports

- **Most frequent**:
  - 53 (DNS): 15,389
  - 443 (HTTPS): 11,684
  - 445 (SMB): 11,674
  - 80 (HTTP): 4,035
  - Others include: 25174, 22114, 50584, 64147, 44847, 23
- **Insight**: Common service ports are expected. High-numbered ports may represent dynamic/malicious traffic and warrant investigation.

### Top Source Ports

- Most common:
  - 27005, 57470, 49418, 6881, 443, etc.
- High-numbered source ports are typical for client-originated traffic; however, any known exploit port should be flagged.

### Elapsed Time

- \~35% of network traffic completes within 1 second.

### Correlation Analysis

- High correlation observed between:
  - `bytes`, `bytes_sent`, `bytes_received`, `packets`, `pkts_sent`, `pkts_received`
- Confirmed with heatmaps and pairplots.

### Feature Engineering

- Created features like `bytes_per_sec` and `burst_transfer`.
- Informative patterns observed across these engineered features.
- Final feature set had minimal multicollinearity.

---

## 2. Model Training

### Model

- **XGBoost** was selected due to its performance and handling of mixed feature types.

### Imbalance Handling

- Tried **SMOTE**, **SMOTEENN**, and **class weight sampling**.
- **Class weight sampling** produced the best results in this case.

---

## 3. Hyperparameter Tuning

- Performed using **Optuna**, a powerful hyperparameter optimization library.

---

## 4. Model Performance

### Metric Used

- **F1-score (macro)**: **0.87**

### Classification Report

```
              precision    recall  f1-score   support

           0       1.00      1.00      1.00      7488
           1       1.00      0.99      0.99      1608
           2       1.00      1.00      1.00      2327
           3       0.56      0.45      0.50        11

    accuracy                           1.00     11434
   macro avg       0.89      0.86      0.87     11434
weighted avg       1.00      1.00      1.00     11434
```

- Class 3 (least frequent) showed lower performance due to data sparsity.

---

## Conclusion

The model is highly accurate for the dominant classes with very strong precision and recall. Further tuning or anomaly-specific approaches (e.g., one-class classification) can improve detection of rare threat types.

