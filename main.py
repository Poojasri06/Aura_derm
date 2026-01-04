# main.py

import torch
import torch.nn as nn
from torchvision import models

class SkinClassifier(nn.Module):
    def __init__(self, num_classes=4):
        super(SkinClassifier, self).__init__()
        self.model = models.resnet18(pretrained=False)
        self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)

    def forward(self, x):
        return self.model(x)       
