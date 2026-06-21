select
    id_item,
    id_pedido,
    moeda_estrangeira,
    quantidade_solicitada,
    taxa_cambio_aplicada
from {{ source('bronze', 'itens_pedido') }}