// Consulta: Locais
let
    Origem     = Csv.Document(File.Contents(PastaDados & "locais.csv"),
                    [Delimiter = ",", Columns = 3, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cabecalhos = Table.PromoteHeaders(Origem, [PromoteAllScalars = true]),
    Tipado     = Table.TransformColumnTypes(Cabecalhos,
                    {{"id_local", type text}, {"nome_local", type text}, {"regiao", type text}})
in
    Tipado
