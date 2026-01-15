from django.db.models import QuerySet
from django.db import transaction
from db.models import Movie


def get_movies(
    genres_ids: list[int] = None,
    actors_ids: list[int] = None,
	title: str = None,
) -> QuerySet:
    queryset = Movie.objects.all()

    if genres_ids:
        queryset = queryset.filter(genres__id__in=genres_ids)

    if actors_ids:
        queryset = queryset.filter(actors__id__in=actors_ids)

    if title is not None:
        queryset = queryset.filter(title__icontains=title)
    return queryset


def get_movie_by_id(movie_id: int) -> Movie:
    return Movie.objects.get(id=movie_id)


def create_movie(
    movie_title: str,
    movie_description: str,
    release_date: str,
    genres: list = None,
    actors: list = None,
) -> Movie:
    with transaction.atomic():
        movie = Movie.objects.create(
            title=movie_title,
            description=movie_description,
            release_date=release_date
        )
        if actors:
            movie.actors.set(actors)
        if genres:
            movie.genres.set(genres)
        return movie
