# Datasets for Image Enhancement Model Training

## 📋 Quick Reference

If you decide to train a custom deep learning model, here are the recommended datasets:

---

## 🏆 Top Recommended Datasets

### 1️⃣ DIV2K (BEST FOR SUPER-RESOLUTION)
**Recommended: ⭐⭐⭐⭐⭐**

| Property | Details |
|----------|---------|
| **Full Name** | Diverse 2K Resolution Image Database |
| **Size** | 800 training + 100 validation images |
| **Resolution** | Up to 2560×1440 (2K) |
| **Image Count** | 900 images |
| **Quality** | High-quality, diverse subjects |
| **URL** | https://data.vision.ee.ethz.ch/cvl/DIV2K/ |
| **File Size** | ~20 GB total |
| **Best For** | ✅ Sharpening, upscaling, super-resolution |
| **Training Time** | 24-48 hours (GPU) |
| **Paper** | "DIV2K: A Large-Scale Diverse Image Database for Image Restoration" |

**Why Use DIV2K:**
- Standard benchmark for super-resolution
- Diverse image types (nature, urban, people, etc.)
- High resolution for training
- Widely used in research
- Pre-split training/validation sets

**Download:**
```bash
# Use official script
git clone https://github.com/chaofuturecoder/BasicSR.git
cd BasicSR
python scripts/download_datasets.py DIV2K
```

---

### 2️⃣ Flickr2K (PROFESSIONAL PHOTOS)
**Recommended: ⭐⭐⭐⭐⭐**

| Property | Details |
|----------|---------|
| **Full Name** | Flickr 2K Images |
| **Size** | 2,650 images |
| **Resolution** | 2K minimum (varied) |
| **Quality** | Professional quality |
| **URL** | https://github.com/xinntao/BasicSR/wiki |
| **Best For** | ✅ Realistic real-world images |
| **File Size** | ~15 GB |
| **Training Time** | 30-60 hours (GPU) |

**Complementary to DIV2K:**
- Professional photographer images
- Real-world degradation patterns
- More natural variations
- Often combined with DIV2K

---

### 3️⃣ BSD68 (NOISE REDUCTION)
**Recommended: ⭐⭐⭐⭐**

| Property | Details |
|----------|---------|
| **Size** | 68 test images |
| **Resolution** | 512×512 (typical) |
| **Category** | Natural image denoising |
| **URL** | http://www.eecs.berkeley.edu/Research/Projects/CS194/ |
| **Best For** | ✅ Noise reduction, denoising training |
| **Training Time** | 10-20 hours |

---

### 4️⃣ ImageNet (LARGE SCALE)
**Recommended: ⭐⭐⭐ (for general features)**

| Property | Details |
|----------|---------|
| **Size** | 1.4 million images |
| **Categories** | 1,000 object classes |
| **Resolution** | Varied (100x100 to 5000x5000) |
| **URL** | http://www.image-net.org/ |
| **Best For** | ✅ Pre-training, feature extraction |
| **Training Time** | Weeks on GPU cluster |
| **Note** | Requires registration |

**Usage Tip:**
Use pre-trained ImageNet models as backbone to speed up training

---

### 5️⃣ COCO (COMPLEX SCENES)
**Recommended: ⭐⭐⭐⭐**

| Property | Details |
|----------|---------|
| **Full Name** | Common Objects in Context |
| **Size** | 330,000 images |
| **Annotations** | 5 captions per image |
| **Resolution** | Varied |
| **URL** | https://cocodataset.org/ |
| **Best For** | ✅ Context-aware enhancement, scene understanding |
| **Training Time** | weeks |

---

## 🎯 Choose Your Dataset Based on Goal

### Goal: Blur Restoration
**Use: DIV2K + Flickr2K**
```python
# Download both
python download_datasets.py DIV2K Flickr2K

# Combine into single training set
# ~4900 images total
# Training time: 50-80 hours
```

### Goal: Super-Resolution (2x/3x/4x upscaling)
**Use: DIV2K**
```python
# Standard benchmark
# Already in correct format for SR tasks
python download_datasets.py DIV2K
```

### Goal: Noise Reduction
**Use: BSD68 + SISR**
```python
# BSD68 for testing
# Train on augmented natural images
python download_datasets.py BSD68
```

### Goal: General Image Enhancement
**Use: DIV2K + Flickr2K + COCO**
```python
# Most comprehensive
# Diverse images and scenarios
# Training time: 100+ hours
```

---

## 📊 Dataset Comparison Table

| Dataset | Size | Resolution | Purpose | Training Time | Quality |
|---------|------|-----------|---------|---------|---------|
| **DIV2K** | 900 imgs | 2K | Super-res | 24-48h | ⭐⭐⭐⭐⭐ |
| **Flickr2K** | 2,650 imgs | 2K+ | Real-world | 30-60h | ⭐⭐⭐⭐⭐ |
| **ImageNet** | 1.4M imgs | Varied | Pre-train | Weeks | ⭐⭐⭐⭐ |
| **COCO** | 330K imgs | Varied | Complex | 40-80h | ⭐⭐⭐⭐ |
| **BSD68** | 68 imgs | 512x512 | Denoise | 10-20h | ⭐⭐⭐⭐ |
| **Set14** | 14 imgs | Varied | Benchmark | Testing | ⭐⭐⭐ |
| **Set5** | 5 imgs | Varied | Benchmark | Testing | ⭐⭐⭐ |

---

## 🚀 Quick Start Setup

