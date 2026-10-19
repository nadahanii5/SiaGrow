from pipeline.loader import get_client, load_to_clickhouse
from pipeline.sources.db_source import fetch_from_db, load_state, save_state
from pipeline.sources.email_source import fetch_from_email, mark_processed
from pipeline.transform import standardize

client = get_client()

raw, new_last = fetch_from_db()               
clean = standardize(raw, "database")          
loaded = load_to_clickhouse(client, clean)    

if new_last:
    state = load_state()
    state["db_last_updated_at"] = new_last
    save_state(state)

print(f"[database] fetched {len(raw)}, loaded {loaded}")

raw, files = fetch_from_email()               
clean = standardize(raw, "email")             
loaded = load_to_clickhouse(client, clean)   
mark_processed(files)                         
print(f"[email] fetched {len(raw)}, loaded {loaded}")

print(client.query_df(
    "SELECT source, count() AS orders, sum(total_amount) AS revenue "
    "FROM siagrow.orders_clean GROUP BY source"
))