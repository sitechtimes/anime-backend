# anime-backend

getting started:

(be sure to create a venv 3.10 plus)

python manage.py makemigrations
python manage.py migrate 
python manage.py runserver 

to run scripts(to get anime)

go to django shell: python manage.py shell

run script: from anime.scripts import db_pop

------------------------------------------------------------------

ANIME MODELS:

Anime- most of the anime model is just scraped from my anime list api but there are a few fields that might be confusing
anime_awards - this is a relationship to awards Model(NOTE: THIS awards model STORES all the awards the ANIME HAS WON)
avg_rating and avg rating - both are defualt 0 and are incremented by the userAnimeInput/Update Mutation.(read Mutations to learn more)

AnimeAwards- this is our vote Model 

------
QuickNote on our Voting system:
  Try to think of the relationship like this: 
    We have alot of awards and each anime can have hundreds awards that users can vote for that anime,but we want to make sure that users only vote once for that award which is why each anime award relationship is unique. Lets look at a example:
    
    allUsers is all users who voted for the award to be given to the anime 
    (each line is a new table and lets say we have two users alpha red and anqi) 
    Anime-> One Piece | Award -> Best Anime | allUsers -> (alpha red and anqi) Anqi trys to vote again but our mutation will reject this req
    Anime-> One Piece | Award -> Best Plot | allUsers -> (alpha red and anqi)
    
    In this example we see that One piece has many awards but there is only one table for each award. Why is this?
    Well we need to track the users that aready voted for the award so people like anqi cant vote for One Piece being the best anime twice.
    
    But keep in mind 
    
    Anime-> Highschool DXD | Award -> Best Anime | allUsers -> (alpha red and anqi)
    Anime-> Highschool DXD | Award -> Best Plot | allUsers -> (alpha red and anqi)
    
    will still work In essence. Its still a many(anime) to many(awards) relationship just formated in a different way.

------

Winner- all awards and there coresponding anime winner

USER MODELS:

------
  How our user system works:
    we are using google oauth and every time a user logins in the frontend our backend will run a receiver named create_user_customer. This reciver creates a user profile for the user who signed up. Lets break userProfile Down.
    
     UserProfile:
      user -> This is the user that django creates from the goauth sign up. (adds user when creating user profile)
      created_date 
      user_voted_animes -> This is all the anime that the user voted for 
      user_anime -> List of all animes that the user rated and watch status of that anime 
      
      Sample user_anime Table:
        SAO
        9.4
        Watching
------
 


GRAPHQL MUTATIONS:
 
ANIME MUTATIONS:

addVote mutation- this mutation takes in the user, anime and award as pramaters and does a vote on the award the user selected hence why we need all of the parameters. lets talk about the Flow of the mutation so first we need to get the user,anime and award form our database. First we check if user is in our all_user field and if the user is there it will return a error because a user can only vote once. Next we will check if there is a anime_award table that corresponds with with the anime and award if it does then we can just add to vote count and add the user to all Users to make sure he wont vote again. If this is false and there is no corsponding anime-award and we will create a new anime-award object/table in our DB.(you can add a new award and it will create a new award as well in the award model)

winner mutation- caculates the winner for the award by most votes(winner is the anime for x award)

USER MUTATIONS:

addUserAnime:
  This mutation takes in 2 arguments the user and the anime.data(this is a object of the anime,rating and watch status). First we check if there is aready a instace of a user_anime with the matching anime. If there is, the mutation will update the old fields with what is provided in anime.data. If not the mutation will create a new user_anime with the inputs given. In addition, if any of the statments want to add or update a rating the mutation will recalculate the avg rating for that anime. For example if 2 people voted a rating of 10 for Horiymia the avg rating will be 10 with a total of 2 people who rated on our anime model. Lets say another person rates that number of people who voted will increase by one and his avg of 8 will be recalculated into the avg. If a person who originally voted and the rating was aready accounted for only the rating avg will change.
  
  
  ------------------------------------------------------------------------------
 Thats It GL.

