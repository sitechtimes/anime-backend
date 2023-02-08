from anime.models import Anime, AnimeAwards, Awards


anime_awards = [
    "Best Anime",
    "Best Character Design",
    "Best Animation",
    "Best New Series",
    "Best Continuing Series",
    "Best Ending Sequence",
    "Best Opening Sequence",
    "Best Main Character",
    "Best Supporting Character",
    "Best Action",
    "Best Comedy",
    "Best Drama",
    "Best Fantasy",
    "Best Romance",
    "Best Anime Song"
]

def determine_winner():

    for anime_award in anime_awards:
        try:
            all_anime_awards = AnimeAwards.objects.filter(award__award_name = anime_award)
            highest_vote_count = max(all_anime_awards, key=lambda y: y.vote_count)
            print(highest_vote_count)
            
            anime_name = highest_vote_count.anime.anime_name
            award_name = highest_vote_count.award.award_name
            anime = Anime.objects.get(anime_name = anime_name)
            award = Awards.objects.get(award_name = award_name)
            anime.anime_awards.add(award)
            anime.save()
            print(anime)
        except:
            print("there is an error")


determine_winner()