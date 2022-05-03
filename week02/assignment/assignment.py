"""
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
"python server.py"
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
URL to retrieve other URLs that you can use to retrieve information from the
server.
- You need to match the output outlined in the decription of the assignment.
Note that the names are sorted.
- You are requied to use a threaded class (inherited from threading.Thread) for
this assignment.  This object will make the API calls to the server. You can
define your class within this Python file (ie., no need to have a seperate
file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
  "characters": "http://127.0.0.1:8790/characters/", 
  "planets": "http://127.0.0.1:8790/planets/", 
  "films": "http://127.0.0.1:8790/films/",
  "species": "http://127.0.0.1:8790/species/", 
  "vehicles": "http://127.0.0.1:8790/vehicles/", 
  "starships": "http://127.0.0.1:8790/starships/"
}
"""

from datetime import datetime, timedelta
from urllib import response
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0




# TODO Add your threaded class definition here
class Request_thread(threading.Thread):
  def __init__(self,url):
      threading.Thread.__init__(self)
      self.url = url
      self.response = {}

  def run(self):
      response = requests.get(self.url)
      global call_count
      call_count += 1

      if response.status_code == 200:
          self.response = response.json()
      else:
          print('Response =', response.status_code)

# TODO Add any functions you need here
def get_element_threads(paths):
  threads = []
  for x in paths:
    threads.append(Request_thread(x))
  for x in threads:
    x.start()
  for x in threads:
    x.join()
  return threads

def get_element(movie_info, element):
  return_text = movie_info[element]
  return return_text

def print_element(elements):
  
  full_text = ""
  for x in elements:
    text = x.response ["name"]
    full_text = f"{full_text}{text}, "
  print(full_text)
  print()

def display_movie(movie_info):
  text = ""

  title = get_element(movie_info,"title")
  print(f"Title: {title}")

  director = get_element(movie_info,"director")
  print(f"Director: {director}")

  producer = get_element(movie_info,"producer")
  print(f"Producer: {producer}")

  released = get_element(movie_info,"release_date")
  print(f"Released: {released}")

  characters_paths = get_element(movie_info, "characters")
  characters = get_element_threads(characters_paths)
  print(f"Characters: {len(characters)}")
  print_element(characters)

  species_path = get_element(movie_info, "species")
  species = get_element_threads(species_path)
  print(f"Species: {len(species)}")
  print_element(species)

  vehicles_path = get_element(movie_info, "vehicles")
  vehicles = get_element_threads(vehicles_path)
  print(f"Vehicles: {len(vehicles)}")
  print_element(vehicles)

  starships_path = get_element(movie_info, "starships")
  starships = get_element_threads(starships_path)
  print(f"Starships: {len(starships)}")
  print_element(starships)


  



def main():
  log = Log(show_terminal=True)
  log.start_timer('Starting to retrieve data from the server')
  threads = []

  # TODO Retrieve Top API urls
  base_t = Request_thread(TOP_API_URL)

  base_t.start()
  base_t.join()
  # TODO Retireve Details on film 6
  films = []

  for x in range(1,7):
    film_path = f"{TOP_API_URL}/films/{x}"
    films.append(Request_thread(film_path))

  for x in films:
    x.start()
  for x in films:
    x.join()
  
  # get each movie with a thread

  #

  # TODO Display results
  # for i in threads:
  #   print(i.response)
  for x in films:
    display_movie(x.response)
    print()
  
  log.stop_timer('Total Time To complete')
  log.write(f'There were {call_count} calls to the server')
  

if __name__ == "__main__":
  main()
