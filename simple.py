from picrawler import Picrawler
from time import sleep

crawler = Picrawler()
speed = 80

def main():
    while True:
        # Move forward
        crawler.do_action('forward', 2, speed)
        sleep(0.05)
        
        # Move backward
        crawler.do_action('backward', 2, speed)
        sleep(0.05)

if __name__ == '__main__':
    main()
