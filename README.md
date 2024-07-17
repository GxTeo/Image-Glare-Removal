## Folder Navigation Overview

This section provides an overview of the key components within the project structure, detailing the purpose and location of each artefact.

### Artefacts

- **Artefact 1**: Jupyter Notebook for GCNet Model
  - **Location**: `notebook/GCNet.ipynb`
  - **Description**: This Jupyter Notebook contains the model training and evaluation for the assignment

- **Artefact 2**: Inference Endpoint
  - **Location**: `endpoint/infer.py`
  - **Description**: Source code for the API endpoints

- **Artefact 3**: Docker Configuration
  - **Location**: `Dockerfile`

- **Artefact 4**: Endpoint Testing Script
  - **Location**: `script/test_endpoint.py`
  - **Description**: A test script to test the functionality and responsiveness of the model's inference endpoint.


## Virtual Environment

First, navigate to your project directory in the terminal. Then, create a virtual environment by running:

```bash
python3 -m venv virtualenv
```

Activate the virtual environment.
```bash
source virtualenv/bin/activate
```

Install Required Packages
```bash
pip install -r requirements.txt
```

## Build the Docker Image

To build the Docker image for the FastAPI application, navigate to the project's root directory where the Dockerfile is located and run the following command:

```bash
docker build -t glare-removal-api .
```

## Run the docker container
```bash
docker run -d -p 4000:4000 glare-removal-api
```

## Test the API endpoints

In your terminal, navigate to the ```script``` folder and run the test script with the following command

```bash
pytest test_endpoint.py
```

The API ```infer``` endpoint expect a single image for inference and returns the JSON response containing the binary value of the enhanced image

In the test script, I was just using a test image from the  ```SD1``` dataset. As the endpoint expects a single glare image, there was a need to crop the glare image. The output image would be saved in the ```script``` folder as ```predicted_image.png```.