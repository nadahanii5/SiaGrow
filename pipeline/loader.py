import clickhouse_connect


def get_client():
    return clickhouse_connect.get_client(
        host="localhost", port=8123, username="siagrow", password="siagrow123"
    )


def load_to_clickhouse(client, df):
    if df.empty:
        return 0
    client.insert_df("siagrow.orders", df)
    return len(df)