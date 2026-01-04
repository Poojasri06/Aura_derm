import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
import os

# ===== Paths =====
data_dir = "D:/Aura_derm/data set/"
model_save_path = "D:/Aura_derm/models/skin_classifier.pth"

# ===== Image Transforms =====
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# ===== Load Dataset =====
dataset = datasets.ImageFolder(root=data_dir, transform=transform)
class_names = dataset.classes  # Automatically grabs folder names
print("Detected classes:", class_names)

dataloader = DataLoader(dataset, batch_size=16, shuffle=True)

# ===== Build Model =====
class SkinClassifier(nn.Module):
    def __init__(self, num_classes):
        super(SkinClassifier, self).__init__()
        self.model = models.resnet18(pretrained=True)
        self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)

    def forward(self, x):
        return self.model(x)

model = SkinClassifier(num_classes=len(class_names))

# ===== Training Setup =====
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# ===== Train Loop =====
epochs = 10
model.train()
for epoch in range(epochs):
    running_loss = 0.0
    correct = 0
    total = 0

    for images, labels in dataloader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    acc = 100 * correct / total
    print(f"Epoch {epoch+1}/{epochs}, Loss: {running_loss:.4f}, Accuracy: {acc:.2f}%")

# ===== Save Model =====
torch.save(model.state_dict(), model_save_path)
print("✅ Model saved to:", model_save_path)