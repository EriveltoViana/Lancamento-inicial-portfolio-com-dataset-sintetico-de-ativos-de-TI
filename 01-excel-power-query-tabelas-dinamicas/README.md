# Projeto 1: Análise de Ativos de TI com Excel, Power Query e Tabelas Dinâmicas

Análise ponta a ponta de um parque simulado de **5.000 ativos de informática** (físicos e virtuais) distribuídos em 12 unidades: de CSVs brutos e sujos a um modelo de dados limpo, indicadores e Tabelas Dinâmicas.

> Todos os dados são **sintéticos**. Veja o [`dicionário de dados`](../docs/dicionario-de-dados.md).

## Perguntas de negócio

1. Qual a idade do parque e que parcela dele está em **fim de vida** ou fora da garantia?
2. Onde o parque envelhecido está concentrado (local, região, tipo de ativo)?
3. Quão bem o **pool de máquinas** (físicas e virtuais) está sendo utilizado?
4. Quais modelos de equipamento concentram **incidentes** e quanto tempo leva a resolução?
5. Quantos ativos são candidatos à renovação e qual o custo original de aquisição deles?

## O que há nesta pasta

| Arquivo | Finalidade |
|---|---|
| `Analise_Gestao_Ativos_TI.xlsx` | Planilha com os dados limpos em Tabelas do Excel, colunas derivadas e uma aba `Indicadores` baseada em fórmulas |
| `power-query/*.m` | Scripts Power Query (M) que reproduzem a limpeza a partir dos CSVs brutos |
| `docs/guia-tabelas-dinamicas.md` | Seis Tabelas Dinâmicas para montar, com campos, filtros e a pergunta que cada uma responde; Modelo de Dados e DAX opcionais |
| `images/` | Prints das Tabelas Dinâmicas e gráficos (adicione os seus aqui) |

## Abordagem

**1. Limpar (Power Query).** O `ativos.csv` bruto tem problemas de qualidade propositais: status com caixa inconsistente, espaços sobrando, departamentos em branco e 25 linhas duplicadas. Os scripts M removem espaços, padronizam o status, preenchem vazios com `Não atribuído`, removem duplicatas por `id_ativo`, definem os tipos de dados e trazem o nome do local.

**2. Enriquecer.** Colunas derivadas: `idade_anos`, `estagio_ciclo_vida` (Atual < 3 anos, Envelhecendo de 3 a 5, Fim de Vida a partir de 5, Virtual) e `status_garantia`. Os limites são premissas e podem ser alterados nas células amarelas da aba `Indicadores`.

**3. Medir.** A aba `Indicadores` calcula os indicadores principais e os detalhamentos por local, tipo de ativo e estágio do ciclo de vida usando fórmulas (`COUNTIFS`, `AVERAGEIFS`, `EDATE`), então tudo se atualiza quando as entradas mudam.

**4. Explorar.** Tabelas Dinâmicas com segmentações de dados e linha do tempo respondem às perguntas de negócio acima.

## Resultados (dados sintéticos, data de referência 18/10/2026)

| Indicador | Valor |
|---|---|
| Ativos ativos (exceto Baixados) | 4.601 de 5.000 |
| Idade média dos ativos físicos ativos | 4,0 anos |
| Ativos físicos ativos em Fim de Vida | 30,6% |
| Ativos físicos ativos fora da garantia | 59,9% |
| Utilização do pool (emprestados / total de 508) | 44,3% |
| Incidentes nos últimos 12 meses | 5.771 (125 por 100 ativos ativos) |
| Tempo médio de resolução | 14,5 horas |

Na janela de 2 anos de incidentes, três modelos se destacam pela taxa de incidentes por 100 ativos ativos: ProBook 450 G8 (424), OptiPlex 7010 (302) e Latitude 5420 (224), contra cerca de 150 na maioria dos demais. Os dados foram gerados com esses padrões de propósito; o objetivo do projeto é o método, não os números.

## Como reproduzir no Excel

1. No Excel, vá em **Dados > Obter Dados > De Outras Fontes > Consulta em Branco** e cole cada arquivo `.m` de `power-query/` (Editor Avançado), em ordem numérica. Dê a cada consulta o nome do arquivo (`PastaDados`, `DataReferencia`, `Locais`, `Ativos_Limpo`, ...).
2. Ajuste o parâmetro `PastaDados` para o caminho local de `data/raw/` (terminando com `\`).
3. Use **Fechar e Carregar** em cada consulta limpa, para uma tabela ou para o Modelo de Dados.
4. Siga o [`guia-tabelas-dinamicas.md`](docs/guia-tabelas-dinamicas.md) para montar as Tabelas Dinâmicas.

## Premissas e limitações

- Os limites de ciclo de vida (3 e 5 anos) são convenções comuns de renovação, não regras universais.
- Máquinas virtuais não têm data de compra, então ficam fora das métricas de idade, garantia e fim de vida.
- A taxa de incidentes compara 12 meses de incidentes com o tamanho atual do parque ativo, uma simplificação.
- A planilha já acompanha os dados limpos; os scripts Power Query reproduzem o mesmo resultado a partir dos arquivos brutos.

## Próximos passos

- [ ] Adicionar prints das Tabelas Dinâmicas e segmentações em `images/`
- [ ] Carregar o modelo no Power Pivot e criar as medidas DAX
- [ ] Repetir a análise em SQL (Projeto 2) e comparar as abordagens
