
import os
import requests

def search_images(query: str, per_page: int = 1) -> list[str]:
    UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY")
    if not UNSPLASH_ACCESS_KEY:
        raise ValueError("UNSPLASH_ACCESS_KEY environment variable not set.")

    headers = {
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
    }
    params = {
        "query": query,
        "per_page": per_page
    }
    response = requests.get("https://api.unsplash.com/search/photos", headers=headers, params=params)
    response.raise_for_status() # Raise an exception for HTTP errors

    data = response.json()
    image_urls = []
    for photo in data.get("results", []):
        image_urls.append(photo["urls"]["regular"])
    return image_urls

if __name__ == '__main__':
    # For testing purposes
    # UNSPLASH_ACCESS_KEYを環境変数に設定してください
    # export UNSPLASH_ACCESS_KEY="YOUR_UNSPLASH_ACCESS_KEY"
    sample_query = "AI technology"
    try:
        urls = search_images(sample_query)
        if urls:
            print(f"Found image URL: {urls[0]}")
        else:
            print("No images found.")
    except Exception as e:
        print(f"Error searching images: {e}")


