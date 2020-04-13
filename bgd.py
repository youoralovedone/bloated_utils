# bgd - bloated game downloader
# scrapes igggames.com for torrent links and automatically starts them in transmission
# TODO: write a setup.py to make it more normie friendly
# TODO: check crackwatch

print("**** bgd - bloated game downloader ****\na lightweight, normie friendly, script that torrents PC games\n")
print("dependencies: bs4 (pip), transmissionrpc (pip), requests (pip), transmission")
print("     transmission: https://github.com/transmission/transmission-releases/raw/master/transmission-2.94-x64.msi")
print("     pip packages: run in cmd ``pip install <package name>``\n")

name_formatted = input("name of game (space separated): ").replace(" ", "+").lower()

query_url = "https://pcgamestorrents.com/?s=" + name_formatted
print("scraping " + query_url + " ...")
results_page = requests.get(query_url)
results_soup = BeautifulSoup(results_page.text, 'html.parser')
results = results_soup.find_all("h1", class_="uk-article-title")
print("done!\n")
if len(results) == 0:
    exit("game not found on igg, exiting ...")

result_count = 0
for result in results:
    print("(" + str(result_count) + ") " + result.text)
    result_count += 1

result_index = input("\nenter a number or e to exit: ")
if (result_index == "e"):
    exit("download cancelled, exiting ... later king")

game_url = results[int(result_index)].findAll("a")[0].get("href")
print("scraping " + game_url + " for torrent link...")
game_page = requests.get(game_url)
game_soup = BeautifulSoup(game_page.text, 'html.parser')
buffer_url = game_soup.find_all("p", class_="uk-card uk-card-body uk-card-default uk-card-hover")[0].findAll("a")[0].get("href")
print("done!\n")

print("opening buffer in browser ...")
print("wait, click download, then copy the magnet link")
webbrowser.open(buffer_url)
torrent_url = input("paste magnet link, or click \"download torrent\" and enter e to exit: ")
if (torrent_url == "e"):
    exit("torrent started manually, exiting ... good luck soldier, you're on your own")

print("starting transmission, make sure your gui client is open and remote access is enabled...")
tc = transmissionrpc.Client("localhost", port=9091)
if input("are you sure you want to start the download (y/n) ? ") != "y":
    exit("download cancelled, exiting ... peace")
print("adding torrent ...")
tc.add_torrent(torrent_url)
print("torrent started successfully ...\n")

print("once the torrent completes, open the game folder and follow the instructions in the readme")
print("when running the installer, make sure you hit \"copy contents of crack to game folder\"")
print("happy pirating!")
