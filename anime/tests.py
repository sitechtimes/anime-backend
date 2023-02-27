from django.test import TestCase
from snapshottest.django import TestCase
from animeBackend.schema import schema
from graphene.test import Client
from .models import Genre, Anime, AnimeAwards, Awards, Studio
from datetime import date
# # Create your tests here.


class AnimeQLTestCase(TestCase):
    def test_anime(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
 {
  allAnime {
    edges {
      node {
        id
        animeName
        episodes
        malId
        mediaType
        imageUrl
        smallImageUrl
        largeImageUrl
        trailerYoutubeUrl
        airedFrom
        airedTo
        animeStudio {
          edges {
            node {
              studio
            }
          }
        }
        animeGenre {
          edges {
            node {
              genre
            }
          }
        }
        summary
        status
      }
    }
  }
}
'''))
        

class AddVoteTestCase(TestCase):
    def test_add_vote(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        mutation {
  addVote(
    awardName: "2"
    userData: {userId: "2"}
    animeData: {animeName: "One Piece"}
  ) {
    animeAward {
      voteCount
      anime {
        animeName
      }
      award {
        awardName
      }
      allUsers {
        edges {
          node {
            user {
              username
              email
            }
          }
        }
      }
    }
  }
}

        '''))

class FindWinnerTestCase(TestCase):
    def test_find_winner(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
       mutation{
winner{
 animeAwards{
   winner{
     anime{
       animeName
     },
     award{
         awardName,
         date
     },
       voteCount
   }
 }
}
 }
        '''))


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

class test_studioModel(TestCase): 
    def setUp(self):
        self.studio = Studio(studio="studio1")
    
    def test_studioModel(self):
        self.assertTrue(isinstance(self.studio, Studio))

class test_animeModel(TestCase):

    def setUp(self):

        self.genre_1 = Genre(
            genre="horror"
        )

        self.genre_2 = Genre(
            genre="drama"
        )

        self.studio_1 = Studio(
            studio="studio1"
        )
        self.studio_1 = Studio(
            studio="studio2"
        )
        # self.award_1 = Awards(award_name="the vincenzo award",award_description="given to anime that vincenzo likes")
        # self.award_2 = Awards(award_name="the  award",award_description="given to anime that kenny likes")

        self.my_anime = Anime(
            mal_id = "1",
            anime_name="test anime",
            media_type = "ONA",
            image_url = "test.jpg",
            small_image_url="test.jpg",
            large_image_url="test.jpg",
            trailer_youtube_url="test.com",
            episodes= 12,
            status="Currently Airing",
            summary="test summary",
            aired_from =date(2023,1,18),
            aired_to =date(2023,2,18),
            # anime_genre={
            #     self.genre_1,
            #     self.genre_2,
            # },
            # anime_studio= {
            # self.studio_1,
            # self.studio_2,
            # },
            number_rating= 5,

        )

    def test_animeModel(self):
        self.assertEqual(self.my_anime.aired_from, date(2023,1,18)),
        self.assertEqual(self.my_anime.aired_to, date(2023,2,18))
        self.assertEqual(self.my_anime.media_type, "ONA")
        self.assertEqual(self.my_anime.image_url, "test.jpg")
        self.assertEqual(self.my_anime.small_image_url, "test.jpg")
        self.assertEqual(self.my_anime.large_image_url, "test.jpg")
        self.assertEqual(self.my_anime.trailer_youtube_url, "test.com")
        self.assertEqual(self.my_anime.episodes, 12)
        self.assertEqual(self.my_anime.anime_name, "test anime")
        self.assertEqual(self.my_anime.summary,"test summary")
        self.assertEqual(self.my_anime.number_rating, 5)
        # self.assertTrue(self.my_anime, Anime())
