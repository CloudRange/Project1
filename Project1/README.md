# Project 1 -- Billboard 

**DUE ~~Feb 28~~ Mar 1, 11:59p**

Learning objectives:

- Use pandas data frames as a fundamental structure
- Filter, project, reassemble data frames to extract information
- Report and visualize information using a variety of plots

In class we explored one technique for extracting data from a web page, and in this project you'll use something a
little bit different. Rather than scraping data from Billboard, we will use a library called Spotipy, which makes 
accessing Spotify data very simple. 
This project uses Spotipy to not only get the rankings, but also audio features about these songs!

### Part 0 -- Getting started
In this project, we will use the (free) [Spotify Web API](https://developer.spotify.com/documentation/web-api/). It provides a set of endpoints for us to query a wide variety of aggregated information about songs, albums, artists, playlists, and more! Here is a link to the complete [Spotify API reference](https://developer.spotify.com/documentation/web-api/reference/) We encourage you to explore the API and maybe build a side project with it if you'd like! 

To access the endpoints, you will need a Spotify developer account:
- Step 1. Go to Spotify developer page (https://developer.spotify.com/) and click on `Dashboard`. Follow the instructions to sign in or to create an account.
- Step 2. Once on the Dashboard page, choose `Create an app` and give your project a name and a description. 
- Step 3. Navigate to the app dashboard, you should see your `Client ID` and `Client Secret` right under the app's name and description.
- Step 4. Copy your `Client ID` and `Client Secret` over to the first `TODO` in `spot.py`

All set! Now we can start querying from Spotify using Spotipy!

### Part 1 -- Organizing the data

In this part of the project you will be completing the code that we began writing
in `spot.py`. Throughout that file you will see comments labeled "`TODO`". In each 
of those locations, you should either complete our code, or completely write your
own. The dataclasses you'll use can be found in a file called `models.py`. 

Complete the following function:

- `def getPlaylist(id: str) -> List[Track]:` which queries spotify and assembles the data into a list of `Track` objects. 
As you write this code, you should scrutinize the results of the spotify queries. They are quite
  complex -- part of your task is to extract the essential (and much simpler) information.

Write the following two functions:

- `getGenres(t: Track) -> List[str]` which takes in a Track and produce a list of unique genres that the artists of this track belong to.

- `doesGenreContains(t: Track, genre: str) -> bool` which checks if the genres of a track contains the key string specified

We will use these functions to assemble a list of `Track` into a `DataFrame` containing various information about the track.

### Part 2 -- The most popular artist of the week

In this section, we would like to find out the most popular artist of the week. We could measure popularity by the total number of tracks that an artist has on the Billboard Hot 100 list.

#### 2.1
Write the function `artist_with_most_tracks(tracks: List[Track]) -> (Artist, int)` which takes in a list of tracks and produce the artist and the number of tracks the artist has on the list.

#### 2.2
Do you think this is a good measurement for popularity? Come up with an alternative definition in your writeup and justify in the write-up! (You don't need to code it out)

### Part 3 -- Visualizing the data

In this section, we would like to explore the audio features that each track has and how they are related to a track's genres. A list of what these audio features represent can be found [here](https://developer.spotify.com/documentation/web-api/reference/#object-audiofeaturesobject).

Complete the following plots based on the data you assembled in Part 1:

#### 3.1
- On a scatter plot, 
display all the tracks with `"danceability"` as x-axis and `"speechiness"` as y-axis. Color the dots based on whether the track `"is_rap"`. 
Label the axis of the plot and add a legend.

- Describe in one sentence what the plot shows about the `rap` genre.
- This is Spotify's take on danceability and speechiness. Do you think it is reasonable based on the result of the plot?

#### 3.2 Ask your own question

Come up with a question that explores the relationship between audio features and genre/artist. Answer and justify your question in the write up. Include at least one scatter plot in your answer. A few ideas to start off with:
- What are the distinct audio features that separate country music from the rest of the tracks on the Hot 100 list?
- Are there genres that do not overlap with each other at all in some feature space?

Feel free to modify `getTrackDataFrame(tracks: List[Track]) -> pd.DataFrame` to include attributes that you think will be useful. If you want to query a playlist different from Billboard Hot 100, call `getPlaylist(id: str) -> List[Track]` with a playlist id of your choosing. You can find playlist id of a playlist here. 
![](./playlist_uri.png)

## Getting the Code

In this repository you'll find the skeleton python files in which you should build your solutions. 

## Deliverables

### Code

Push your well-commented code solutions to your student repository. Make sure that you have listed the `staff` team as one of the collaborators, 
and that you have removed the `students` team. 

### PrairieLearn

Please make a final submission of `spot.py` to PrairieLearn before the due date. There will be no autograder tests
for the project. Also, submit a `README.md` file (similar to this one!) containing your written responses.

### Part 2 Popular Artist Writeup

Describe and justify your choice of measurement for popularity. 

### Part 3 Data visualization Writeup

#### 3.1 interpretation:

Give an interpretation of the plot from Part 3.1

#### 3.2

Write a paragraph or so describing what you have found in your own exploration. 








