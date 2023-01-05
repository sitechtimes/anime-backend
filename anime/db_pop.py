from anime.models import Anime, Genre, Studio
import requests
import datetime
import time

class DBPopulate():
    def __init__(self):
        self.base_top_api_url = "https://api.jikan.moe/v4/top/anime/?filter=bypopularity"
        self.base_airing_api_url = "https://api.jikan.moe/v4/anime?status=airing"
        self.response = None

    def addAnime(self, anime_instance):
        # if the rating is not school appropriate
            # move on to the next anime, dont add it
        if anime_instance["rating"] == "Rx - Hentai" or anime_instance["rating"] == "R+ - Mild Nudity":
            print("not school appropriate")
            return

        # if the anime is not popular enough
            # move on to the next anime, dont add it
        if instance["members"] < 1000:
            print("not enough members")
            return

        # get anime title
        if anime_instance["title_english"] is not None:
            my_anime_name = anime_instance["title_english"]
        else:
            my_anime_name = anime_instance["title"]

        # get the date where the anime started airing, if any
        date = anime_instance["aired"]["prop"]["from"]
        if date["day"] is not None:
            my_from_date = datetime.date(date["year"], date["month"], date["day"])
        else:
            my_from_date = None

        # get the date where the anime stopped airing, if any
        date = anime_instance["aired"]["prop"]["to"]
        if date["day"] is not None:
            my_to_date = datetime.date(date["year"], date["month"], date["day"])
        else:
            my_to_date = None

        try:
            my_anime = Anime.objects.get(anime_name=my_anime_name) # try finding a django Anime with the title of the anime

            # if it does exist, update all of its attributes to what the api says
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

            my_anime.save()

        #if it does not exist
        except Anime.DoesNotExist:

            # create a new Anime with the attributes of the anime
            my_anime = Anime(
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
            )
            my_anime.save()

        # create a list of the names of the anime's genres
        genre_list = []
        for genre in anime_instance["genres"]:
            genre_list.append(genre["name"])

        # for every name in the genre list
        for genre_name in genre_list:
            try:
                Genre.objects.get(genre=genre_name) # try and find a Genre object that matches the genre name
                print(f"genre already exists: {genre_name}") # if it does exist just print that it already exists
            except Genre.DoesNotExist: # if it does not exist
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
                Studio.objects.get(studio=studio_name) # try and find a Studio object that matches the studio name
                print(f"studio already exists: {studio_name}") # if it does exist, just print that it already exists
            except: # if it does not exist
                # create a Studio object with that name and print that it was created
                my_studio = Studio(
                    studio=studio_name
                )
                my_studio.save()
                print(f"new studio created: {my_studio}")

            # associate the Studio object that has the name that we want with our Anime object
            my_anime.anime_studio.add(Studio.objects.get(studio=studio_name))
            my_anime.save()


    def initialPopulation(self, page_num: int = 1,):
        api_url = f"{self.base_top_api_url}&page={page_num}"
        response = requests.get(api_url)
        self.response = response.json()

        for instance in self.response["data"]: # instance is the anime
            self.addAnime(instance)

    def updateAiringAnime(self):

            api_url = f"{self.base_airing_api_url}"
            response = requests.get(api_url)
            response = response.json()

            page_count = response["pagination"]["last_visible_page"]
            for page_num in range(1, (page_count+1)):
                time.sleep(4)

                api_url = f"{self.base_airing_api_url}&page={page_num}"
                response = requests.get(api_url)
                response = response.json()

                for instance in response["data"]:
                    self.addAnime(instance)


# DBPopulate = DBPopulate()
#
# for page_num in range(10):
#     DBPopulate.initialPopulation(page_num)
#     time.sleep(4)