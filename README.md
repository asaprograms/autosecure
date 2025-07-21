# Autosecure

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repo-url>
cd autosecure
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Node.js Dependencies (for Lunar integration)
```bash
npm install
```

### 4. Set API Keys in `config.py`
- Open `config.py` and set your Hypixel API key and 2captcha key:

```python
KEYS = {
    "hypixel": "YOUR_HYPIXEL_API_KEY",
    "2captcha": "YOUR_2CAPTCHA_API_KEY",
}
```
- The Hypixel API key is used for Minecraft-related features.
- The 2captcha key is required for solving captchas during account operations.

---

## License

MIT