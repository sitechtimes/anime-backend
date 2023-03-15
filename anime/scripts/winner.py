from anime.models import Anime, AnimeAwards, Awards
from datetime import date
import types


class FindAwardWinner: 
     def __init__(self):
        self.date = date.today()
        self.anime_awards = []
        self.all_winners = []


     def determine_winner(self):
        all_awards = Awards.objects.all()
        
        for award in all_awards:
            self.anime_awards.append(award)

        for anime_award in self.anime_awards:
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
                    # return filtered_anime
                    self.all_winners.append(filtered_anime_award)
                    # print(self.all_winners)
                    # print(filtered_anime_award, filtered_anime_name)
                    print(f"The {filtered_award_name} Award goes to {filtered_anime_name}")

            except:
                print("there is an error")
        print(self.all_winners)
        return self.all_winners

FindAwardWinner = FindAwardWinner()

FindAwardWinner.determine_winner()