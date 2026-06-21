select distinct
    canal_venda as canal
from {{ ref('stg_pedidos') }}