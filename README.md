# Classifier based Image Sorter
This app can use an image classifier to detect any number of target labels, then sort those images into 1 of 2 folders.

## Requirements
- Sign up for [alwaysAI](https://dashboard.alwaysai.co/auth?register=true)
- Install [alwaysAI tooling](https://dashboard.alwaysai.co/docs/getting_started/development_computer_setup.html)

## Worflow Options
This app can run on either a desktop/laptop development machine or on an edge device such as a Jetson Nano, Dragonboard, or Raspberry Pi that has docker installed. See the above install instruction link for more details.

## Configuration
This app makes use of key-values in the `config.json` file for set up and variable assignments:

Key | Value Type | Description
-----| ---------- | ----------
found_folder | string | Optional location within the app's root folder to put images that have target objects in them. Default is `output_images/found`
empty_folder | string | Optional location within the app's root folder to put images that had no detected target objects. Default is `output_images/not_found`
source_folder | string | Optional location within the app's root folder to process images from. Default is `source_images`
classifier | object | A dictionary with classifier information. See below for expected key-values

Classifier Information:

Key | Value Type | Description
-----| ---------- | ----------
model_id | string | The model id as found from [alwaysAI's Model Catalog](https://dashboard.alwaysai.co/model-catalog/models?category=Classification). Note that there should be a duplicate of this string value in the higher level 'models' key-value pair which is used by alwaysAI's CLI tool. This app has not been keyed to use that string as any number of models may be downloaded to an app for other purposes. To add or remove models for download, see [the docs here](https://docs.alwaysai.co/application_development/application_configuration.html#change-the-computer-vision-model).
confidence_level | float | This is the minimum required confidence level value required by a detected object to be considered found. Each model has a [confidence_level](https://dashboard.alwaysai.co/docs/reference/edgeiq.html#edgeiq.image_classification.ClassificationPrediction) value that's provided with each [classification prediction](https://dashboard.alwaysai.co/docs/reference/edgeiq.html#edgeiq.image_classification.ClassificationResults). Many models will use a float value from 0.0-1.0 with 1.0 = 100%, but some models may have a different value based system, like `squeezenet_v1_1`
target_labels | array of strings | List of all labels this model should be filtering / looking for. This will usually be a subset of all the available labels this model is capable of detecting. If no labels are specified nothing will be returned, in other words the `found_folder` will be empty after processing

## Running
Use the alwaysAI CLI to build and start this app:

Configure (once): `aai app configure`

Build: `aai app install`

Run: `aai app start`

## Support
Docs: https://dashboard.alwaysai.co/docs/getting_started/introduction.html

Community Discord: https://discord.gg/alwaysai

Email: contact@alwaysai.co

