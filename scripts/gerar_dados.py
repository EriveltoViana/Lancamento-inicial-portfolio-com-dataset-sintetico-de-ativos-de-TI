"""Gera um conjunto de dados SINTÉTICO de gestão de ativos de TI (CSVs brutos, com sujeira proposital).

Todos os dados são simulados. Não vêm de nenhuma organização real e não
representam nenhuma organização real. Com a mesma semente, os arquivos
gerados são idênticos.
"""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

SEMENTE = 42
N_ATIVOS = 5000
N_VMS = 200
N_MOVIMENTACOES = 12000
N_INCIDENTES = 9000
HOJE = date(2026, 10, 18)

random.seed(SEMENTE)
SAIDA = Path(__file__).resolve().parent.parent / "data" / "raw"
SAIDA.mkdir(parents=True, exist_ok=True)

LOCAIS = [
    ("LOC-01", "Sede - Brasília", "Centro-Oeste", 0.20),
    ("LOC-02", "Regional - São Paulo", "Sudeste", 0.17),
    ("LOC-03", "Regional - Rio de Janeiro", "Sudeste", 0.12),
    ("LOC-04", "Regional - Belo Horizonte", "Sudeste", 0.07),
    ("LOC-05", "Regional - Porto Alegre", "Sul", 0.07),
    ("LOC-06", "Regional - Curitiba", "Sul", 0.06),
    ("LOC-07", "Regional - Salvador", "Nordeste", 0.07),
    ("LOC-08", "Regional - Recife", "Nordeste", 0.06),
    ("LOC-09", "Regional - Fortaleza", "Nordeste", 0.05),
    ("LOC-10", "Regional - Belém", "Norte", 0.05),
    ("LOC-11", "Regional - Manaus", "Norte", 0.04),
    ("LOC-12", "Regional - Goiânia", "Centro-Oeste", 0.04),
]
DEPARTAMENTOS = ["Finanças", "RH", "Jurídico", "TI", "Operações", "Auditoria",
                 "Comunicação", "Riscos", "Compras", "Administração"]
MODELOS = {
    "Desktop": [("Dell", "OptiPlex 7010"), ("Dell", "OptiPlex 7090"),
                ("HP", "EliteDesk 800 G6"), ("Lenovo", "ThinkCentre M70q")],
    "Notebook": [("Dell", "Latitude 5420"), ("Dell", "Latitude 5440"),
                 ("HP", "ProBook 450 G8"), ("Lenovo", "ThinkPad T14")],
    "Workstation": [("Dell", "Precision 3660"), ("HP", "Z2 G9")],
    "Thin Client": [("HP", "t640"), ("Dell", "Wyse 5070")],
}
CUSTO = {"Desktop": (4500, 6500), "Notebook": (7000, 11000),
         "Workstation": (14000, 22000), "Thin Client": (2000, 3000)}
# alguns modelos falham mais, para a análise de incidentes ter o que encontrar
PESO_FALHA = {"ProBook 450 G8": 3.0, "OptiPlex 7010": 2.0, "Latitude 5420": 1.5}

MOV_POOL = ("Retirada do Pool", "Devolução ao Pool")


def data_aleatoria(inicio, fim, moda=0.8):
    a, b = inicio.toordinal(), fim.toordinal()
    return date.fromordinal(int(random.triangular(a, b, a + (b - a) * moda)))


ids_local = [l[0] for l in LOCAIS]
pesos_local = [l[3] for l in LOCAIS]

# ---- ativos (registros limpos primeiro; a sujeira é adicionada na escrita) ----
ativos = []
n_fisicos = N_ATIVOS - N_VMS
tipos = random.choices(["Desktop", "Notebook", "Workstation", "Thin Client"],
                       weights=[0.45, 0.38, 0.10, 0.07], k=n_fisicos)
for i, t in enumerate(tipos, start=1):
    fabricante, modelo = random.choice(MODELOS[t])
    data_compra = data_aleatoria(date(2017, 1, 1), date(2026, 6, 30))
    anos_garantia = 5 if t == "Workstation" else 3
    fim_garantia = data_compra + timedelta(days=365 * anos_garantia)
    idade = (HOJE - data_compra).days / 365.25
    no_pool = random.random() < 0.06
    if no_pool:
        status = random.choices(["Pool - Disponível", "Pool - Emprestado"], [0.55, 0.45])[0]
    elif idade >= 8 and random.random() < 0.6:
        status = "Baixado"
    else:
        status = random.choices(["Em Uso", "Em Estoque", "Em Manutenção", "Baixado"],
                                [0.78, 0.12, 0.04, 0.06])[0]
    lo, hi = CUSTO[t]
    ativos.append(dict(
        id_ativo=f"ATV-{i:05d}", tipo_ativo=t, fabricante=fabricante, modelo=modelo,
        data_compra=data_compra, fim_garantia=fim_garantia, status=status,
        id_local=random.choices(ids_local, pesos_local)[0],
        departamento=random.choice(DEPARTAMENTOS),
        pertence_pool="S" if no_pool else "N",
        custo_aquisicao_brl=round(random.uniform(lo, hi), 2)))
