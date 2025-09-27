from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

print("Pneumonia Detection System")
print("=" * 40)

base_dir = "chest_xray"
train_dir = os.path.join(base_dir, "train")
test_dir = os.path.join(base_dir, "test")

def load_dataset(directory, img_size=(150, 150), max_samples=1000):
    images = []
    labels = []
    class_names = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    
    for class_idx, class_name in enumerate(class_names):
        class_dir = os.path.join(directory, class_name)
        image_files = [f for f in os.listdir(class_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if max_samples:
            image_files = image_files[:max_samples]
        
        print(f"Loading {len(image_files)} images from {class_name}")
        
        for img_file in image_files:
            try:
                img_path = os.path.join(class_dir, img_file)
                img = Image.open(img_path).resize(img_size).convert('RGB')
                img_array = np.array(img) / 255.0
                images.append(img_array)
                labels.append(class_idx)
            except:
                continue
    
    return np.array(images), np.array(labels), class_names

X_train_full, y_train_full, class_names = load_dataset(train_dir, max_samples=800)
X_test, y_test, _ = load_dataset(test_dir, max_samples=400)

print(f"Dataset loaded: Train={len(X_train_full)}, Test={len(X_test)}")

X_train, X_val, y_train, y_val = train_test_split(
    X_train_full, y_train_full, 
    test_size=0.2, 
    random_state=42,
    stratify=y_train_full
)

print(f"Data split: Train={len(X_train)}, Val={len(X_val)}, Test={len(X_test)}")

def create_model():
    model = Sequential([
        Conv2D(32, (3,3), activation='relu', input_shape=(150, 150, 3)),
        MaxPooling2D(2,2),
        Dropout(0.3),
        
        Conv2D(64, (3,3), activation='relu'),
        MaxPooling2D(2,2),
        Dropout(0.3),
        
        Conv2D(128, (3,3), activation='relu'),
        MaxPooling2D(2,2),
        Dropout(0.4),
        
        Conv2D(256, (3,3), activation='relu'),
        MaxPooling2D(2,2),
        Dropout(0.4),
        
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')
    ])
    return model

model = create_model()

model.compile(
    optimizer=Adam(learning_rate=0.0001),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

print("Model Summary:")
model.summary()

callbacks = [
    EarlyStopping(monitor='val_accuracy', patience=8, restore_best_weights=True, mode='max'),
    ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=4, min_lr=0.00001)
]

print("Starting training...")

history = model.fit(
    X_train, y_train,
    epochs=25,
    batch_size=32,
    validation_data=(X_val, y_val),
    callbacks=callbacks,
    verbose=1,
    shuffle=True
)

print("Training completed")

test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")

predictions = model.predict(X_test)
predicted_classes = (predictions > 0.5).astype(int).flatten()

print("Classification Report:")
print(classification_report(y_test, predicted_classes, target_names=class_names))

cm = confusion_matrix(y_test, predicted_classes)
print("Confusion Matrix:")
print(cm)

plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training')
plt.plot(history.history['val_accuracy'], label='Validation')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training')
plt.plot(history.history['val_loss'], label='Validation')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

def diagnose_xray(image_path):
    try:
        img = Image.open(image_path).resize((150, 150)).convert('RGB')
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        prediction = model.predict(img_array, verbose=0)
        probability = prediction[0][0]
        
        if probability > 0.5:
            diagnosis = "PNEUMONIA DETECTED"
            confidence = probability
            advice = "Consult a doctor immediately"
        else:
            diagnosis = "NORMAL CHEST X-RAY"
            confidence = 1 - probability
            advice = "No signs of pneumonia detected"
        
        plt.figure(figsize=(5, 5))
        plt.imshow(img)
        plt.title(f"{diagnosis}\nConfidence: {confidence:.2%}")
        plt.axis('off')
        plt.show()
        
        print(f"Diagnosis: {diagnosis}")
        print(f"Confidence: {confidence:.2%}")
        print(f"Advice: {advice}")
        
        return diagnosis, confidence
        
    except Exception as e:
        print(f"Error: {e}")
        return None, None

model.save('pneumonia_model.h5')
print("Model saved as pneumonia_model.h5")

print("Pneumonia detection system ready")
print("Usage: diagnose_xray('path_to_xray_image.jpg')")