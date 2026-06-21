select
    id_cliente,
    nome_completo,
    cpf,
    email,
    telefone,
    data_cadastro::date as data_cadastro
from {{ source('bronze', 'clientes') }}