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

flag_labels = {
	"noRape": "No rape or sexual assault",
	"sexHarOnScrn": "Sexual harassment",
	"sexAdultTeen": "Adult-teen sexual relationship",
	"childSexAbuse": "Child sexual abuse",
	"incest": "Incest",
	"rapeMenDisimp": "Rape implied or discussed",
	"attemptedRape": "Attempted rape",
	"RapeOffScrn": "Rape off-screen or implied",
	"rapeOnScreen": "Rape shown on-screen"
}

def rate_warnings(row):
	warnings = []
	score = 0

	for col, weight in flag_scores.items():
		if str(row.get(col)).strip().upper() == "TRUE":
			label = flag_labels.get(col, col)
			warnings.append(label)
			score += weight

	if score >= 4:
		rating = "🔴"
	elif score >= 1:
		rating = "🟠"
	else:
		rating = "🟢"
		
	return warnings, rating
