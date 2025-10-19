from datetime import datetime, timedelta
import pandas as pd
import sqlite3
from pathlib import Path
from urllib.parse import urlparse
from shutil import copy2

# ---------- SETTINGS ----------
USE_REAL_DATA = True  # Set False to use sample CSV
SAMPLE_CSV = "../data/sample_history.csv"
SAMPLE_DB = "../data/sample_history.sqlite"
UPDATED_DB = "../data/updated_history.sqlite"
UPDATED_CSV = "../data/updated_history.csv"
CHROME_HISTORY_COPY = Path("../private_data") / "History_copy.sqlite"




# ---------- LOAD DATA ----------
if USE_REAL_DATA:

    # Copy Chrome History only if backup doesn't already exist
    if not CHROME_HISTORY_COPY.exists():
        DEFAULT_CHROME_PATH = Path.home() / "AppData/Local/Google/Chrome/User Data/Default/History"

        user_input = input(f"Enter Chrome History path or press Enter to use default ({DEFAULT_CHROME_PATH}): ")
        chrome_history_path = Path(user_input) if user_input.strip() else DEFAULT_CHROME_PATH
        copy2(chrome_history_path, CHROME_HISTORY_COPY)
        print("Chrome history copied to private_data")
    else:
        print("✅ Using local real browsing history.")
        print("Backup already exists — using existing copy.")
    db_path = CHROME_HISTORY_COPY



    # Connect and read Chrome history table
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT url, title, last_visit_time FROM urls", conn)
    conn.close()

    # Convert Chrome microsecond timestamps to datetime
    def chrome_ts_to_datetime(x):
        try:
            return datetime(1601, 1, 1) + timedelta(microseconds=int(x))
        except:
            return pd.NaT

    df['last_visit_time'] = df['last_visit_time'].apply(chrome_ts_to_datetime)


else:
    # Load sample CSV and create sample DB
    df = pd.read_csv(SAMPLE_CSV)
    conn = sqlite3.connect(SAMPLE_DB)
    df.to_sql('urls', conn, if_exists='replace', index=False)
    conn.close()
    db_path = SAMPLE_DB
    print("✅ Using sample data for demonstration.")



#  Transform - extract domain and categorize
def categorize(url):
    if "openai" in url:
        return "Work"
    elif "bbc" in url:
        return "News"
    else:
        return "Learning"

df["category"] = df["url"].apply(categorize)



# What time of day browse most
df = df.dropna(subset=['last_visit_time'])
df['last_visit_time'] = pd.to_datetime(df['last_visit_time'], errors='coerce')
df["hour"] = df["last_visit_time"].dt.hour
browsing_by_hour = df.groupby("hour").size().reset_index(name="count")
busiest_hour = browsing_by_hour.sort_values("count", ascending=False).head(1)
print("⏰ Peak browsing hour:\n", busiest_hour)
browsing_by_hour.to_csv("../data/summary_browsing_by_hour.csv", index=False)

# Which websites dominate your daily activity
df["domain"] = df["url"].apply(lambda x: urlparse(x).netloc.replace("www.", ""))
domain_stats = df.groupby("domain").size().reset_index(name="visits")
top_domains = domain_stats.sort_values("visits", ascending=False).head(10)
print('🌐 Top websites visited:\n', top_domains)
domain_stats.to_csv("../data/summary_domains.csv", index=False)

# Load - save into a new database
conn = sqlite3.connect("../data/updated_history.sqlite")
df.to_sql("updated_history", conn, if_exists="replace", index=False)
df.to_csv("../data/updated_history.csv", index=False)

print(df)
conn.close()

print("Data successfully loaded into database!")