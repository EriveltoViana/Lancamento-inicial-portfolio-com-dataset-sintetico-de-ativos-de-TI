# Guia de Tabelas Dinâmicas

Crie estas Tabelas Dinâmicas no Excel desktop a partir das tabelas de `Analise_Gestao_Ativos_TI.xlsx` (**Inserir > Tabela Dinâmica > De Tabela/Intervalo**, escolhendo `tbl_Ativos`, `tbl_Incidentes` ou `tbl_Movimentacoes`). Coloque cada uma em uma aba própria e use os nomes abaixo. Depois de montar, salve prints em `../images/` e linke no README do projeto.

| # | Nome | Fonte | Linhas | Colunas | Valores | Pergunta que responde |
|---|---|---|---|---|---|---|
| 1 | `tdn_Parque_por_Local` | tbl_Ativos | nome_local | estagio_ciclo_vida | Contagem de id_ativo | Onde o parque envelhecido está concentrado? |
| 2 | `tdn_Idade_por_Tipo` | tbl_Ativos | tipo_ativo | status | Média de idade_anos | Quais tipos de ativo são mais antigos? |
| 3 | `tdn_Candidatos_Renovacao` | tbl_Ativos | regiao, nome_local | - | Contagem de id_ativo, Soma de custo_aquisicao_brl | Quantos ativos em Fim de Vida e qual o custo original deles? (filtre estagio_ciclo_vida = Fim de Vida e status <> Baixado) |
| 4 | `tdn_Atividade_do_Pool` | tbl_Movimentacoes | data_movimentacao (agrupar por Meses e Anos) | tipo_movimentacao | Contagem de id_movimentacao | Como a demanda do pool varia ao longo do tempo? (filtre tipo_movimentacao = Retirada do Pool / Devolução ao Pool) |
| 5 | `tdn_Incidentes_por_Modelo` | tbl_Incidentes | modelo | gravidade | Contagem de id_incidente | Quais modelos concentram incidentes? |
| 6 | `tdn_Tempo_de_Resolucao` | tbl_Incidentes | categoria | gravidade | Média de horas_resolucao | Onde a resolução demora mais? |

> As tabelas de incidentes e movimentações só trazem `id_ativo`. Para analisar por modelo ou tipo, use a consulta `Incidentes_Limpo` (que já traz modelo e tipo_ativo) ou crie relacionamentos no Power Pivot (veja abaixo).

## Adicionando interatividade
- **Segmentação de Dados:** Inserir > Segmentação de Dados em `regiao`, `tipo_ativo` e `status`. Conecte a todas as tabelas dinâmicas (Segmentação > Conexões de Relatório).
- **Linha do Tempo:** Inserir > Linha do Tempo em `data_abertura` para as tabelas de incidentes.
- **Gráficos Dinâmicos:** um gráfico por tabela dinâmica; prefira barras, colunas ou linhas e evite pizza com mais de 4 categorias.

## Opcional: Modelo de Dados (Power Pivot)
Quando chegar nos estudos de Power Pivot, carregue `Ativos_Limpo`, `Locais`, `Movimentacoes_Limpo` e `Incidentes_Limpo` no Modelo de Dados e defina:

- `Locais[id_local]` 1 -> * `Ativos_Limpo[id_local]`
- `Ativos_Limpo[id_ativo]` 1 -> * `Movimentacoes_Limpo[id_ativo]`
- `Ativos_Limpo[id_ativo]` 1 -> * `Incidentes_Limpo[id_ativo]`

Medidas DAX iniciais:

```dax
Ativos Ativos := CALCULATE ( COUNTROWS ( Ativos_Limpo ), Ativos_Limpo[status] <> "Baixado" )
Ativos em Fim de Vida := CALCULATE ( [Ativos Ativos], Ativos_Limpo[estagio_ciclo_vida] = "Fim de Vida" )
% Fim de Vida := DIVIDE ( [Ativos em Fim de Vida], [Ativos Ativos] )
Utilizacao do Pool := DIVIDE (
    CALCULATE ( COUNTROWS ( Ativos_Limpo ), Ativos_Limpo[status] = "Pool - Emprestado" ),
    CALCULATE ( COUNTROWS ( Ativos_Limpo ), Ativos_Limpo[pertence_pool] = "S" ) )
Incidentes por 100 Ativos := DIVIDE ( COUNTROWS ( Incidentes_Limpo ), [Ativos Ativos] ) * 100
```

> No Excel em português, dependendo da configuração regional, o separador de argumentos do DAX pode ser o ponto e vírgula (`;`) em vez da vírgula. Se der erro de sintaxe ao colar, troque os separadores.
