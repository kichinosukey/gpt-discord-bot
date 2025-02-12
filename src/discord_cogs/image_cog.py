# src/discord_cogs/image_cog.py
import discord
from discord import app_commands
from discord.ext import commands
from src.openai_api import dalle_api

class ImageCog(commands.Cog):
    """A Cog for generating images using the DALL·E 3 API.

    Attributes:
        bot (commands.Bot): The Discord bot instance.
    """
    def __init__(self, bot: commands.Bot) -> None:
        """
        Initializes the ImageCog.

        Args:
            bot (commands.Bot): The Discord bot instance.
        """
        self.bot = bot

    @app_commands.command(name="image", description="DALL·E 3 を利用して画像を生成します")
    async def image(self, interaction: discord.Interaction, prompt: str) -> None:
        """
        Generate an image using DALL·E 3 based on the given prompt.

        This command defers the interaction response to allow for the asynchronous
        API call to DALL·E 3. Upon successful image generation, an embed containing
        the generated image is sent to the user. In case of an error, an appropriate
        error message is sent as an ephemeral message.

        Args:
            interaction (discord.Interaction): The interaction context from Discord.
            prompt (str): The text prompt for image generation.
        """
        await interaction.response.defer()
        try:
            # Call the DALL·E 3 API to generate the image
            image_url = await dalle_api.generate_image(prompt)
            embed = discord.Embed(
                title="生成された画像",
                description=f"プロンプト: {prompt}",
                color=discord.Color.blue()
            )
            embed.set_image(url=image_url)
            await interaction.followup.send(embed=embed)
        except Exception as e:
            # Return an error message if image generation fails
            await interaction.followup.send(
                "画像生成に失敗しました。しばらくしてから再度お試しください。",
                ephemeral=True
            )

async def setup(bot: commands.Bot) -> None:
    """
    Adds the ImageCog to the bot.

    Args:
        bot (commands.Bot): The Discord bot instance.
    """
    await bot.add_cog(ImageCog(bot))
