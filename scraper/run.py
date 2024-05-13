# from cripto.spiders.cripto import ScrapingDriftSpider
# from twisted.internet import reactor
# from twisted.internet.task import LoopingCall
# import schedule
import time
import subprocess
import time
time.sleep(20)

drift = ["scrapy", "crawl", "drift", '--nolog']
kamino = ["scrapy", "crawl", "kamino", '--nolog']
magnifiLand = ["scrapy", "crawl", "marginfi-land", '--nolog']
magnifiBorrow = ["scrapy", "crawl", "marginfi-borrow", '--nolog']
solblaze = ["scrapy", "crawl", "solblaze"]
marinade = ["scrapy", "crawl", "marinade"]

while True:
    subprocess.run(drift)
    subprocess.run(kamino)
    subprocess.run(magnifiLand)
    subprocess.run(magnifiBorrow)
    subprocess.run(solblaze)
    subprocess.run(marinade)
    time.sleep(60.0)
