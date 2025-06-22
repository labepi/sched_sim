#!/bin/bash

# Nome do algoritmo como argumento
if [ "$#" -ne 1 ]; then
    echo "Uso: $0 <ALG_NAME>"
    echo "Exemplo: $0 SJF"
    exit 1
fi

ALG_NAME=$1
DATA_FOLDER="data_${ALG_NAME}"

mkdir -p "$DATA_FOLDER"

# Loop principal
for NUM_PROC in {10..100..10}; do
    for ITER in {1..10}; do
        FILE="${DATA_FOLDER}/tme_${NUM_PROC}_${ITER}.txt"

        if [ -f "$FILE" ]; then
            echo "⚠️  [Skip] Arquivo já existe: $FILE"
            continue
        fi

        echo "✅ Executando $ALG_NAME com $NUM_PROC processos (Iteração $ITER)..."
        python3 run_analysis.py "$ALG_NAME" "$NUM_PROC" "$ITER"
    done
done
