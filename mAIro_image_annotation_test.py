import cv2 as cv
import json
import os

# Caminho para o arquivo de anotações e para a imagem que deseja exibir
annotations_path = './img/game_prints/game_print_annotations_via.json'
image_path = './img/game_prints/scene02046.png'

# Carregar a imagem
image = cv.imread(image_path)

# Carregar as anotações do arquivo JSON
with open(annotations_path, 'r') as json_file:
    annotations = json.load(json_file)

# Pegando o nome da imagem a partir do caminho (apenas o nome do arquivo)
image_name = os.path.basename(image_path)

# Verificar se a imagem tem anotações no arquivo
if image_name in annotations:
    regions = annotations[image_name]["regions"]

    # Desenhar os retângulos baseados nas anotações
    for region in regions:
        shape = region["shape_attributes"]
        x, y = shape["x"], shape["y"]
        width, height = shape["width"], shape["height"]
        # Desenhar o retângulo na imagem (cor azul)
        cv.rectangle(image, (x, y), (x + width, y + height), (255, 0, 0), 1)

    # Exibir a imagem com os retângulos desenhados
    cv.imshow("Imagem com Anotas", image)
    cv.waitKey(0)  # Aguardar tecla para fechar
    cv.destroyAllWindows()

else:
    print(f"Não há anotações para a imagem {image_name} no arquivo {annotations_path}")
