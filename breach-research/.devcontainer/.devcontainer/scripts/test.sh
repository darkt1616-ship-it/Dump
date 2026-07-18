#!/bin/bash
# Script per testare il sistema di sicurezza

echo "🛡️ TEST SISTEMA DI SICUREZZA"
echo "============================"
echo ""

# Controlla se il file esiste
if [ ! -f "data/breach_dataset.txt" ]; then
    echo "❌ File data/breach_dataset.txt non trovato!"
    echo "Esegui prima: ./scripts/generate.sh"
    exit 1
fi

# Chiedi il numero di credenziali da testare
read -p "Numero di credenziali da testare (default: 1000): " credenziali
credenziali=${credenziali:-1000}

# Esegui test
echo ""
echo "🎯 Avvio test..."
python main.py test --credenziali $credenziali

# Salva risultati
echo ""
read -p "Salvare i risultati? (s/n): " salva_risultati
if [[ $salva_risultati == "s" || $salva_risultati == "S" ]]; then
    timestamp=$(date +"%Y%m%d_%H%M%S")
    result_file="reports/test_results_${timestamp}.txt"
    mkdir -p reports
    
    # Cattura l'output del test
    {
        echo "🛡️ TEST SISTEMA DI SICUREZZA"
        echo "============================"
        echo "Data: $(date)"
        echo ""
        python main.py test --credenziali $credenziali
    } > $result_file
    
    echo "✅ Risultati salvati in: $result_file"
fi

echo ""
echo "✅ Test completato!"