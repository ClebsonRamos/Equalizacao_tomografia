from numpy import zeros
from os import system
from PIL import Image

def extracao_dos_dados(nome_camada, numero_arquivo, quantidade_arquivos):
    for i in range(quantidade_arquivos):
        if nome_camada == 'imagem':
            print(f'Lendo arquivo {nome_camada}_{numero_arquivo}.txt')
            arquivo = open(f'Dados\\{nome_camada}_{numero_arquivo}.txt')
        else:
            print(f'Lendo arquivo {nome_camada}_{i + 1}.txt')
            arquivo = open(f'Dados\\{nome_camada}_{i + 1}.txt', 'r')
        linhas = arquivo.readlines()
        for i in range(len(linhas)):
            linhas[i] = linhas[i].split()
        for i in range(altura):
            for j in range(largura):
                if nome_camada == 'dark':
                    camada_dark[i][j] += int(linhas[i][j])
                elif nome_camada == 'flat':
                    camada_flat[i][j] += int(linhas[i][j])
                elif nome_camada == 'imagem':
                    camada_imagem[i][j] = int(linhas[i][j])
        arquivo.close()
        system('cls')
        linhas.clear()
    # Ajuste dos valores acumulados nas matrizes DARK e FLAT com a média.
    if nome_camada != 'imagem':
        if nome_camada == 'dark':
            print(f'Ajustando a matriz DARK. Aguarde...')
            for i in range(altura):
                for j in range(largura):
                    camada_dark[i][j] = int(camada_dark[i][j] / quantidade_arquivos)
        elif nome_camada == 'flat':
            print(f'Ajustando a matriz FLAT. Aguarde...')
            for i in range(altura):
                for j in range(largura):
                    camada_flat[i][j] = int(camada_flat[i][j] / quantidade_arquivos)


def histograma_imagem(camada, num_arquivo, vetor_hist, total_pixels):
    arquivo_txt = open(f'Graficos\\{camada}_{num_arquivo}.txt', 'w')
    for i in range(len(vetor_hist)):
        porcentagem = 100 * vetor_hist[i] / total_pixels
        arquivo_txt.write(f'{i}\t{porcentagem}\n'.replace('.', ','))
    arquivo_txt.close()


def maximo_minimo_da_matriz(tipo, matriz):
    maximo_minimo = [0, 0]
    maximo_minimo[0] = matriz[0][0]
    maximo_minimo[1] = matriz[0][0]
    print(f'Procurando o valor máximo da matriz {tipo} - Aguarde...')
    for x in range(altura):
        for y in range(largura):
            if maximo_minimo[0] < matriz[x][y]:
                maximo_minimo[0] = matriz[x][y]
            if maximo_minimo[1] > matriz[x][y]:
                maximo_minimo[1] = matriz[x][y]
    return maximo_minimo


def pixels_fora_do_range(identificador_imagem):
    system('cls')
    print('Checando pixels fora do intervalo de equalização...')
    for x in range(altura):
        for y in range(largura):
            if camada_imagem[x][y] > camada_flat[x][y]:
                pixels_bugados_acima[identificador_imagem] += 1
            if camada_imagem[x][y] < camada_dark[x][y]:
                pixels_bugados_abaixo[identificador_imagem] += 1


#-----PROGRAMA PRINCIPAL-----
# Dimensões das imagens.
largura = 1400
altura = 1200
total_de_pixels = altura * largura

# Matrizes para armazenamento dos dados.
camada_dark = zeros((altura, largura), dtype = 'i')
camada_flat = zeros((altura, largura), dtype = 'i')
camada_imagem = zeros((altura, largura), dtype = 'i')

# Vetor para exibição de progresso em porcentagem.
faixa_porcentagem = []
contador = marcador_faixa_porcentagem = 0
for i in range(101):
    faixa_porcentagem.append(i)

# Solicitação ao usuário das quantidades de arquivos dark, flat e imagem que serão usadas.
system('cls')
print('PARÂMETROS INICIAIS')
quantidade_dark = int(input('\tQuantidade de arquivos dark: '))
quantidade_flat = int(input('\tQuantidade de arquivos flat: '))
quantidade_imagem = int(input('\tQuantidade de arquivos de imagem: '))
system('cls')

# Vetor de frequência de pixels.
distribuicao_pixels_imagem = []
distribuicao_pixel_imagem_bruta = []
for i in range(256):
    distribuicao_pixels_imagem.append(0)
    distribuicao_pixel_imagem_bruta.append(0)

