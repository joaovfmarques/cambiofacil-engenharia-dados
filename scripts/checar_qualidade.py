from soda.scan import Scan
import psycopg2
from datetime import datetime

scan = Scan()
scan.set_data_source_name("cambiofacil")
scan.add_configuration_yaml_file("soda/configuration.yml")
scan.add_sodacl_yaml_file("soda/checks.yml")
scan.execute()

resultados = scan.get_scan_results()

conn = psycopg2.connect(
    host="localhost",
    dbname="cambiofacil_db",
    user="cambiofacil",
    password="cambiofacil123"
)
cur = conn.cursor()

cur.execute("""
    CREATE SCHEMA IF NOT EXISTS monitoramento;
    CREATE TABLE IF NOT EXISTS monitoramento.alertas_qualidade (
        id SERIAL PRIMARY KEY,
        data_execucao TIMESTAMP DEFAULT now(),
        check_name TEXT,
        outcome TEXT
    );
""")

for check in resultados.get("checks", []):
    cur.execute(
        "INSERT INTO monitoramento.alertas_qualidade (check_name, outcome) VALUES (%s, %s)",
        (check.get("name"), check.get("outcome"))
    )

conn.commit()
cur.close()
conn.close()

print("Resultados do scan gravados em monitoramento.alertas_qualidade")
print(scan.get_logs_text())