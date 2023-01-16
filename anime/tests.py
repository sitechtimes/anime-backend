# from django.test import TestCase
# from .models import Genre, Awards, AnimeAwards, Anime
# import datetime
# # Create your tests here.


# class test_genreModel(TestCase):
#     def setUp(self):
#         self.genre = Genre(genre="my cool genre")

#     def test_genreCreation(self):
#         self.assertEqual(self.genre.__str__(), "my cool genre")
#         self.assertEqual(self.genre.genre, "my cool genre")
#         self.assertTrue(isinstance(self.genre, Genre))

# class test_awardModel(TestCase):
#     def setUp(self):
#         self.award = Awards(award_name="the harvey jiang award",award_description="given to anime that harvey likes")


#     def test_awardCreation(self):
#         self.assertEqual(self.award.__str__(), "the harvey jiang award")
#         self.assertEqual(self.award.award_name, "the harvey jiang award")
#         self.assertEqual(self.award.award_description, "given to anime that harvey likes")
#         self.assertTrue(isinstance(self.award, Awards))

# class test_animeAwardsModel(TestCase):
#     def setUp(self):
#         self.award = Awards(award_name="the kenny tung award",award_description="given to anime that kenny likes")
#         self.anime_awards = AnimeAwards(
#             nominated_for_award = True,
#             has_award = False,
#             anime_award_name = self.award
#         )
#     def test_animeAwardsModel(self):
#         self.assertEqual(self.award.__str__(), "the kenny tung award")
#         self.assertEqual(self.award.award_name, "the kenny tung award")
#         self.assertEqual(self.award.award_description, "given to anime that kenny likes")
#         self.assertTrue(isinstance(self.award, Awards))

#         self.assertEqual(self.anime_awards.anime_award_name, self.award)
#         self.assertEqual(self.anime_awards.nominated_for_award, True)
#         self.assertEqual(self.anime_awards.has_award, False)
#         self.assertEqual(self.anime_awards.anime_award_name.award_description, "given to anime that kenny likes")
#         self.assertEqual(self.anime_awards.anime_award_name.award_name, "the kenny tung award")

# class test_animeModel(TestCase):

#     def setUp(self):

#         self.genre_1 = Genre(
#             genre="horror"
#         )

#         self.genre_2 = Genre(
#             genre="drama"
#         )

#         self.award_1 = Awards(award_name="the vincenzo award",award_description="given to anime that vincenzo likes")
#         self.award_2 = Awards(award_name="the  award",award_description="given to anime that kenny likes")

#         self.my_anime = Anime(
#             anime_name="mr. whalen: the anime",
#             episodes=6969,
#             studio_name="staten island tech studios",
#             aired=True,
#             status=datetime.date(1970, 1, 1),
#             seasons=69,
#             summary="mr. whalen checks everyone's projects on november 22nd",

#             # anime_genre={
#             #     self.genre_1,
#             #     self.genre_2
#             # },

#             # anime_awards={
#             #     AnimeAwards(
#             #         nominated_for_award=True,
#             #         has_award=False,
#             #         anime_award_name=self.award_1
#             #     ),
#             #     AnimeAwards(
#             #         nominated_for_award = True,
#             #         has_award = True,
#             #         anime_award_name = self.award_2
#             #     )
#             # }
#         )

#     def test_animeModel(self):
#         self.assertEqual(self.my_anime.__str__(), "mr. whalen: the anime")
#         self.assertTrue(isinstance(self.my_anime, Anime))
#         self.assertEqual(self.my_anime.episodes, 6969)
#         self.assertEqual(self.my_anime.studio_name, "staten island tech studios")
#         self.assertEqual(self.my_anime.aired, True)
#         self.assertEqual(str(self.my_anime.status), "1970-01-01")
#         self.assertTrue(isinstance(self.my_anime.status,datetime.date))
#         self.assertEqual(self.my_anime.seasons, 69)
#         self.assertEqual(self.my_anime.anime_name, "mr. whalen: the anime")
#         self.assertEqual(self.my_anime.summary, "mr. whalen checks everyone's projects on november 22nd")







