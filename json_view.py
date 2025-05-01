import json

def json_formatter(data):
	formatted = json.dumps(data, indent=4, ensure_ascii=False)
	print(formatted)