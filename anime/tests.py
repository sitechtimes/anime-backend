from django.test import TestCase
from .models import Genre, Awards, AnimeAwards

# Create your tests here.


class test_genreModel(TestCase):
    def setUp(self):
        self.genre = Genre(genre="my cool genre")

    def test_genreCreation(self):
        self.assertEqual(self.genre.__str__(), "my cool genre")
        self.assertEqual(self.genre.genre, "my cool genre")
        self.assertTrue(isinstance(self.genre, Genre))

class test_awardModel(TestCase):
    def setUp(self):
        self.award = Awards(award_name="the harvey jiang award",award_description="given to anime that harvey likes")


    def test_awardCreation(self):
        self.assertEqual(self.award.__str__(), "the harvey jiang award")
        self.assertEqual(self.award.award_name, "the harvey jiang award")
        self.assertEqual(self.award.award_description, "given to anime that harvey likes")
        self.assertTrue(isinstance(self.award, Awards))

class test_animeAwardsModel(TestCase):
    def setUp(self):
        self.award = Awards(award_name="the kenny tung award",award_description="given to anime that kenny likes")
        self.anime_awards = AnimeAwards(
            
        )





