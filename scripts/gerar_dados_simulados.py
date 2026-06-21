from faker import Faker
import pandas as pd
import random
import os

fake = Faker('pt_BR')

NUM_CLIENTES = 500
NUM_PEDIDOS = 3000
MOEDAS = ['USD', 'EUR', 'GBP', 'JPY', 'CHF', 'CAD', 'AUD', 'ARS']
CANAIS_VENDA = ['App', 'Site', 'Agência Parceira']

TAXAS_BASE = {
    'USD': (4.5, 6.5),
    'EUR': (5.0, 7.0),
    'GBP': (6.0, 8.0),
    'JPY': (0.03, 0.05),
    'CHF': (5.5, 7.5),
    'CAD': (3.5, 5.0),
    'AUD': (3.0, 4.5),
    'ARS': (0.005, 0.01)
}

# Gerar Clientes
clientes = []
for i in range(1, NUM_CLIENTES + 1):
    clientes.append({
        'id_cliente': i,
        'nome_completo': fake.name(),
        'cpf': fake.cpf(),
        'email': fake.email(),
        'telefone': fake.phone_number(),
        'data_cadastro': fake.date_between(start_date='-2y', end_date='today')
    })
df_clientes = pd.DataFrame(clientes)

# Gerar Pedidos e Itens do Pedido
pedidos = []
itens = []
item_id = 1

for i in range(1, NUM_PEDIDOS + 1):
    id_cliente = random.randint(1, NUM_CLIENTES)
    data_pedido = fake.date_between(start_date='-1y', end_date='today')
    status = random.choice(['pendente', 'concluido', 'cancelado'])
    endereco = fake.address()
    canal_venda = random.choice(CANAIS_VENDA)

    num_itens = random.randint(1, 3)
    valor_total = 0
    for _ in range(num_itens):
        moeda = random.choice(MOEDAS)
        taxa_min, taxa_max = TAXAS_BASE[moeda]
        quantidade = round(random.uniform(100, 5000), 2)
        taxa = round(random.uniform(taxa_min, taxa_max), 4)
        valor_item = round(quantidade * taxa, 2)
        valor_total += valor_item

        itens.append({
            'id_item': item_id,
            'id_pedido': i,
            'moeda_estrangeira': moeda,
            'quantidade_solicitada': quantidade,
            'taxa_cambio_aplicada': taxa
        })
        item_id += 1

    pedidos.append({
        'id_pedido': i,
        'id_cliente': id_cliente,
        'data_pedido': data_pedido,
        'valor_total_brl': round(valor_total, 2),
        'status': status,
        'endereco_retirada': endereco,
        'canal_venda': canal_venda
    })

df_pedidos = pd.DataFrame(pedidos)
df_itens = pd.DataFrame(itens)

os.makedirs('data/raw', exist_ok=True)
df_clientes.to_csv('data/raw/clientes.csv', index=False)
df_pedidos.to_csv('data/raw/pedidos.csv', index=False)
df_itens.to_csv('data/raw/itens_pedido.csv', index=False)

print(f"Gerados: {len(df_clientes)} clientes, {len(df_pedidos)} pedidos, {len(df_itens)} itens de pedido.")