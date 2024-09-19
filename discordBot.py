import discord
from discord.ext import commands
import json
import datetime
import requests

# Configure Token from config.json
with open("config.json") as config_file:
    config = json.load(config_file)
discordToken = config["tokenDiscord"]
weatherApi = config["weatherApi"]

# Define the intents
intents = discord.Intents.default()
intents.message_content = True  # Ensure that your bot can read message content


# Custom help command
class CustomHelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="Help", description="Here are the available commands:"
        )
        prefix = self.context.prefix  # Get the prefix from the context
        for cog, cmds in mapping.items():
            for cmd in cmds:
                if cmd:
                    embed.add_field(
                        name=f"{prefix}{cmd.name}",
                        value=cmd.help or "No description provided.",
                        inline=False,
                    )
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(
            title=f"Help: {command.name}",
            description=command.help or "No description provided.",
        )
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(
            title=f"Help: {cog.qualified_name}",
            description="Here are the commands in this category:",
        )
        prefix = self.context.prefix  # Get the prefix from the context
        for command in cog.get_commands():
            embed.add_field(
                name=f"{prefix}{command.name}",
                value=command.help or "No description provided.",
                inline=False,
            )
        await self.get_destination().send(embed=embed)


# Set up the bot with custom help command
bot = commands.Bot(
    command_prefix="!", intents=intents, help_command=CustomHelpCommand()
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def author(ctx):
    """
    Sends a message with the author's name.
    Ussage: !author
    """
    await ctx.send(
        "This is bot is created by Arif. You can contact me on Instagram @arifswn."
    )


@bot.command()
async def hello(ctx):
    """
    Sends a greeting message.
    Usage: !hello
    """
    await ctx.send("Hello! I'm a bot. Can I help you?")


@bot.command()
async def cuaca(ctx, *, location: str = None):
    """
    Fetches weather information for the specified location.
    Usage: !cuaca <location>
    """
    if not location:
        await ctx.send("Please provide a location. Usage: !cuaca <location>")
        return

    # API URL Weather
    weather_api_url = "https://api.openweathermap.org/data/2.5/weather"

    try:
        response = requests.get(
            weather_api_url,
            params={
                "q": location,
                "appid": weatherApi,
                "units": "metric",  # Change to imperial for Fahrenheit / metric for Celsius
            },
        )
        weather_data = response.json()

        if weather_data["cod"] != 200:
            await ctx.send(
                "Sorry, I was unable to retrieve the weather information for that location."
            )
            return

        temperature = weather_data["main"]["temp"]
        condition = weather_data["weather"][0]["description"]
        location_name = weather_data["name"]
        await ctx.send(
            f"The current weather in {location_name} is {condition} with a temperature of {temperature}°C."
        )
    except Exception as e:
        await ctx.send("Sorry, I was unable to retrieve the weather information.")


@bot.command()
async def jam(ctx):
    """
    Displays the current time.
    Usage: !jam
    """
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    await ctx.send(f"The current time is {current_time}.")


@bot.command()
async def hariini(ctx):
    """
    Display the current date. Provides the day, month, and year.
    Usage: !hariini
    """
    now = datetime.datetime.now()
    day_of_week = now.strftime("%A")
    date_today = now.strftime("%d %B %Y")
    await ctx.send(f"Today is {day_of_week}, {date_today}.")


if __name__ == "__main__":
    bot.run(discordToken)
