import dlt
import pandas as pd

@dlt.resource(name="clientes")
def clientes():
    df = pd.read_csv("data/raw/clientes.csv")
    yield df.to_dict(orient="records")

@dlt.resource(name="pedidos")
def pedidos():
    df = pd.read_csv("data/raw/pedidos.csv")
    yield df.to_dict(orient="records")

@dlt.resource(name="itens_pedido")
def itens_pedido():
    df = pd.read_csv("data/raw/itens_pedido.csv")
    yield df.to_dict(orient="records")

pipeline = dlt.pipeline(
    pipeline_name="ingestao_dados_simulados",
    destination="filesystem",
    dataset_name="bronze"
)

load_info = pipeline.run([clientes(), pedidos(), itens_pedido()])
print(load_info)