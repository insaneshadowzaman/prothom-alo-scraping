import io
import json
with io.open("results.json",'w', encoding="utf-8") as outfile:
    infile = io.open("prothom.json", 'r', encoding="utf-8")
    js = json.load(infile)
    outfile.write(json.dumps(js, ensure_ascii=False, indent=4))
