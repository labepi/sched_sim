import subprocess
import os
import sys
from datetime import datetime

# ---------- USO ----------
# python3 run_analysis.py <ALG_NAME> <NUM_PROC> <ITERACAO>
# Exemplo: python3 run_analysis.py SJF 10 1
# -------------------------

executables = {
    "FIFO": "./main_fifo",
    "SJF": "./main_sjf",
    "LJF": "./main_ljf",
    "PRIO_STATIC": "./main_prio_static",
    "PRIO_DYNAMIC": "./main_prio_dynamic",
    "PRIO_DYNAMIC_QUANTUM": "./main_prio_dynamic_quantum"
}

# Verifica argumentos
if len(sys.argv) != 4:
    print("Uso: python3 run_analysis.py <ALG_NAME> <NUM_PROC> <ITERACAO>")
    sys.exit(1)

alg_name = sys.argv[1].upper()
try:
    nproc = int(sys.argv[2])
    iter_num = int(sys.argv[3])
except ValueError:
    print("[Erro] Número de processos e iteração devem ser inteiros.")
    sys.exit(1)

if alg_name not in executables:
    print(f"[Erro] Algoritmo '{alg_name}' não reconhecido.")
    sys.exit(1)

exec_path = executables[alg_name]
output_folder = f"data_{alg_name}"
filename = os.path.join(output_folder, f"tme_{nproc}_{iter_num}.txt")

os.makedirs(output_folder, exist_ok=True)

print(f"\n🚀 Executando {alg_name} com {nproc} processos (iter {iter_num})...")

try:
    result = subprocess.check_output([exec_path, str(nproc)], text=True)

    tme_found = False
    with open(filename, "w") as f:
        f.write(f"# Algoritmo: {alg_name}\n")
        f.write(f"# Num. processos: {nproc}\n")
        f.write(f"# Iteração: {iter_num}\n")
        f.write(f"# Timestamp: {datetime.now()}\n\n")

        for line in result.splitlines():
            f.write(line + "\n")
            if "TME:" in line:
                tme = float(line.split("TME:")[1].strip())
                tme_found = True

        if not tme_found:
            print("⚠️  [Aviso] TME não encontrado na saída!")
        else:
            print(f"✅ TME salvo em {filename}")

except subprocess.CalledProcessError as e:
    print(f"[Erro] Falha na execução: {e}")
