import pandas as pd
import requests
import shutil
from pathlib import Path

CSV_URL = "https://www.unconsentingmedia.org/list.csv"
DATA_DIR = Path("data")
CACHE_PATH = DATA_DIR/("list.csv")

def fetch_and_cache_csv():
	if DATA_DIR.exists():
		shutil.rmtree(DATA_DIR)

	DATA_DIR.mkdir(parents=True, exist_ok=True)


	response = requests.get(CSV_URL)
	response.raise_for_status()
	
	with open(CACHE_PATH, "wb") as f:
		f.write(response.content)
		
	print("Data fetched successfully. New CSV downloaded and saved.")

def load_csv():
	if not CACHE_PATH.exists():
		fetch_and_cache_csv()
	return pd.read_csv(CACHE_PATH)