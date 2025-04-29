from numpy import zeros, arange, linspace
from os import system
from PIL import Image
from matplotlib import pyplot as plt
from skimage.io import imread

tam_imagem = (10, 5) # Tamanho das imagens dos gráficos.

def extracao_dos_dados(nome_camada, quantidade_arquivos):
    for i in range(quantidade_arquivos):
        try:
            extensao = 'jpg'
            arquivo_imagem = Image.open(f'Dados\\{nome_camada}_{i + 1}.{extensao}')
        except:
            try:
                extensao = 'jpeg'
                arquivo_imagem = Image.open(f'Dados\\{nome_camada}_{i + 1}.{extensao}')
            except:
                try:
                    extensao = 'png'
                    arquivo_imagem = Image.open(f'Dados\\{nome_camada}_{i + 1}.{extensao}')
                except:
                    print(f'ERRO: não foi possível abrir o arquivo {nome_camada}_{i + 1}.\n')
                    system('pause')
                    exit()

        print(f'Lendo arquivo {nome_camada}_{i + 1}.{extensao}')

        if nome_camada == 'dark':
            for x in range(largura):
                for y in range(altura):
                    camada_dark[i][x][y] = arquivo_imagem.getpixel((x, y))
        elif nome_camada == 'flat':
            for x in range(largura):
                for y in range(altura):
                    camada_flat[i][x][y] = arquivo_imagem.getpixel((x, y))
        elif nome_camada == 'imagem':
            for x in range(largura):
                for y in range(altura):
                    camada_imagem[i][x][y] = arquivo_imagem.getpixel((x, y))
        system('cls')


def histograma_dark():
    imagem_png = Image.new('RGB', (largura, altura), (0, 0, 0))

    for quant in range(quantidade_dark):
        system('cls')
        print(f'Criando histograma do dark {quant + 1}...')

        figura, eixo = plt.subplots(nrows = 1, ncols = 2, figsize = tam_imagem)
        plt.subplots_adjust(left = 0.06, bottom = 0.11, right = 0.95, top = 0.88, wspace = 0.229, hspace = 0.45)

        maximo = minimo = 0
        for x in range(largura):
            for y in range(altura):
                if maximo < camada_dark[quant][x][y]:
                    maximo = camada_dark[quant][x][y]
                if minimo > camada_dark[quant][x][y]:
                    minimo = camada_dark[quant][x][y]
        
        for x in range(largura):
            for y in range(altura):
                proporcao = (camada_dark[quant][x][y] - minimo) * 255 / (maximo - minimo)
                if proporcao > 1:
                    proporcao = 1
                p = 255 - int(255 * proporcao)
                imagem_png.putpixel((x, y), (p, p, p))

        eixo_x = arange(0, maximo + 1, 1)
        eixo_y = arange(0, maximo + 1, 1)
        for i in range(len(eixo_y)):
            eixo_y[i] = 0

        for x in range(largura):
            for y in range(altura):
                aux_pixel = camada_dark[quant][x][y]
                eixo_y[aux_pixel] += 1
        
        eixo[0].imshow(imagem_png)
        eixo[1].plot(eixo_x, eixo_y, color = 'blue')

        plt.suptitle(f'DARK {quant + 1}')
        eixo[0].set_title('Imagem dark', fontsize = 12)

        eixo[1].set_title('Histograma', fontsize = 12)
        eixo[1].set_xlabel('Intensidade do pixel', fontsize = 10)
        eixo[1].set_ylabel('Frequência absoluta', fontsize = 10)
        eixo[1].set_yscale('log')

        plt.savefig(f'Graficos\\Histograma_dark_{quant + 1}.png', dpi = 400)
        plt.close()
        del figura


def histograma_dark_medio():
    system('cls')
    print('Criando histograma do dark médio...')

    imagem_png = Image.new('RGB', (largura, altura), (0, 0, 0))
    figura, eixo = plt.subplots(nrows = 1, ncols = 2, figsize = tam_imagem)
    plt.subplots_adjust(left = 0.06, bottom = 0.11, right = 0.95, top = 0.88, wspace = 0.229, hspace = 0.45)

    maximo = minimo = 0
    for x in range(largura):
        for y in range(altura):
            if maximo < media_dark[x][y]:
                maximo = media_dark[x][y]
            if minimo > media_dark[x][y]:
                minimo = media_dark[x][y]
    
    for x in range(largura):
        for y in range(altura):
            proporcao = (media_dark[x][y] - minimo) * 255 / (maximo - minimo)
            if proporcao > 1:
                proporcao = 1
            p = 255 - int(255 * proporcao)
            imagem_png.putpixel((x, y), (p, p, p))

    eixo_x = arange(0, maximo + 1, 1)
    eixo_y = arange(0, maximo + 1, 1)
    for i in range(len(eixo_y)):
        eixo_y[i] = 0

    for x in range(largura):
        for y in range(altura):
            aux_pixel = media_dark[x][y]
            eixo_y[aux_pixel] += 1
    
    eixo[0].imshow(imagem_png)
    eixo[1].plot(eixo_x, eixo_y, color = 'blue')

    plt.suptitle(f'DARK MÉDIO')
    eixo[0].set_title('Imagem dark', fontsize = 12)

    eixo[1].set_title('Histograma', fontsize = 12)
    eixo[1].set_xlabel('Intensidade do pixel', fontsize = 10)
    eixo[1].set_ylabel('Frequência absoluta', fontsize = 10)
    eixo[1].set_yscale('log')

    plt.savefig('Graficos\\Histograma_dark_medio.png', dpi = 400)
    plt.close()
    del figura

    
