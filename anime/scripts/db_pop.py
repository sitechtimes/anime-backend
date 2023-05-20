from anime.models import Anime, Genre, Studio, Character
import requests
from requests.exceptions import HTTPError
import datetime
import time


class DBPopulate():
    def __init__(self):
        self.base_top_api_url = "https://api.jikan.moe/v4/top/anime/?filter=bypopularity"
        self.base_airing_api_url = "https://api.jikan.moe/v4/anime?status=airing"
        self.our_airing_anime = set()
        self.their_airing_anime = set()
        self.update_characters_anime = set()
        self.response = None

    def requestAPI(self, api_url):

        try:
            self.response = requests.get(api_url)
            self.response = self.response.json()
        except HTTPError as http_err:
            raise HTTPError(f'HTTP error occurred: {http_err}')
        except Exception as err:
            raise Exception(f'Other error occurred: {err}')

    def addAnime(self, anime_instance: dict):
        try:
            # get anime title
            if not anime_instance["title_english"] is None:
                my_anime_name = anime_instance["title_english"]
            else:
                my_anime_name = anime_instance["title"]

            # if the rating is not school appropriate
                # move on to the next anime, don't add it
            if anime_instance["rating"] == "Rx - Hentai" or anime_instance["rating"] == "R+ - Mild Nudity":
                print(f"not school appropriate: {my_anime_name}")
                return

            # if the anime is not popular enough
                # move on to the next anime, don't add it
            if anime_instance["members"] < 5000:
                print(f"not popular enough: {my_anime_name}")
                return

            # get the date where the anime started airing, if any
            date = anime_instance["aired"]["prop"]["from"]
            if date["day"] is not None:
                my_from_date = datetime.date(
                    date["year"], date["month"], date["day"])
            else:
                my_from_date = None

            # get the season if the month the anime aired is available
            if my_from_date is not None:
                if my_from_date.month is not None:
                    my_month = my_from_date.month

                    match my_month:
                        case 1 | 2 | 3:
                            my_time_of_year = "Winter"
                        case 4 | 5 | 6:
                            my_time_of_year = "Spring"
                        case 7 | 8 | 9:
                            my_time_of_year = "Summer"
                        case 10 | 11 | 12:
                            my_time_of_year = "Fall"
                        case None:
                            my_time_of_year = ""

                    if my_time_of_year is not "":
                        my_season = f"{my_time_of_year} {my_from_date.year}"

            else:
                my_season = None

            # get the date where the anime stopped airing, if any
            date = anime_instance["aired"]["prop"]["to"]
            if date["day"] is not None:
                my_to_date = datetime.date(
                    date["year"], date["month"], date["day"])
            else:
                my_to_date = None

        except Exception as err:
            raise Exception(
                f"something in the special anime attributes didnt work: {err}")

        try:
            # try finding a django Anime with the MAL id of the anime
            my_anime = Anime.objects.get(mal_id=anime_instance["mal_id"])

            # if it does exist, update all of its attributes to what the api says
            my_anime.mal_id = anime_instance["mal_id"]
            my_anime.anime_name = my_anime_name
            my_anime.media_type = anime_instance["type"]
            my_anime.image_url = anime_instance["images"]["jpg"]["image_url"]
            my_anime.small_image_url = anime_instance["images"]["jpg"]["small_image_url"]
            my_anime.large_image_url = anime_instance["images"]["jpg"]["large_image_url"]
            my_anime.trailer_youtube_url = anime_instance["trailer"]["url"]
            my_anime.episodes = anime_instance["episodes"]
            my_anime.status = anime_instance["status"]
            my_anime.aired_from = my_from_date
            my_anime.aired_to = my_to_date
            my_anime.summary = anime_instance["synopsis"]
            my_anime.season = my_season

            my_anime.save()

        # if it does not exist
        except Anime.DoesNotExist:

            # create a new Anime with the attributes of the anime
            my_anime = Anime(
                mal_id=anime_instance["mal_id"],
                anime_name=my_anime_name,
                media_type=anime_instance["type"],
                image_url=anime_instance["images"]["jpg"]["image_url"],
                small_image_url=anime_instance["images"]["jpg"]["small_image_url"],
                large_image_url=anime_instance["images"]["jpg"]["large_image_url"],
                trailer_youtube_url=anime_instance["trailer"]["url"],
                episodes=anime_instance["episodes"],
                status=anime_instance["status"],
                aired_from=my_from_date,
                aired_to=my_to_date,
                summary=anime_instance["synopsis"],
                season=my_season
            )
            my_anime.save()

        # create a list of the names of the anime's genres
        genre_list = []
        for genre in anime_instance["genres"]:
            genre_list.append(genre["name"])

        # for every name in the genre list
        for genre_name in genre_list:
            try:
                # try and find a Genre object that matches the genre name
                Genre.objects.get(genre=genre_name)
                # if it does exist just print that it already exists
                print(f"genre already exists: {genre_name}")
            except Genre.DoesNotExist:  # if it does not exist
                # create a Genre object with that name and print that it was created
                my_genre = Genre(
                    genre=genre_name
                )
                my_genre.save()
                print(f"new genre created: {my_genre}")

            # associate the Genre object that has the name that we want with our Anime object
            my_anime.anime_genre.add(Genre.objects.get(genre=genre_name))
            my_anime.save()

        # create a list of the names of the anime's studios
        studio_list = []
        for studio in anime_instance["studios"]:
            studio_list.append(studio["name"])

        # for every name in the studio list
        for studio_name in studio_list:
            try:
                # try and find a Studio object that matches the studio name
                Studio.objects.get(studio=studio_name)
                # if it does exist, just print that it already exists
                print(f"studio already exists: {studio_name}")
            except Studio.DoesNotExist:  # if it does not exist
                # create a Studio object with that name and print that it was created
                my_studio = Studio(
                    studio=studio_name
                )
                my_studio.save()
                print(f"new studio created: {my_studio}")

            # associate the Studio object that has the name that we want with our Anime object
            my_anime.anime_studio.add(Studio.objects.get(studio=studio_name))
            my_anime.save()

    def initialPopulation(self, pages: int = 5, min_characters: int = 10, min_side_characters: int = 5, add_characters: bool = True):

        for page_num in range(1, pages+1):

            api_url = f"{self.base_top_api_url}&page={page_num}"
            self.requestAPI(api_url)

            for instance in self.response["data"]:  # instance is the anime
                self.addAnime(instance)
                
            time.sleep(1)

        if add_characters is True:
            self.noCharacterAnime(min_characters, min_side_characters)

    def updateAiringAnime(self, min_characters: int = 10, min_side_characters: int = 5,):

        # get all the anime that we have that are airing
        try:
            my_set = set(Anime.objects.filter(status="Currently Airing"))
            for anime in my_set:
                self.our_airing_anime.add(anime.mal_id)
            print(f"our_airing_anime: {self.our_airing_anime}")
        except Anime.DoesNotExist:
            # if there are none then just say so
            print("our_airing_anime: none")

        api_url = f"{self.base_airing_api_url}"
        self.requestAPI(api_url)

        page_count = self.response["pagination"]["last_visible_page"]
        for page_num in range(1, (page_count+1)):
            time.sleep(1)

            api_url = f"{self.base_airing_api_url}&page={page_num}"
            self.requestAPI(api_url)

            for instance in self.response["data"]:
                # add the anime's id to their airing anime
                self.their_airing_anime.add(instance["mal_id"])
                self.addAnime(instance)
                # add the newly created anime to the update characters set
                self.update_characters_anime.add(
                    Anime.objects.get(mal_id=instance["mal_id"]))

        self.updateCharacters(self.update_characters_anime,
                              min_characters, min_side_characters,)

        print(f"our_airing_anime: {self.our_airing_anime}")
        print(f"their_airing_anime: {self.their_airing_anime}")
        # get the anime that are in our_airing_anime but not their_airing_anime                                                                      # this means that they are not airing anymore and our info is outdated
        wrong_anime = self.our_airing_anime.difference(self.their_airing_anime)
        print(f"wrong_anime: {wrong_anime}")

        for mal_id in wrong_anime:
            my_anime = Anime.objects.get(mal_id=mal_id)
            # so just set the status to "Finished Airing"
            my_anime.status = "Finished Airing"
            my_anime.save()

        self.our_airing_anime = set()
        self.their_airing_anime = set()

    def noCharacterAnime(self, min_characters: int = 10, min_side_characters: int = 5,):
        no_character_anime_set = set(
            Anime.objects.filter(anime_characters=None))
        self.updateCharacters(no_character_anime_set,
                              min_characters, min_side_characters)

    def updateCharacters(self, anime_set: set, min_characters: int = 10, min_side_characters: int = 5,):

        for anime in anime_set:
            my_mal_id = anime.mal_id
            self.requestAPI(
                f"https://api.jikan.moe/v4/anime/{my_mal_id}/characters")
            supporting_index_favorites = dict()

            for character in self.response["data"]:
                if character["role"] == "Main":
                    self.addCharacter(character, my_mal_id)
                else:
                    # add a key value pair to the dictionary {(character mal id): (number of favorites)}
                    supporting_index_favorites[self.response["data"].index(
                        character)] = character["favorites"]

            sorted_supporting_index_favorites = dict(sorted(supporting_index_favorites.items(
            ), key=lambda x: x[1], reverse=True))  # sort the dictionary by descending order of favorites
            print(f"SORTED: {sorted_supporting_index_favorites}")

            main_characters = anime.anime_characters.all().count()

            if main_characters >= min_characters - min_side_characters:
                side_characters = min_side_characters
            else:
                side_characters = min_characters - main_characters

            side_characters_to_add = list(sorted_supporting_index_favorites.keys())[
                :side_characters]  # get the first (side_characters) mal ids of the set
            for character_index in side_characters_to_add:
                # find the character that corresponds to the given index
                side_character = self.response["data"][character_index]
                # add that character
                self.addCharacter(side_character, my_mal_id)

            time.sleep(1)

    def addCharacter(self, character: dict, anime_mal_id: int):
        try:
            my_character_mal_id = character["character"]["mal_id"]
            my_character_name = character["character"]["name"]
            my_anime = Anime.objects.get(mal_id=anime_mal_id)
            # if it exists it will move on fine
            my_character = Character.objects.get(mal_id=my_character_mal_id)
            # if not then it will move onto except
            print(f"character already exists: {my_character_name}")
            my_anime.anime_characters.add(my_character)
        except Character.DoesNotExist:
            my_character = Character(
                mal_id=my_character_mal_id,
                character_name=my_character_name,
                role=character["role"],
                image_url=character["character"]["images"]["jpg"]["image_url"],
            )
            my_character.save()
            my_anime.anime_characters.add(my_character)


DBPopulate = DBPopulate()

DBPopulate.initialPopulation(pages=7)
