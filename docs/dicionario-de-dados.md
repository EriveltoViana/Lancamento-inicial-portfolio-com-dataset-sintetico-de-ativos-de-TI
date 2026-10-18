# Dicionário de dados

> Todos os dados são **sintéticos**, gerados por `scripts/gerar_dados.py` (semente 42). Não vêm de nenhuma organização real e não representam nenhuma organização real.

> **Dica:** os CSVs estão em UTF-8. Para abri-los direto no Excel, use **Dados > De Texto/CSV** e escolha a origem do arquivo "65001: Unicode (UTF-8)", senão os acentos aparecem errados. No Power Query os scripts já tratam isso (`Encoding = 65001`).

## ativos.csv (bruto: 5.025 linhas, incluindo 25 duplicadas)

| Coluna | Tipo | Descrição |
|---|---|---|
| id_ativo | texto | Chave única do ativo (`ATV-00001`) |
| tipo_ativo | texto | Desktop, Notebook, Workstation, Thin Client, Máquina Virtual |
| fabricante, modelo | texto | Fabricante e modelo do equipamento (`Virtual` / `VM-*` para máquinas virtuais) |
| data_compra | data | Em branco para máquinas virtuais |
| fim_garantia | data | 3 anos após a compra (5 para workstations); em branco para VMs |
| status | texto | Em Uso, Em Estoque, Em Manutenção, Baixado, Pool - Disponível, Pool - Emprestado |
| id_local | texto | Chave estrangeira para locais |
| departamento | texto | Departamento responsável ou de destino (alguns em branco no dado bruto) |
| pertence_pool | S/N | O ativo faz parte do pool compartilhado de máquinas |
| custo_aquisicao_brl | número | Custo de aquisição em reais (0 para VMs) |

**Problemas de qualidade propositais no arquivo bruto** (para corrigir no Power Query): status com caixa mista e espaços no final, cerca de 2% de departamentos em branco, 25 linhas duplicadas.

## locais.csv
`id_local`, `nome_local`, `regiao` (12 unidades simuladas).

## movimentacoes.csv (12.000 linhas)
`id_movimentacao`, `id_ativo`, `tipo_movimentacao` (Despacho, Devolução, Transferência, Retirada do Pool, Devolução ao Pool), `data_movimentacao`, `id_local_origem`, `id_local_destino`, `departamento_solicitante`.

## incidentes.csv (9.000 linhas)
`id_incidente`, `id_ativo`, `id_local`, `categoria` (Hardware, Software, Rede, Acesso, Desempenho), `gravidade` (Baixa, Média, Alta, Crítica), `data_abertura`, `data_resolucao`, `horas_resolucao`.

Alguns modelos receberam peso maior de falha de propósito, para que a análise de incidentes tenha padrões reais a encontrar.

## Campos derivados (criados no Power Query e na planilha)

| Campo | Regra |
|---|---|
| idade_anos | (data de referência - data_compra) / 365,25, arredondada a 1 casa decimal |
| estagio_ciclo_vida | `Atual` < 3 anos, `Envelhecendo` de 3 a menos de 5 anos, `Fim de Vida` >= 5 anos, `Virtual` se não houver data de compra |
| status_garantia | `Vencida` se fim_garantia < data de referência, `Vigente` caso contrário, `N/A` para VMs |

Os limites (3 e 5 anos) são **premissas**, editáveis nas células amarelas da aba `Indicadores`.
