# Autosecure

## Setup Instructions

### 0. Install git
- Easy enough

### 1. Clone the Repository
```bash
git clone https://github.com/asaprograms/autosecure
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

### 4. Set API Keys in `config.example.py`
- Open `config.example.py` and set your Hypixel API key and 2captcha key:

```python
KEYS = {
    "hypixel": "YOUR_HYPIXEL_API_KEY",
    "2captcha": "YOUR_2CAPTCHA_API_KEY",
}
```
- Then, change config.example.py filename to config.py

- Optionally, change config.example.py to be compatible with .env and modify .env.example

```bash
hypixel= # a given, please add if using .env
2captcha= # a given, please add if using .env
```

### If any problems arise,

- https://chatgpt.com/ and https://gemini.google.com/ are great resources and are smarter than us all lmao

- The Hypixel API key is used for Minecraft-related features and is required.
- The 2captcha key is required for solving captchas during account operations and is required.

---

## License

MIT