### Step 1: Install Dataset Tools
```bash
pip install datasets basicsr
```

### Step 2: Download DIV2K (Easiest)
```bash
# Using BasicSR
from basicsr.archs.rrdbnet_arch import RRDBNet
from basicsr.data import build_dataloader

# Automatically downloads DIV2K
config = dict(
    name='DIV2K',
    type='DIV2KDataset'
)
```

### Step 3: Prepare Custom Dataset
```python
# Your own images
dataset_structure = """
data/
├── train/
│   ├── HR/
│   │   ├── img1.jpg
│   │   ├── img2.jpg
│   │   └── ...
│   └── LR/
│       ├── img1.jpg
│       ├── img2.jpg
│       └── ...
└── val/
    ├── HR/
    └── LR/
"""
```

---

## 💾 Download Instructions

### DIV2K
```bash
# Official download
wget http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_train_HR.zip
wget http://data.vision.ee.ethz.ch/cvl/DIV2K/DIV2K_valid_HR.zip

# Or use script
git clone https://github.com/xinntao/BasicSR
cd BasicSR
python scripts/download_div2k.py
```

### Flickr2K
```bash
# From author's repo
git clone https://github.com/xinntao/BasicSR
# Follow instructions for Flickr2K download
```

### ImageNet
```bash
# Register at: http://www.image-net.org/
# Download via academic access
# Extract to folder structure
```

---

## 🎓 Recommended Training Combinations

### Beginner Setup
**Dataset:** DIV2K only  
**Size:** 900 images  
**Training Time:** 24-48 hours  
**Recommended:** ✅ Start here

```python
config = {
    'dataset': 'DIV2K',
    'train_size': 800,
    'val_size': 100,
    'batch_size': 32,
    'epochs': 100
}
```

### Intermediate Setup
**Dataset:** DIV2K + Flickr2K  
**Size:** ~3,550 images  
**Training Time:** 50-80 hours  
**Recommended:** ✅ For production

```python
config = {
    'datasets': ['DIV2K', 'Flickr2K'],
    'total_images': 3550,
    'batch_size': 32,
    'epochs': 100
}
```

### Advanced Setup
**Dataset:** DIV2K + Flickr2K + ImageNet (pre-train)  
**Size:** 1.4M+ images  
**Training Time:** Weeks  
**Recommended:** ✅ For research

---

## 🔗 Download Links

| Dataset | URL | Size |
|---------|-----|------|
| DIV2K | https://data.vision.ee.ethz.ch/cvl/DIV2K/ | 20 GB |
| Flickr2K | https://github.com/xinntao/BasicSR | 15 GB |
| ImageNet | http://www.image-net.org/ | 155 GB |
| COCO | https://cocodataset.org/ | 25 GB |
| BSD68 | http://www.eecs.berkeley.edu/ | 50 MB |
| Set14 | http://people.cs.uchicago.edu/ | 1 MB |
| Set5 | http://people.cs.uchicago.edu/ | 1 MB |

---

## ⚠️ Before Training

### System Requirements
- **GPU:** NVIDIA GTX 1080 minimum (RTX 3080 recommended)
- **RAM:** 16GB minimum (32GB recommended)
- **Storage:** 100GB free space
- **OS:** Linux (recommended), Windows, macOS

### GPU Requirements
| Task | GPU Memory | GPU Type |
|------|-----------|----------|
| DIV2K Training | 6-8GB | GTX 1070+ |
| DIV2K + Flickr2K | 10-12GB | RTX 2080+ |
| Full Setup | 24GB+ | RTX 3090/A6000 |

### Framework Setup
```bash
# PyTorch (Recommended)
pip install torch torchvision pytorch-lightning

# TensorFlow (Alternative)
pip install tensorflow tensorflow-addons

# Training utilities
pip install basicsr tensorboard wandb
```

---

## 📝 Training Example

```python
import torch
from basicsr.archs.rrdbnet_arch import RRDBNet
from basicsr.data import build_dataloader

# Setup
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23)
model = model.to(device)

# Load dataset
data_config = {
    'name': 'DIV2K',
    'type': 'DIV2KDataset',
    'dataroot_gt': './datasets/DIV2K/DIV2K_train_HR',
    'io_backend': 'disk',
    'gt_size': 128,
    'use_flip': True,
    'use_rot': True,
}

train_loader = build_dataloader(data_config, dataset_opt=data_config, seed=0)

# Training loop
optimizer = torch.optim.Adam(model.parameters(), lr=2e-4)
criterion = torch.nn.L1Loss()

for epoch in range(100):
    for batch in train_loader:
        # Training code here
        pass
```

---

## 🎯 Summary Recommendation

**For your Image Enhancement project:**

1. **START:** Use current classical methods (no training needed)
2. **MEASURE:** Use new Quality Metrics module
3. **IF NEEDED:** Use **DIV2K** dataset
4. **UPGRADE:** Add **Flickr2K** for diverse images
5. **SCALE:** Add ImageNet pre-training for faster convergence

**Typical Timeline:**
- ✅ Current: Ready now
- ⏰ Add metrics: Today
- 🚀 Try DIV2K training: 2-3 days (48 hours GPU)
- 📈 Full setup: 1 week (GPU training)

**Cost Estimate:**
- DIV2K training on Google Colab: Free (with limitations)
- AWS GPU instance: $1-3/hour
- Azure GPU: $1-2/hour
- Full setup: $100-500 for complete training

---

**Next Step: Use Quality Metrics module to measure current enhancement quality!**
