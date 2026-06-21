import dlt
import requests
from datetime import datetime, timedelta

@dlt.resource(name="cotacao_diaria")
def cotacao_diaria():
    data_final = datetime.today()
    data_inicial = data_final - timedelta(days=30)

    url = (
        "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
        "CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)"
        f"?@dataInicial='{data_inicial.strftime('%m-%d-%Y')}'"
        f"&@dataFinalCotacao='{data_final.strftime('%m-%d-%Y')}'"
        "&$format=json"
    )

    response = requests.get(url)
    response.raise_for_status()
    dados = response.json()

    for registro in dados.get("value", []):
        yield {
            "data_cotacao": registro["dataHoraCotacao"],
            "moeda": "USD",
            "taxa_compra": registro["cotacaoCompra"],
            "taxa_venda": registro["cotacaoVenda"]
        }

pipeline = dlt.pipeline(
    pipeline_name="ingestao_cotacao_ptax",
    destination="filesystem",
    dataset_name="bronze"
)

load_info = pipeline.run(cotacao_diaria())
print(load_info)