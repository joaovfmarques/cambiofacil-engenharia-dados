from dagster import op, job, schedule, Definitions, RunRequest
import subprocess

@op
def gerar_dados_simulados():
    subprocess.run(["python3", "scripts/gerar_dados_simulados.py"], check=True)

@op
def ingestao_dados_simulados(start):
    subprocess.run(["python3", "scripts/ingestao_dados_simulados.py"], check=True)

@op
def ingestao_cotacao_ptax(start):
    subprocess.run(["python3", "scripts/ingestao_cotacao_ptax.py"], check=True)

@op
def carregar_bronze_postgres(a, b):
    subprocess.run(["python3", "scripts/carregar_bronze_postgres.py"], check=True)

@op
def transformar_dbt(start):
    subprocess.run(["dbt", "run"], cwd="cambiofacil_dbt", check=True)

@op
def checar_qualidade(start):
    subprocess.run(["python3", "scripts/checar_qualidade.py"], check=True)

@job
def pipeline_cambiofacil():
    gerados = gerar_dados_simulados()
    ing_sim = ingestao_dados_simulados(gerados)
    ing_ptax = ingestao_cotacao_ptax(gerados)
    bronze_pg = carregar_bronze_postgres(ing_sim, ing_ptax)
    transformado = transformar_dbt(bronze_pg)
    checar_qualidade(transformado)

@schedule(cron_schedule="0 6 * * *", job=pipeline_cambiofacil)
def pipeline_diario(context):
    return RunRequest()

defs = Definitions(
    jobs=[pipeline_cambiofacil],
    schedules=[pipeline_diario]
)