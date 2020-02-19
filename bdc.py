# bdc - bloated discord client
# a <100 LOC minimal curses discord client that can change channels (wow! so cool!)
# **written by null over a grueling long weekend and tuesday study hall**

import curses, discord, asyncio

stdscr = curses.initscr()
height, width = curses.LINES, curses.COLS

class bdc_client(discord.Client):
    # TODO: store current channel DONE
    # TODO: non-blocking message input, research curses textbox DONE
    # TODO: ghetto on_ready, just wait 1.5 seconds

    line = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.text_win = curses.newwin(height - 2, width, 0, 0)
        self.text_win.refresh()

        self.input_win = curses.newwin(1, width, height - 1, 0)
        self.input_win.echo()
        self.input_win.refresh()

        self.messaging_daemon = self.loop.create_task(self.send_message())

    async def on_ready(self):
        # on_ready not running, see: https://github.com/Rapptz/discord.py/issues/2567
        # throwing error because its executing before client is ready
        self.current_channel = discord.utils.get(self.get_all_channels(), name="<defualt channel name>") # default channel, possibly not needed
        self.text_win.addstr(self.line, 0, "logged in as" + self.user.name)

    async def on_message(self, message):
        if(message.channel != self.current_channel):
            return

        if(self.line >= height-2):
            self.text_win.clear()
            self.line = 0

        self.text_win.addstr(self.line, 0, message.author.name + ": " + message.content)
        self.text_win.refresh()
        self.line += 1

    async def send_message(self):
        await self.wait_until_ready()

        while not self.is_closed():
            # block but only the while loop should be blocked, not on_message
            # no way to test this until the bug gets patched :|
            input_text = self.input_win.getstr().decode("utf-8")

            if(len(input_text) > 0 and input_text[0] == "/"):
                command = input_text[1:]
                if(command == "exit"):
                    curses.endwin()
                    await self.close()
                elif(command == "join"):
                    ch = discord.utils.get(self.get_all_channels(), name=input_text.split(" ")[1]) # arg
                    if(ch != None):
                        self.current_channel = ch
            else:
                await self.current_channel.send(input_text)

client = bdc_client()
client.run("<token>", bot=False)
