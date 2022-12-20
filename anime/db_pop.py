from anime.models import Anime, Genre, Studio
import requests
import datetime
import time

class DBPopulate():
    def __init__(self):
        self.base_top_api_url = "https://api.jikan.moe/v4/top/anime/?filter=bypopularity"
        self.base_airing_api_url = "https://api.jikan.moe/v4/anime?status=airing"
        self.response = None

    def addAnime(self, page_num: int = 1,):
        api_url = f"{self.base_top_api_url}&page={page_num}"
        response = requests.get(api_url)
        self.response = response.json()

        for instance in self.response["data"]: # instance is the anime

            if instance["rating"] == "r" or instance["rating"] == "rx":  # if the rating is not school appropriate
                print("not school appropriate")
                continue                                                 # move on to the next anime, dont add it

            if instance["title_english"] is not None:
                my_anime_name = instance["title_english"]
            else:
                my_anime_name = instance["title"]

            date = instance["aired"]["prop"]["from"]
            if date["day"] is not None:
                my_from_date = datetime.date(date["year"],date["month"],date["day"])
            else:
                my_from_date = None

            date = instance["aired"]["prop"]["to"]
            if date["day"] is not None:
                my_to_date = datetime.date(date["year"],date["month"],date["day"])
            else:
                my_to_date = None

            my_anime = Anime(
                anime_name=my_anime_name,
                media_type=instance["type"],
                image_url=instance["images"]["jpg"]["image_url"],
                small_image_url=instance["images"]["jpg"]["small_image_url"],
                large_image_url=instance["images"]["jpg"]["large_image_url"],
                trailer_youtube_url=instance["trailer"]["url"],
                episodes=instance["episodes"],
                status=instance["status"],
                aired_from=my_from_date,
                aired_to=my_to_date,
                summary=instance["synopsis"],
            )
            my_anime.save()


            genre_list = []
            for genre in instance["genres"]:
                genre_list.append(genre["name"])


            for genre_name in genre_list:
                try:
                    Genre.objects.get(genre=genre_name)
                    print(f"genre already exists: {genre_name}")
                except:
                    my_genre = Genre(
                        genre=genre_name
                    )
                    my_genre.save()
                    print(f"new genre created: {my_genre}")

                my_anime.anime_genre.add(Genre.objects.get(genre=genre_name))
                my_anime.save()

            studio_list = []
            for studio in instance["studios"]:
                studio_list.append(studio["name"])


            for studio_name in studio_list:
                try:
                    Studio.objects.get(studio=studio_name)
                    print(f"studio already exists: {studio_name}")
                except:
                    my_studio = Studio(
                        studio=studio_name
                    )
                    my_studio.save()
                    print(f"new studio created: {my_studio}")

                my_anime.anime_studio.add(Studio.objects.get(studio=studio_name))
                my_anime.save()

    def updateAiringAnime(self):

            our_airing_anime = set()
            for anime in Anime.objects.filter(status="Currently Airing"):
                our_airing_anime.add(anime.anime_name)
            print(our_airing_anime)

            their_airing_anime = set()
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

                    # if the rating is not school appropriate
                        # move on to the next anime, dont add it
                    if instance["rating"] == "Rx - Hentai" or instance["rating"] == "R+ - Mild Nudity":
                        print("not school appropriate")
                        continue

                    # if the anime is not popular enough
                        # move on to the next anime, dont add it
                    if instance["members"] < 1000:
                        print("not enough members")
                        continue

                    # set my_anime_name to the name of the anime
                    if instance["title_english"] is not None:
                        my_anime_name = instance["title_english"]
                    else:
                        my_anime_name = instance["title"]

                    their_airing_anime.add(my_anime_name)

                    try:
                        my_anime = Anime.objects.get(anime_name=my_anime_name)

                        date = instance["aired"]["prop"]["from"]
                        if date["day"] is not None:
                            my_from_date = datetime.date(date["year"], date["month"], date["day"])
                        else:
                            my_from_date = None

                        date = instance["aired"]["prop"]["to"]
                        if date["day"] is not None:
                            my_to_date = datetime.date(date["year"], date["month"], date["day"])
                        else:
                            my_to_date = None

                        my_anime.anime_name = my_anime_name
                        my_anime.media_type = instance["type"]
                        my_anime.image_url = instance["images"]["jpg"]["image_url"]
                        my_anime.small_image_url = instance["images"]["jpg"]["small_image_url"]
                        my_anime.large_image_url = instance["images"]["jpg"]["large_image_url"]
                        my_anime.trailer_youtube_url = instance["trailer"]["url"]
                        my_anime.episodes = instance["episodes"]
                        my_anime.status = instance["status"]
                        my_anime.aired_from = my_from_date
                        my_anime.aired_to = my_to_date
                        my_anime.summary = instance["synopsis"]

                        my_anime.save()

                    except Anime.DoesNotExist:

                        date = instance["aired"]["prop"]["from"]
                        if date["day"] is not None:
                            my_from_date = datetime.date(date["year"], date["month"], date["day"])
                        else:
                            my_from_date = None

                        date = instance["aired"]["prop"]["to"]
                        if date["day"] is not None:
                            my_to_date = datetime.date(date["year"], date["month"], date["day"])
                        else:
                            my_to_date = None

                        my_anime = Anime(
                            anime_name=my_anime_name,
                            media_type=instance["type"],
                            image_url=instance["images"]["jpg"]["image_url"],
                            small_image_url=instance["images"]["jpg"]["small_image_url"],
                            large_image_url=instance["images"]["jpg"]["large_image_url"],
                            trailer_youtube_url=instance["trailer"]["url"],
                            episodes=instance["episodes"],
                            status=instance["status"],
                            aired_from=my_from_date,
                            aired_to=my_to_date,
                            summary=instance["synopsis"],
                        )
                        my_anime.save()












DBPopulate = DBPopulate()

DBPopulate.updateAiringAnime()