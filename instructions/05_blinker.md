# Blinker Module Deploy

Update the code in [modules/blinker/module.json](modules/blinker/module.json) to the correct registry. Then to deploy, either install the [Azure IoT Edge extension](https://github.com/microsoft/vscode-azure-iot-edge) then right click `module.json` and run Build and Push.

![Push Edge 1](img/azure-edge-push-01.png)

Alternatively run the following substituting in the correct information

```bash
docker build  --rm -f ./blinker/Dockerfile.arm32v7 -t glover.azurecr.io/blinkler:0.0.1-arm32v7 ./blinker && docker push glover.azurecr.io/blinkler:0.0.1-arm32v7
```

Get your credentials for your repository

```bash
az acr update --name "glover" --admin-enabled true
az acr credential show --name "glover"
```

You need to add credentials for the repository to auth. Change this in `config/deployment.json`

```json
"registryCredentials": {
  "glover": {
    "username": "glover",
    "password": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "address": "glover.azurecr.io"
  }
}
```

Once pushed to ACR, you can update the deployment to the Raspberry Pi. This is also done within the `config/deployment.json` file

```json
"modules": {
  "blinkled": {
    "type": "docker",
    "status": "running",
    "restartPolicy": "always",
    "settings": {
      "image": "glover.azurecr.io/blinkler:0.0.1-arm32v7",
      "createOptions": "{\"HostConfig\":{\"Privileged\": true}}"
    }
  }
}
```

![Push Edge 2](img/azure-edge-push-02.png)
