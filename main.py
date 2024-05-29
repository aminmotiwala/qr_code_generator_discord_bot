import discord
import config #remove this config file
from discord import app_commands
import qrcode
import re

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await tree.sync()

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#
#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')

@tree.command(name="generate-text-qr",description="Generate QR code from text/url")
@app_commands.describe(user_input="Input from the user")
async def generate_qr(interaction: discord.Interaction, user_input: str):
    # Generate a QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(user_input)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    # Sanitize the user_input to create a valid filename
    sanitized_input = re.sub(r'[\\/*?:"<>|]', "", user_input)
    file_name = sanitized_input + 'qrcode.png'

    img.save(file_name)

    with open("user_inputs.txt", "a") as file:
        file.write(user_input + "\n")

    with open(file_name, 'rb') as f:
        picture = discord.File(f)
        await interaction.response.send_message("QR code for: "+user_input+" by Amin Motiwala", file=picture)

@tree.command(name="generate-wifi-qr", description="Generate QR code for Wi-Fi connection")
@app_commands.describe(ssid="Wi-Fi SSID", password="Wi-Fi Password")
async def generate_wifi_qr(interaction: discord.Interaction, ssid: str, password: str):
    # Format the Wi-Fi information into a string
    wifi_data = f"WIFI:S:{ssid};T:WPA;P:{password};;"

    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add the Wi-Fi data to the QR code
    qr.add_data(wifi_data)
    qr.make(fit=True)

    # Create an image from the QR code
    qr_image = qr.make_image(fill_color="black", back_color="white")

    qr_image.save(ssid + 'qrcode.png')

    with open("user_inputs.txt", "a") as file:
        file.write(wifi_data)

    with open(ssid + 'qrcode.png', 'rb') as f:
        picture = discord.File(f)
        await interaction.response.send_message("QR code for: " + ssid + " by Amin Motiwala", file=picture)



#add your bot secret here
# example client.run('my-secret-here')
client.run(config.secret_token)