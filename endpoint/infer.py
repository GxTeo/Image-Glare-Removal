import sys
sys.path.append("../GCNet")
from GCNet_model import GCNet

import torch
from torchvision import transforms
from torch.utils.data import Dataset


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = GCNet(in_channels=3, out_channels=3).to(device)
model.load_state_dict(torch.load("../checkpoint/best_model.pth", map_location=device),strict=False)

# Freeze all layers
for param in model.parameters():
    param.requires_grad = False

model.eval()

transform = transforms.Compose([
    # change to grayscale
    transforms.Grayscale(),
    transforms.Resize((512, 512)),
    transforms.ToTensor()
])

from typing import List, Union
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

import os
from PIL import Image
from io import BytesIO
import base64


class ImageDataset(Dataset):
    def __init__(self, image_bytes, transform=None):
        self.image_bytes = image_bytes
        self.transform = transform

    def __len__(self):
        return 1  # There's only one image

    def __getitem__(self, idx):
        image = Image.open(BytesIO(self.image_bytes))
        width, height = image.size        
        truth_image = image.crop((0, 0, width // 3, height))
        glare_image = image.crop((width // 3, 0, (width // 3) * 2, height))

        if self.transform:
            truth_image = self.transform(truth_image)
            glare_image = self.transform(glare_image)

            truth_image = truth_image.expand(3, -1, -1)
            glare_image = glare_image.expand(3, -1, -1)

        return glare_image, truth_image

app = FastAPI()

@app.get("/ping")
async def ping():
    try:
        return JSONResponse(content={"message": "pong"})
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {e}"})

@app.post("/infer")
async def infer(image: UploadFile = File(...)):

    try:
        image_bytes = await image.read()
        dataset = ImageDataset(image_bytes, transform=transform)

        for glare_image, truth_image in dataset:
            glare_image = glare_image.unsqueeze(0).to(device)
            truth_image = truth_image.unsqueeze(0).to(device)

            with torch.no_grad():
                predicted_image = model(glare_image)

            predicted_image = predicted_image.squeeze(0).cpu().numpy()
            predicted_image = predicted_image.transpose(1, 2, 0)
            predicted_image= transforms.ToPILImage()(predicted_image)


            # Convert image to binary format
            buffered = BytesIO()
            predicted_image.save(buffered, format="PNG")
            img_binary = buffered.getvalue()
            img_base64 = base64.b64encode(img_binary).decode("utf-8")

            return JSONResponse(content={"image": img_base64})
        
    except Exception as e:
        return JSONResponse(content={"Error": f"Error: {e}"})







 

