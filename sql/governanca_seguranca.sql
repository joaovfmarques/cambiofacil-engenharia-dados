-- Mascaramento de CPF: view que expõe apenas os 2 últimos dígitos do CPF
CREATE OR REPLACE VIEW gold.dim_cliente_mascarado AS
SELECT
    id_cliente,
    nome_completo,
    'XXX.XXX.XXX-' || RIGHT(cpf, 2) AS cpf_mascarado,
    email,
    telefone,
    data_cadastro
FROM gold.dim_cliente;

-- Papel (role) de leitura restrita, sem acesso ao CPF completo
CREATE ROLE leitor_mascarado LOGIN PASSWORD 'leitor123';

-- Revoga qualquer acesso direto à tabela com CPF completo
REVOKE ALL ON gold.dim_cliente FROM leitor_mascarado;

-- Concede acesso apenas à view mascarada e às demais tabelas não sensíveis
GRANT CONNECT ON DATABASE cambiofacil_db TO leitor_mascarado;
GRANT USAGE ON SCHEMA gold TO leitor_mascarado;
GRANT SELECT ON gold.dim_cliente_mascarado TO leitor_mascarado;
GRANT SELECT ON gold.dim_data TO leitor_mascarado;
GRANT SELECT ON gold.dim_moeda TO leitor_mascarado;
GRANT SELECT ON gold.fato_pedido TO leitor_mascarado;

-- Documentação de catálogo (governança)
COMMENT ON TABLE gold.fato_pedido IS 'Tabela fato: registra cada item de pedido de câmbio, com valores e taxas aplicadas.';
COMMENT ON TABLE gold.dim_cliente IS 'Dimensão de clientes da plataforma CambioFácil. Contém dado pessoal sensível (CPF) — acesso irrestrito deve ser limitado.';
COMMENT ON COLUMN gold.dim_cliente.cpf IS 'Dado pessoal sensível (LGPD). Usuários sem permissão plena devem consultar gold.dim_cliente_mascarado.';
COMMENT ON TABLE gold.dim_data IS 'Dimensão de datas dos pedidos.';
COMMENT ON TABLE gold.dim_moeda IS 'Dimensão de moedas estrangeiras negociadas.';