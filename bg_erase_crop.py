from PIL import Image
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


# Caminho das pastas
input_dir = './img/cropped_sprites/'  # Pasta de entrada com as imagens
# Pasta para salvar imagens temporárias sem fundo
output_dir_temp = './img/sprites_no_bg_temp/'
# Pasta para salvar imagens recortadas
output_dir_cropped = './img/sprites_no_bg/'

# Criar as pastas de saída se elas não existirem
if not os.path.exists(output_dir_temp):
    os.makedirs(output_dir_temp)
if not os.path.exists(output_dir_cropped):
    os.makedirs(output_dir_cropped)

# Definir as cores do fundo
cor_fundo1 = (0, 116, 116, 255)  # #007474 em RGBA
cor_fundo2 = (0, 84, 84, 255)    # #005454 em RGBA
cor_fundo3 = (0, 52, 52, 255)    # #003434 em RGBA

# Processar cada imagem na pasta de entrada
for filename in os.listdir(input_dir):
    if filename.endswith('.png'):  # Somente arquivos PNG
        # Carregar a imagem
        img_path = os.path.join(input_dir, filename)
        img = Image.open(img_path).convert("RGBA")
        datas = img.getdata()

        nova_imagem = []

        # Percorrer cada pixel da imagem
        for item in datas:
            # Se o pixel corresponder a uma das cores de fundo, torná-lo transparente
            if item == cor_fundo1 or item == cor_fundo2 or item == cor_fundo3:
                nova_imagem.append((255, 255, 255, 0))  # Transparente
            else:
                nova_imagem.append(item)  # Manter o pixel original

        # Criar uma nova imagem sem o fundo
        img.putdata(nova_imagem)

        # Salvar a nova imagem temporária sem o fundo
        output_temp_path = os.path.join(output_dir_temp, filename)
        img.save(output_temp_path, "PNG")

        # Recortar a imagem sem fundo e salvar na pasta de saída final
        output_cropped_path = os.path.join(output_dir_cropped, filename)
        crop_sprite(output_temp_path, output_cropped_path)

print("Processamento completo!")
