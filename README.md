# 🚀 Crypto Analyzer App

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## 🌟 Overview

**Crypto Analyzer** è un'app desktop scritta in **Python** con interfaccia moderna grazie a [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter). Ti permette di:

- 📈 Visualizzare il prezzo in tempo reale di una criptovaluta.
- 📊 Esplorare metriche come variazioni % (24h, 30d, 60d, 90d) e supply (circolante, totale, massimo).
- 🏆 Consultare la classifica **Top 50 Crypto** per capitalizzazione di mercato.
- 🔒 Memorizzare la tua API Key in modo sicuro grazie a **Keyring**. 

---

## 📦 Requisiti

Assicurati di avere **Python ≥ 3.8** installato.  
Installa le dipendenze con:

```bash
pip install -r requirements.txt
```

---

## 🔑 API Key CoinMarketCap

- Per funzionare, l'app richiede una API Key gratuita da CoinMarketCap Developer Portal.
- 1 Registrati su pro.coinmarketcap.com.
- 2 Copia la chiave.
- 3 La prima volta che avvii l'app, ti verrà chiesto di inserirla.
- 4 Verrà salvata in modo sicuro sul sistema tramite keyring.

---

## 🚀 Usage

```bash
python CryptoAnalyzer.py
```

- Alla **prima esecuzione** verrà richiesto di inserire la API Key  
- Inserisci il simbolo (es. `BTC`) e premi **Analizza**  
- Usa **Aggiorna API Key** per modificare la chiave in qualunque momento  

---

## 📁 Project Structure

```text
crypto-analyzer-app/
├── main.py             # Entry point
├── requirements.txt    # Requirements
├── LICENSE             # Licenza MIT
└── README.md           # Documentazione
```

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
© 2025 - Sviluppato con ❤️ da **nickabra**  

