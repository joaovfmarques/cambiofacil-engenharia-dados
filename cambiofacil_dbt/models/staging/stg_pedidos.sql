select
    id_pedido,
    id_cliente,
    data_pedido,
    valor_total_brl,
    status,
    endereco_retirada
from {{ source('bronze', 'pedidos') }}