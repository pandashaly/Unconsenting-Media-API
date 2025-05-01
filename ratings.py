import pandas as pd

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

def rate_warnings(row):
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
