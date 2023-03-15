from django.test import TestCase
from graphene.test import Client
from snapshottest import TestCase as SnapshotTestCase
from anime.models import Genre, Studio, Character, Awards, AnimeAwards, Anime
from animeBackend.schema import schema
import datetime
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
        self.award = Awards(award_name="the harvey jiang award")


    def test_awardCreation(self):
        self.assertEqual(self.award.__str__(), "the harvey jiang award")
        self.assertEqual(self.award.award_name, "the harvey jiang award")
        self.assertTrue(isinstance(self.award, Awards))

class test_animeAwardsModel(TestCase):
    def setUp(self):
        self.award = Awards(award_name="the kenny tung award")
        self.anime_awards = AnimeAwards(
            nominated_for_award=True,
            nominated_date=datetime.date(1776, 7, 4),
            has_award=False,
            recieved_date=datetime.date(2023, 3, 14),
            anime_award_name=self.award,
        )
    def test_animeAwardsModel(self):
        self.assertEqual(self.award.__str__(), "the kenny tung award")
        self.assertEqual(self.award.award_name, "the kenny tung award")
        self.assertTrue(isinstance(self.award, Awards))

        self.assertEqual(self.anime_awards.anime_award_name, self.award)
        self.assertEqual(self.anime_awards.nominated_for_award, True)
        self.assertEqual(self.anime_awards.nominated_date.month, 7)
        self.assertEqual(str(self.anime_awards.nominated_date), "1776-07-04")
        self.assertEqual(self.anime_awards.received_date.day, 14)
        self.assertEqual(str(self.anime_awards.received_date), "2023-03-14")
        self.assertEqual(self.anime_awards.has_award, False)
        self.assertEqual(self.anime_awards.anime_award_name.award_name, "the kenny tung award")

class test_characterModel(TestCase):

    def setUp(self):
        self.my_character = Character(
            mal_id=123456,
            character_name="Jiang, Harvey",
            role="Main",
            image_url="https://example.com/image.jpg"
        )

    def test_characterModel(self):
        self.assertEqual(self.my_character.__str__(), "Jiang, Harvey")
        self.assertEqual(self.my_character.mal_id, 123456)
        self.assertEqual(self.my_character.character_name, "Jiang, Harvey")
        self.assertEqual(self.my_character.role, "Main")
        self.assertEqual(self.my_character.image_url, "https://example.com/image.jpg")
        self.assertTrue(isinstance(self.my_character, Character))

class test_animeModel(TestCase):

    def setUp(self):

        self.award_1 = Awards(award_name="the vincenzo award")
        self.award_2 = Awards(award_name="the kenny tung award")


        self.my_anime = Anime(
            mal_id=12345,
            anime_name="mr. whalen: the anime",
            media_type="OVA",
            image_url="https://example.com/image_n.jpg",
            small_image_url="https://example.com/image_s.jpg",
            large_image_url="https://example.com/image_l.jpg",
            trailer_youtube_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            episodes=6969,
            status="Finished Airing",
            aired_from=datetime.date(2017, 1, 13),
            aired_to=datetime.date(2017, 12, 9),
            summary="mr. whalen checks everyone's projects on november 22nd",
        )

        self.my_anime.anime_studio.add(Studio(
            studio="staten island tech studios"
        ))

        self.my_anime.anime_genre.add(Genre(
            genre="Comedy"
        ))

        self.my_anime.anime_genre.add(Genre(
            genre="Horror"
        ))

        self.my_anime.anime_awards.add(AnimeAwards(
            nominated_for_award=True,
            nominated_date=datetime.date(2005, 9, 14),
            has_award=True,
            received_date=datetime.date(2005, 10, 1),
            anime_award_name=self.award_1
        ))

        self.my_anime.anime_awards.add()

            # anime_awards={
            #     AnimeAwards(
            #         nominated_for_award=True,
            #         has_award=False,
            #         anime_award_name=self.award_1
            #     ),
            #     AnimeAwards(
            #         nominated_for_award = True,
            #         has_award = True,
            #         anime_award_name = self.award_2
            #     )
            # }

    def test_animeModel(self):
        self.assertEqual(self.my_anime.__str__(), "mr. whalen: the anime")
        self.assertTrue(isinstance(self.my_anime, Anime))
        self.assertEqual(self.my_anime.episodes, 6969)
        self.assertEqual(self.my_anime.studio_name, "staten island tech studios")
        self.assertEqual(self.my_anime.aired, True)
        self.assertEqual(str(self.my_anime.status), "1970-01-01")
        self.assertTrue(isinstance(self.my_anime.status,datetime.date))
        self.assertEqual(self.my_anime.seasons, 69)
        self.assertEqual(self.my_anime.anime_name, "mr. whalen: the anime")
        self.assertEqual(self.my_anime.summary, "mr. whalen checks everyone's projects on november 22nd")

class GraphQLTests(SnapshotTestCase):
    def test_create_award(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute(
            '''
            mutation{
              createAward(name:"goober award"){
                award{
                  awardName
                }
              }
            }
            '''
        ))

        def test_create_award(self):
            client = Client(schema)
            self.assertMatchSnapshot(client.execute(
                '''
                mutation{
                  createAward(name:"goober award"){
                    award{
                      awardName
                        }
                  }
                }
                '''
            ))





