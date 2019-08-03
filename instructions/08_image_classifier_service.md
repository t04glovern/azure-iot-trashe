# Image Classifier Service

Similar to the Camera Capture module we will now deploy a Image Classifier module to perform inference at the edge

## Build & Push Container

Update the code in [modules/image-classifier/module.json](modules/image-classifier/module.json) to the correct registry. Then to deploy, either install the [Azure IoT Edge extension](https://github.com/microsoft/vscode-azure-iot-edge) then right click `module.json` and run Build and Push.

Alternatively run the following substituting in the correct information

```bash
docker build  --rm -f ./image-classifier/Dockerfile.arm32v7 -t glover.azurecr.io/image-classifier:0.0.1-arm32v7 ./image-classifier && docker push glover.azurecr.io/image-classifier:0.0.1-arm32v7
```

**NOTE**: You might need to re-login to ACR with `az acr login --name "glover"`

## Include Module

Update the `config/deployment.json` file with the image details that will be deployed to the Pi.

```json
"image-classifier-service": {
  "type": "docker",
  "status": "running",
  "restartPolicy": "always",
  "settings": {
    "image": "glover.azurecr.io/image-classifier:0.0.1-arm32v7",
    "createOptions": ""
  }
}
```

## Update Camera Capture

Update the Camera Capture module to pass on the video feed to the image classifier service by adding the following environment variable `IMAGE_PROCESSING_ENDPOINT`

```json
"env": {
  "VIDEO_PATH": {"value": "0"},
  "IMAGE_PROCESSING_ENDPOINT":  {"value": "http://image-classifier:80/image"},
  "RESIZE_WIDTH":  {"value": "352"},
  "RESIZE_HEIGHT":  {"value": "288"},
  "SHOW_VIDEO":  {"value": "True"}
},
```
