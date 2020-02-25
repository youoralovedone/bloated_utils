# bdc - bloated discord client
# ~100 LOC curses discord client

import curses, discord, asyncio, time

stdscr = curses.initscr()
height, width = curses.LINES, curses.COLS
curses.echo()

class bdc_client(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start_time = time.time()

        self.text_win = curses.newwin(height - 3, width, 0, 0)
        self.text_win.refresh()
        self.input_win = curses.newwin(1, width, height - 2, 0)
        self.input_win.refresh()
        self.status_win = curses.newwin(1, width, height - 1, 0)
        self.status_win.refresh()

        self.messaging_daemon = self.loop.create_task(self.send_message())

        self.current_channel = None
        self.current_guild = None
        self.line = 0
        self.commands = {"connect": self.bdc_connect, "exit": self.exit, "join": self.join}

    async def bdc_connect(self, input_text):
        if len(input_text.split(" ")) < 2:
            return

        gl = discord.utils.get(self.guilds, name=input_text.split(" ")[1])

        if gl is not None:
            self.current_guild = gl
            self.current_channel = None

    async def exit(self, input_text):
        await self.close()
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    async def join(self, input_text):
        if self.current_guild is None or len(input_text.split(" ")) < 2:
            return

        ch = discord.utils.get(self.current_guild.channels, name=input_text.split(" ")[1])

        if ch is not None and self.current_guild is not None:
            self.current_channel = ch

    async def on_message(self, message):
        if message.channel != self.current_channel:
            return

        if self.line >= height-3:
            self.text_win.clear()
            self.line = 0

        self.text_win.addstr(self.line, 0, message.author.name + ": " + message.content)
        self.text_win.refresh()
        self.line += 1

    async def send_message(self):
            while not self.is_closed():
                if time.time() - self.start_time < 1:
                    self.status_win.addstr(0, 0, "NOT READY" + " " * (width - len("NOT READY") - 1), curses.A_STANDOUT)
                    self.status_win.refresh()
                    continue

                self.status_win.clear()
                self.status_win.refresh()
                status_bar = "Press ENTER to refresh chat | {} | #{}".format(
                    self.current_guild.name if self.current_guild is not None else "~",
                    self.current_channel.name if self.current_channel is not None else "~"
                )

                status_bar += " " * (width - len(status_bar) - 1)
                self.status_win.addstr(0, 0, status_bar, curses.A_STANDOUT)
                self.status_win.refresh()

                input_text = self.input_win.getstr().decode("utf-8")
                self.input_win.clear()

                if len(input_text) > 0 and input_text[0] == "/":
                    command = input_text.split(" ")[0][1:]
                    if command in self.commands.keys():
                        await self.commands.get(command)(input_text)

                elif input_text != "" and self.current_channel is not None:
                        await self.current_channel.send(input_text)

                await asyncio.sleep(0.1)

client = bdc_client()
client.run("<token>", bot=False)
