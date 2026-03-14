import requests
from PIL import Image
from io import BytesIO
import numpy as np

import matplotlib.pyplot as plt

# NASA Mars Rover Photos API endpoint
API_KEY = "DEMO_KEY"  # Replace with your own API key for more requests
API_URL = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"

def fetch_mars_photos(sol=1000, camera="FHAZ", max_photos=5):
    params = {
        "sol": sol,
        "camera": camera,
        "api_key": API_KEY
    }
    response = requests.get(API_URL, params=params)
    data = response.json()
    photos = data.get("photos", [])[:max_photos]
    return [photo["img_src"] for photo in photos]

def show_mars_images(image_urls):
    fig, axes = plt.subplots(1, len(image_urls), figsize=(15, 5))
    if len(image_urls) == 1:
        axes = [axes]
    for ax, url in zip(axes, image_urls):
        img_data = requests.get(url).content
        img = Image.open(BytesIO(img_data))
        ax.imshow(img)
        ax.axis('off')
    plt.suptitle("Mars Rover Images from NASA")
    plt.show()

if __name__ == "__main__":
    print("Fetching Mars images from NASA...")
    image_urls = fetch_mars_photos()
    if image_urls:
        show_mars_images(image_urls)
    else:
        print("No images found for the given parameters.")
        # Example: Calculate and plot the average brightness of each image

        avg_brightness = []
        for url in image_urls:
            img_data = requests.get(url).content
            img = Image.open(BytesIO(img_data)).convert('L')  # Convert to grayscale
            arr = np.array(img)
            avg_brightness.append(arr.mean())

        plt.figure(figsize=(8, 4))
        plt.bar(range(1, len(avg_brightness) + 1), avg_brightness, color='orange')
        plt.xlabel("Image Number")
        plt.ylabel("Average Brightness")
        plt.title("Average Brightness of Mars Rover Images")