def histograma_flat():
    imagem_png = Image.new('RGB', (largura, altura), (0, 0, 0))

    for quant in range(quantidade_flat):
        system('cls')
        print(f'Criando histograma do flat {quant + 1}...')

        figura, eixo = plt.subplots(nrows = 1, ncols = 2, figsize = tam_imagem)
        plt.subplots_adjust(left = 0.06, bottom = 0.11, right = 0.95, top = 0.88, wspace = 0.229, hspace = 0.45)

        maximo = minimo = 0
        for x in range(largura):
            for y in range(altura):
                if maximo < camada_flat[quant][x][y]:
                    maximo = camada_flat[quant][x][y]
                if minimo > camada_flat[quant][x][y]:
                    minimo = camada_flat[quant][x][y]
        
        for x in range(largura):
            for y in range(altura):
                proporcao = (camada_flat[quant][x][y] - minimo) * 255 / (maximo - minimo)
                if proporcao > 1:
                    proporcao = 1
                p = int(255 * proporcao)
                imagem_png.putpixel((x, y), (p, p, p))

        eixo_x = arange(0, maximo + 1, 1)
        eixo_y = arange(0, maximo + 1, 1)
        for i in range(len(eixo_y)):
            eixo_y[i] = 0

        for x in range(largura):
            for y in range(altura):
                aux_pixel = camada_flat[quant][x][y]
                eixo_y[aux_pixel] += 1
        
        eixo[0].imshow(imagem_png)
        eixo[1].plot(eixo_x, eixo_y, color = 'blue')

        plt.suptitle(f'FLAT {quant + 1}')
        eixo[0].set_title('Imagem flat', fontsize = 12)

        eixo[1].set_title('Histograma', fontsize = 12)
        eixo[1].set_xlabel('Intensidade do pixel', fontsize = 10)
        eixo[1].set_ylabel('Frequência absoluta', fontsize = 10)
        eixo[1].set_yscale('log')

        plt.savefig(f'Graficos\\Histograma_flat_{quant + 1}.png', dpi = 400)
        plt.close()
        del figura


def histograma_flat_medio():
    system('cls')
    print('Criando histograma do flat médio...')

    imagem_png = Image.new('RGB', (largura, altura), (0, 0, 0))
    figura, eixo = plt.subplots(nrows = 1, ncols = 2, figsize = tam_imagem)
    plt.subplots_adjust(left = 0.06, bottom = 0.11, right = 0.95, top = 0.88, wspace = 0.229, hspace = 0.45)

    maximo = minimo = 0
    for x in range(largura):
        for y in range(altura):
            if maximo < media_flat[x][y]:
                maximo = media_flat[x][y]
            if minimo > media_flat[x][y]:
                minimo = media_flat[x][y]
    
    for x in range(largura):
        for y in range(altura):
            proporcao = (media_flat[x][y] - minimo) * 255 / (maximo - minimo)
            if proporcao > 1:
                proporcao = 1
            p = int(255 * proporcao)
            imagem_png.putpixel((x, y), (p, p, p))

    eixo_x = arange(0, maximo + 1, 1)
    eixo_y = arange(0, maximo + 1, 1)
    for i in range(len(eixo_y)):
        eixo_y[i] = 0

    for x in range(largura):
        for y in range(altura):
            aux_pixel = media_flat[x][y]
            eixo_y[aux_pixel] += 1

    eixo[0].imshow(imagem_png)
    eixo[1].plot(eixo_x, eixo_y, color = 'blue')

    plt.suptitle(f'FLAT MÉDIO')
    eixo[0].set_title('Imagem flat', fontsize = 12)

    eixo[1].set_title('Histograma', fontsize = 12)
    eixo[1].set_xlabel('Intensidade do pixel', fontsize = 10)
    eixo[1].set_ylabel('Frequência absoluta', fontsize = 10)
    eixo[1].set_yscale('log')

    plt.savefig('Graficos\\Histograma_flat_medio.png', dpi = 400)
    plt.close()
    del figura


