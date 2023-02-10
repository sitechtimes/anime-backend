from anime.models import Anime, AnimeAwards, Awards
from datetime import date

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

class FindAwardWinner: 
     def __init__(self):
        self.date = date.today()


    def determine_winner(self, anime_awards: List[str]):

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
                    filtered_award.date = self.date
                    filtered_award.save()
                    print(self.date)
                    filtered_anime.anime_awards.add(filtered_award)
                    filtered_anime.save()
                    print(f"The {filtered_award_name} Award goes to {filtered_anime_name}")
            except:
                print("there is an error")

FindAwardWinner = FindAwardWinner()

FindAwardWinner.determine_winner(anime_awards)