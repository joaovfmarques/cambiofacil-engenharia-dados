select
    data_cotacao::date as data_cotacao,
    moeda,
    taxa_compra,
    taxa_venda
from {{ source('bronze', 'cotacao_diaria') }}