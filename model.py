import onnxruntime as ort
import numpy as np
from PIL import Image


class Model:
    def __init__(self, path) -> None:
        self.session = ort.InferenceSession(path)
        self.img_size = self.session.get_inputs()[0].shape[1:3][::-1]
        self.classes = [
            "Bird",
            "Blank",
            "Buffalo_African",
            "Cat_Golden",
            "Chevrotain_Water",
            "Chimpanzee",
            "Civet_African_Palm",
            "Duiker_Blue",
            "Duiker_Red",
            "Duiker_Yellow_Backed",
            "Elephant_African",
            "Genet",
            "Gorilla",
            "Guineafowl_Black",
            "Guineafowl_Crested",
            "Hog_Red_River",
            "Human",
            "Leopard_African",
            "Mandrillus",
            "Mongoose",
            "Mongoose_Black_Footed",
            "Monkey",
            "Pangolin",
            "Porcupine_Brush_Tailed",
            "Rail_Nkulengu",
            "Rat_Giant",
            "Rodent",
            "Squirrel",
        ]

    def _preprocess_image(self, img: Image.Image):
        img = img.resize(self.img_size).convert("RGB")
        x = np.array(img).astype(np.float32) / 255
        x = np.expand_dims(x, 0)
        return x

    def predict(self, img: Image.Image):
        A = self._preprocess_image(img)
        y_pred = self.session.run(None, {"input": A})[0][0]
        label = self.classes[np.argmax(y_pred)]
        confidence = y_pred.max()
        return label, confidence
