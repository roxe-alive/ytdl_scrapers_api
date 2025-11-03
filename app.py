from flask import Flask, request, jsonify
import requests
import urllib.parse

app = Flask(__name__)

VIDFLY_API = "https://api.vidfly.ai/api/media/youtube/download"


def decode_url(url: str):
    if not url:
        return url
    url = url.replace("\\u0026", "&").replace("////", "//")
    return urllib.parse.unquote(url)


@app.route("/api/youtube/download", methods=["GET"])
def youtube_download():
    youtube_url = request.args.get("url")
    if not youtube_url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    try:
        # Step 1: Call Vidfly API
        res = requests.get(VIDFLY_API, params={"url": youtube_url}, timeout=15)
        res.raise_for_status()
        data = res.json()

        # Step 2: Decode video URLs
        if "data" in data and "items" in data["data"]:
            for item in data["data"]["items"]:
                if "url" in item:
                    item["url"] = decode_url(item["url"])

        # Step 3: Return cleaned JSON
        return jsonify(data)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()
