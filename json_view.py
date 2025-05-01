import json

def json_formatter(data):
	formatted = json.dumps(data, indent=4)
	print(formatted)