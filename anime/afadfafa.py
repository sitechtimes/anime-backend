if anime_instance["rating"] == "r" or anime_instance["rating"] == "rx":  # if the rating is not school appropriate
    print("not school appropriate")
    continue  # move on to the next anime, dont add it

if anime_instance["title_english"] is not None:
    my_anime_name = anime_instance["title_english"]
else:
    my_anime_name = anime_instance["title"]

date = anime_instance["aired"]["prop"]["from"]
if date["day"] is not None:
    my_from_date = datetime.date(date["year"], date["month"], date["day"])
else:
    my_from_date = None

date = anime_instance["aired"]["prop"]["to"]
if date["day"] is not None:
    my_to_date = datetime.date(date["year"], date["month"], date["day"])
else:
    my_to_date = None

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

genre_list = []
for genre in anime_instance["genres"]:
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
for studio in anime_instance["studios"]:
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