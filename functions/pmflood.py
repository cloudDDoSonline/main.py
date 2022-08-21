import asyncio
import random
import os
from rich.prompt import Prompt, Confirm
from rich.console import Console

from functions.function import Function

console = Console()


class PmFloodFunc(Function):
    """Flood to PM"""

    async def flood(self, session, peer, text, media):
        count = 0
        errors = 0

        async with self.storage.ainitialize_session(session):
            me = await session.get_me()

            while True:
                try:
                    if not media:
                        await session.send_message(peer, text)
                    else:
                        file = random.choice(os.listdir("media"))

                        await session.send_file(
                            peer,
                            os.path.join("media", file),
                            caption=text,
                            parse_mode="html"
                        )
                except Exception as err:
                    console.print(
                        "[{name}] [bold red]not sent.[/] {err}"
                        .format(name=me.first_name, err=err)
                    )

                    if errors >= 5:
                        break

                    errors += 1
                else:
                    count += 1
                    console.print(
                        "[{name}] [bold green]sent.[/] COUNT: [yellow]{count}[/]"
                        .format(name=me.first_name, count=count)
                    )
                finally:
                    await self.delay()

    async def execute(self):
        self.ask_accounts_count()

        peer = console.input("[bold red]enter uid or username> [/]")
        media = Confirm.ask("[bold red]media")
        text = console.input("[bold red]text> [/]")

        delay = Prompt.ask(
            "[bold red]delay[/]",
            default="-".join(str(x) for x in self.settings.delay)
        )

        self.settings.delay = self.parse_delay(delay)

        await asyncio.wait([
            self.flood(session, peer, text, media)
            for session in self.sessions
        ])
