## Run the application
Prepare directory to clone a application.

*mkdir movie_api* 

*cd movie_api*

You can check source code on my public GitHub [repository](https://github.com/mario-pe/movie_api/tree/master).

Clone repository from github.com, you can do it by using command.

```git clone https://github.com/mario-pe/movie_api.git ``` 


In directory where you clone a repository, use comand 

```./run_movie_api```

Wait a second script prepare virtual environment for application and install into all requirements and run the server

##User Guidline

The application is deployed on Heroku link to a application https://movie-api-mp.herokuapp.com/movies/

###Good URL examples

* List of movie stored in data base.

    * GET https://movie-api-mp.herokuapp.com/movies/
    
* Fatch movie data for title of a movie. 
    
    * POST https://movie-api-mp.herokuapp.com/movies/
    * request body: 
        ```
        {
	           title": "rambo"
        }
        ```
* List all comments in database.
    * GET https://movie-api-mp.herokuapp.com/comments/
    
* List of comments related with chosen movie.
    * Get https://movie-api-mp.herokuapp.com/comments?movie=1

* Creat new comment.
    ```
    {
    	"content": "comment content", 
	           "movie": 2
    }
    
    ```
* List most commnted movies in period of time between dates 
    * https://movie-api-mp.herokuapp.com/top?date_from=2001-02-14&date_to=2001-02-20
    
### Bad URL examples

* List of comments related with chosen movie.
    
    * movie parameter must by a movie pk
    
        Get https://movie-api-mp.herokuapp.com/comments?movie=blade runner

* List most commnted movies in period of time between dates. 
    
    * Wrong date format. The date must be written in the format yyyy-mm-dd
      
         https://movie-api-mp.herokuapp.com/top?date_from=2001.02.14&date_to=21/02/2001
    
    * Wrong dates: date_from must less than date_to
    
        https://movie-api-mp.herokuapp.com/top?date_from=2019-02-14&date_to=2001-02-20
