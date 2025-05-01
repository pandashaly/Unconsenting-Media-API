import sys
from csv_handler import get_rating_for_title

if len(sys.argv) < 2:
    print("❌ Please provide a movie title.")
    sys.exit()

title = " ".join(sys.argv[1:])
result = get_rating_for_title(title)

if "error" in result:
    print(result["error"])
else:
    for match in result:
        print(f"\n🎬 {match['name']}")
        print(f"⚠️  Warnings: {match['warnings']}")
        print(f"🟢 Safety Rating: {match['safetyRating']}")
