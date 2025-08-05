from flask import Flask, Response
import requests
import csv
import io
import os

app = Flask(__name__)

# Replace with your actual published CSV URL
SOURCE_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRmEw4QdEY1cE9CkfibBYpLdx013b0y_NVUFGVPHcYJ59K1fUP6SsNJgue0qejUdxJHt5eM1R-JcLaa/pub?output=csv"

@app.route("/sheet.xml")
def serve_xml():
    try:
        response = requests.get(SOURCE_URL)
        response.raise_for_status()
        
        csv_file = io.StringIO(response.text)
        reader = list(csv.reader(csv_file))

        # C8 = row 8 (index 7), column C = index 2
        # E8 = row 8 (index 7), column E = index 4
        c8 = reader[7][2] if len(reader) > 7 and len(reader[7]) > 2 else "N/A"
        e8 = reader[7][4] if len(reader) > 7 and len(reader[7]) > 4 else "N/A"

        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<SheetData>
  <C8>{c8}</C8>
  <E8>{e8}</E8>
</SheetData>"""

        return Response(xml, mimetype='application/xml')

    except Exception as e:
        return Response(f"<error>{str(e)}</error>", mimetype='application/xml')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
