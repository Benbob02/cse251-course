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
  "people": "http://127.0.0.1:8790/people/", 
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

all_people = {}
all_planets = {}
all_species = {}
all_vehicles = {}
all_starships = {}


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
def getFilm(filmNumber):
  film_Location = f"{TOP_API_URL}/films/{filmNumber}/"
  print(film_Location)
  total = (Request_thread(film_Location))

  total.start()
  total.join()
  global all_people
  people = total.response["characters"]
  planets = total.response["planets"]
  species = total.response["species"]
  vehicles = total.response["vehicles"]
  starships = total.response["starships"]
  add = {}
  add = all_people.copy()
  pos = ""
  for x in people:
    pos = ""
    if x[len(x)-3] != f"/":
      pos = f"{x[len(x)-3]}"
    pos = (f"{pos}{x[len(x)-2]}")
    for i in all_people:
      if i[0] != x:
        add[pos] = x 
    if len(all_people) == 0:
      add[pos] = x 
  all_people = add.copy()

  


def main():
  log = Log(show_terminal=True)
  log.start_timer('Starting to retrieve data from the server')
  threads = []

  # TODO Retrieve Top API urls
  base_t = Request_thread(TOP_API_URL)

  base_t.start()
  base_t.join()
  # TODO Retireve Details on film 6
  # if base_t.response != {}:
  #   for i in base_t.response:
  #     threads.append(Request_thread(base_t.response [i]))


  #   for i in threads:
  #     i.start()
  #   for i in threads:
  #     i.join()
  getFilm(1)
  print(all_people)

  # TODO Display results
  # for i in threads:
  #   print(i.response)
  log.stop_timer('Total Time To complete')
  log.write(f'There were {call_count} calls to the server')
  

if __name__ == "__main__":
  main()
