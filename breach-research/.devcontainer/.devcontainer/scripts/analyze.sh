#!/bin/bash
# Script per analizzare il dataset generato

echo "📊 ANALISI DATASET BREACH"
echo "========================"
echo ""

# Controlla se il file esiste
if [ ! -f "data/breach_dataset.txt" ]; then
    echo "❌ File data/breach_dataset.txt non trovato!"
    echo "Esegui prima: ./scripts/generate.sh"
    exit 1
fi

# Chiedi il numero di campione
read -p "Numero di credenziali da analizzare (default: 10000): " campione
campione=${campione:-10000}

# Esegui analisi
echo ""
echo "🔍 Avvio analisi..."
python main.py analyze --campione $campione

# Salva report
echo ""
read -p "Salvare il report? (s/n): " salva_report
if [[ $salva_report == "s" || $salva_report == "S" ]]; then
    timestamp=$(date +"%Y%m%d_%H%M%S")
    report_file="reports/analysis_report_${timestamp}.txt"
    mkdir -p reports
    
    # Cattura l'output dell'analisi
    {
        echo "📊 REPORT ANALISI DATASET BREACH"
        echo "================================="
        echo "Data: $(date)"
        echo ""
        python main.py analyze --campione $campione
    } > $report_file
    
    echo "✅ Report salvato in: $report_file"
fi

echo ""
echo "✅ Analisi completata!"