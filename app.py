from flask import Flask, Response
import requests
from lxml import html, etree
import os

app = Flask(__name__)

SOURCE_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRmEw4QdEY1cE9CkfibBYpLdx013b0y_NVUFGVPHcYJ59K1fUP6SsNJgue0qejUdxJHt5eM1R-JcLaa/pubhtml?gid=0&single=true"

@app.route("/sheet.xml")
def serve_xml():
    try:
        response = requests.get(SOURCE_URL)
        response.raise_for_status()
        tree = html.fromstring(response.content)
        xml_string = etree.tostring(tree, pretty_print=True, method="xml", encoding="utf-8")
        return Response(xml_string, mimetype='application/xml')
    except Exception as e:
        return Response(f"<error>{str(e)}</error>", mimetype='application/xml')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
