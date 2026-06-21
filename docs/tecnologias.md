# Tecnologias — Como será feito

Para cada etapa do ciclo de vida de engenharia de dados, foi escolhida uma tecnologia gratuita e open-source, validada nos laboratórios da disciplina e compatível com hardware modesto (sem necessidade de GPU dedicada).

---

## Ingestão — dlt

**O que é:** um framework Python leve para ingestão de dados, com inferência automática de schema e cargas idempotentes (evita duplicar dados em reprocessamentos).

**Por que foi escolhido:** é a ferramenta utilizada no laboratório da disciplina, é gratuita, não exige infraestrutura própria (roda como um script Python comum) e se encaixa perfeitamente nas duas fontes deste projeto: a API REST do PTAX e os arquivos CSV simulados de clientes/pedidos. Não há necessidade de uma ferramenta mais robusta (como Airbyte ou Fivetran), já que o volume e a complexidade das fontes são baixos.

**Como se integra:** o `dlt` lê os dados das fontes (API e CSV) e grava os dados brutos diretamente na camada Bronze, no MinIO, já adicionando metadados de carga (data, origem, ID do processo) que sustentam a rastreabilidade (linhagem) dos dados.

---

## Armazenamento — MinIO + PostgreSQL

**O que é:** MinIO é um armazenamento de objetos compatível com a API do S3, usado como Data Lake local. PostgreSQL é um banco de dados relacional.

**Por que foi escolhido:** essa combinação foi validada no Laboratório de Armazenamento da disciplina, é totalmente gratuita e self-hosted via Docker, e não exige nenhum serviço de nuvem pago. O MinIO simula, em ambiente local, o comportamento de um Data Lake real (como S3, GCS ou Azure Blob), enquanto o PostgreSQL oferece a robustez relacional necessária para consultas analíticas nas camadas Silver e Gold.

**Como se integra:** a camada Bronze (dados brutos) é armazenada no MinIO; as camadas Silver e Gold (dados já tratados e modelados) são armazenadas no PostgreSQL, de onde são consumidas pelas ferramentas de transformação e consumo.

---

## Processamento e Transformação — dbt

**O que é:** uma ferramenta de transformação baseada em SQL declarativo e versionado, com testes automatizados embutidos.

**Por que foi escolhido:** para o volume e a complexidade deste projeto, escrever as transformações em SQL via `dbt` é muito mais simples e rápido de manter do que usar um motor de processamento distribuído como Spark — que seria um exagero de complexidade (e de exigência de hardware) para este cenário. O `dbt` também gera automaticamente a documentação e a linhagem das transformações, o que reforça a governança do projeto.

**Como se integra:** o `dbt` lê os dados brutos da camada Bronze (MinIO), aplica as transformações de limpeza e padronização para gerar a camada Silver (PostgreSQL), e em seguida aplica as agregações e a modelagem em star schema para gerar a camada Gold (PostgreSQL).

---

## Orquestração — Dagster

**O que é:** uma ferramenta de orquestração de pipelines de dados, com interface visual de monitoramento.

**Por que foi escolhido:** o `Dagster` foi a ferramenta de orquestração ensinada e validada no laboratório da disciplina. Além de agendar e encadear as etapas do pipeline (ingestão → transformação), ele fornece observabilidade nativa — logs, status de execução e falhas visíveis em uma interface única — o que atende diretamente ao requisito de **monitoramento** do ciclo de vida, sem necessidade de nenhuma ferramenta adicional.

**Como se integra:** o `Dagster` orquestra, em sequência diária, a execução do `dlt` (ingestão), do `dbt` (transformação) e dos checks do `Soda Core` (qualidade), garantindo que cada etapa só seja executada após o sucesso da anterior.

---

## Consumo / Serving — Metabase

**O que é:** uma ferramenta open-source de criação de dashboards, sem necessidade de escrever código.

**Por que foi escolhido:** é gratuito, self-hosted via Docker, e permite que o time financeiro da fintech visualize os dados da camada Gold (volume de pedidos, cotação aplicada, faturamento) sem depender de uma equipe técnica para gerar relatórios. Alternativas como Power BI exigiriam licenciamento pago; o Metabase atende plenamente à necessidade de consumo deste projeto sem custo algum.

**Como se integra:** o Metabase se conecta diretamente ao PostgreSQL, consultando as tabelas da camada Gold para montar os dashboards.

---

## Correntes do Ciclo de Vida: Segurança, Governança, Qualidade e Monitoramento

Essas quatro correntes não pertencem a uma etapa isolada — atuam transversalmente sobre toda a arquitetura.

### Segurança (LGPD)
Implementada diretamente no PostgreSQL, utilizando **ROLES e GRANT** para controlar quem pode acessar quais tabelas, **Row-Level Security (RLS)** para restringir o acesso a linhas específicas quando necessário, e uma **view de mascaramento** sobre o CPF dos clientes, exibindo apenas parte do número para usuários sem permissão de acesso total — atendendo à exigência de proteção de dados pessoais da LGPD.

### Governança
Implementada utilizando os recursos nativos do próprio PostgreSQL: comandos `COMMENT ON` para documentar o significado de cada tabela e coluna, e consultas ao `information_schema` para funcionar como um catálogo de dados simples e gratuito — sem necessidade de uma ferramenta de catalogação externa.

### Qualidade de Dados
Implementada com o **Soda Core**, que executa verificações declarativas (checks) sobre os dados — por exemplo, validando que não existem CPFs duplicados ou valores de pedido negativos — antes que os dados avancem para a camada Gold.

### Monitoramento e Alertas
Implementado com a combinação de duas ferramentas já presentes no projeto: a **interface do Dagster**, que exibe o status de cada execução do pipeline (sucesso, falha, duração), e os resultados dos checks do **Soda Core**, que são gravados em uma tabela dedicada no PostgreSQL (`monitoramento.alertas_qualidade`). Essa combinação garante observabilidade, logging e alerta de falhas sem exigir nenhuma ferramenta paga ou serviço de notificação externo (como Slack ou e-mail).
