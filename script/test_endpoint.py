import pytest
import requests
from PIL import Image
import io
import base64


url = "http://127.0.0.1:4000"
@pytest.fixture()
def image_path():
    return "test_glare_image.png"


def test_ping():
    response = requests.get(f"{url}/ping")
    assert response.status_code == 200, "Ping failed"
    assert response.json().get("message") == "pong", "Ping response is not 'pong'"
    print("Ping successful")


def test_infer(image_path):
    files = {"image": open(image_path, "rb")}
    response = requests.post(f"{url}/infer", files=files)

    assert response.status_code == 200, "Inference failed"
    image_binary = base64.b64decode(response.json().get("image"))
    image = Image.open(io.BytesIO(image_binary))
    image.save("predicted_image.png")
    print("Image saved as predicted_image.png")


if __name__ == "__main__":
    pytest.main()