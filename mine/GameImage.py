#encoding=utf-8

import json

class GameImage:
    def __init__(self):
        self.data = {}
        with open('images.json') as fin:
            data = json.load(fin)
            for obj in data:
                self.data[ obj["name"] ] = obj
    def get(self, imgName):
        return self.data[imgName]