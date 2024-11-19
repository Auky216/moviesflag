-- Estructura de la base de datos SQLite

-- Tabla que almacena las películas
CREATE TABLE IF NOT EXISTS Movie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    imdbID TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    year INTEGER NOT NULL
);

-- Tabla que almacena los países
CREATE TABLE IF NOT EXISTS Country (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    flag_url TEXT
);

-- Tabla intermedia que relaciona películas con países
CREATE TABLE IF NOT EXISTS MovieCountry (
    movie_id INTEGER NOT NULL,
    country_id INTEGER NOT NULL,
    PRIMARY KEY (movie_id, country_id),
    FOREIGN KEY (movie_id) REFERENCES Movie(id),
    FOREIGN KEY (country_id) REFERENCES Country(id)
);
