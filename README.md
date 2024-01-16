# SI-507-Final

# Packages 
Pandas, matplotlib, json, os, requests

# Data Sources
OMDB database, 
Kaggle (https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset?resource=download&select=movies_metadata.csv)
First, I requested API key from the OMDB database. In order to get detailed information for each movie, I downloaded a movie metadata dataset from kaggle. I randomly selected 5000 movie names and saved them into a csv file called 'title.csv'. After that, I used 'movie.get_movie()' to retrieve each movie's information from OMDB database and saved what I retrieved into a cache file. 

# Data Structure
I used tree structure to save the data. It has three levels, which are years, languages and length of movies (greater than 100 minutes or not). The repo contains a json file called 'tree.json'

# Interaction and Presentation Options
In this program, users will be promoted to five different options, which are 0(exit), 1(statistical information of movies in each year), 2(statistical information of movies with different languages), 3(statistical information of the length of each movie), 4 (movie recommendations). Option 1 to Option 3 will be displayed as in the format of graph. Option 4 will promote users with three questions and recommend movies to them. These three questions are 'Which year would you like to enter (2001 - 2020)', 'Which language would you like to enter' and 'whether the movie is longer than 100 minutes or not.' In the end, users should get personalized movie recommendations based on their answers. 


# Demo Link 
