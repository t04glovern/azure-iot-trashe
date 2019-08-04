# Camera Capture Module Deploy

Similar to the Blinker module we will now deploy a Camera Capture module for the attached webcam

## Build & Push Container

Update the code in [modules/camera-capture/module.json](../modules/camera-capture/module.json) to the correct registry. Then to deploy, either install the [Azure IoT Edge extension](https://github.com/microsoft/vscode-azure-iot-edge) then right click `module.json` and run Build and Push.

Alternatively run the following substituting in the correct information

```bash
docker build  --rm -f ./modules/camera-capture/Dockerfile.arm32v7 -t glover.azurecr.io/camera-capture:0.0.1-arm32v7 ./modules/camera-capture && docker push glover.azurecr.io/camera-capture:0.0.1-arm32v7
```

**NOTE**: You might need to re-login to ACR with `az acr login --name "glover"`

## Include Module

Update the `deployment.template.json` file with the image details that will be deployed to the Pi. You can replace the Blinker code (remove it now if you want)

```json
"camera-capture": {
  "version": "1.0",
  "type": "docker",
  "status": "running",
  "restartPolicy": "always",
  "settings": {
    "image": "${MODULES.camera-capture.arm32v7}",
    "createOptions": {
      "Env": [
        "VIDEO_PATH=0",
        "RESIZE_WIDTH=352",
        "RESIZE_HEIGHT=288",
        "SHOW_VIDEO=True"
      ],
      "HostConfig": {
        "PortBindings": {
          "5678/tcp": [{
            "HostPort": "5678"
          }]
        },
        "Devices": [{
            "PathOnHost": "/dev/video0",
            "PathInContainer": "/dev/video0",
            "CgroupPermissions": "mrw"
          },
          {
            "PathOnHost": "/dev/snd",
            "PathInContainer": "/dev/snd",
            "CgroupPermissions": "mrw"
          }
        ]
      }
    }
  }
}
```

## Testing Camera

Navigate to [http://raspberrypi.local:5012](http://raspberrypi.local:5012) on your local network to view the feed

![Nathan Test Image 2](img/nathan-test-image-02.png)

## Attribution

* [CameraCapture Example](https://github.com/Azure-Samples/Custom-vision-service-iot-edge-raspberry-pi/tree/master/modules/CameraCapture)
