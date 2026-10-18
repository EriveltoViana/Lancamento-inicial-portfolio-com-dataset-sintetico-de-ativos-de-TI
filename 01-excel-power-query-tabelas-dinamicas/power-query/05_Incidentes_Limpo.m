// Consulta: Incidentes_Limpo
// Depende de: PastaDados, Ativos_Limpo
let
    Origem     = Csv.Document(File.Contents(PastaDados & "incidentes.csv"),
                    [Delimiter = ",", Columns = 8, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cabecalhos = Table.PromoteHeaders(Origem, [PromoteAllScalars = true]),
    Tipado     = Table.TransformColumnTypes(Cabecalhos, {
                    {"id_incidente", type text}, {"id_ativo", type text}, {"id_local", type text},
                    {"categoria", type text}, {"gravidade", type text}, {"data_abertura", type date},
                    {"data_resolucao", type date}, {"horas_resolucao", type number}}, "en-US"),
    ComMes     = Table.AddColumn(Tipado, "mes", each Date.StartOfMonth([data_abertura]), type date),
    // Une aos ativos para analisar incidentes por modelo e tipo de ativo
    Unido      = Table.NestedJoin(ComMes, {"id_ativo"}, Ativos_Limpo, {"id_ativo"}, "a", JoinKind.LeftOuter),
    Expandido  = Table.ExpandTableColumn(Unido, "a", {"tipo_ativo", "fabricante", "modelo", "estagio_ciclo_vida"})
in
    Expandido
