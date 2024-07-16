import requests
from PIL import Image
import io
import base64

url = "http://127.0.0.1:4000"

def test_ping():
    response = requests.get(f"{url}/ping")
    assert response.json() == {"message": "pong"}

    print("Ping test passed")

def test_infer(image_path):
    files = {"image": open(image_path, "rb")}
    response = requests.post(f"{url}/infer", files=files)
    
    image_binary = base64.b64decode(response.json().get("image"))
    image = Image.open(io.BytesIO(image_binary))
    image.save("predicted_image.png")

    print("Image saved as predicted_image.png")

    return


if __name__ == "__main__":
    test_ping()
    test_infer("../SD1/val/006.png")