select distinct
    moeda_estrangeira as moeda
from {{ ref('stg_itens_pedido') }}