import cv2 as cv
import numpy as np
import os

# Função para recortar a área de interesse do sprite (remover espaços vazios)


def crop_sprite(image_path, output_path):
    # Carregar a imagem com fundo transparente
    # Carregar com canal alfa
    image = cv.imread(image_path, cv.IMREAD_UNCHANGED)

    # Separar os canais de cor e o canal alfa (transparência)
    if image.shape[2] == 4:  # Se a imagem tem 4 canais (RGBA)
        alpha_channel = image[:, :, 3]  # Canal de transparência (alfa)

        # Criar uma máscara binária onde o canal alfa é maior que zero (não transparente)
        mask = alpha_channel > 0

        # Encontrar as coordenadas do retângulo que contém o sprite
        coords = np.argwhere(mask)

        # Pegar o ponto superior-esquerdo e inferior-direito do retângulo que contém o sprite
        y0, x0 = coords.min(axis=0)
        # Adicionando 1 para incluir o último pixel
        y1, x1 = coords.max(axis=0) + 1

        # Recortar a imagem original com base nessas coordenadas
        cropped_image = image[y0:y1, x0:x1]

        # Salvar a imagem recortada
        cv.imwrite(output_path, cropped_image)

        print(f"Sprite recortado salvo em: {output_path}")
    else:
        print("A imagem não contém canal alfa (não é transparente).")


# Exemplo de uso:
image_path = './img/sprites_no_bg/marinho_0.png'
output_path = 'marinho_cropped.png'
crop_sprite(image_path, output_path)
