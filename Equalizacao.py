import numpy as np
from os import system
from PIL import Image
from matplotlib import pyplot as plt
from skimage.io import imread

def extracao_dos_dados(nome_camada, quantidade_arquivos):
    system('cls')
    print('RECORTE DA PORÇÃO DEFEITUOSA DA IMAGEM BRUTA')
    for indice in range(quantidade_arquivos):
        # Abertura dos arquivos brutos de imagem e recorte para remoção da porção com defeito.
        try:
            extensao = 'jpg'
            arquivo_imagem = Image.open(f'Dados\\{nome_camada}_{indice + 1}.{extensao}')
        except:
            try:
                extensao = 'jpeg'
                arquivo_imagem = Image.open(f'Dados\\{nome_camada}_{indice + 1}.{extensao}')
            except:
                try:
                    extensao = 'png'
                    arquivo_imagem = Image.open(f'Dados\\{nome_camada}_{indice + 1}.{extensao}')
                except:
                    print(f'ERRO: não foi possível abrir o arquivo {nome_camada}_{indice + 1}.\n')
                    system('pause')
                    exit()
        print(f'\tRedimensionando o arquivo {nome_camada}_{indice + 1}.{extensao}')
        tamanho = arquivo_imagem.size
        imagem_reduzida = arquivo_imagem.crop((corte_da_borda, 0, tamanho[0], tamanho[1]))
        imagem_reduzida.save(f'Dados_formatados\\imagem_cortada_{indice + 1}.{extensao}')

    system('cls')
    print('EXTRAÇÃO DOS DADOS DAS IMAGENS CORTADAS')
    for indice in range(quantidade_arquivos):
        # Abertura dos arquivos brutos de imagem.
        try:
            extensao = 'jpg'
            arquivo_imagem = Image.open(f'Dados_formatados\\{nome_camada}_cortada_{indice + 1}.{extensao}')
        except:
            try:
                extensao = 'jpeg'
                arquivo_imagem = Image.open(f'Dados_formatados\\{nome_camada}_cortada_{indice + 1}.{extensao}')
            except:
                try:
                    extensao = 'png'
                    arquivo_imagem = Image.open(f'Dados_formatados\\{nome_camada}_cortada_{indice + 1}.{extensao}')
                except:
                    print(f'ERRO: não foi possível abrir o arquivo {nome_camada}_cortada_{indice + 1}.\n')
                    system('pause')
                    exit()
        print(f'\tLendo arquivo {nome_camada}_cortada_{indice + 1}.{extensao}')
        lista_de_arquivos.append(arquivo_imagem)
        tamanho = arquivo_imagem.size
        maximo = minimo = 0
        for x in range(tamanho[0]):
            for y in range(tamanho[1]):
                camada_imagem[indice][x][y] = arquivo_imagem.getpixel((x, y))
                if maximo < camada_imagem[indice][x][y]:
                    maximo = camada_imagem[indice][x][y]
                if minimo > camada_imagem[indice][x][y]:
                    minimo = camada_imagem[indice][x][y]
        maximo_minimo_img_bruta[indice][0] = maximo
        maximo_minimo_img_bruta[indice][1] = minimo
    return extensao


def fator_de_pico(quantidade_arquivos):
    razao = np.zeros((largura, altura))
    for indice in range(quantidade_arquivos):
        system('cls')
        print(f'CÁLCULO DO FATOR DE PICO - IMAGEM {indice + 1}')
        # Cálculo da razão da imagem pelo flat.
        print('\tCálculo da razão da imagem pelo flat.')
        for x in range(largura):
            for y in range(altura):
                razao[x][y] = camada_imagem[indice][x][y] / dados_arquivo_flat[x][y]

        # Monitoramento da frequência absoluta.
        print('\tMonitoramento da frequência absoluta.')
        aux_lista = razao.flatten() # Converte uma matriz multidimensional em um vetor unidimensional.
        frequencia = np.unique(aux_lista, return_counts = True) # Verifica a frequência absoluta dos valores da lista.

        maior_frequencia = 0
        maior_valor_frequencia = 0.0

        for x in range(len(frequencia[0])):
            if maior_frequencia < frequencia[1][x]:
                maior_frequencia = frequencia[1][x]
                maior_valor_frequencia = frequencia[0][x]
        '''
        for x in range(len(frequencia[0])):
            if maior_valor_frequencia < frequencia[0][x]:
                maior_frequencia = frequencia[1][x]
                maior_valor_frequencia = frequencia[0][x]
        '''

        # Gráfico da frequência da razão.
        figura = plt.figure(figsize = (8, 4))
        plt.plot(frequencia[0], frequencia[1], color = 'red', lw = 0.6)
        plt.xlabel('Frequência absoluta', fontsize = 10)
        plt.ylabel('Razão', fontsize = 10)
        plt.title(f'RAZÃO DA IMAGEM {indice + 1}', fontsize = 12)
        plt.grid(True)
        figura.savefig(f'Graficos\\Frequencia_razao_{indice + 1}.png', dpi = 400)
        plt.close(figura)

        #maior_valor_frequencia = max(frequencia[0]) # Linha de código para utilizar o valor máximo da razão imagem / flat.

        # Cálculo do fator.
        fator = 1 / maior_valor_frequencia

        # Multiplicação da matriz razão pelo fator de correção.
        print('\tMultiplicação da matriz razão pelo fator de correção.')
        maximo = minimo = 0
        for x in range(largura):
            for y in range(altura):
                nova_camada_imagem[indice][x][y] = int(fator * camada_imagem[indice][x][y])
                if maximo < nova_camada_imagem[indice][x][y]:
                    maximo = nova_camada_imagem[indice][x][y]
                if minimo > nova_camada_imagem[indice][x][y]:
                    minimo = nova_camada_imagem[indice][x][y]
        maximo_minimo_img_ajustada[indice][0] = maximo
        maximo_minimo_img_ajustada[indice][1] = minimo


