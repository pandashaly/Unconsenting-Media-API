from fastapi import FastAPI, Query
import requests
import csv
from io import StringIO
from typing import List
from csv_handler import load_csv
from json_view import json_formatter
import difflib
from ratings import rate_warnings

app = FastAPI()

@app.get("/")
def root():
	return {"Unconsenting Media API is running"}

def data_frame():
	df = load_csv()
	df = df[df["itemType"].isin(["movie", "TV Show"])].copy()
	df["warnings"], df["safetyRating"] = zip(*df.apply(rate_warnings, axis=1))

	return df

@app.get("/titles")
def get_titles():
	df = data_frame()
	result = df[["id", "name", "itemType", "warnings", "safetyRating"]].rename(
		columns={"itemType": "type"}).to_dict(orient="records")
	print(json_formatter(result))
	return (result)
