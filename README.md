# 🚀 Crypto Analyzer App

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## 🌟 Overview

**Crypto Analyzer App** è un'applicazione desktop leggera, sviluppata in Python e `tkinter`, che consente di:

- 📈 Visualizzare il **prezzo**, il **volume** e le **variazioni percentuali** (1h, 24h, 30d, 60d, 90d) delle criptovalute via API CoinMarketCap  
- 🥇 Consultare la **Top 50** criptovalute ordinate per capitalizzazione di mercato  
- 💵 **Calcolare** in tempo reale il valore in USD di una quantità definita di crypto  
- 🔐 Gestire la **API Key** in modo sicuro, memorizzandola nel keyring del sistema operativo  

## 🛠️ Installation

```bash
# 1. Clona il repository
git clone https://github.com/<tuo-username>/crypto-analyzer-app.git
cd crypto-analyzer-app

# 2. (Opzionale) Crea e attiva un virtualenv
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate    # Windows
```

---

## 🚀 Usage

```bash
python main.py
```

- Alla **prima esecuzione** verrà richiesto di inserire la API Key  
- Inserisci il simbolo (es. `BTC`) e premi **Analizza**  
- Usa **Aggiorna API Key** per modificare la chiave in qualunque momento  

---

## 📁 Project Structure

```text
crypto-analyzer-app/
├── main.py             # Entry point
├── LICENSE             # Licenza MIT
└── README.md           # Documentazione
```

---

## ✨ Features

- **Intuitive GUI**: basata su `tkinter` e `ttk.Notebook`  
- **Secure API Key**: gestita con `keyring`, mai in chiaro  
- **Caching**: evita chiamate API ripetute entro 5 minuti  
- **Interactive Updates**: popup iniziale e pulsante dedicato  
- **On-the-fly Calculation**: converti quantità di crypto in USD  

---

## 📦 Dependencies

- `requests`  
- `keyring`
- `ttkbootstrap`
- `tkinter` (builtin)
-  `pandas`

---

## 🤝 Contributing

Contribuzioni, issue e PR sono benvenuti!  
1. Fork del progetto  
2. Crea un branch feature (`git checkout -b feature/nome`)  
3. Commit (`git commit -m 'Aggiungi feature'`)  
4. Push (`git push origin feature/nome`)  
5. Apri una Pull Request  

---

## 📝 License

Questo progetto è distribuito sotto licenza **MIT**.  