def histograma_total(quant_imagens, extensao):
    for indice in range(quant_imagens):
        system('cls')
        print(f'CRIAÇÃO DOS HISTOGRAMAS - IMAGEM {indice + 1}\n\tExtração dos extremos dos dados originais.')
        eixo_x_1 = np.arange(maximo_minimo_img_bruta[indice][1], maximo_minimo_img_bruta[indice][0] + 1, 1)
        eixo_y_1 = np.full(len(eixo_x_1), 0)
        eixo_x_2 = np.arange(maximo_minimo_img_ajustada[indice][1], maximo_minimo_img_ajustada[indice][0] + 1, 1)
        eixo_y_2 = np.full(len(eixo_x_2), 0)

        # Monitoramento das frequências absolutas dos dados.
        print('\tMonitoramento das frequências absolutas dos dados.')
        for x in range(largura):
            for y in range(altura):
                pixel = camada_imagem[indice][x][y]
                eixo_y_1[pixel] += 1
                pixel = nova_camada_imagem[indice][x][y]
                eixo_y_2[pixel] += 1
        
        # Plotagem do gráfico.
        print('\tPlotagem do gráfico.')
        figura, axes = plt.subplots(nrows = 2, ncols = 2, figsize = (8, 4))
        plt.subplots_adjust(left = 0.045, right = 0.94, hspace = 0.329)
        imagem = imread(f'Dados_formatados\\imagem_cortada_{indice + 1}.{extensao}')
        axes[0][0].imshow(imagem, cmap = 'gray')
        axes[0][1].plot(eixo_x_1, eixo_y_1, color = 'blue', lw = 0.6)
        imagem = imread(f'Imagens_equalizadas\\Imagem_ajustada_{indice + 1}.{extensao}')
        axes[1][0].imshow(imagem, cmap = 'gray')
        axes[1][1].plot(eixo_x_2, eixo_y_2, color = 'blue', lw = 0.6)
        # Legendas e rótulos.
        plt.suptitle(f'IMAGEM {indice + 1}', fontsize = 12)
        axes[0][1].set_xlabel('Pixels', fontsize = 10)
        axes[0][1].set_ylabel('Frequência absoluta', fontsize = 10)
        axes[0][1].grid(True)
        axes[1][1].set_xlabel('Pixels', fontsize = 10)
        axes[1][1].set_ylabel('Frequência absoluta', fontsize = 10)
        axes[1][1].grid(True)
        axes[0][0].set_title('Imagem bruta', fontsize = 10)
        axes[1][0].set_title('Imagem filtrada', fontsize = 10)
        figura.savefig(f'Graficos\\Resultado_{indice + 1}.{extensao}', dpi = 400)
        plt.close(figura)
        # Plotagem dos gráficos sobrepostos para comparação.
        figura_2 = plt.figure(figsize = (8, 4))
        plt.plot(eixo_x_1, eixo_y_1, color = 'green', lw = 0.7, label = 'Imagem bruta')
        plt.plot(eixo_x_2, eixo_y_2, color = 'red', lw = 0.7, label = 'Imagem ajustada')
        plt.title(f'IMAGEM {indice + 1} - SOBREPOSIÇÃO', fontsize = 12)
        plt.xlabel('Pixels', fontsize = 10)
        plt.ylabel('Frequência absoluta', fontsize = 10)
        plt.legend()
        plt.grid(True)
        figura_2.savefig(f'Graficos\\Sobrep_grafico_img_{indice + 1}.{extensao}', dpi = 400)
        plt.close(figura)


