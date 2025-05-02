from fastapi import FastAPI, Query
import requests
import csv
import pandas as pd
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
	df = df[df["itemType"].isin(["movie", "TV show"])].copy()
	df["warnings"], df["safetyRating"] = zip(*df.apply(rate_warnings, axis=1))

	return df

@app.get("/titles")
def get_titles():
	df = data_frame()
	result = df[["id", "name", "itemType", "warnings", "safetyRating"]].rename(
		columns={"itemType": "type"}).to_dict(orient="records")
	print(json_formatter(result))
	return (result)

@app.get("/titles/search")
def search_titles(q: str = Query(...,description="Movie or TV show or title.")):
	df = data_frame()
	df["full_name"] = (df["name"]).str.strip().str.lower()
	df["clean_name"] = df.get("cleanName").fillna(df["name"]).str.strip().str.lower()
	query = q.strip().lower()

	match = df[df["full_name"] == query] #exact match
	if not match.empty:
		match = df[df["clean_name"] == query]

	#fuzzy match full
	if match.empty:
		titles_full = df["full_name"].tolist()
		best_full = difflib.get_close_matches(q, titles_full, n=1, cutoff=0.9)
		if best_full:
			match = df[df["full_name"] == best_full[0]]
	
	#fuzzy match clean
	if match.empty:
		titles_clean = df["clean_name"].tolist()
		best_clean = difflib.get_close_matches(q, titles_full, n=1, cutoff=0.9)
		if best_full:
			match = df[df["clean_name"] == best_clean[0]]
	
	if match.empty:
		partial = df[df["full_name"].str.contains(query, na=False)]
		if partial.empty:
			return {"error": f"No matches found for '{q}'"}
		results = partial

	output = match[["id", "name", "itemType", "warnings", "safetyRating", "comment"]]
	output = output.rename(columns={"itemType": "type"})
	#output["comment"] = (output["comment"].fillna("").apply(lambda txt: [p for p in txt.split("\n\n") if p]))
	output = output.fillna("")
	res = output.to_dict(orient="records")
	print(json_formatter(res))
	return (res)
