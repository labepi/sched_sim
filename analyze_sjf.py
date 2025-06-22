#!/usr/bin/env python3
"""
Script para analisar os resultados do algoritmo SJF
Calcula a média dos TME's e gera gráficos de comparação
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import re
from pathlib import Path

# Configurar o estilo dos gráficos
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_sjf_data():
    """Carrega os dados TME do algoritmo SJF"""
    sjf_data = []
    data_dir = Path("data_SJF")
    
    if not data_dir.exists():
        print(f"Erro: Diretório {data_dir} não encontrado!")
        return None
    
    # Agrupar arquivos por número de processos
    process_groups = {}
    
    for file_path in data_dir.glob("tme_*.txt"):
        # Extrair número de processos do nome do arquivo (formato: tme_10_1.txt)
        parts = file_path.stem.split('_')
        if len(parts) >= 3:
            num_processos = int(parts[1])
            run_number = int(parts[2])
            
            if num_processos not in process_groups:
                process_groups[num_processos] = []
            
            process_groups[num_processos].append((run_number, file_path))
    
    # Processar cada grupo de processos
    for num_processos in sorted(process_groups.keys()):
        group_files = process_groups[num_processos]
        group_files.sort(key=lambda x: x[0])  # Ordenar por número da rodada
        
        all_tme_values = []
        
        print(f"\nProcessando {num_processos} processos:")
        
        # Processar cada arquivo do grupo
        for run_number, file_path in group_files:
            # Ler o arquivo e procurar por linhas com "TME:"
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    # Procurar por padrão "TME: VALOR"
                    match = re.search(r'TME:\s*([0-9]+\.?[0-9]*)', line)
                    if match:
                        tme_value = float(match.group(1))
                        all_tme_values.append(tme_value)
                        break  # Pegar apenas o primeiro TME encontrado no arquivo
            
            print(f"  Rodada {run_number}: TME = {all_tme_values[-1] if all_tme_values else 'N/A'}")
        
        if not all_tme_values:
            print(f"Aviso: Nenhum valor TME encontrado para {num_processos} processos")
            continue
        
        # Calcular estatísticas para este grupo
        media = np.mean(all_tme_values)
        desvio_padrao = np.std(all_tme_values)
        variancia = np.var(all_tme_values)
        minimo = np.min(all_tme_values)
        maximo = np.max(all_tme_values)
        
        sjf_data.append({
            'Processos': num_processos,
            'Media': media,
            'Desvio_Padrao': desvio_padrao,
            'Variancia': variancia,
            'Minimo': minimo,
            'Maximo': maximo,
            'Num_Execucoes': len(all_tme_values)
        })
        
        print(f"  Média dos {len(all_tme_values)} valores: {media:.2f}")
    
    return pd.DataFrame(sjf_data)

def plot_sjf_analysis(df):
    """Gera gráficos de análise para o algoritmo SJF"""
    
    # Criar diretório de saída se não existir
    output_dir = Path("data_SJF")
    output_dir.mkdir(exist_ok=True)
    
    # Gráfico 1: TME vs Número de Processos
    plt.figure(figsize=(12, 8))
    
    plt.plot(df['Processos'], df['Media'], 
            marker='o', linewidth=3, markersize=10, 
            color='#ff7f0e', label='TME Médio')
    
    # Adicionar barras de erro (desvio padrão)
    plt.errorbar(df['Processos'], df['Media'], 
                yerr=df['Desvio_Padrao'], 
                fmt='none', capsize=5, capthick=2, 
                color='#ff7f0e', alpha=0.7, label='±1 Desvio Padrão')
    
    plt.xlabel('Número de Processos', fontsize=14)
    plt.ylabel('Tempo Médio de Espera (TME)', fontsize=14)
    plt.title('Análise do TME - Algoritmo SJF', fontsize=16, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'sjf_tme_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Gráfico 2: Variância vs Número de Processos
    plt.figure(figsize=(12, 8))
    
    plt.plot(df['Processos'], df['Variancia'], 
            marker='s', linewidth=3, markersize=10, 
            color='#d62728', label='Variância')
    
    plt.xlabel('Número de Processos', fontsize=14)
    plt.ylabel('Variância do TME', fontsize=14)
    plt.title('Variância do TME - Algoritmo SJF', fontsize=16, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'sjf_variance_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Gráfico 3: Range (Máximo - Mínimo) vs Número de Processos
    plt.figure(figsize=(12, 8))
    
    range_values = df['Maximo'] - df['Minimo']
    plt.plot(df['Processos'], range_values, 
            marker='^', linewidth=3, markersize=10, 
            color='#9467bd', label='Range (Máx - Mín)')
    
    plt.xlabel('Número de Processos', fontsize=14)
    plt.ylabel('Range do TME', fontsize=14)
    plt.title('Range do TME - Algoritmo SJF', fontsize=16, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'sjf_range_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Gráfico 4: Comparação Mínimo, Médio, Máximo
    plt.figure(figsize=(12, 8))
    
    plt.plot(df['Processos'], df['Minimo'], 
            marker='v', linewidth=2, markersize=8, 
            color='#d62728', label='Mínimo', alpha=0.8)
    plt.plot(df['Processos'], df['Media'], 
            marker='o', linewidth=3, markersize=10, 
            color='#ff7f0e', label='Médio', alpha=0.9)
    plt.plot(df['Processos'], df['Maximo'], 
            marker='^', linewidth=2, markersize=8, 
            color='#9467bd', label='Máximo', alpha=0.8)
    
    plt.xlabel('Número de Processos', fontsize=14)
    plt.ylabel('Tempo Médio de Espera (TME)', fontsize=14)
    plt.title('Comparação Mínimo/Médio/Máximo - Algoritmo SJF', fontsize=16, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'sjf_min_med_max_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_sjf_summary(df):
    """Cria um resumo estatístico do algoritmo SJF"""
    print("\n" + "="*80)
    print("RESUMO ESTATÍSTICO - ALGORITMO SJF")
    print("="*80)
    
    print(f"\nTotal de configurações testadas: {len(df)}")
    print(f"Range de processos: {df['Processos'].min()} - {df['Processos'].max()}")
    print(f"Número de execuções por configuração: {df['Num_Execucoes'].iloc[0]}")
    
    print("\nEstatísticas Gerais:")
    print(f"TME Médio Geral: {df['Media'].mean():.2f}")
    print(f"TME Médio Mínimo: {df['Media'].min():.2f} (com {df.loc[df['Media'].idxmin(), 'Processos']} processos)")
    print(f"TME Médio Máximo: {df['Media'].max():.2f} (com {df.loc[df['Media'].idxmax(), 'Processos']} processos)")
    print(f"Variância Média: {df['Variancia'].mean():.2f}")
    
    print("\nDetalhamento por Número de Processos:")
    print("-" * 60)
    print(f"{'Processos':<10} {'TME Médio':<12} {'Desvio':<10} {'Variância':<12} {'Range':<10}")
    print("-" * 60)
    
    for _, row in df.iterrows():
        range_val = row['Maximo'] - row['Minimo']
        print(f"{row['Processos']:<10} {row['Media']:<12.2f} {row['Desvio_Padrao']:<10.2f} "
              f"{row['Variancia']:<12.2f} {range_val:<10.2f}")
    
    # Salvar resumo em CSV dentro da pasta data_SJF
    output_dir = Path("data_SJF")
    output_dir.mkdir(exist_ok=True)
    df.to_csv(output_dir / 'sjf_summary.csv', index=False)
    print(f"\nResumo salvo em 'data_SJF/sjf_summary.csv'")

def main():
    """Função principal"""
    print("Analisando dados do algoritmo SJF...")
    
    # Carregar dados
    df = load_sjf_data()
    
    if df is None:
        return
    
    print(f"Dados carregados com sucesso!")
    print(f"Configurações analisadas: {len(df)}")
    
    # Criar gráficos
    print("\nGerando gráficos...")
    plot_sjf_analysis(df)
    
    # Criar resumo
    create_sjf_summary(df)
    
    print("\nAnálise concluída!")
    print("Arquivos gerados em 'data_SJF/':")
    print("- sjf_tme_analysis.png")
    print("- sjf_variance_analysis.png")
    print("- sjf_range_analysis.png")
    print("- sjf_min_med_max_comparison.png")
    print("- sjf_summary.csv")

if __name__ == "__main__":
    main() 