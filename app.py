from flask import Flask, render_template, request, jsonify
import requests
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
apikey = "a0e7d14c"

country_flags_cache = {}

executor = ThreadPoolExecutor(max_workers=10)

def searchfilms(search_text, page=1):
    """Función para buscar películas en OMDB."""
    url = f"https://www.omdbapi.com/?s={search_text}&page={page}&apikey={apikey}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve search results.")
        return None

def getmoviedetails(movie_id):
    """Función para obtener detalles de una película."""
    url = f"https://www.omdbapi.com/?i={movie_id}&apikey={apikey}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve movie details.")
        return None

def get_country_flag(fullname):
    """Función para obtener la bandera de un país utilizando caché."""
    if fullname in country_flags_cache:
        return country_flags_cache[fullname]
    
    url = f"https://restcountries.com/v3.1/name/{fullname}?fullText=true"
    response = requests.get(url)
    if response.status_code == 200:
        country_data = response.json()
        if country_data:
            flag_url = country_data[0].get("flags", {}).get("svg", None)
            country_flags_cache[fullname] = flag_url
            return flag_url
    print(f"Failed to retrieve flag for country: {fullname}")
    return None

def merge_data_with_flags(search_text, page=1):
    """Función para combinar datos de películas con las banderas de sus países."""
    filmssearch = searchfilms(search_text, page)
    if not filmssearch or "Search" not in filmssearch:
        return []
    
    moviesdetailswithflags = []
    
    # Obtener detalles de películas en paralelo
    futures = {executor.submit(getmoviedetails, movie["imdbID"]): movie for movie in filmssearch["Search"]}
    for future in futures:
        moviedetails = future.result()
        if moviedetails and "Country" in moviedetails:
            countriesNames = moviedetails["Country"].split(",")
            countries = [
                {"name": country.strip(), "flag": get_country_flag(country.strip())}
                for country in countriesNames
            ]
            moviewithflags = {
                "title": moviedetails["Title"],
                "year": moviedetails["Year"],
                "countries": countries
            }
            moviesdetailswithflags.append(moviewithflags)

    return moviesdetailswithflags

@app.route("/")
def index():
    """Ruta principal para renderizar la página HTML."""
    search_text = request.args.get("filter", "").upper()
    page = int(request.args.get("page", 1))
    movies = merge_data_with_flags(search_text, page)
    return render_template("index.html", movies=movies, search_text=search_text, page=page)

@app.route("/api/movies")
def api_movies():
    """API para obtener los datos en formato JSON."""
    search_text = request.args.get("filter", "")
    page = int(request.args.get("page", 1))
    return jsonify(merge_data_with_flags(search_text, page))

if __name__ == "__main__":
    app.run(debug=True)
