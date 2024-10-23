from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace with your own OpenWeatherMap API key
API_KEY = "2c38e319fd273050bd0ff4713e694042"

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    if request.method == "POST":
        city = request.form.get("city")
        if city:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            print(response.json())  # Print the API response for debugging
            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    "city": data["name"],
                    "temperature": data["main"]["temp"],
                    "description": data["weather"][0]["description"],
                    "humidity": data["main"]["humidity"]
                }
            elif response.status_code == 404:
                weather_data = {"error": "City not found!"}
            elif response.status_code == 401:
                weather_data = {"error": "Invalid API Key!"}
            else:
                weather_data = {"error": "Something went wrong. Please try again later."}
    
    return render_template("index.html", weather=weather_data)

if __name__ == "__main__":
    app.run(debug=True)
