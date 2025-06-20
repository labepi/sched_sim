import subprocess
import statistics
import os

# Algoritmos disponíveis e seus executáveis
executables = {
    "FIFO": "./main_fifo",
    "SJF": "./main_sjf",
    "LJF": "./main_ljf",
    "PRIO_STATIC": "./main_prio_static",
    "PRIO_DYNAMIC": "./main_prio_dynamic"
}


proc_counts = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
runs_per_setting = 10


# Resultados {algoritmo: {proc_count: [tmes]}}
results = {alg: {} for alg in executables}

print("Iniciando simulações...\n")

for alg_name, exec_path in executables.items():
    print(f"Executando algoritmo: {alg_name}")
    for count in proc_counts:
        tmes = []
        for i in range(runs_per_setting):
            try:
                # Executa o simulador com o número de processos
                output = subprocess.check_output([exec_path, str(count)], text=True)

                # Procura no output o valor do TME
                for line in output.splitlines():
                    if "TME:" in line:
                        tme = float(line.split("TME:")[1].strip())
                        tmes.append(tme)
                        break
            except Exception as e:
                print(f"[Erro] Falha na execução de {alg_name} com {count} processos na rodada {i+1}: {e}")

        results[alg_name][count] = tmes

# Cálculo estatístico
print("\nCalculando estatísticas...")
stats_output = "resultados_tme.csv"
with open(stats_output, "w") as f:
    f.write("Algoritmo,Processos,Media,Variancia\n")
    for alg_name, data in results.items():
        for proc_count, samples in data.items():
            if samples:
                media = statistics.mean(samples)
                var = statistics.variance(samples) if len(samples) > 1 else 0
                f.write(f"{alg_name},{proc_count},{media},{var}\n")

print(f"\nEstatísticas salvas em: {stats_output}")
