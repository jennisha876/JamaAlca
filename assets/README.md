# Assets Module

This directory contains static files and resources used in the JamaAlca application.

## Directory Structure

```
assets/
├── images/        # Image resources
├── icons/         # UI icons
└── data/          # Static data files
```

## Usage

To use assets in the application:

```python
import os
from PIL import Image, ImageTk

def load_image(filename):
    path = os.path.join("assets", "images", filename)
    return ImageTk.PhotoImage(Image.open(path))
```

## Asset Types

1. Images
   - Plant disease samples
   - Weather icons
   - UI elements

2. Icons
   - Navigation icons
   - Status indicators
   - Action buttons

3. Data
   - Crop information
   - Disease references
   - Regional weather patterns

## Guidelines

1. Use appropriate file formats:
   - Images: PNG or JPG
   - Icons: PNG (with transparency)
   - Data: JSON or CSV

2. Follow naming conventions:
   - Use lowercase
   - Separate words with underscores
   - Include category prefix