# from cripto.spiders.cripto import ScrapingDriftSpider
# from twisted.internet import reactor
# from twisted.internet.task import LoopingCall
# import schedule
import time
import subprocess

drift = ["scrapy", "crawl", "drift"]
kamino = ["scrapy", "crawl", "kamino"]

# schedule.every(1).minute.do(subprocess.Popen(cmd).wait())
# while True:
#     schedule.run_pending()


starttime = time.monotonic()
while True:
    subprocess.run(drift)
    subprocess.run(kamino)
    time.sleep(60.0 - ((time.monotonic() - starttime) % 60.0))