def importacao_dados_flat():
    system('cls')
    print('RECORTE DA PORÇÃO DEFEITUOSA DO ARQUIVO FLAT')
    try:
        extensao = 'jpg'
        arquivo_imagem = Image.open(f'Dados\\flat.{extensao}')
    except:
        try:
            extensao = 'jpeg'
            arquivo_imagem = Image.open(f'Dados\\flat.{extensao}')
        except:
            try:
                extensao = 'png'
                arquivo_imagem = Image.open(f'Dados\\flat.{extensao}')
            except:
                print('ERRO: não foi possível abrir o arquivo FLAT.\n')
                system('pause')
                exit()

    tamanho = arquivo_imagem.size
    imagem_reduzida = arquivo_imagem.crop((corte_da_borda, 0, tamanho[0], tamanho[1]))
    imagem_reduzida.save(f'Dados_formatados\\flat_cortado.{extensao}')

    print('IMPORTAÇÃO DOS DADOS DO ARQUIVO FLAT CORTADO')
    try:
        extensao = 'jpg'
        arquivo_imagem = Image.open(f'Dados_formatados\\flat_cortado.{extensao}')
    except:
        try:
            extensao = 'jpeg'
            arquivo_imagem = Image.open(f'Dados_formatados\\flat_cortado.{extensao}')
        except:
            try:
                extensao = 'png'
                arquivo_imagem = Image.open(f'Dados_formatados\\flat_cortado.{extensao}')
            except:
                print('ERRO: não foi possível abrir o arquivo FLAT.\n')
                system('pause')
                exit()

    tamanho = arquivo_imagem.size
    for x in range(tamanho[0]):
        for y in range(tamanho[1]):
            dados_arquivo_flat[x][y] = arquivo_imagem.getpixel((x, y))


def plotagem_imagem_ajustada(quant_imagens, extensao):
    arquivo_imagem = Image.new('RGB', (largura, altura), 'red')
    for indice in range(quant_imagens):
        # Verificação do máximo e mínimo valor da matriz.
        system('cls')
        print(f'PLOTAGEM DA IMAGEM AJUSTADA - IMAGEM {indice + 1}')
        minimo = maximo_minimo_img_ajustada[indice][1]
        maximo = maximo_minimo_img_ajustada[indice][0]

        # Plotagem das imagens ajustadas.
        print('\tPlotagem das imagens ajustadas.')
        for x in range(largura):
            for y in range(altura):
                pixel = int(255 * (nova_camada_imagem[indice][x][y] + minimo) / (maximo + minimo))
                arquivo_imagem.putpixel((x, y), (pixel, pixel, pixel))
        # Salvando a imagem gerada.
        print('\tSalvando a imagem gerada.')
        arquivo_imagem.save(f'Imagens_equalizadas\\Imagem_ajustada_{indice + 1}.{extensao}')


#-----PROGRAMA PRINCIPAL-----
# Dimensões das imagens.
corte_da_borda = 50
largura = 1400 - corte_da_borda
altura = 1200

lista_de_arquivos = []
lista_de_arquivos_brutos = []

# Solicitação ao usuário das quantidades de arquivos dark, flat e imagem que serão usadas.
system('cls')
print('PARÂMETROS INICIAIS')
quantidade_imagem = int(input('\tQuantidade de arquivos de imagem: '))
system('cls')

# Matrizes para armazenamento dos dados.
dados_arquivo_flat = np.zeros((largura, altura), dtype = 'i')
camada_imagem = np.zeros((quantidade_imagem, largura, altura), dtype = 'i')
nova_camada_imagem = np.zeros((quantidade_imagem, largura, altura), dtype = 'i')
maximo_minimo_img_bruta = np.zeros((quantidade_imagem, 2), dtype = 'i')
maximo_minimo_img_ajustada = np.zeros((quantidade_imagem, 2), dtype = 'i')

# Aquisição dos dados dos arquivos imagem.
importacao_dados_flat()
extensao_das_imagens = extracao_dos_dados('imagem', quantidade_imagem)
fator_de_pico(quantidade_imagem)
plotagem_imagem_ajustada(quantidade_imagem, extensao_das_imagens)
histograma_total(quantidade_imagem, extensao_das_imagens)

print('\nPrograma executado com sucesso!\n')
system('pause')