for j in range(1, N_VMS + 1):
    ativos.append(dict(
        id_ativo=f"ATV-{n_fisicos + j:05d}", tipo_ativo="Máquina Virtual",
        fabricante="Virtual", modelo=random.choice(["VM-Padrão", "VM-Desempenho"]),
        data_compra=None, fim_garantia=None,
        status=random.choices(["Pool - Disponível", "Pool - Emprestado"], [0.5, 0.5])[0],
        id_local="LOC-01", departamento="TI", pertence_pool="S", custo_aquisicao_brl=0))

# ---- escreve ativos brutos com sujeira proposital e realista ----
campos = ["id_ativo", "tipo_ativo", "fabricante", "modelo", "data_compra",
          "fim_garantia", "status", "id_local", "departamento", "pertence_pool",
          "custo_aquisicao_brl"]
linhas = []
for a in ativos:
    r = dict(a)
    r["data_compra"] = a["data_compra"].isoformat() if a["data_compra"] else ""
    r["fim_garantia"] = a["fim_garantia"].isoformat() if a["fim_garantia"] else ""
    x = random.random()
    if x < 0.03:
        r["status"] = r["status"].lower()
    elif x < 0.05:
        r["status"] = r["status"] + " "
    if random.random() < 0.02:
        r["departamento"] = ""
    linhas.append(r)
linhas += random.sample(linhas, 25)          # linhas duplicadas
random.shuffle(linhas)
with open(SAIDA / "ativos.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=campos)
    w.writeheader()
    w.writerows(linhas)

# ---- locais ----
with open(SAIDA / "locais.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id_local", "nome_local", "regiao"])
    for l in LOCAIS:
        w.writerow(l[:3])

# ---- movimentações ----
ativos_pool = [a for a in ativos if a["pertence_pool"] == "S"]
tipos_mov = ["Despacho", "Devolução", "Transferência", "Retirada do Pool", "Devolução ao Pool"]
pesos_mov = [0.28, 0.20, 0.17, 0.20, 0.15]
with open(SAIDA / "movimentacoes.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id_movimentacao", "id_ativo", "tipo_movimentacao", "data_movimentacao",
                "id_local_origem", "id_local_destino", "departamento_solicitante"])
    for k in range(1, N_MOVIMENTACOES + 1):
        tm = random.choices(tipos_mov, pesos_mov)[0]
        a = random.choice(ativos_pool if tm in MOV_POOL else ativos)
        if tm in ("Despacho", "Retirada do Pool"):
            origem, destino = "LOC-01", a["id_local"]
        elif tm in ("Devolução", "Devolução ao Pool"):
            origem, destino = a["id_local"], "LOC-01"
        else:
            origem, destino = random.sample(ids_local, 2)
        d = data_aleatoria(date(2024, 1, 1), date(2026, 10, 15), moda=0.5)
        w.writerow([f"MOV-{k:06d}", a["id_ativo"], tm, d.isoformat(), origem, destino,
                    random.choice(DEPARTAMENTOS)])

# ---- incidentes ----
ativos_ativos = [a for a in ativos if a["status"] != "Baixado"]
pesos = [PESO_FALHA.get(a["modelo"], 1.0) for a in ativos_ativos]
params_grav = {"Baixa": (2.8, 0.6), "Média": (2.4, 0.6), "Alta": (1.8, 0.5), "Crítica": (1.0, 0.5)}
with open(SAIDA / "incidentes.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id_incidente", "id_ativo", "id_local", "categoria", "gravidade",
                "data_abertura", "data_resolucao", "horas_resolucao"])
    for k in range(1, N_INCIDENTES + 1):
        a = random.choices(ativos_ativos, pesos)[0]
        grav = random.choices(list(params_grav), [0.45, 0.35, 0.15, 0.05])[0]
        horas = round(random.lognormvariate(*params_grav[grav]), 1)
        abertura = data_aleatoria(date(2024, 10, 19), HOJE, moda=0.7)
        resolucao = abertura + timedelta(days=int(horas // 24))
        cat = random.choices(["Hardware", "Software", "Rede", "Acesso", "Desempenho"],
                             [0.25, 0.30, 0.15, 0.18, 0.12])[0]
        w.writerow([f"INC-{k:06d}", a["id_ativo"], a["id_local"], cat, grav,
                    abertura.isoformat(), resolucao.isoformat(), horas])

print("CSVs sintéticos gravados em", SAIDA)
