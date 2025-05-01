import pandas as pd

def UM_ratings(csv_path):
	flag_scores = {
		"noRape": 0,
		"sexHarOnScrn": 1,
		"sexAdultTeen": 1,
		"childSexAbuse": 1,
		"incest": 1,
		"rapeMenDisimp": 2,
		"attemptedRape": 2,
		"RapeOffScrn": 2,
		"rapeOnScreen": 4
	}

	df = pd.read_csv(csv_path)
	df = df[df["itemType"].isin(["movie", "TV Show"])].copy()

	def weigh_warnings(row):
		warnings = []
		score = 0

		for col, weight in flag_scores.items():
			if str(row.get(col)).strip().upper() == "TRUE":
				warnings.append(col)
				score += weight

		if score >= 4:
			rating = "🔴"
		elif score >= 1:
			rating = "🟠"
		else:
			rating = "🟢"
		
		return warnings, rating
	
	df["warnings"], df["safetyRating"] = zip(*df.apply(weigh_warnings, axis=1))

	return df
