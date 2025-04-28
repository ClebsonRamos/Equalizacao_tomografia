from os import system
import matplotlib.pyplot as plt
from PIL import Image

def histograma(eixo_x, eixo_y, titulo, titulo_x, titulo_y, caminho_salvamento):
    plt.bar(eixo_x, eixo_y)
    plt.xlabel(f'{titulo_x}', fontsize = 12)
    plt.ylabel(f'{titulo_y}', fontsize = 12)
    plt.title(f'{titulo}')
    plt.plot()
    plt.savefig(f'{caminho_salvamento}')


num_imagens = int(input('Número de imagens: '))

eixo_x = []
eixo_y = []

for i in range(256):
    eixo_x.append(i)
    eixo_y.append(0)

system('cls')
print('RENDERIZANDO...\n')
for i in range(num_imagens):
    print(f'\tHistograma da imagem bruta {i + 1}', end = '')
    arquivo_imagem_1 = Image.open(f'Imagens_brutas\\Imagem_bruta_{i + 1}.png')
    dimensoes = arquivo_imagem_1.size
    total_de_pixels = dimensoes[0] * dimensoes[1]
    for x in range(dimensoes[0]):
        for y in range(dimensoes[1]):
            pixel = arquivo_imagem_1.getpixel((x, y))
            eixo_y[pixel[0]] += 1
    for x in range(len(eixo_y)):
        eixo_y[x] = 100 * eixo_y[x] / total_de_pixels
    histograma(eixo_x, eixo_y, f'Histograma imagem bruta {i + 1}', 'Escala de cinza', 'Frequência (%)', f'Imagens_brutas\\Histograma_imagem_bruta_{i + 1}.png')
    print(' --- OK')
    for x in range(len(eixo_y)):
        eixo_y[x] = 0

print('\n')

for i in range(num_imagens):
    print(f'\tHistograma da imagem equalizada {i + 1}', end = '')
    arquivo_imagem_1 = Image.open(f'Imagens_equalizadas\\Imagem_equalizada_{i + 1}.png')
    dimensoes = arquivo_imagem_1.size
    total_de_pixels = dimensoes[0] * dimensoes[1]
    for x in range(dimensoes[0]):
        for y in range(dimensoes[1]):
            pixel = arquivo_imagem_1.getpixel((x, y))
            eixo_y[pixel[0]] += 1
    for x in range(len(eixo_y)):
        eixo_y[x] = 100 * eixo_y[x] / total_de_pixels
    histograma(eixo_x, eixo_y, f'Histograma imagem equalizada {i + 1}', 'Escala de cinza', 'Frequência (%)', f'Imagens_equalizadas\\Histograma_imagem_equalizada_{i + 1}.png')
    print(' --- OK')
    for x in range(len(eixo_y)):
        eixo_y[x] = 0
