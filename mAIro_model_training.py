import tensorflow as tf
import json
import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Configuração do caminho
IMAGES_PATH = "./img/game_prints"
ANNOTATIONS_FILE = "./img/game_prints/game_print_annotations_via.json"
TEST_IMAGE_PATH = "./test_print.png"

# Carregar anotações
with open(ANNOTATIONS_FILE, 'r') as f:
    annotations = json.load(f)

# Preparar dados e rótulos
images = []
labels = []

for image_name, annotation in annotations.items():
    img_path = os.path.join(IMAGES_PATH, image_name)
    if not os.path.exists(img_path):
        continue
    img = cv2.imread(img_path)
    img_resized = cv2.resize(img, (128, 128))  # Ajuste o tamanho conforme necessário
    images.append(img_resized)

    # Extrair coordenadas do Mario
    x = annotation['regions'][0]['shape_attributes']['x']
    y = annotation['regions'][0]['shape_attributes']['y']
    width = annotation['regions'][0]['shape_attributes']['width']
    height = annotation['regions'][0]['shape_attributes']['height']
    labels.append([x, y, width, height])

images = np.array(images) / 255.0  # Normalizar as imagens
labels = np.array(labels)

# Dividir conjunto de dados
train_images, val_images, train_labels, val_labels = train_test_split(images, labels, test_size=0.2, random_state=42)

# Modelo simples de detecção de bounding box
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(16, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(4)  # Saída com 4 valores: x, y, largura, altura
])

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

# Treinar o modelo e monitorar precisão
history = model.fit(
    train_images, train_labels,
    validation_data=(val_images, val_labels),
    epochs=20,  # Ajuste conforme necessário
    batch_size=16,
    verbose=1
)

# Plotar a precisão a cada geração
plt.plot(history.history['accuracy'], label='Acurácia de Treinamento')
plt.plot(history.history['val_accuracy'], label='Acurácia de Validação')
plt.xlabel('Épocas')
plt.ylabel('Acurácia')
plt.legend()
plt.show()

# Carregar e processar imagem de teste
test_img = cv2.imread(TEST_IMAGE_PATH)
test_img_resized = cv2.resize(test_img, (128, 128)) / 255.0
test_img_expanded = np.expand_dims(test_img_resized, axis=0)

# Fazer previsão
pred_box = model.predict(test_img_expanded)[0]
x, y, width, height = [int(v) for v in pred_box]

# Desenhar o retângulo em volta do Mario
cv2.rectangle(test_img, (x, y), (x + width, y + height), (0, 255, 0), 2)
cv2.imshow("Resultado", test_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
