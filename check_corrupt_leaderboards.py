import json

filename = '/Users/petercotton/github/timeseries-elo-ratings/ratings/univariate-k_002.json'
with open(filename) as infile:
    data = json.loads("[" + infile.read().replace("}\n{", "},\n{") + "]")
    for i in data:
        print(i)