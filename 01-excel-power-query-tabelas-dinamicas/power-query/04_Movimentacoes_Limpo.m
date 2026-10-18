// Consulta: Movimentacoes_Limpo
let
    Origem     = Csv.Document(File.Contents(PastaDados & "movimentacoes.csv"),
                    [Delimiter = ",", Columns = 7, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cabecalhos = Table.PromoteHeaders(Origem, [PromoteAllScalars = true]),
    Tipado     = Table.TransformColumnTypes(Cabecalhos, {
                    {"id_movimentacao", type text}, {"id_ativo", type text}, {"tipo_movimentacao", type text},
                    {"data_movimentacao", type date}, {"id_local_origem", type text},
                    {"id_local_destino", type text}, {"departamento_solicitante", type text}}, "en-US"),
    // Colunas de agrupamento úteis para as tabelas dinâmicas
    ComMes = Table.AddColumn(Tipado, "mes", each Date.StartOfMonth([data_movimentacao]), type date),
    ComAno = Table.AddColumn(ComMes, "ano", each Date.Year([data_movimentacao]), Int64.Type)
in
    ComAno
