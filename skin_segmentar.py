# app/skin_segmenter.py

import torch
import numpy as np
from torchvision import transforms
from PIL import Image
from unetplusplus import UNetPP  # Import your custom UNet++ model

class SkinSegmenter:
    def __init__(self, weights_path):
        self.model = UNetPP(num_classes=3)  # 3: acne, pigmentation, wrinkles
        self.model.load_state_dict(torch.load(weights_path, map_location='cpu'))
        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor()
        ])

    def analyze(self, image_path):
        image = Image.open(image_path).convert("RGB")
        input_tensor = self.transform(image).unsqueeze(0)  # (1, 3, 256, 256)

        with torch.no_grad():
            output = self.model(input_tensor)

        output = torch.softmax(output, dim=1)[0]  # (3, 256, 256)

        # Class labels
        issues = ['acne', 'pigmentation', 'wrinkles']
        predictions = {}

        for i, issue in enumerate(issues):
            prob_map = output[i].numpy()
            if np.mean(prob_map) > 0.05:  # Confidence threshold
                predictions[issue] = True
            else:
                predictions[issue] = False

        return predictions
