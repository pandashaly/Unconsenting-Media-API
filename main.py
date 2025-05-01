from fastapi import FastAPI, Query
import requests
import csv
from io import StringIO
from typing import List
from csv_handler import load_csv
from json_view import json_formatter
import difflib
from ratings import UM_ratings

app = FastAPI()

def root():
	return {"Unconsenting Media API is running"}

@app.get("/titles")
def get_titles():
	df = load_csv()
	df = df[df["itemType"].isin(["movie", "TV Show"])].copy()
	df["warnings"], df["safetyRating"] = zip(*df.apply(UM_ratings, axis=1))
	return df[["id", "name", "itemType", "warnings", "safetyRating"]].rename(
		columns={"itemType": "type"}).to_dict(orient="records")
