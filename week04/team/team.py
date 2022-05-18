"""
Course: CSE 251
Lesson Week: 04
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- See in I-Learn

"""

from asyncio import queues
from multiprocessing import Semaphore
import threading
import queue
from cv2 import line
import requests
import json

# Include cse 251 common Python files
from cse251 import *

RETRIEVE_THREADS = 4        # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue

def retrieve_thread(queue, log):  # TODO add arguments
    """ Process values from the data_queue """

    while True:
        # TODO check to see if anything is in the queue
        queue_empty = queue.get()
        if queue_empty == NO_MORE_VALUES:
            return 0
        else:
            url = queue_empty[0]
        # TODO process the value retrieved from the queue
        url_proccessed = requests.get(url)
        # TODO make Internet call to get characters name and log it
        
        if url_proccessed.status_code == 200:
            response = url_proccessed.json()
            log.write(response['name'])
        



def file_reader(queue, log): # TODO add arguments
    """ This thread reading the data file and places the values in the data_queue """
    # TODO Open the data file "data.txt" and place items into a queue

    with open('urls.txt') as file:
        for line in file:
            queue.put(line.split())

    log.write('finished reading file')

    # TODO signal the retrieve threads one more time that there are "no more values"
    for x in range(RETRIEVE_THREADS):
        queue.put(NO_MORE_VALUES)



def main():
    """ Main function """

    log = Log(show_terminal=True)

    # TODO create queue
    characters = queues.Queue()
    # TODO create semaphore (if needed)
    
    # TODO create the threads. 1 filereader() and RETRIEVE_THREADS retrieve_thread()s
    # Pass any arguments to these thread need to do their job
    threads = []
    file_reader(characters,log)
    for x in range(1, RETRIEVE_THREADS + 1):
        t = threading.Thread(target= (retrieve_thread), args= (characters,log))
        threads.append(t)
    t = threading.Thread(target= (file_reader), args= (characters,log))
    threads.append(t)

    log.start_timer()

    # TODO Get them going - start the retrieve_threads first, then file_reader
    for x in threads:
        x.start()
    for x in threads:
        x.join()
    # TODO Wait for them to finish - The order doesn't matter

    log.stop_timer('Time to process all URLS')


if __name__ == '__main__':
    main()




