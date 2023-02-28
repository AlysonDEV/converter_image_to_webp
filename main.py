import os

import PySimpleGUI as sg
from PIL import Image

# Função para conversão de uma imagem


def convert_image(image_path, delete_original):
    try:
        webp_path = os.path.splitext(image_path)[0] + '.webp'

        with Image.open(image_path) as im:
            im.save(webp_path, 'webp')

        # Apaga a imagem original, se necessário
        if delete_original:
            os.remove(image_path)

        return f'Concluído ({image_path})'
    except:
        # Caso ocorra algum erro na conversão, atualiza o status da imagem na lista
        return f'Erro ({image_path})'

# Função para conversão de todas as imagens de uma pasta


def convert_images(folder_path, delete_original, multithreading):
    # Lista os tipos de imagem que serão convertidos
    image_extensions = ('.png', '.jpeg', '.jpg')

    # Lista todas as imagens na pasta selecionada com os tipos de imagem especificados
    images = [os.path.join(folder_path, file) for file in os.listdir(
        folder_path) if file.endswith(image_extensions)]
    total_images = len(images)

    # Cria a lista de resultados
    results = []

    # Verifica se o multithreading está ativado
    if multithreading:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Executa a função convert_image em cada imagem da lista usando as threads da pool
            results = [executor.submit(
                convert_image, image, delete_original) for image in images]
    else:
        # Executa a função convert_image em cada imagem da lista de forma sequencial
        results = [convert_image(image, delete_original) for image in images]

    # Retorna a lista de resultados
    return results

# Função para apagar todas as imagens de uma lista


def delete_images(images):
    # Percorre a lista de imagens e apaga cada uma
    for image in images:
        os.remove(image)


# Cria o layout do formulário
layout = [
    [sg.Text('Selecione a pasta contendo as imagens:')],
    [sg.Input(key='folder_path'), sg.FolderBrowse()],
    [sg.Checkbox('Excluir arquivos originais', key='delete_original')],
    [sg.Checkbox('Usar multithreading', key='multithreading')],
    [sg.Button('Converter')]
]

# Cria a janela do formulário
window = sg.Window('Conversor de imagens', layout, icon='icon.png')

# Loop principal do programa
while True:
    event, values = window.read()

    # Fecha a janela se o usuário clicar no botão de fechar ou em Cancelar
    if event in (sg.WINDOW_CLOSED, 'Cancel'):
        break

    # Executa a conversão se o usuário clicar em Converter
    if event == 'Converter':
        folder_path = values['folder_path']
        delete_original = values['delete_original']
        multithreading = values['multithreading']

        # Executa a conversão das imagens
        results = convert_images(folder_path, delete_original, multithreading)

        # Exibe o status da conversão na tela
        for status in results:
            print(status)

        # Exibe uma mensagem de conclusão após a conversão
        sg.popup('Conversão concluída!')

# Fecha a janela do formulário
window.close
