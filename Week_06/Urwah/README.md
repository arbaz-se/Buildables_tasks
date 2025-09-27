# Brain Tumor Classification using Deep Learning

This project applies deep learning to classify MRI brain images into four categories: Glioma Tumor, Meningioma Tumor, Pituitary Tumor, and No Tumor. It demonstrates the use of transfer learning with MobileNetV2 to detect tumors in medical images.

## Dataset

The dataset used is the Brain Tumor Classification Dataset, which contains MRI images organized into training and testing folders.

Training set: 2870 images

Testing set: 394 images

Classes: 4 (Glioma, Meningioma, Pituitary, No Tumor)

Preprocessing steps included:

Rescaling pixel values (normalization)

Data augmentation (rotation, shifting, zooming, flipping)

## Model

The model was built using TensorFlow and Keras with transfer learning.

Architecture:

Base Model: MobileNetV2 (pre-trained on ImageNet)

Added Layers:

Global Average Pooling

Dense (128 units, ReLU activation)

Dropout (0.5 for regularization)

Dense (4 units, Softmax for multi-class classification)

Initially, the MobileNetV2 base was frozen so only the new layers were trained.

## Training

Optimizer: Adam (with learning rate scheduling)

Loss: Categorical Crossentropy

Metric: Accuracy

Callbacks: EarlyStopping and ReduceLROnPlateau

Training was performed for 25 epochs on Google Colab GPU, with each epoch taking ~40–45 seconds.

## Results

Training Accuracy: ~97%

Validation Accuracy: ~79%

Test Accuracy: ~79%

The model can correctly classify around 8 out of 10 MRIs. This is a strong result for an initial transfer learning attempt, though further tuning is needed for clinical-level accuracy.

## Usage

To test the model on a single MRI image in Google Colab:

import numpy as np
from tensorflow.keras.preprocessing import image

# Load and preprocess image
img_path = "path_to_your_mri.jpg"
img = image.load_img(img_path, target_size=(224, 224))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0) / 255.0

# Predict
prediction = model.predict(img_array)
classes = ["Glioma Tumor", "Meningioma Tumor", "Pituitary Tumor", "No Tumor"]

print("Predicted Class:", classes[np.argmax(prediction)])

## Hurdles and Challenges

Reaching ~79% validation accuracy required overcoming several challenges:

### Dataset Issues:

The dataset structure had to be carefully extracted and matched (Training vs Testing directories).

Some file path mismatches caused errors when loading images.

### Overfitting:

Initially, training accuracy rose quickly (~95%), but validation accuracy stayed low (~50%).

This indicated overfitting. Data augmentation, dropout layers, and learning rate scheduling were introduced to address this.

### Long Training Time:

Training with large images (224x224) on Google Colab GPU took ~40–45 seconds per epoch.

Total training time for 25 epochs was ~20 minutes.

### Model Tuning:

Early attempts with a simple CNN gave poor accuracy (~50%).

Switching to transfer learning with MobileNetV2 significantly improved results.

### Accuracy Plateau:

Despite improvements, validation accuracy plateaued around ~79%.

This can be improved further with fine-tuning (unfreezing deeper layers) or experimenting with more advanced models like EfficientNet.

## Future Work

Fine-tune deeper MobileNetV2 layers for higher accuracy.

Experiment with EfficientNet and ResNet architectures.

Add more advanced augmentation (contrast, brightness adjustments).

Build a simple web app for uploading an MRI and predicting the tumor class.

## Acknowledgments

The dataset is publicly available for educational and research purposes. Special thanks to the contributors who compiled it.
