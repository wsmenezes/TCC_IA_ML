import pickle5 as pickle

class getModel ():
    def __init__(self, file:str)-> object:
        self.fileModel = file

    def model(self):
        return pickle.load(self.fileModel)