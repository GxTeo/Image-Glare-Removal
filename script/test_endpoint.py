import requests
from PIL import Image
import io
import base64

url = "http://127.0.0.1:4000"

def test_ping():
    response = requests.get(f"{url}/ping")
    assert response.json() == {"message": "pong"}

    print("Ping test passed")
    return

def test_infer(image_path):
    files = {"image": open(image_path, "rb")}
    response = requests.post(f"{url}/infer", files=files)

    if 'Error' in response.json():
        print(f"Error: {response.json()['Error']}")
        return
    
    image_binary = base64.b64decode(response.json().get("image"))
    image = Image.open(io.BytesIO(image_binary))
    image.save("predicted_image.png")

    print("Image saved as predicted_image.png")
    return


if __name__ == "__main__":
    test_ping()

    # Given that we are using the image from the validation dataset, we need to crop out the glare image
    image_path = "../SD1/val/006.png"
    image = Image.open(image_path)

    width, height = image.size
    truth_image = image.crop((0, 0, width // 3, height))
    glare_image = image.crop((width // 3, 0, (width//3)*2, height))



    # Save the glare image
    glare_image.save("test_glare_image.png")
    test_infer("test_glare_image.png")