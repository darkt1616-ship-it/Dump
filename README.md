# Breach Research - Cybersecurity Academic Project

## 📚 Descrizione
Progetto per la ricerca sul credential stuffing e la cybersecurity. Genera dataset realistici di breach e testa sistemi di sicurezza.

## 🎯 Obiettivi
- Generare dataset realistici di credenziali rubate
- Analizzare pattern di breach
- Testare sistemi di sicurezza contro credential stuffing

## 📂 Struttura del progetto
```
.
├── main.py               # Entry point della CLI
├── requirements.txt      # Dipendenze Python
├── setup.py              # Configurazione del pacchetto
├── .devcontainer/        # Configurazione GitHub Codespaces
├── scripts/              # Script bash di supporto
├── src/                  # Pacchetto Python
│   ├── generator.py      # Generazione dataset
│   ├── analyzer.py       # Analisi statistica
│   ├── security_tester.py# Test del sistema di sicurezza
│   └── utils.py          # Funzioni di utilità
├── tests/                # Test unitari
└── data/                 # Output generati (ignorati da git)
```

## 🚀 Installazione

### Con GitHub Codespaces (Consigliato)
1. Clicca su "Code" -> "Codespaces" -> "New codespace"
2. Attendi l'installazione automatica delle dipendenze
3. Esegui i comandi qui sotto

### Locale
```bash
git clone <repository>
cd Dump
pip install -r requirements.txt
```

## 🛠️ Utilizzo

Tutti i comandi si lanciano tramite `main.py`:

```bash
# Mostra l'elenco dei comandi disponibili
python main.py --help

# Genera il dataset (numero di righe personalizzabile)
python main.py generate --righe 100000

# Analizza il dataset generato
python main.py analyze --campione 10000

# Testa il sistema di sicurezza
python main.py test --credenziali 1000

# Esegui l'intero workflow (genera + analizza + testa)
python main.py full
```

In alternativa puoi usare gli script bash interattivi:

```bash
chmod +x scripts/*.sh
./scripts/generate.sh
./scripts/analyze.sh
./scripts/test.sh
```

## ✅ Test
```bash
pip install pytest
python -m pytest tests/ -v
```
