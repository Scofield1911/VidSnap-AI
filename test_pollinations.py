import requests
import urllib.parse
import os

prompts = ["A futuristic city"]

for i, prompt in enumerate(prompts):
    # Method 1: image.pollinations.ai
    encoded = urllib.parse.quote(prompt)
    url1 = f"https://image.pollinations.ai/prompt/{encoded}?width=1080&height=1920&seed={i}&model=flux"
    print(f"Testing URL 1: {url1}")
    try:
        r1 = requests.get(url1, headers={"User-Agent": "Mozilla/5.0"})
        print(f"Status 1: {r1.status_code}")
        print(f"Content-Type 1: {r1.headers.get('Content-Type')}")
        if "image" in r1.headers.get('Content-Type', ''):
            with open(f"test_img_1_{i}.jpg", "wb") as f:
                f.write(r1.content)
            print("Saved test_img_1.jpg")
        else:
            print("Not an image (1)")
            # print(r1.text[:200])
    except Exception as e:
        print(f"Error 1: {e}")

    # Method 2: pollinations.ai/p
    url2 = f"https://pollinations.ai/p/{encoded}?width=1080&height=1920&seed={i}&model=flux"
    print(f"Testing URL 2: {url2}")
    try:
        r2 = requests.get(url2, headers={"User-Agent": "Mozilla/5.0"})
        print(f"Status 2: {r2.status_code}")
        print(f"Content-Type 2: {r2.headers.get('Content-Type')}")
         
        # Check if it redirects or returns image
        if "image" in r2.headers.get('Content-Type', ''):
            with open(f"test_img_2_{i}.jpg", "wb") as f:
                f.write(r2.content)
            print("Saved test_img_2.jpg")
        else:
            print("Not an image (2)")
            # print(r2.text[:200])

    except Exception as e:
        print(f"Error 2: {e}")
