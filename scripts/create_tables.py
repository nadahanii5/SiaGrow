import clickhouse_connect

client = clickhouse_connect.get_client(
    host="localhost", port=8123, username="siagrow", password="siagrow123"
)

client.command("CREATE DATABASE IF NOT EXISTS siagrow")

sql = open("sql/create_tables.sql", encoding="utf-8").read()

for statement in sql.split(";"):
    if statement.strip():
        client.command(statement)

print("Tables:", client.command("SHOW TABLES FROM siagrow"))