"""Configuration objects and defaults for the deepfake detector project."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


# Normalization constants taken from ImageNet-pretrained models.
IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)


@dataclass
class DataConfig:
    """Configuration for data loading and preprocessing."""

    frames_per_clip: int = 32
    image_size: Tuple[int, int] = (224, 224)
    num_workers: int = 4
    pin_memory: bool = True


@dataclass
class OptimConfig:
    """Configuration for the optimizer."""

    lr: float = 1e-4
    weight_decay: float = 1e-4
    betas: Tuple[float, float] = (0.9, 0.999)
    eps: float = 1e-8


@dataclass
class TrainingConfig:
    """High-level configuration for model training."""

    train_manifest: Path
    val_manifest: Path
    output_dir: Path = Path("artifacts")
    epochs: int = 10
    batch_size: int = 4
    gradient_clip: float | None = 1.0
    seed: int = 42

    data: DataConfig = DataConfig()
    optim: OptimConfig = OptimConfig()


DEFAULT_CLASS_NAMES = ("real", "fake")

