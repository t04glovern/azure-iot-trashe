# Custom Vision Model


## Create Custom Vision Model
Navigate to the [https://www.customvision.ai/projects](https://www.customvision.ai/projects) page.

Create a new project and model selecting the following settings

![Custom Vision Setup 1](img/custom-vision-create-01.png)

Make use of [Trashnet](https://github.com/garythung/trashnet) to build a trash dataset

```bash
wget https://github.com/garythung/trashnet/raw/master/data/dataset-resized.zip
unzip dataset-resized.zip
```

![Custom Vision Setup 2](img/custom-vision-create-02.png)


![Custom Vision Setup 3](img/custom-vision-create-04.png)

Select Quick test to see what your model predicts for unseen images.


![Custom Vision Setup 4](img/custom-vision-trained-test-01.jpg)

With this model, you can build an application around the [REST API for cognitive services](https://azure.microsoft.com/en-au/resources/samples/cognitive-services-rest-api-samples/).
Because this process is so well documented, we wanted to try to deploy this model to an edge IOT device. To do this we are exporting the model as a dockerfile built for a Raspberry Pi.



![Custom Vision Setup 5](img/custom-vision-create-03.png)

Export the model along with the Dockerfile. Replace the `labels.txt` and `model.pb` in `modules/image-classifier/app`
