from anime.models import Anime, AnimeAwards, Awards
from datetime import date

today = date.today()
print(today)
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
            highest_vote_count = max(all_anime_awards, key=lambda y: y.vote_count).vote_count
            print(highest_vote_count)
            
            filtered_anime_awards = all_anime_awards.filter(vote_count = highest_vote_count)
            print(len(filtered_anime_awards))
            for filtered_anime_award in filtered_anime_awards:
                filtered_anime_name = filtered_anime_award.anime.anime_name
                filtered_award_name = filtered_anime_award.award.award_name
                filtered_anime = Anime.objects.get(anime_name = filtered_anime_name)
                filtered_award = Awards.objects.get(award_name = filtered_award_name)
                filtered_award.date = today
                filtered_award.save()
                print(today)
                filtered_anime.anime_awards.add(filtered_award)
                filtered_anime.save()
                
                
                print(f"The {filtered_award_name} Award goes to {filtered_anime_name}")
            
                
                
                
                
            # if len(filtered_anime_awards) > 1:
            #     for filtered_anime_award in filtered_anime_awards:
            #         filtered_anime_name = filtered_anime_award.anime.anime_name
            #         filtered_award_name = filtered_anime_award.award.award_name
            #         filtered_anime = Anime.objects.get(anime_name = filtered_anime_name)
            #         filtered_award = Awards.objects.get(award_name = filtered_award_name)
            #         filtered_anime.anime_awards.add(filtered_award)
            #         filtered_anime.save()
            #         print(filtered_anime)
            # else:
            #     anime_name = highest_vote_count.anime.anime_name
            #     award_name = highest_vote_count.award.award_name
            #     anime = Anime.objects.get(anime_name = anime_name)
            #     award = Awards.objects.get(award_name = award_name)
            #     anime.anime_awards.add(award)
            #     anime.save()
            #     print(anime)
        except:
            print("there is an error")


determine_winner()