def histograma_imagem(num_arquivo, vetor_hist_bruto, vetor_hist_equal, total_pixels):
    system('cls')
    print(f'Criando histograma da Imagem {num_arquivo + 1}...')

    figura, eixos = plt.subplots(nrows = 2, ncols = 2, figsize = tam_imagem)
    plt.subplots_adjust(left = 0.024, bottom = 0.11, right = 0.95, top = 0.88, wspace = 0.2, hspace = 0.45)

    x_bruto = arange(0, len(vetor_hist_bruto), 1)
    x_equal = arange(0, len(vetor_hist_equal), 1)
    y_equal = linspace(0, len(vetor_hist_bruto) + 1, 256)

    for i in range(len(x_equal)):
        y_equal[i] = 100 * vetor_hist_equal[i] / total_pixels

    imagem = imread(f'Imagens_brutas\\Imagem_bruta_{num_arquivo + 1}.png')
    eixos[0][0].imshow(imagem)
    eixos[0][0].set_title('Imagem bruta')

    imagem = imread(f'Imagens_equalizadas\\Imagem_equalizada_{num_arquivo + 1}.png')
    eixos[1][0].imshow(imagem)
    eixos[1][0].set_title('Imagem equalizada', fontsize = 12)

    eixos[0][1].plot(x_bruto, vetor_hist_bruto, color = 'blue')
    eixos[0][1].set_title('Histograma', fontsize = 12)
    eixos[0][1].set_xlabel('Intensidade do pixel', fontsize = 10)
    eixos[0][1].set_ylabel('Frequência absoluta', fontsize = 10)
    eixos[0][1].set_yscale('log')
    eixos[0][1].grid(True)

    eixos[1][1].plot(x_equal, y_equal, color = 'blue')
    eixos[1][1].set_title('Histograma', fontsize = 12)
    eixos[1][1].set_xlabel('Intensidade do pixel', fontsize = 10)
    eixos[1][1].set_ylabel('Frequência relativa (%)', fontsize = 10)
    eixos[1][1].set_yscale('log')
    eixos[1][1].grid(True)

    plt.suptitle(f'IMAGEM {num_arquivo + 1}')
    plt.savefig(f'Graficos\\Imagem_{num_arquivo + 1}.png', dpi = 400)
    plt.close()
    del figura


def maximo_minimo_da_matriz(tipo, matriz, identificador):
    maximo_minimo = [0, 0]
    maximo_minimo[0] = matriz[identificador][0][0]
    maximo_minimo[1] = matriz[identificador][0][0]
    print(f'Procurando o valor máximo da matriz {tipo} - Aguarde...')
    for x in range(largura):
        for y in range(altura):
            if maximo_minimo[0] < matriz[identificador][x][y]:
                maximo_minimo[0] = matriz[identificador][x][y]
            if maximo_minimo[1] > matriz[identificador][x][y]:
                maximo_minimo[1] = matriz[identificador][x][y]
    return maximo_minimo


def pixels_fora_do_range(identificador_imagem):
    system('cls')
    print('Checando pixels fora do intervalo de equalização...')
    for x in range(largura):
        for y in range(altura):
            if camada_imagem[identificador_imagem][x][y] > media_flat[x][y]:
                pixels_bugados_acima[identificador_imagem] += 1
            if camada_imagem[identificador_imagem][x][y] < media_dark[x][y]:
                pixels_bugados_abaixo[identificador_imagem] += 1


#-----PROGRAMA PRINCIPAL-----
# Dimensões das imagens.
largura = 1400
altura = 1200
total_de_pixels = altura * largura

# Solicitação ao usuário das quantidades de arquivos dark, flat e imagem que serão usadas.
system('cls')
print('PARÂMETROS INICIAIS')
quantidade_dark = int(input('\tQuantidade de arquivos dark: '))
quantidade_flat = int(input('\tQuantidade de arquivos flat: '))
quantidade_imagem = int(input('\tQuantidade de arquivos de imagem: '))
system('cls')

# Matrizes para armazenamento dos dados.
camada_dark = zeros((quantidade_dark, largura, altura), dtype = 'i')
camada_flat = zeros((quantidade_flat, largura, altura), dtype = 'i')
camada_imagem = zeros((quantidade_imagem, largura, altura), dtype = 'i')

# Vetor para exibição de progresso em porcentagem.
faixa_porcentagem = []
contador = marcador_faixa_porcentagem = 0
for i in range(101):
    faixa_porcentagem.append(i)

# Vetor de frequência de pixels.
distribuicao_pixels_imagem_equal = []
#distribuicao_pixel_imagem_bruta = []
for i in range(256):
    distribuicao_pixels_imagem_equal.append(0)
    #distribuicao_pixel_imagem_bruta.append(0)

