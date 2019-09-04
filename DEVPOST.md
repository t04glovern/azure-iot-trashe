# Trashè

Trashè is a SmartBin which aim to help you get better at recycling. Making use of Azure Cognitive Services to create a deep learning model to detect plastic, glass and metal recyclables in real time, using Azure IOT Edge to perform inference and transport predictions to other Azure Services.

## Inspiration

---

TODO

## How we built it

---
The architectural block diagram is available here.
![Architecture Diagram](designs/trashe-azure-architecture.png)
At a high level this diagram can be broken into three distinct sections
1. Building a multiclass predictor using [customvision.ai](www.customvision.ai), one of Microsofts Cognitive Services.
2. Using Azures IOT suite to do edge inference on live images provided by a camera connected to a Raspberry Pi
3. Creating a nodejs backend, using azure functions to write data from the IOT Hub into a CosmoDB instance.

Our initial hardware design for this project is to attach the Raspberry Pi, Camera and light to a bin, to do inference on a bins content to see what is recyclable and what isn't.

![Bin Design](designs/trashe-bin-design.jpg)

## Challenges we ran into

---

There were a number of challenges that we ran into during the design and execution phase of this project.

### Gathering the Dataset

A key part of our design was to incorporate a custom Machine Learning model that could classify different kinds of trash. 
While we could have gone the time consuming route of collecting our own images / scraping the internet for images and building our own dataset, we decided to repurpose two existing MIT licened datasets:

* [garythung/trashnet](https://github.com/garythung/trashnet)
* [pedropro/TACO](https://github.com/pedropro/TACO)

These models were built to detect the presence of trash, not to try to classify trash into recyclables and non recyclables, so some manual annotations were required to build the required classes of images.
We classified all our images by hand using the drop and drag interface on [https://customvision.ai](https://customvision.ai). After classifying over 2500 images into 14 classes we had a usable dataset.

After doing the labeling, customvision.ai made it easy to train our model, automatically doing the model selection, test/train split and model training processes. The output of this was a set of predictions and a docker container targeted towards our desired architecture (ARM for a Raspberry Pi).

![CustomVision Prediction Results](designs/custom-ai-prediction-01.jpg)
Based on our results, the outcomes seem perfectly reasonable for the current use-case, especially for a proof of concept of "is this actually possible", and gives us a baseline to move forward from.

### Model Deployment
We'd set ourselves a bit of a challenge: for the actual creation of everything IOT related we would try to do as much service creation and deployment as code, trying to keep our steps repeatable. **** MORE CONTENT, TLDR: Platform as code, try to avoid as much manual work, how we used IOT hub and private container repo to do deployment and how we can push updates*****


### Dark Bin
Surprisingly with all of the technical challenges, one of the problems we encounted was actually simplistic. Our model did not perform well when we attempted it in real life because the lighting of the bin was insufficent to get a clear image. We wanted to avoid manual interaction so a simple lighting system was cobbled together using a small [USB LED light](https://www.altronics.com.au/p/d0385-dimmable-usb-gooseneck-led-light/) we had laying around.

![Lighting Example](designs/trashe-light-example.gif)




## Accomplishments that we're proud of

---

### End to End Solution

Initially we only planned to work on a Vision model, however as we progressed we became more ambitious and eventually built out the end-to-end solution we're submitting now.

### Open Sourced Guide

Another thing we're really proud of is the level of details put into the guide written as we built out this system. Not only should all steps be automated, but they give a good understanding of the decisions made during the development of Trashè.

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

## What we learned

---

This was the first time using Azure and it was great to expereience some of the details in using the platform. 

We particuarly found it surprisingly easy to create a containerised machine learning model using the Azure Cognitive Vision service. Not having to worry about manually deciding a neural network architecture (or reading papers on architectures that are well suited to our specific task) allowed us to remove distractions and focus on how to get to our goal of an end to end system faster.


### Azure Resource Manager

We loved being able to use Azure Resource Manager in order to repeatably deploy the entire backend stack. It really helped when co-working on this project as it meant that both of us knew with certainty that we had the same setups.

### Azure IoT Edge

We learnt that Azure IoT Edge was a great platform to work with in respects to managing containerised deployments to the edge.

It was fantastic to be able to setup the Raspberry Pi on the bin with IoT Edge and then fully manage deployments to it using VSCode and deployment templates.

## What's next for Trashè

The big next technical step for a proper production system is to investigate how to use gathered predictions to further improve the vision model and how to automatically train the model using new data and push to the IOT device if our desired metric has increased.

We would like to increase the number of labels and dataset that we use to do a better job of detecting things that people constantly get wrong when recycling. Eg plastic bags often aren't accepted as recycling, bottles need to have their lids taken off.

It would also be useful to have Trashè be more of standalone unit. We see it being useful for recycling centers to be able to get a better idea of what the composition from each truck is to get a better idea of specific areas where councils can target education programs. It could also be more useful to monitor the metrics of the kinds of materials coming in vs the materials that are actually recycled to monitor things like contamination rates for specific classes of materials.

For consumers we would like to work on making the feedback loop of educating users on what's recyclable and what isn't significantly better.

---
### Further Training Model

As mention above, the model currently has a reasonable accuracy that works fine for this proof of concept, however incorporating more and more annotated data would only further better the product.

The [TACO dataset](http://tacodataset.org/) will be a good group to work with as we can leverage their crowd sourced data, whilst also feeding back in the work we do on annotation.

### Frontend & Mobile Experience

We would like to improve on in the frontend and mobile experience of the system. Most of the work around this project initially has been on the IoT Edge system, and the model for inference; however if we are to productionise this it will need a better user expereience for monitoring and resolving recyling events.

We would also like to build in some databoarding and stats to help users understand what they are throwing away and the impact they can have by recycling.
