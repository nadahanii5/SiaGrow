import os
import shutil

import pandas as pd

from pipeline.transform import RENAME

INBOX = "sample_data/email_inbox"          
DONE = "sample_data/email_inbox/processed"  


def read_attachment(path):
    name = path.lower()
    if name.endswith(".csv"):
        return pd.read_csv(path)
    if name.endswith((".xlsx", ".xls")):
        return pd.read_excel(path)
    return None   


def fetch_from_email():
    os.makedirs(DONE, exist_ok=True)
    frames, files = [], []

    for name in sorted(os.listdir(INBOX)):
        path = os.path.join(INBOX, name)
        if not os.path.isfile(path):
            continue
        df = read_attachment(path)
        if df is None:
            continue

        df.columns = [str(c).strip().lower() for c in df.columns]
        df = df.rename(columns=RENAME)

        df["sender"] = "client@example.com"
        frames.append(df)
        files.append(path)
        print(f"  [email] read {name}: {len(df)} rows")

    if not frames:
        return pd.DataFrame(), []
    return pd.concat(frames, ignore_index=True), files


def mark_processed(files):
    for path in files:
        shutil.move(path, os.path.join(DONE, os.path.basename(path)))


if __name__ == "__main__":
    df, files = fetch_from_email()
    print(f"Fetched {len(df)} rows from {len(files)} file(s)")
    print(df.head(10))