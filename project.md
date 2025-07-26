# 📘 Approach Documentation

## 1. Problem Statement 
The objective is to utilize data analysis and machine learning techniques to comprehensively examine firewall logs, with the goal of identifying potential security incidents such as   errors, threats, and suspicious activities in real time. The requests will be labelled either as "allow", "deny", "drop", and "reset-both"

---

## 2. Data Understanding
- **Data Source**: Kaggle Internet Firewall Dataset
- **Data Source Link** :  https://www.kaggle.com/datasets/tunguz/internet-firewall-data-set

| Column Name             | Data Type | Description |
|-------------------------|-----------|-------------|
| **Source Port**         | Integer   | The port number on the source device from which the traffic originated. |
| **Destination Port**    | Integer   | The port number on the destination device to which the traffic is directed. |
| **NAT Source Port**     | Integer   | Source port number after applying Network Address Translation (NAT). |
| **NAT Destination Port**| Integer   | Destination port number after NAT is applied. |
| **Action**              | String    | Indicates whether the traffic was allowed, denied, or dropped (e.g., "allow", "deny"). |
| **Bytes**               | Integer   | Total number of bytes transferred during the session. |
| **Bytes Sent**          | Integer   | Number of bytes sent from source to destination. |
| **Bytes Received**      | Integer   | Number of bytes received at the source from the destination. |
| **Packets**             | Integer   | Total number of packets transferred during the session. |
| **Elapsed Time (sec)**  | Float     | Duration of the session or traffic flow, in seconds. |
| **pkts_sent**           | Integer   | Number of packets sent from the source. |
| **pkts_received**       | Integer   | Number of packets received by the source. |

- **Data Size**:  (65532, 12)
---

## 3. Data Preprocessing
- **Cleaning**:
  - Removed nulls and duplicates
  - Standardized column names and formats
- **Feature Engineering**:
  - Encoded categorical variables using `.astype('category').cat.codes`
  - Extracted derived features where applicable
- **Splitting Strategy**:
  - Train/Validation/Test: 60/20/20 split - **initialtraining and hyperparameter tuning**
  - Train/Validation/Test: 80/20 split - **final training**

## 4. 🧮 Final Feature Schema

| Column Name              | Data Type | Description |
|--------------------------|-----------|-------------|
| **high_activity**        | Boolean   | Indicates whether the flow exhibits unusually high packet or byte volume (binary feature). |
| **packets_ratio**        | Float     | Ratio of packets sent to packets received (pkts_sent / pkts_received). Captures directional packet imbalance. |
| **source_port**          | Integer   | Original source port used in the network connection. |
| **low_activity**         | Boolean   | Indicates whether the flow shows minimal activity (binary feature). |
| **bytes_ratio**          | Float     | Ratio of bytes sent to bytes received (bytes_sent / bytes_received). Highlights directional byte volume differences. |
| **destination_port**     | Integer   | Original destination port before any NAT. |
| **nat_destination_port**| Integer   | Destination port after NAT translation. |
| **elapsed_time_(sec)**   | Float     | Total session duration in seconds. |
| **nat_source_port**      | Integer   | Source port after NAT translation. |
| **burst_transfer**       | Boolean   | Indicates whether the traffic was transferred in a short time but with high volume (burst behavior). |
| **bytes_per_sec**        | Float     | Rate of byte transfer over time (`bytes / elapsed_time_(sec)`). Useful for identifying heavy or suspicious flows. |

- **Data Size**: (57170, 12)
---

## 5. Modeling
- **Model Used**: XGBoost Classifier (multi-class setup)
- **Reason for Choice**: Handles non-linearities well, robust with categorical + numerical data, requires less preprocessing
- **Training Details**:
  + Used Optuna for hyperparameter tuning
---

## 6. Evaluation
- **Metrics**:
  - Precision, Recall, **F1-score**
  - Class-wise performance
- **Handling Class Imbalance**:
  - Applied **sample weights** during training

---

## 7. Prediction Pipeline
- **Input**: JSON via FastAPI
- **Output**: Predicted label(s) like "allow", "deny", "drop", and "reset-both"

---

## 8. Deployment
- **Framework**: FastAPI
- **Endpoint**: `POST /predict`
- **Schema**: Defined using Pydantic (`PredictionInput` model)
- **Error Handling**: Try-except blocks with 500 responses for internal errors

---

## 9. Monitoring & Logging
    - can use Grafana for this purpose
---

## 10. Limitations & Assumptions
- Assumes consistency in incoming data schema
- No concept drift detection in current version

---

## 11. Future Work
- Add model explainability (e.g., SHAP values)
- Improve UI/UX with a simple frontend for input submission
- Automate retraining pipelines
- Implement model versioning and rollback support
- Build a dashboard to summarized security incidents using **streamlit**
