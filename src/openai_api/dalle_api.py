# src/openai_api/dalle_api.py
import aiohttp
from src.constants import DALL_E_API_ENDPOINT, DALL_E_API_KEY

async def generate_image(prompt: str, size: str = "1024x1024") -> str:
    """
    Generate an image using the DALL·E 3 API.

    Sends a POST request to the DALL·E 3 API with the specified prompt and image size.
    If the request is successful, the URL of the generated image is returned.
    In case of an error, an exception is raised.

    Args:
        prompt (str): The text prompt for image generation.
        size (str, optional): The desired image size (e.g., "1024x1024"). Defaults to "1024x1024".

    Returns:
        str: The URL of the generated image.

    Raises:
        Exception: If the API request fails or returns a non-200 status code.
    """
    payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": size
    }
    headers = {
        "Authorization": f"Bearer {DALL_E_API_KEY}",
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(DALL_E_API_ENDPOINT, json=payload, headers=headers) as response:
            if response.status != 200:
                error_text = await response.text()
                raise Exception(f"API Error {response.status}: {error_text}")
            data = await response.json()
            # Extract image URL from the API response; adjust key names as necessary
            image_url = data["data"][0]["url"]
            return image_url
