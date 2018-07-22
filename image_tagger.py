import sys
import json

from google.cloud import exceptions
from google.cloud import storage
from google.cloud import vision
from google.cloud.vision import types


class ImageTagger:
    def __init__(self):
        self.storage_client = storage.Client()
        self.vision_client = vision.ImageAnnotatorClient()
        self.results = {}

    def run(self, bucket_name, output_file):
        """
        Args:
            - bucket name: contains images to be labeled
            - output filename
        """
        try:
            bucket = self.storage_client.get_bucket(bucket_name)
        except exceptions.NotFound:
            print('bucket does not exist')


        #iterate over all objects in bucket
        for i, blob in enumerate(bucket.list_blobs()):
            blob.make_public() #otherwise vision api can't access it
            uid = self.extract_uid(blob.id)
            print(f'processing image #{i+1}: {uid}')
            self.detect_labels(blob.public_url, uid)

        output = json.dumps(self.results, indent=2)
        with open('out.json', 'w') as f:
            f.write(output)
        print('Completed!')

    def extract_uid(self, id):
        """extracts unique identifier of object for *this* collection"""
        return id[10:18]

    def detect_labels(self, uri, uid):
        image = types.Image()
        image.source.image_uri = uri
        response = self.vision_client.label_detection(image=image)
        labels = response.label_annotations

        obj_labels = [] 
        self.results[uid] = obj_labels

        for label in labels:
            label_data = label.description, label.score
            obj_labels.append(label_data)


if __name__ == '__main__':
    bucket_name = sys.argv[1]
    output_file = sys.argv[2]
    ImageTagger().run(bucket_name, output_file)
