import clickhouse_connect

client = clickhouse_connect.get_client(
    host="localhost",
    port=8123,
    username="siagrow",
    password="siagrow123",
)

version = client.command("SELECT version()")
print("Connected! ClickHouse version:", version)

client.command("CREATE DATABASE IF NOT EXISTS siagrow")
print("Databases:", client.command("SHOW DATABASES"))