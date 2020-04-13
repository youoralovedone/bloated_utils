# bgd - bloated game downloader
# scrapes igggames.com for torrent links and automatically starts them in transmission
import requests
from bs4 import BeautifulSoup
import transmissionrpc

query_url = "https://pcgamestorrents.com/?s="
print("welcome to bgd, you could just use your browser like a normal person you autistic fuck")
query_url += input("name of game (space separated): ").replace(" ", "+")

print("scraping " + query_url + " ...")
results_page = requests.get(query_url)
results_soup = BeautifulSoup(results_page.text, 'html.parser')
results = results_soup.find_all("h1", class_="uk-article-title")
print("done!\n")

result_count = 0
for result in results:
    print("(" + str(result_count) + ") " + result.text)
    result_count += 1

result_index = input("\nenter a number or e to exit: ")
if (result_index == "e"):
    exit("see ya later, nerd")

game_url = results[int(result_index)].findAll("a")[0].get("href")
print("scraping " + game_url + " for torrent link...")
game_page = requests.get(game_url)
game_soup = BeautifulSoup(game_page.text, 'html.parser')
torrent_url = game_soup.find_all("p", class_="uk-card uk-card-body uk-card-default uk-card-hover")[0].findAll("a")[0].get("href")
print("done!\n")

print("starting torrent, make sure your transmission client is open...")
tc = transmissionrpc.Client('localhost', port=9091)
print("adding torrent " + torrent_url)
tc.add_torrent(torrent_url)
print("torrent started ... eta: " + tc.get_torrent(1).eta)
exit("imagine paying for shit, fuck capitalism")
