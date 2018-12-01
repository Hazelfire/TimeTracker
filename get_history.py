import sqlite3
import sys
from datetime import datetime
conn = sqlite3.connect("/home/sam/.mozilla/firefox/gn0vclfx.default/places.sqlite")
for row in conn.execute("""
        SELECT moz_historyvisits.visit_date, moz_places.url FROM moz_historyvisits INNER JOIN moz_places ON moz_historyvisits.place_id=moz_places.id ORDER BY moz_historyvisits.id DESC LIMIT 1;
        """):
    date = datetime.utcfromtimestamp(row[0] / 1000000).strftime("%Y-%m-%d %H:%M:%S")
    print(row[1])
