import jsonlines

def cleaner():
    known_urls = []

    never_known_urls = []
    with jsonlines.open('scrapingproject/scrapingproject/spiders/data.jl') as jl:
        while True:
            try:
                data = jl.read()
            except EOFError:
                break
            if data["url"] in known_urls:
                continue
            else:
                never_known_urls.append(data)
                known_urls.append(data["url"])
                print("Now knows about", len(known_urls), "unique urls")
    with jsonlines.open('scrapingproject/scrapingproject/spiders/data.jl', mode='w') as jl:
        for data in never_known_urls:
            jl.write(data)
