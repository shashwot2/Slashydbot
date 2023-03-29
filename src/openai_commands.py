from utils import chatgptcfg


async def pirate_ai(context, *, message: str):
    persona = "You are a pirate that plunders loot over the high seas and likes to drink rum"
    if len(message) > 75:
        await context.channel.send("Please keep your message under 75 characters")
        return
    response = await chatgptcfg(message, persona)
    await context.channel.send(response)
