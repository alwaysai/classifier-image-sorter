import cv2
import edgeiq
import os
import json
import shutil

"""
Use image classification to sort a batch of images. The
classification labels can be changed by selecting different models.
Different images can be used by updating the files in the *source_images/*
directory.

NOTE: When developing onto a remote device, removing
images in the local *source_images/* directory on your dev machine won't remove images
from the device. They can be removed using the `aai app shell` command and
deleting them from the remote's *source_images/* directory.

To change the computer vision model, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_model.html

NOTE: This app will auto-detect and use an Intel Movidius Neural Compute stick if
present. However, not all models can make use of it!
"""

# Static keys for extracting data from config JSON file
CONFIG_FILE = 'config.json'
CLASSIFIER = 'classifier'
FOUND_FOLDER = 'found_folder'
EMPTY_FOLDER = 'empty_folder'
SOURCE_FOLDER = 'source_folder'
MODEL_ID = 'model_id'
THRESHOLD = 'confidence_level'
TARGETS = 'target_labels'


def load_json(filepath):
    '''
    Convenience to check and load a JSON file
    '''
    if os.path.exists(filepath) is False:
        raise Exception(
            'app.py: load_json: File at {} does not exist'.format(filepath))
    with open(filepath) as data:
        return json.load(data)


def main():

    # 1. Load configuration data from the alwaysai.app.json file
    config = load_json(
        CONFIG_FILE)
    found_folder = config.get(FOUND_FOLDER, 'output_images/found')
    empty_folder = config.get(EMPTY_FOLDER, 'output_images/not_found')
    source_folder = config.get(SOURCE_FOLDER, 'source_images')
    classifier_config = config.get(CLASSIFIER, None)

    # 2. Spin up just the classifier
    model_id = classifier_config.get(MODEL_ID)
    print('app.py: main(): initializing classifier with model id: {}'.format(
        model_id))
    classifier = edgeiq.Classification(model_id)
    classifier.load(engine=edgeiq.Engine.DNN)

    # 3. Loop through all source images
    image_paths = sorted(list(edgeiq.list_images(source_folder + '/')))
    image_count = len(image_paths)
    print("app.py: main: Checking {} images from '{}' folder ...".format(
        image_count, SOURCE_FOLDER))

    for image_path in image_paths:
        # 3a. Load the image to check
        image_display = cv2.imread(image_path)
        image = image_display.copy()

        empty_path = image_path.replace(source_folder, empty_folder)
        confidence = classifier_config.get(THRESHOLD)

        # 3b. Find all objects the classifier is capable of finding
        results = classifier.classify_image(image, confidence)
        if len(results.predictions) == 0:
            # Nothing found with given confidence level - move to the empty folder
            shutil.move(image_path, empty_path)
            continue
        predictions = results.predictions

        # 3c. Filter results by the target labels if specified
        targets = classifier_config.get(TARGETS, None)
        if targets is not None:
            predictions = edgeiq.filter_predictions_by_label(
                results.predictions, targets)
            if len(predictions) == 0:
                # No found labels match taget labels - move to the empty folder
                shutil.move(image_path, empty_path)
                continue

        # 3d. At least one target found, move image to found folder
        _, filename = os.path.split(image_path)
        print('app.py: main: targets found in {}: {}'.format(
            filename, predictions))
        found_path = image_path.replace(source_folder, found_folder)
        shutil.move(image_path, found_path)

    # Print info to console upon completion
    print("app.py: main: Completed sorting of {} images".format(image_count))
    found_images_count = len(
        list(edgeiq.list_images(found_folder)))
    print("app.py: main: {} images in the output folder".format(
        found_images_count))


if __name__ == "__main__":
    main()
