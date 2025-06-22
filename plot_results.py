#!/usr/bin/env python3
"""
Script para plotar os resultados dos algoritmos de escalonamento
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configurar o estilo dos gráficos
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def plot_tme_comparison(df):
    """Plot 1: Comparação do TME entre algoritmos"""
    plt.figure(figsize=(12, 8))
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    # Criar gráfico de linha para cada algoritmo
    for i, algoritmo in enumerate(df['Algoritmo'].unique()):
        data = df[df['Algoritmo'] == algoritmo]
        color = colors[i % len(colors)]  # Usar cores ciclicamente
        plt.plot(data['Processos'], data['Media'], 
                marker='o', linewidth=2.5, markersize=8, 
                label=algoritmo, alpha=0.9, color=color)
    
    plt.xlabel('Número de Processos', fontsize=12)
    plt.ylabel('Tempo Médio de Espera (TME)', fontsize=12)
    plt.title('Comparação do Tempo Médio de Espera (TME) por Algoritmo', fontsize=14, fontweight='bold')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('tme_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_variance_analysis(df):
    """Plot 2: Análise da variância por algoritmo"""
    plt.figure(figsize=(12, 8))
    
    # Criar gráfico de barras para variância
    algoritmos = df['Algoritmo'].unique()
    x = np.arange(len(algoritmos))
    width = 0.35
    
    # Calcular média da variância para cada algoritmo
    var_means = []
    for algoritmo in algoritmos:
        var_mean = df[df['Algoritmo'] == algoritmo]['Variancia'].mean()
        var_means.append(var_mean)
    
    bars = plt.bar(x, var_means, width, alpha=0.8, edgecolor='black')
    
    # Adicionar valores nas barras
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + max(var_means)*0.01,
                f'{height:.0f}', ha='center', va='bottom', fontsize=10)
    
    plt.xlabel('Algoritmo', fontsize=12)
    plt.ylabel('Variância Média', fontsize=12)
    plt.title('Análise da Variância do TME por Algoritmo', fontsize=14, fontweight='bold')
    plt.xticks(x, algoritmos, rotation=45)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('variance_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_heatmap(df):
    """Plot 3: Heatmap da performance por algoritmo e número de processos"""
    plt.figure(figsize=(14, 8))
    
    # Pivotar os dados para criar a matriz
    pivot_data = df.pivot(index='Algoritmo', columns='Processos', values='Media')
    
    # Criar heatmap
    sns.heatmap(pivot_data, annot=True, fmt='.0f', cmap='YlOrRd', 
                cbar_kws={'label': 'Tempo Médio de Espera (TME)'})
    
    plt.title('Heatmap: TME por Algoritmo e Número de Processos', fontsize=14, fontweight='bold')
    plt.xlabel('Número de Processos', fontsize=12)
    plt.ylabel('Algoritmo', fontsize=12)
    plt.tight_layout()
    plt.savefig('performance_heatmap.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_boxplot_style(df):
    """Plot 4: Gráfico estilo boxplot mostrando distribuição por algoritmo"""
    plt.figure(figsize=(12, 8))
    
    # Criar dados para boxplot
    data_for_box = []
    labels = []
    
    for algoritmo in df['Algoritmo'].unique():
        data = df[df['Algoritmo'] == algoritmo]['Media'].values
        data_for_box.append(data)
        labels.append(algoritmo)
    
    # Criar boxplot
    box_plot = plt.boxplot(data_for_box, labels=labels, patch_artist=True)
    
    # Colorir as caixas
    colors = plt.cm.Set3(np.linspace(0, 1, len(box_plot['boxes'])))
    for patch, color in zip(box_plot['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    plt.xlabel('Algoritmo', fontsize=12)
    plt.ylabel('Tempo Médio de Espera (TME)', fontsize=12)
    plt.title('Distribuição do TME por Algoritmo', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('tme_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_scatter_with_trends(df):
    """Plot 5: Gráfico de dispersão com tendências"""
    plt.figure(figsize=(12, 8))
    
    # Criar gráfico de dispersão para cada algoritmo
    for algoritmo in df['Algoritmo'].unique():
        data = df[df['Algoritmo'] == algoritmo]
        
        # Scatter plot
        plt.scatter(data['Processos'], data['Media'], 
                   alpha=0.7, s=60, label=algoritmo)
        
        # Linha de tendência
        z = np.polyfit(data['Processos'], data['Media'], 1)
        p = np.poly1d(z)
        plt.plot(data['Processos'], p(data['Processos']), 
                alpha=0.5, linewidth=2)
    
    plt.xlabel('Número de Processos', fontsize=12)
    plt.ylabel('Tempo Médio de Espera (TME)', fontsize=12)
    plt.title('TME vs Número de Processos com Tendências', fontsize=14, fontweight='bold')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('scatter_with_trends.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_summary_table(df):
    """Criar tabela resumo das estatísticas"""
    print("\n" + "="*80)
    print("RESUMO ESTATÍSTICO DOS ALGORITMOS DE ESCALONAMENTO")
    print("="*80)
    
    summary = df.groupby('Algoritmo').agg({
        'Media': ['mean', 'std', 'min', 'max'],
        'Variancia': ['mean', 'max']
    }).round(2)
    
    print(summary)
    
    # Salvar tabela em arquivo
    summary.to_csv('resumo_estatistico.csv')
    print("\nTabela resumo salva em 'resumo_estatistico.csv'")

def main():
    """Função principal"""
    try:
        # Carregar dados do CSV
        df = pd.read_csv('resultados_tme.csv')
        
        print("Dados carregados com sucesso!")
        print(f"Shape dos dados: {df.shape}")
        print(f"Algoritmos disponíveis: {df['Algoritmo'].unique()}")
        print(f"Range de processos: {df['Processos'].min()} - {df['Processos'].max()}")
        
        # Criar todos os gráficos
        print("\nCriando gráficos...")
        
        plot_tme_comparison(df)
        plot_variance_analysis(df)
        plot_heatmap(df)
        plot_boxplot_style(df)
        plot_scatter_with_trends(df)
        
        # Criar tabela resumo
        create_summary_table(df)
        
        print("\nTodos os gráficos foram salvos como arquivos PNG!")
        print("Arquivos gerados:")
        print("- tme_comparison.png")
        print("- variance_analysis.png") 
        print("- performance_heatmap.png")
        print("- tme_distribution.png")
        print("- scatter_with_trends.png")
        print("- resumo_estatistico.csv")
        
    except FileNotFoundError:
        print("Erro: Arquivo 'resultados_tme.csv' não encontrado!")
        print("Certifique-se de que o arquivo está no mesmo diretório deste script.")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main() 
