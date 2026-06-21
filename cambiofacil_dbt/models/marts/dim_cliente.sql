select
    id_cliente,
    nome_completo,
    cpf,
    email,
    telefone,
    data_cadastro
from {{ ref('stg_clientes') }}