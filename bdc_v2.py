# couch-talk id: 679470283714854915

# bdc - bloated discord client
# written by null over a grueling long weekend and 1 tuesday study hall

import curses, discord, asyncio, time

stdscr = curses.initscr()
height, width = curses.LINES, curses.COLS
curses.echo()

class bdc_client(discord.Client):
    # TODO: fix input
    # TODO: add guild to /join command
    # TODO: add colors to names and statusbar
    # TODO: write a ghetto on_ready event that can be awaited
    # TODO: update status bar
    # TODO: fix None showing up on boot for no reason?
    # TODO: add errors to status window, red if command doesn't run properly or something

    # gonna have to rewrite all this once the bug gets fixed
    # see: https://github.com/Rapptz/discord.py/issues/2567

    # read about async
    # see: https://realpython.com/async-io-python/

    line = 0
    init = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = time.time()

        self.text_win = curses.newwin(height - 3, width, 0, 0)
        self.text_win.refresh()

        self.input_win = curses.newwin(1, width, height - 2, 0)
        self.input_win.refresh()

        self.status_win = curses.newwin(1, width, height - 1, 0)
        statusbar = "Press ENTER to refresh chat | {} | #{}".format("NO CONNECTION", "~")
        statusbar += " " * (width - len(statusbar)-1)
        self.status_win.addstr(0, 0, statusbar, curses.A_STANDOUT)
        self.status_win.refresh()

        self.messaging_daemon = self.loop.create_task(self.send_message())
        self.current_channel = None

    async def on_message(self, message):
        if(message.channel != self.current_channel):
            return

        if(self.line >= height-3):
            self.text_win.clear()
            self.line = 0

        self.text_win.addstr(self.line, 0, message.author.name + ": " + message.content)
        self.text_win.refresh()
        self.line += 1

    async def send_message(self):
            while not self.is_closed():
                if (not time.time() - self.start_time > 0.5):
                    continue

                curses.echo()
                input_text = self.input_win.getstr().decode("utf-8")
                self.input_win.clear()

                if (len(input_text) > 0 and input_text[0] == "/"):
                    command = input_text.split(" ")[0][1:]

                    if (command == "exit"):
                        await self.close()

                        # reset everything
                        curses.nocbreak()
                        stdscr.keypad(False)
                        curses.echo()
                        curses.endwin()
                    elif (command == "join"):
                        # both of these return errors, possibly chunking problem
                        # ch = discord.utils.get(self.get_all_channels(), guild_name=input_text.split(" ")[1], name=input_text.split(" ")[2])
                        ch = self.get_channel(int(input_text.split(" ")[1]))

                        if (ch != None):
                            self.current_channel = ch
                            statusbar = "Press ENTER to refresh chat | {} | #{}".format(ch.guild.name, ch.name)
                            statusbar += " " * (width - len(statusbar) - 1)
                            self.status_win.addstr(0, 0, statusbar, curses.A_STANDOUT)
                            self.status_win.refresh()
                elif (input_text != "" and self.current_channel != None):
                        await self.current_channel.send(input_text)

                await asyncio.sleep(0.1)

client = bdc_client()
client.run("MjQ0MTc3NDUyNTAxMzAzMjk2.XkLiVw.l0RprUrngz4P5fdwn1nv-2hwKrM", bot=False)