pixels_bugados_acima = []
pixels_bugados_abaixo = []
for i in range(quantidade_imagem):
    pixels_bugados_acima.append(0)
    pixels_bugados_abaixo.append(0)

# Aquisição dos dados dos arquivos dark.
extracao_dos_dados('dark', quantidade_dark)

# Aquisição dos dados dos arquivos flat.
extracao_dos_dados('flat', quantidade_flat)

# Aquisição dos dados dos arquivos imagem.
extracao_dos_dados('imagem', quantidade_imagem)

# Dark e flat médios.
media_dark = zeros((largura, altura), dtype = 'i')
media_flat = zeros((largura, altura), dtype = 'i')

# Cálculo dos valores médios do dark e flat.
system('cls')
print('Calculando os valores médios dos arquivos DARK e FLAT...')

for x in range(largura):
    for y in range(altura):
        soma = 0
        for i in range(quantidade_dark):
            soma += camada_dark[i][x][y]
        media_dark[x][y] = soma // quantidade_dark
        soma = 0
        for i in range(quantidade_flat):
            soma += camada_flat[i][x][y]
        media_flat[x][y] = soma // quantidade_flat

# Histogramas para o dark e flat.
histograma_dark()
histograma_flat()
histograma_dark_medio()
histograma_flat_medio()

# Crição da estrutura da imagem no padrão RGB.
imagem_bruta = Image.new('RGB', (largura, altura), (0, 0, 0))
imagem_equalizada = Image.new('RGB', (largura, altura), (0, 0, 0))

for quant_img in range(quantidade_imagem):
    # Mínimo do arquivo DARK.
    aux_list = maximo_minimo_da_matriz('IMAGEM', camada_imagem, quant_img)
    maximo_imagem = aux_list[0]
    minimo_imagem = aux_list[1]

    distribuicao_pixel_imagem_bruta = arange(0, maximo_imagem + 1, 1)
    for i in range(maximo_imagem):
        distribuicao_pixel_imagem_bruta[i] = 0

    # Checagem de quantidade de pixels fora do range.
    pixels_fora_do_range(quant_img)

    contador = marcador_faixa_porcentagem = 0
    for i in range(largura):
        porcentagem = 100 * contador / total_de_pixels
        if porcentagem > faixa_porcentagem[marcador_faixa_porcentagem]:
            marcador_faixa_porcentagem += 1
            system('cls')
            print(f'Imagem_{quant_img + 1} --- Processando... [{porcentagem:.0f}%]')
        for j in range(altura):
            contador += 1
            proporcao_bruta = (camada_imagem[quant_img][i][j] - minimo_imagem) * 255 / (maximo_imagem - minimo_imagem)
            proporcao = (camada_imagem[quant_img][i][j] + media_dark[i][j]) / (media_flat[i][j] + media_dark[i][j])
            pixel = int(255 * proporcao)
            pixel_bruto = int(proporcao_bruta)
            if pixel > 255:
                pixel = 255
            if pixel_bruto > 255:
                pixel_bruto = 255
            distribuicao_pixels_imagem_equal[pixel] += 1
            p = camada_imagem[quant_img][i][j]
            distribuicao_pixel_imagem_bruta[p] += 1
            imagem_bruta.putpixel((i, j), (pixel_bruto, pixel_bruto, pixel_bruto))
            imagem_equalizada.putpixel((i, j), (pixel, pixel, pixel))
    imagem_bruta.save(f'Imagens_brutas\\Imagem_bruta_{quant_img + 1}.png')
    imagem_equalizada.save(f'Imagens_equalizadas\\Imagem_equalizada_{quant_img + 1}.png')
    histograma_imagem(quant_img, distribuicao_pixel_imagem_bruta, distribuicao_pixels_imagem_equal, total_de_pixels)
    # Limpando o vetor histrograma.
    for i in range(len(distribuicao_pixels_imagem_equal)):
        distribuicao_pixels_imagem_equal[i] = 0
        distribuicao_pixel_imagem_bruta[i] = 0

for i in range(quantidade_imagem):
    if pixels_bugados_acima[i] > 0 or pixels_bugados_abaixo[i] > 0:
        porcentagem = 100 * (pixels_bugados_acima[i] + pixels_bugados_abaixo[i]) / total_de_pixels
        print(f'O arquivo imagem_{i + 1}.png apresentou:\n\t{pixels_bugados_acima[i]} pixels acima do limite superior')
        print(f'\t{pixels_bugados_abaixo[i]} pixels abaixo do limite superior')
        print(f'\tPorcentagem total discrepante: {porcentagem:.3f}%\n')

system('pause')
system('cls')
print('\nPrograma executado com sucesso.\n')
system('pause')
