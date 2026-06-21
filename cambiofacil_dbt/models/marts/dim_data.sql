select distinct
    data_pedido as data
from {{ ref('stg_pedidos') }}