from bottle import route
from bottle import run
from bottle import HTTPError, request
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums


def save(album):
    """
        Сохраняет альбом в базу данных
    """
    session = connect_db()
    session.add(album)
    session.commit()
    return album


def check_unique(album):
    """
        Проверяет уникальность названия альбома
    """
    artist = request.forms.get("artist")
    albums_list = find(artist)
    for item in albums_list:
        if str(album.album).lower() == str(item.album).lower():
            return False
    return True


@route("/albums/<artist>", method='GET')
def albums(artist):
    """
        Обрабатывает запрос списка альбомов для артиста
    """
    albums_list = find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "<h1> Найдено альбомов исполнителя {}: {}</h1>".format(artist, len(album_names))
        result += "<h2>Список альбомов {}:</h2>".format(artist)
        result += "<br><li>"
        result += "<br><li>".join(album_names)

    return result


@route("/albums", method='POST')
def save_album():
    """
        Обрабатывает запрос на сохранение нового альбома
    """
    new_album = Album()
    try:
        int(request.forms.get("year"))
    except:
        return HTTPError(status=400, message="The specified year is invalid. Please enter a number.")

    else:
        if not request.forms.get("album"):
            return HTTPError(status=400, message="You did not enter an album name.")
        new_album.year = int(request.forms.get("year")) or 0000
        new_album.artist = request.forms.get("artist") or ""
        new_album.genre = request.forms.get("genre") or ""
        new_album.album = request.forms.get("album")

        if check_unique(new_album):
            saved_album = save(new_album)
            return "Album {} created successfully".format(saved_album.album)
        else:
            return HTTPError(status=409, message="This album already exists in database")


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
