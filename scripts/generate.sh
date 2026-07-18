#!/bin/bash
# Script per generare il dataset di breach

echo "🔐 GENERAZIONE DATASET BREACH"
echo "============================="
echo ""

# Chiedi il numero di righe da generare
read -p "Numero di righe da generare (default: 1000000): " righe
righe=${righe:-1000000}

# Esegui la generazione
echo ""
echo "⚡ Avvio generazione..."
python main.py generate --righe $righe

echo ""
echo "✅ Generazione completata!"
echo "📁 Dataset salvato in: data/breach_dataset.txt"
