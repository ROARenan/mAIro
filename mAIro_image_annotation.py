import cv2 as cv
import numpy as np
import os
import json
from multiprocessing import Pool, cpu_count

# Pasta contendo os sprites do Mario
sprites_folder = './img/sprites_no_bg'
# Pasta contendo as imagens do jogo
game_prints_folder = './img/game_prints'
# Threshold para uma correspondência ser considerada válida
threshold = 0.4
high_confidence_threshold = 0.8  # Se uma correspondência for > 0.8, ela é aceita diretamente

# Listar as imagens de game prints
game_prints = [f for f in os.listdir(game_prints_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

def process_game_print(game_print_name):
    game_print_path = os.path.join(game_prints_folder, game_print_name)
    game_print = cv.imread(game_print_path)

    if game_print is None:
        print(f"Erro ao carregar a imagem {game_print_name}")
        return game_print_name, None

    best_match_val = threshold
    best_region = None

    # Procurando correspondências com cada sprite
    sprites = [f for f in os.listdir(sprites_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

    for sprite_name in sprites:
        sprite_path = os.path.join(sprites_folder, sprite_name)
        mario_template = cv.imread(sprite_path)

        if mario_template is None:
            continue

        # Comparação entre o sprite e a imagem do jogo
        result = cv.matchTemplate(mario_template, game_print, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        # Verificar se a correspondência atual é a melhor encontrada
        if max_val > best_match_val:
            template_h, template_w = mario_template.shape[:2]
            rect_top_left = max_loc

            best_region = {
                "shape_attributes": {
                    "name": "rect",
                    "x": rect_top_left[0],
                    "y": rect_top_left[1],
                    "width": template_w,
                    "height": template_h
                },
                "region_attributes": {
                    "sprite": "mario",
                    "status": "",
                    "powerUp": ""
                }
            }

            best_match_val = max_val

            # Parar a busca se a correspondência for maior que 0.8
            if max_val >= high_confidence_threshold:
                print(f"Correspondência de alta confiança encontrada ({max_val:.2f}) para {game_print_name}")
                break

    # Retorna o nome da imagem e a região de melhor correspondência, se existir
    return game_print_name, best_region

if __name__ == "__main__":
    print(f"Iniciando a categorização de {len(game_prints)} game prints...\n")

    # Usar todos os núcleos disponíveis
    with Pool(cpu_count()) as pool:
        results = pool.map(process_game_print, game_prints)

    # Criar as anotações a partir dos resultados
    annotations = {}
    for game_print_name, best_region in results:
        if best_region is not None:
            annotations[game_print_name] = {
                "filename": game_print_name,
                "size": os.path.getsize(os.path.join(game_prints_folder, game_print_name)),
                "regions": [best_region],  # Apenas a melhor região
                "file_attributes": {}
            }

    # Salvando todas as anotações em um arquivo JSON
    with open('game_print_annotations_via.json', 'w') as json_file:
        json.dump(annotations, json_file, indent=4)

    print(f"\nAnotações geradas e salvas em 'game_print_annotations_via.json'")
