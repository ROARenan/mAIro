import cv2 as cv
import numpy as np
import os
import json

# Verifique se o OpenCV com CUDA está disponível
if not cv.cuda.getCudaEnabledDeviceCount():
    raise Exception("Nenhuma GPU compatível com CUDA foi detectada!")

# Pasta contendo os sprites do Mario
sprites_folder = './img/sprites_no_bg'
# Pasta contendo as imagens do jogo
game_prints_folder = './img/game_prints'
# Threshold para uma correspondência ser considerada válida
threshold = 0.4

# Inicializando o dicionário para salvar as anotações de todas as imagens
annotations = {}

# Listando todas as imagens de game prints
game_prints = [f for f in os.listdir(game_prints_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
total_game_prints = len(game_prints)
print(f"Iniciando a categorização de {total_game_prints} game prints...\n")

# Loop sobre cada imagem de game print
for i, game_print_name in enumerate(game_prints):
    game_print_path = os.path.join(game_prints_folder, game_print_name)
    game_print = cv.imread(game_print_path)

    # Verifique se a imagem foi carregada corretamente
    if game_print is None:
        print(f"[{i+1}/{total_game_prints}] Erro ao carregar a imagem {game_print_name}")
        continue

    # Converta a imagem para GPU
    game_print_gpu = cv.cuda_GpuMat()
    game_print_gpu.upload(game_print)

    # Inicializando as anotações para essa imagem
    annotations[game_print_name] = {
        "filename": game_print_name,
        "size": os.path.getsize(game_print_path),
        "regions": [],
        "file_attributes": {}
    }

    print(f"[{i+1}/{total_game_prints}] Processando game print: {game_print_name}")

    # Variáveis para rastrear a melhor correspondência
    best_match_val = threshold
    best_region = None

    # Procurando correspondências com cada sprite
    sprites = [f for f in os.listdir(sprites_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    total_sprites = len(sprites)

    for j, sprite_name in enumerate(sprites):
        sprite_path = os.path.join(sprites_folder, sprite_name)
        mario_template = cv.imread(sprite_path)

        # Certifique-se de que o sprite foi carregado corretamente
        if mario_template is None:
            print(f"Erro ao carregar o sprite {sprite_name}")
            continue

        # Converta o sprite para GPU
        mario_template_gpu = cv.cuda_GpuMat()
        mario_template_gpu.upload(mario_template)

        # Realizando a correspondência na GPU
        result_gpu = cv.cuda.matchTemplate(game_print_gpu, mario_template_gpu, cv.TM_CCOEFF_NORMED)
        result = result_gpu.download()

        # Aplicando a função minMaxLoc para obter a melhor correspondência
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        # Se a correspondência for maior que o threshold e maior que a melhor encontrada
        if max_val >= best_match_val:
            template_h, template_w = mario_template.shape[:2]
            rect_top_left = max_loc

            # Criar a região com a melhor correspondência
            best_region = {
                "shape_attributes": {
                    "name": "rect",
                    "x": rect_top_left[0],
                    "y": rect_top_left[1],
                    "width": template_w,
                    "height": template_h
                },
                "region_attributes": {
                    "sprite": sprite_name  # Identificando o sprite encontrado
                }
            }

            # Atualizar a melhor correspondência
            best_match_val = max_val

        print(f"Sprite [{j+1}/{total_sprites}] {sprite_name} processado - Correspondência: {max_val:.2f}")

    # Se encontramos uma correspondência válida, adicioná-la às anotações da imagem
    if best_region is not None:
        annotations[game_print_name]["regions"].append(best_region)

# Salvando todas as anotações em um arquivo JSON
with open('game_print_annotations_via.json', 'w') as json_file:
    json.dump(annotations, json_file, indent=4)

print(f"\nAnotações geradas e salvas em 'game_print_annotations_via.json'")
