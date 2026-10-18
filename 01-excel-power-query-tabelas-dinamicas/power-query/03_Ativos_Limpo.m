// Consulta: Ativos_Limpo
// Limpa o arquivo bruto de ativos e cria os campos de ciclo de vida.
// Depende de: PastaDados, DataReferencia, Locais
let
    Origem     = Csv.Document(File.Contents(PastaDados & "ativos.csv"),
                    [Delimiter = ",", Columns = 11, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cabecalhos = Table.PromoteHeaders(Origem, [PromoteAllScalars = true]),

    // 1. Tipos de dados. A cultura "en-US" é proposital: os CSVs usam datas ISO (aaaa-mm-dd)
    //    e ponto decimal, então isso evita erros com a configuração regional pt-BR.
    Tipado = Table.TransformColumnTypes(Cabecalhos, {
                {"id_ativo", type text}, {"tipo_ativo", type text}, {"fabricante", type text},
                {"modelo", type text}, {"data_compra", type date}, {"fim_garantia", type date},
                {"status", type text}, {"id_local", type text}, {"departamento", type text},
                {"pertence_pool", type text}, {"custo_aquisicao_brl", type number}}, "en-US"),

    // 2. Remove espaços extras das colunas de texto
    Aparado = Table.TransformColumns(Tipado, {
                {"id_ativo", Text.Trim, type text}, {"tipo_ativo", Text.Trim, type text},
                {"fabricante", Text.Trim, type text}, {"modelo", Text.Trim, type text},
                {"id_local", Text.Trim, type text}, {"pertence_pool", Text.Trim, type text}}),

    // 3. Padroniza o status: "pool - disponível " -> "Pool - Disponível"
    Status = Table.TransformColumns(Aparado,
                {{"status", each Text.Proper(Text.Trim(_)), type text}}),

    // 4. Departamentos em branco viram "Não atribuído"
    Departamento = Table.TransformColumns(Status,
                {{"departamento", each if _ = null or Text.Trim(_) = "" then "Não atribuído" else Text.Trim(_), type text}}),

    // 5. Remove ativos duplicados (mesmo id_ativo)
    SemDuplicados = Table.Distinct(Departamento, {"id_ativo"}),

    // 6. Colunas derivadas
    Idade = Table.AddColumn(SemDuplicados, "idade_anos",
                each if [data_compra] = null then null
                     else Number.Round(Duration.Days(DataReferencia - [data_compra]) / 365.25, 1),
                type number),
    Estagio = Table.AddColumn(Idade, "estagio_ciclo_vida",
                each if [idade_anos] = null then "Virtual"
                     else if [idade_anos] >= 5 then "Fim de Vida"
                     else if [idade_anos] >= 3 then "Envelhecendo"
                     else "Atual",
                type text),
    Garantia = Table.AddColumn(Estagio, "status_garantia",
                each if [fim_garantia] = null then "N/A"
                     else if [fim_garantia] < DataReferencia then "Vencida"
                     else "Vigente",
                type text),

    // 7. Traz o nome do local e a região
    Unido     = Table.NestedJoin(Garantia, {"id_local"}, Locais, {"id_local"}, "loc", JoinKind.LeftOuter),
    Expandido = Table.ExpandTableColumn(Unido, "loc", {"nome_local", "regiao"})
in
    Expandido
