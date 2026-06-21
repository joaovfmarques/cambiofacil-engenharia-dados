# Definição e Classificação dos Dados

## Visão Geral

O projeto **CambioFácil** utiliza duas fontes de dados distintas, ambas processadas em modo **batch (lote)**. Não há nenhuma fonte de streaming neste projeto — a justificativa para essa escolha está detalhada na seção 3 deste documento.

---

## 1. Cotação Cambial Diária (PTAX — Banco Central do Brasil)

| Aspecto | Detalhe |
|---|---|
| **Origem** | API pública do Banco Central do Brasil (PTAX) |
| **Formato** | JSON |
| **Volume estimado** | Muito baixo — poucas linhas por dia (cotação de compra e venda do dólar) |
| **Frequência de atualização** | Diária (1x por dia, após o fechamento PTAX) |
| **Latência esperada** | Tolerante a horas — não há exigência de tempo real |
| **Classificação** | **Dado operacional / batch histórico** |

Essa fonte é externa à empresa, pública e gratuita, e serve como referência de preço para a precificação das operações de câmbio realizadas pelos clientes.

---

## 2. Clientes e Pedidos da Plataforma (dados simulados)

Como o CambioFácil é uma fintech fictícia, sem um sistema de produção real, os dados de clientes e pedidos são **gerados de forma sintética** utilizando a biblioteca Python `Faker`, simulando o comportamento de um sistema transacional real.

| Aspecto | Detalhe |
|---|---|
| **Origem** | Dados sintéticos gerados via Faker (simulando um sistema interno da fintech) |
| **Formato** | CSV / estruturado relacional |
| **Volume estimado** | Baixo — volume compatível com um protótipo educacional |
| **Frequência de atualização** | Diária (carga incremental simulando novos pedidos) |
| **Latência esperada** | Tolerante a horas — não há exigência de tempo real |
| **Classificação** | **Dado operacional / transacional** |

Essa fonte representa os dois principais registros de negócio da fintech:
- **Clientes**: cadastro das pessoas físicas que utilizam a plataforma.
- **Pedidos**: operações de câmbio solicitadas pelos clientes (ver `docs/modelagem-dados.md` para detalhamento completo das entidades e atributos).

---

## 3. Por que não há dados de streaming?

Um dos critérios fundamentais ao desenhar uma arquitetura de dados é avaliar se **existe necessidade real de processamento em tempo real** (conforme discutido na Aula 07 da disciplina). No caso do CambioFácil:

- A cotação PTAX é divulgada **apenas uma vez por dia** pelo Banco Central — não existe "tempo real" possível nessa fonte, pois o próprio dado de origem só é atualizado diariamente.
- Os pedidos dos clientes não exigem processamento imediato (em segundos ou minutos) para que o negócio funcione corretamente — um atraso de algumas horas no processamento não compromete a operação nem a experiência do cliente.

Por esses motivos, **optou-se conscientemente por uma arquitetura 100% batch**, evitando a complexidade adicional (e o custo de implementação e manutenção) de uma arquitetura híbrida como Lambda ou Kappa, que não traria benefício real para este cenário de negócio.
