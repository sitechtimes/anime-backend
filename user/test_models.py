from django.test import TestCase
from model_bakery import baker
from .models import User, UserAnime
from anime.schema import Anime, Genre, AnimeAwards, Awards
from pprint import pprint

# Create your tests here.
class testUserModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.genre = Genre(
            genre = "test genre"
        )
        cls.genre.save()
        # cls.genre.save()
        cls.genre_two = Genre(
            genre = "two"
        )
        cls.genre_two.save()
        cls.award = Awards(
            award_name = "harvey award",
            award_description = "this is an award"
        )
        cls.award.save()
        cls.anime_award = AnimeAwards(
            nominated_for_award = True,
            has_award = True,
            anime_award_name = cls.award
        )
        cls.anime_award.save()
        # cls.anime = baker.make(Anime, anime_genre = cls.genre, anime_awards = cls.award)
        cls.anime = Anime(
            id = 1,
            anime_name = "test anime name",
            episodes = 7,
            studio_name = "test studio name",
            aired = False,
            status = "2022-11-21",
            seasons = 7,
            summary = "This is a test summary",
            # anime_genre = cls.genre,
            # anime_awards = cls.anime_award
        )
        cls.anime.save()
        pprint(cls.anime)
        cls.user_anime = UserAnime(
            anime = cls.anime,
            currently_watching = False,
            watchlist = True,
            finished_anime = True,
            rating = 7
        )
        cls.user_anime.save()
        cls.user = User(
            user_name = "test username",
            grade = 11,
            email = "Johnsonw3@nycstudents.net",
            # user_anime = cls.user_anime
        )
        cls.user.save()
        pprint(cls.user)

    def test_userAnime(self):
        pprint(self.user)
        # self.anime.anime_genre.set([self.genre.pk, self.genre_two.pk])
        # self.assertEqual(self.anime.anime_genre.count(), 2)
        self.assertIsInstance(self.user_anime, UserAnime)
        self.assertEqual(self.user_anime.__str__(), self.anime)

    def test_user(self):
        self.assertIsInstance(self.user, User)
        self.assertEqual(self.user.__str__(), "test username")
        # self.assertEqual(self.user.grade, 11)
