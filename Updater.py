import feedparser
import time
import socket
import threading

class RssThread(threading.Thread):
    def __init__(self, rss_url, file_name):
        self.rss_url = rss_url
        self.file_name = file_name
        super().__init__()

    def run(self):
        while True:
            # Get Previous contents
            with open(self.file_name, 'r') as file:
                prev_contents = file.read()

            # Check and extract data for QUOTE and SPECIAL
            if self.rss_url == rss_links[3][0] or self.rss_url == rss_links[6][0]:
                try:
                    feed = feedparser.parse(self.rss_url)
                    if feed.entries:
                        with open(self.file_name, 'w') as file:
                            file.write('<hr>')
                            count = 1
                            for entry in feed.entries:
                                file.write('<h2>' + entry.title + '</h2>'+ '<p>"' + entry.description + '"</p>'+'<hr>')
                                count+=1
                                if count == 3:
                                    break
                except:
                    with open(self.file_name, 'w') as file:
                        file.write(prev_contents)

            # Check and extract data for P-NUMBER
            elif self.rss_url == rss_links[5][0]:
                try:
                    feed = feedparser.parse(self.rss_url)
                    if feed.entries:
                        with open(self.file_name, 'w') as file:
                            entry = feed.entries[0]
                            file.write(entry.title+'\n'+entry.description)
                            
                except:
                    with open(self.file_name, 'w') as file:
                        file.write(prev_contents)

            # Extract data for other pages
            else:
                try:
                    feed = feedparser.parse(self.rss_url)
                    if feed.entries:
                        with open(self.file_name, 'w') as file:
                            count = 1
                            for entry in feed.entries:
                                file.write('<h2>' + entry.title + '</h2>'+'<hr>')
                                count+=1
                                if count == num:
                                    break
                except:
                    with open(self.file_name, 'w') as file:
                        file.write(prev_contents)

            # Also extract top label from updates
            if self.rss_url == rss_links[0][0]:
                with open('rss/top.txt', 'r') as file:
                    prev_contents = file.read()
                try:
                    feed = feedparser.parse(self.rss_url)
                    if feed.entries:
                        with open('rss/top.txt', 'w') as file:
                            entry = feed.entries[0]
                            entry2 = feed.entries[1]
                            file.write(entry.title+'\t\t'+entry2.title)
                except:
                    with open('rss/top.txt', 'w') as file:
                        file.write(prev_contents)
            

rss_links = [
        ('https://1-updates.blogspot.com/feeds/posts/default?alt=rss', 'rss/updates.txt'),
        ('https://2-notices.blogspot.com/feeds/posts/default?alt=rss', 'rss/notices.txt'),
        ('https://3-event.blogspot.com/feeds/posts/default?alt=rss', 'rss/events.txt'),
        ('https://4-quote.blogspot.com/feeds/posts/default?alt=rss', 'rss/quote.txt'),
        ('https://5-placements.blogspot.com/feeds/posts/default?alt=rss', 'rss/placements.txt'),
        ('https://6-placed.blogspot.com/feeds/posts/default?alt=rss', 'rss/placed.txt'),
        ('https://7-specials.blogspot.com/feeds/posts/default?alt=rss', 'rss/special.txt')
            ]

num = 10

threads = [RssThread(*link) for link in rss_links]
for thread in threads:
    thread.start()
