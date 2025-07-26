
---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/firewall-threat-detection.git
```
### 2. Install dependencies and auto-create .venv if missing
```
cd your folder
pip install uv
uv pip install --all-extras .
```
### 3. activate the env
```.venv\Scripts\activate ```

### 4. Run your app
```uvicorn api.app.main:app --reload```
