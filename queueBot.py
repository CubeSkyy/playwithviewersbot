import random
from twitchio.ext import commands

class QueueBot(commands.Bot):
    def __init__(self, token, prefix, initial_channels):
        super().__init__(token=token, prefix=prefix, initial_channels=initial_channels)
        self.queue = []
        self.queue_closed = True
        self.allowed_users = ['cubesky', 'charmies']  # Add your predetermined users here

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @commands.command(name='join')
    async def join_command(self, ctx):
        if not self.queue_closed or ctx.author.name in self.allowed_users:
            if ctx.author.name not in self.queue:
                self.queue.append(ctx.author.name)
                await ctx.send(f'@{ctx.author.name} joined the queue. Position: {len(self.queue)}')
            else:
                await ctx.send(f'@{ctx.author.name}, you are already in the queue.')
        else:
            await ctx.send(f'@{ctx.author.name}, the queue is currently closed.')

    @commands.command(name='leave')
    async def leave_command(self, ctx):
        if ctx.author.name in self.queue:
            self.queue.remove(ctx.author.name)
            await ctx.send(f'@{ctx.author.name} left the queue.')
        else:
            await ctx.send(f'@{ctx.author.name}, you are not in the queue.')

    @commands.command(name='queue')
    async def queue_command(self, ctx):
        queue_list = self.format_queue()
        await ctx.send(f'Queue: {queue_list}')

    @commands.command(name='next')
    async def next_command(self, ctx):
        if len(self.queue) >= 4:
            next_players = self.queue[4:min(len(self.queue), 8)]
            self.queue = self.queue[4:]
            formatted_next_players = [f"{player} [NEXT]" for player in next_players]
            await ctx.send(f'Next game: {", ".join(formatted_next_players)}')
        else:
            self.queue = []
            await ctx.send('Next game: ')

    @commands.command(name='close')
    async def close_command(self, ctx):
        if ctx.author.name in self.allowed_users:
            self.queue_closed = True
            await ctx.send('Queue is now closed.')

    @commands.command(name='open')
    async def open_command(self, ctx):
        if ctx.author.name in self.allowed_users:
            self.queue_closed = False
            await ctx.send('Queue is now open.')

    @commands.command(name='remove')
    async def remove_command(self, ctx, user: str):
        if ctx.author.name in self.allowed_users:
            if user in self.queue:
                self.queue.remove(user)
                await ctx.send(f'{user} removed from the queue.')
            else:
                await ctx.send(f'{user} is not in the queue.')
        else:
            await ctx.send(f'@{ctx.author.name}, you do not have permission to use !remove.')

    async def event_message(self, message):
        if message.echo:
            return
        print(message.content)
        await self.handle_commands(message)

    def format_queue(self):
        live_players = self.queue[:4]
        next_players = self.queue[4:8]
        after_players = self.queue[8:20]
        formatted_queue = [f"@{player} [LIVE]" for player in live_players] + [f"@{player} [NEXT]" for player in next_players] + [f"@{player}" for player in after_players]
        return ', '.join(formatted_queue) if formatted_queue else 'Empty'


if __name__ == "__main__":
    bot = QueueBot(token="token", prefix='!', initial_channels=['cubesky'])
    bot.run()
