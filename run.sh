echo "" > prothom.json
scrapy crawl prothom -o prothom.json
python converttoutf.py
