import discord
from discord.ext import tasks
from scraper.pokemon import scrape_pokemon
from scraper.onepiece import scrape_onepiece
from scraper.football import scrape_football
from ai.classify import classify_release
from db.store import is_new, save_release
from config import DISCORD_TOKEN

CHANNEL_NAMES = {
    "pokemon": "pokemon-releases",
    "onepiece": "onepiece-releases",
    "football": "football-releases"
}

channel_ids = {}

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

    guild = client.guilds[0]

    # Create channels if they don't exist
    for key, name in CHANNEL_NAMES.items():
        channel = discord.utils.get(guild.channels, name=name)
        if channel is None:
            channel = await guild.create_text_channel(name)
        channel_ids[key] = channel.id

    check_releases.start()

@tasks.loop(minutes=60)
async def check_releases():
    sources = [
        ("pokemon", scrape_pokemon),
        ("onepiece", scrape_onepiece),
        ("football", scrape_football)
    ]

    for category, scraper in sources:
        releases = scraper()
        for r in releases:
            if is_new(r["url"]):
                result = classify_release(r["description"])

                if result["is_release"]:
                    await send_release(
                        category,
                        r["title"],
                        r["url"],
                        result["summary"]
                    )
                    save_release(r)

async def send_release(category, title, url, summary):
    channel_id = channel_ids.get(category)
    if channel_id:
        channel = client.get_channel(channel_id)
        await channel.send(
            f"🔥 **New {category.capitalize()} Release Detected!**\n"
            f"**{title}**\n"
            f"{summary}\n"
            f"{url}"
        )

client.run(DISCORD_TOKEN)
