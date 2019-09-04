# Trashè

Trashè is a SmartBin which aim to help you get better at recycling.

Making use of Azure IoT Edge we're able to leverage our trash detection model to detect plastic, glass & metals in realtime.

## Design

---

![Design](designs/trashe-bin-design.jpg)

## Architecture

---

![Architecture](designs/trashe-azure-architecture-broken-up.png)

## Setup

---

* [01 - Raspberry Pi Installation](instructions/01_raspberry_pi.md)
* [02 - Azure IoT Edge Software Pre-requisites](instructions/02_azure_iot_edge.md)
* [03 - Azure IoT Hub / Device Setup](instructions/03_azure_iot.md)
* [04 - Azure Container Registry Creation](instructions/04_container_registry.md)
* [05 - Blinker Module Deploy](instructions/05_blinker.md)
* [06 - USB Camera Setup](instructions/06_usb_camera.md)
* [07 - Camera Capture Module Deploy](instructions/07_camera_capture.md)
* [08 - Image Classifier Service](instructions/08_image_classifier_service.md)
* [09 - Custom Vision Model](instructions/09_custom_vision_model.md)
* [10 - Service Bus / Queue Setup](instructions/10_service_bus.md)
* [11 - Queue Processing w/ Azure Function](instructions/11_queue_process.md)
* [12 - CosmosDB Webapp](instructions/12_cosmos_db_webapp.md)
* [13 - Queue Processing Revisited](instructions/13_queue_processing_revisited.md)

## Web

---

![Trasheboard](designs/trasheboard-example.png)

## Attribution

---

* [https://desertbot.io/blog/headless-raspberry-pi-3-bplus-ssh-wifi-setup](https://desertbot.io/blog/headless-raspberry-pi-3-bplus-ssh-wifi-setup)
* [https://docs.microsoft.com/en-au/azure/iot-edge/how-to-install-iot-edge-linux#configure-the-security-daemon](https://docs.microsoft.com/en-au/azure/iot-edge/how-to-install-iot-edge-linux#configure-the-security-daemon)
* [https://www.hackster.io/saka/azure-iot-edge-for-dummies-blink-an-led-e8b2e4](https://www.hackster.io/saka/azure-iot-edge-for-dummies-blink-an-led-e8b2e4)
* [https://github.com/Azure-Samples/Custom-vision-service-iot-edge-raspberry-pi](https://github.com/Azure-Samples/Custom-vision-service-iot-edge-raspberry-pi)
* [https://docs.microsoft.com/en-us/azure/cognitive-services/custom-vision-service/getting-started-build-a-classifier?WT.mc_id=devto-blog-dglover](https://docs.microsoft.com/en-us/azure/cognitive-services/custom-vision-service/getting-started-build-a-classifier?WT.mc_id=devto-blog-dglover)
* [https://github.com/gloveboxes/Creating-an-image-recognition-solution-with-Azure-IoT-Edge-and-Azure-Cognitive-Services](https://github.com/gloveboxes/Creating-an-image-recognition-solution-with-Azure-IoT-Edge-and-Azure-Cognitive-Services)
* [https://dev.to/azure/azure-iot-edge-on-raspberry-pi-buster-plus-tips-for-raspberry-pi-4-22nn](https://dev.to/azure/azure-iot-edge-on-raspberry-pi-buster-plus-tips-for-raspberry-pi-4-22nn)
