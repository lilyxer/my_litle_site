from enum import Flag, auto


class MovieGenres(Flag):
    ACTION = auto()
    COMEDY = auto()
    DRAMA = auto()
    FANTASY = auto()
    HORROR = auto()


class Movie:
    def __init__(self, name: str, genres: MovieGenres) -> None:
        self.name = name
        self.genres = genres

    def in_genre(self, genre: MovieGenres) -> bool:
        return genre in self.genres
    
    def __str__(self) -> str:
        return str(self.name)
    

movie = Movie('The Lord of the Rings', MovieGenres.ACTION | MovieGenres.FANTASY)

print(movie.in_genre(MovieGenres.FANTASY))
print(movie.in_genre(MovieGenres.COMEDY))
print(movie.in_genre(MovieGenres.ACTION | MovieGenres.FANTASY))