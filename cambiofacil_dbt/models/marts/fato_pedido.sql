select
    ip.id_item,
    p.id_pedido,
    p.id_cliente,
    p.data_pedido as data,
    ip.moeda_estrangeira as moeda,
    ip.quantidade_solicitada,
    ip.taxa_cambio_aplicada,
    p.valor_total_brl,
    p.status
from {{ ref('stg_pedidos') }} p
join {{ ref('stg_itens_pedido') }} ip
    on p.id_pedido = ip.id_pedido