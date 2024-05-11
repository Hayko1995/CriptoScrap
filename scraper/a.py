# from cripto.spiders.cripto import ScrapingDriftSpider
# from twisted.internet import reactor
# from twisted.internet.task import LoopingCall
# import schedule
import time
import subprocess

cmd = ["scrapy", "crawl", "drift"]

# schedule.every(1).minute.do(subprocess.Popen(cmd).wait())
# while True:
#     schedule.run_pending()


starttime = time.monotonic()
while True:
    subprocess.run(cmd)
    time.sleep(60.0 - ((time.monotonic() - starttime) % 60.0))
