from PIL import Image

# Função para realizar recortes


def realizar_recortes(caminho_imagem, caminho_saida, x_inicio, y_inicio, altura, largura, passo, direcao, recorte_num,crops):
    # Carregar a imagem
    img = Image.open(caminho_imagem)
    w, h = img.size

    # Variáveis de controle
    x, y = x_inicio, y_inicio
    # Contador para nomear os arquivos de recorte

    while 0 <= x < w and 0 <= y < h:
        # Realiza o recorte
        box = (x, y, x + largura, y + altura)
        cropped_img = img.crop(box)

        # Salva o recorte com nome sequencial
        #cropped_img.save(f"{caminho_saida}/marinho_{recorte_num}_{x}_{y}.png")
        cropped_img.save(f"{caminho_saida}/mario_{recorte_num}.png")
        print(f"Recorte {recorte_num} realizado em: ({x}, {y})")
        recorte_num += 1

        # Atualiza a posição com base na direção
        if direcao == "direita":
            x += largura + passo
        elif direcao == "esquerda":
            x -= largura + passo
        elif direcao == "baixo":
            y += altura + passo
        elif direcao == "cima":
            y -= altura + passo

        # Verifica se ainda está dentro dos limites da imagem
        # if x < 0 or x + largura > w or y < 0 or y + altura > h:
        if crops == recorte_num:
            break


# Configurações
caminho_imagem = "./img/SMW_Sprites.png"  # Insira o caminho da sua imagem
caminho_saida = "./img/cropped_sprites"
altura = 48  # Altura do recorte em pixels
largura = 48 # Largura do recorte em pixels
x_inicio = 8  # Coordenada X de início
y_inicio = 576 + altura + 23 + altura + 29 + altura + 29 + altura + 29# Coordenada Y de início
passo = 4  # Quantidade de pixels a pular entre um recorte e outro
direcao = "direita"  # Direção do recorte: 'direita', 'esquerda', 'cima', 'baixo'
recorte_num = 9 + 14 + 16 + 17 # Número de inicio dos recortes (para nomear as imagens)
crops = 13 + recorte_num # Quantidade de Recortes a serem feitos

# Chama a função para realizar os recortes
realizar_recortes(caminho_imagem, caminho_saida, x_inicio,
                  y_inicio, altura, largura, passo, direcao, recorte_num, crops)
