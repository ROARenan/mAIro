from PIL import Image
import os

# Função para espelhar as imagens verticalmente
def espelhar_vertical(pasta_origem, pasta_destino):
    # Se a pasta de destino não existir, ela será criada
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
    
    # Iterar por todos os arquivos na pasta de origem
    for nome_arquivo in os.listdir(pasta_origem):
        caminho_completo = os.path.join(pasta_origem, nome_arquivo)
        
        # Verificar se é um arquivo de imagem
        if nome_arquivo.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            # Abrir a imagem
            imagem = Image.open(caminho_completo)
            
            # Espelhar a imagem verticalmente
            imagem_espelhada = imagem.transpose(Image.FLIP_LEFT_RIGHT)
            
            # Salvar a imagem espelhada na pasta de destino
            caminho_destino = os.path.join(pasta_destino, nome_arquivo)
            imagem_espelhada.save(caminho_destino)
            print(f"Imagem {nome_arquivo} espelhada e salva em {caminho_destino}")

# Exemplo de uso
pasta_origem = './img/cropped_sprites'
pasta_destino = './img/cropped_sprites_mirror'
espelhar_vertical(pasta_origem, pasta_destino)
