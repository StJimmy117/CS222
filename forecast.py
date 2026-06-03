import json
import urllib.request


def fetch_json(url):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; Python script)"},
    )
    with urllib.request.urlopen(request) as response:
        return json.load(response)


def main():
    point_url = "https://api.weather.gov/points/40.1934,-85.3864"
    point_data = fetch_json(point_url)
    forecast_url = point_data["properties"]["forecast"]

    forecast_data = fetch_json(forecast_url)
    periods = forecast_data["properties"]["periods"]

    for period in periods:
        name = period.get("name", "")
        temperature = period.get("temperature", "")
        unit = period.get("temperatureUnit", "")
        detailed = period.get("detailedForecast", "")

        print(f"{name}: {temperature} {unit}".strip())
        print(detailed)
        print()


if __name__ == "__main__":
    main()
