from flask import Flask, redirect, url_for, render_template, request
import jsonlines

app = Flask(__name__)

@app.route("/", methods=["GET"])
def main():
    return render_template("index.html", show=True)


@app.route("/query", methods=["POST"])
def query():
    query = request.form["query"]
    result = []
    data = {}
    query = query.lower()
    if not query:
        return render_template("index.html", show=False)
    with jsonlines.open('scrapingproject/scrapingproject/spiders/data.jl') as reader:
        data = reader.read()
        known_urls = []
        for x in range(500000):
            print(x)
            try:
                data = reader.read()
            except EOFError:
                print("EOF")
                break
            if data["url"] in known_urls:
                continue
            count = 0
            if query in data["url"].lower():
                result.append(data)
                known_urls.append(data["url"])
                count += 1
    
            elif query in data["headings"].lower():
                result.append(data)
                count += 1
                known_urls.append(data["url"])
    
            # sort with smallest url first
            result.sort(key=lambda x: len(x["url"]))

            if count > 10:
                print("breaking cuz count is now 10")
                break
    
    print("\n".join([x["url"] for x in result]))

    url_list = [x["url"] for x in result]
    heading_list = [x["headings"] for x in result]
    return render_template("query.html", show=True, url_list=url_list, heading_list=heading_list, query=query)

app.run(host="0.0.0.0", port=2000, debug=True)
