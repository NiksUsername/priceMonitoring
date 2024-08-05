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
drop_client = discord.Client(intents=intents)
app = Quart(__name__)


@drop_client.event
async def on_ready():
    print('Logged in as', drop_client.user.name)
    print('------')
    await drop_client.loop.create_task(app.run_task('0.0.0.0', 10080))


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
    notifications = await get_emdeds(pings, "")
    i = 0
    for notification in notifications:
        view = ModalView(pings[i]["link"], pings[i]["price"])
        i += 1
        if len(notification) != 2:
            await send_message(channel, notification, view=view)
        else:
            await send_message(channel, notification[0], notification[1], view=view)

async def send_message(channel, message, file=None, view=None):
    channel = drop_client.get_channel(channel)
    if not file:
        await channel.send(embed=message, view=view)
    else:
        await channel.send(embed=message, files=file, view=view)


async def run_bot():
    try:
        await drop_client.start(config.BOT_DROPS)
    except:
        await drop_client.close()


async def get_emdeds(prices, website):
    messages = []
    for price in prices:
        if price["old_price"] == 0:
            old_price = "n/a"
            change = "n/a"
            continue
        else:
            old_price = f"£{round(price['old_price'], 2)}"
            change = str(round((price["old_price"] - price["price"]) / price["old_price"] * 100)) + "%"
        print(price)
        if "file" in price:
            price["image"] = "attachment://thumbnail.jpg"
        link_name = price["name"].replace(" ", "%20").replace("\xa0", "%20")
        mobile_name = link_name.split("%20")
        words_size = min(len(mobile_name), 5)
        mobile_name = "%20".join(mobile_name[0:words_size])
        embed = discord.Embed(
            title=f"Price Drop - {change}",
            description="",
            color=0x0000ff
        )
        embed.add_field(name="Product:", value=f"[{price['name']}]({price['link']})")
        embed.add_field(name="New Price:", value=f"£{price['price']}")
        embed.add_field(name="Old Price:", value=f"{old_price}")
        embed.add_field(name="Links:", value= f""
                    f"[Amazon](https://www.amazon.co.uk/s?k={link_name}) | "
                    f"[Keepa](https://keepa.com/#!search/2-{link_name}) | "
                    f"[SellerAmp](https://sas.selleramp.com/sas/lookup?SasLookup&search_term={link_name}) | "
                    f"[SellerAmp(Mobile)](https://sas.selleramp.com/sas/lookup?SasLookup&search_term={mobile_name})\n",)

        embed.set_thumbnail(url=price["image"])
        if "file" not in price:
            return_message = embed
        else:
            return_message = (embed, price["file"])
        messages.append(return_message)
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