import asyncio

import discord
from curl_cffi import requests
from quart import Quart, request, jsonify

from bots import config

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True
keepa_client = discord.Client(intents=intents)
app = Quart(__name__)


@keepa_client.event
async def on_ready():
    print(f"keepa bot is ready {keepa_client.user}")
    await keepa_client.loop.create_task(app.run_task('0.0.0.0', 10081))

@app.post('/send_message')
async def get_message():
    request_data = await request.get_json()

    if not request_data:
        return jsonify({'error': 'channel_id and content are required'}), 400

    data = request_data["data"]
    ping_type = request_data["type"]
    website_name = request_data["website"]

    if not data:
        return jsonify({'error': 'channel_id and content are required'}), 400

    # Send message via the bot
    await notify(data, config.channel_ids[ping_type][website_name])

    return jsonify({'status': 'success'}), 200

async def notify(pings, channel):
    notifications = await get_embeds(pings, "")
    i = 0
    for notification in notifications:
        view = ModalView(pings[i]["link"], pings[i]["price"])
        i += 1
        if len(notification) != 2:
            await send_message(channel, notification, view=view)
        else:
            await send_message(channel, notification[0], notification[1], view=view)

async def send_message(channel, message, file=None, view=None):
    channel = keepa_client.get_channel(channel)
    if not file:
        await channel.send(embed=message, view=view)
    else:
        await channel.send(embed=message, file=file, view=view)


async def run_bot():
    try:
        await keepa_client.start(config.BOT_KEEPA)
    except:
        print("closed")
        await keepa_client.close()


async def get_embeds(prices, website):
    messages = []
    for price in prices:
        keepa_price = round(price['keepa_price'], 2)
        margin = str(round(price["margin"] * 100)) + "%"
        print(price)
        if "file" in price:
            price["image"] = "attachment://thumbnail.jpg"
        link_name = price["name"].replace(" ", "%20").replace("\xa0", "%20")
        mobile_name = link_name.split("%20")
        words_size = min(len(mobile_name), 5)
        mobile_name = "%20".join(mobile_name[0:words_size])
        graph = None
        if price.get("graph"):
            graph = discord.File(price.get("graph"), filename='graph.jpg')
        embed = discord.Embed(
            title="",
            description="",
            color=0x0000ff
        )
        embed.set_thumbnail(url=price["image"])
        if price['match_percentage']:
            embed.add_field(name="Match", value=f"{round(price['match_percentage'] * 100, 2)}%", inline=True)
        embed.add_field(name="Product", value=f"[{price['name']}]({price['link']})", inline=False)
        embed.add_field(name="ASIN", value=f"{price['ASIN']}", inline=False)
        embed.add_field(name="Price", value=f"£{price['price']}", inline=True)
        embed.add_field(name="Average 90 Day Price", value=f"{price['avg']}", inline=False)
        if price.get("monthly_sold"):
            embed.add_field(name="Monthly Sold", value=f"{price['monthly_sold']}",
                            inline=True)
        if price.get("rank_drop"):
            embed.add_field(name="Sales rank drops 30 day", value=f"{price['rank_drop']}",
                            inline=True)
        embed.add_field(name="Expected Profit", value=f"£{round(price['margin'] * price['keepa_price'], 2)}",
                        inline=True)
        embed.add_field(name="Margin", value=f"{round(price['margin'] * 100, 2)}%", inline=True)
        embed.add_field(name="\nLinks: \n", value=f""
                                                  f"[Amazon](https://www.amazon.co.uk/dp/{price['ASIN']}) | "
                                                  f"[Keepa](https://keepa.com/#!product/2-{price['ASIN']}) | "
                                                  f"[SellerAmp](https://sas.selleramp.com/sas/lookup?SasLookup&search_term={price['ASIN']}&sas_cost_price={price['price']}&sas_sale_price={keepa_price})\n",
                        inline=False)
        if graph:
            embed.set_image(url="attachment://graph.jpg")
        if "file" not in price:
            messages.append((embed, [graph]))
        else:
            messages.append((embed, [price["file"], graph]))
    return messages


class ModalView(discord.ui.View):
    def __init__(self, url, price):
        self.url = url
        self.price = price
        super().__init__()

    @discord.ui.button(label="Checkout", style=discord.ButtonStyle.primary, custom_id="checkout")
    async def open_menu_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = ThresholdModal(self.url, self.price)
        await interaction.response.send_modal(modal)


class ThresholdModal(discord.ui.Modal):
    def __init__(self, url, price):
        super().__init__(title="Set Preferences")
        self.url = url

        self.threshold_price = discord.ui.TextInput(
            label="Threshold Price",
            style=discord.TextStyle.short,
            placeholder=f"{price}",
            default=f"{price}",
            required=True
        )
        self.amount = discord.ui.TextInput(
            label="Amount of Items",
            style=discord.TextStyle.short,
            required=True
        )
        self.instances = discord.ui.TextInput(
            label="Number of Instances",
            style=discord.TextStyle.short,
            required=True
        )

        self.add_item(self.threshold_price)
        self.add_item(self.amount)
        self.add_item(self.instances)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            threshold_price = float(self.threshold_price.value)
            amount = int(self.amount.value)
            instances = int(self.instances.value)

            await interaction.response.send_message(
                f"Threshold Price for [item]({self.url}): {threshold_price}\nAmount: {amount}\nInstances: {instances}",
                ephemeral=True
            )

            website_name = get_website_name(self.url)
            requests.post(f"{config.base_host}{config.site_ports[website_name]}/checkout",
                          json={"url":self.url,
                                "price":threshold_price,
                                "number":amount,
                                "tasks":instances})

        except:
            await interaction.response.send_message(
                f"Wrong data, write numbers only into the checkout form, to proceed with checkout",
                ephemeral=True
            )


def get_website_name(url: str):
    return url.replace("www.", "").split(".")[0]


asyncio.run(run_bot())