pixels_bugados_acima = []
pixels_bugados_abaixo = []
for i in range(quantidade_imagem):
    pixels_bugados_acima.append(0)
    pixels_bugados_abaixo.append(0)

# Aquisição dos dados dos arquivos dark.
extracao_dos_dados('dark', 0, quantidade_dark)

# Aquisição dos dados dos arquivos flat.
extracao_dos_dados('flat', 0, quantidade_flat)

imagem_bruta = Image.new('RGB', (altura, largura), (0, 0, 0))
imagem_equalizada = Image.new('RGB', (altura, largura), (0, 0, 0))
imagem_de_erro = Image.new('RGB', (altura, largura), (0, 0, 0))

max_imagem = []
min_imagem = []

for quant_img in range(quantidade_imagem):
    # Abertura do arquivo de imagem e aquisição dos dados.
    extracao_dos_dados('imagem', quant_img + 1, 1)

    # Mínimo do arquivo DARK.
    aux_list = maximo_minimo_da_matriz('IMAGEM', camada_imagem)
    maximo_imagem = aux_list[0]
    minimo_imagem = aux_list[1]
    max_imagem.append(maximo_imagem)
    min_imagem.append(minimo_imagem)

    # Checagem de quantidade de pixels fora do range.
    pixels_fora_do_range(quant_img)

    contador = marcador_faixa_porcentagem = 0
    for i in range(altura):
        porcentagem = 100 * contador / total_de_pixels
        if porcentagem > faixa_porcentagem[marcador_faixa_porcentagem]:
            marcador_faixa_porcentagem += 1
            system('cls')
            print(f'Imagem_{quant_img + 1} --- Processando... [{porcentagem:.0f}%]')
        for j in range(largura):
            contador += 1
            proporcao_bruta = (camada_imagem[i][j] - minimo_imagem) * 255 / (maximo_imagem - minimo_imagem)
            proporcao = (camada_imagem[i][j] + camada_dark[i][j]) / (camada_flat[i][j] + camada_dark[i][j])
            pixel = int(255 * proporcao)
            pixel_bruto = int(proporcao_bruta)
            if pixel > 255:
                pixel = 255
                imagem_de_erro.putpixel((i, j), (255, 0, 0))
            else:
                imagem_de_erro.putpixel((i, j), (pixel, pixel, pixel))
            if pixel_bruto > 255:
                pixel_bruto = 255
            distribuicao_pixels_imagem[pixel] += 1
            distribuicao_pixel_imagem_bruta[pixel_bruto] += 1
            imagem_bruta.putpixel((i, j), (pixel_bruto, pixel_bruto, pixel_bruto))
            imagem_equalizada.putpixel((i, j), (pixel, pixel, pixel))
    imagem_bruta.save(f'Imagens_brutas\\Imagem_bruta_{quant_img + 1}.png')
    imagem_equalizada.save(f'Imagens_equalizadas\\Imagem_equalizada_{quant_img + 1}.png')
    imagem_de_erro.save(f'Regioes_inconstantes\\Imagem_de_erro_{quant_img + 1}.png')
    system('cls')
    histograma_imagem('imagem', quant_img + 1, distribuicao_pixels_imagem, total_de_pixels)
    histograma_imagem('imagem_bruta', quant_img + 1, distribuicao_pixel_imagem_bruta, total_de_pixels)
    # Limpando o vetor histrograma.
    for i in range(len(distribuicao_pixels_imagem)):
        distribuicao_pixels_imagem[i] = 0
        distribuicao_pixel_imagem_bruta[i] = 0

for i in range(quantidade_imagem):
    if pixels_bugados_acima[i] > 0 or pixels_bugados_abaixo[i] > 0:
        porcentagem = 100 * (pixels_bugados_acima[i] + pixels_bugados_abaixo[i]) / total_de_pixels
        print(f'O arquivo imagem_{i + 1}.txt apresentou:\n\t{pixels_bugados_acima[i]} pixels acima do limite superior')
        print(f'\t{pixels_bugados_abaixo[i]} pixels abaixo do limite superior')
        print(f'\tPorcentagem total discrepante: {porcentagem:.3f}%\n')

system('pause')
system('cls')
for i in range(quantidade_imagem):
    print(f'IMAGEM {i + 1}:\n\tMáximo: {max_imagem[i]}\n\tMínimo: {min_imagem[i]}\n')
print('\nPrograma executado com sucesso.\n')
system('pause')
