select
    id_pedido,
    id_cliente,
    data_pedido::date as data_pedido,
    valor_total_brl,
    status,
    endereco_retirada,
    canal_venda
from {{ source('bronze', 'pedidos') }}