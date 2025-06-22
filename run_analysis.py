import subprocess
import statistics
import os
import sys

# Dicionário com os executáveis
executables = {
    "FIFO": "./main_fifo",
    "SJF": "./main_sjf",
    "LJF": "./main_ljf",
    "PRIO_STATIC": "./main_prio_static",
    "PRIO_DYNAMIC": "./main_prio_dynamic",
    "PRIO_DYNAMIC_QUANTUM": "./main_prio_dynamic_quantum"
}

if len(sys.argv) != 3:
    print("Uso: python3 run_analysis.py [ALG_NAME] [NUM_PROCESSOS]")
    print("Exemplo: python3 run_analysis.py SJF 10")
    sys.exit(1)

alg_name = sys.argv[1].upper()
proc_count = int(sys.argv[2])

if alg_name not in executables:
    print(f"[ERRO] Algoritmo '{alg_name}' não encontrado.")
    print("Algoritmos disponíveis:", ", ".join(executables.keys()))
    sys.exit(1)

exec_path = executables[alg_name]
folder = f"data_{alg_name}"
os.makedirs(folder, exist_ok=True)
output_path = os.path.join(folder, f"tme_{proc_count}.txt")

print(f"\n[INFO] Executando {alg_name} com {proc_count} processos (10 rodadas)...")

tmes = []

for i in range(10):
    try:
        print(f" -> Rodada {i+1}/10...")
        output = subprocess.check_output([exec_path, str(proc_count)], text=True)

        for line in output.splitlines():
            if "TME:" in line:
                tme = float(line.split("TME:")[1].strip())
                tmes.append(tme)
                break

    except Exception as e:
        print(f"[ERRO] Rodada {i+1} falhou: {e}")

# Salva os TME em arquivo
with open(output_path, "w") as f:
    for tme in tmes:
        f.write(f"{tme}\n")

print(f"\n[OK] Resultados salvos em: {output_path}")
