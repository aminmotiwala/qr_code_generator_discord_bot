import discord
import config #remove this config file
from discord import app_commands
import qrcode

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

@tree.command(name="generate-qr",description="Generate QR code from text/url")
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
    img.save(user_input+'qrcode.png')

    with open("user_inputs.txt", "a") as file:
        file.write(user_input + "\n")

    with open(user_input+'qrcode.png', 'rb') as f:
        picture = discord.File(f)
        await interaction.response.send_message("QR code for: "+user_input+" by Amin Motiwala", file=picture)

#add your bot secret here
# example client.run('my-secret-here')
client.run(config.secret_token)