#######################################################################################################################################################
# Esse código faz a integração do código que resolve o jogo e o site.
# De maneira resumida, ele recebe a palavra do código e escreve no site, passando as informações para as funções do "wordle.py".
# Existem alguns casos que podem ocasionar em um corportamento inesperado:
# - Quando uma palavra está no dicionário mas não está no site o código trata esse erro adicionando no arquivo "descarte.txt" a palavra, evitando erros futuros
# - Quando uma palavra não está presente no dicionário da aplicação, o programa identifica isso e desiste do jogo, adicionando a palavra ao arquivo "adicao.txt"
# De maneira geral estou muito satisfeito com o projeto, a taxa de acerto é alta com uma taxa de chutes satisfatória.
# Caso queira rodar o código instale as bibliotecas nltk e selenium, depois rode o game.py o código irá testar 10 palavras. Para uma maior amostragem,
# apenas mude o valor no While principal.
# Importante ressaltar que muitos dos erros acontecem pois o dicionario atual não tem a palavra necessária por isso é necessário desistir.
######################################################################################################################################################
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import time
import wordle


def write_word(driver, word):
    if len(word) != 5:
        raise ValueError("A palavra deve ter exatamente 5 letras.")

    driver.find_element(By.TAG_NAME, 'body').send_keys(word)
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.RETURN)


def analyze_row_colors(driver, row_index):
    # Mapeamento de emojis para cores
    colors = {
        "⬛": "#",   # Letra não presente (black tile)
        "🟨": "$",   # Letra na palavra, mas posição errada (yellow tile)
        "🟩": "@",   # Letra na posição correta (green tile)
    }

    board = driver.find_element(By.CLASS_NAME, 'board')
    board_rows = board.find_elements(By.CLASS_NAME, 'board-row')

    # Seleciona a linha correta (row_index)
    row_tiles = board_rows[row_index].find_elements(By.CLASS_NAME, 'tile')

    result = ""
    for tile in row_tiles:
        # Obtendo o emoji (símbolo de cor) e o conteúdo do front
        color_symbol = tile.get_attribute("class").split(
            " ")[1]  # Pega a segunda classe, que representa a cor
        # Obtém o texto do elemento 'front'
        letter = tile.find_element(By.CLASS_NAME, 'front').text

        # Adiciona a cor correspondente e a letra ao resultado
        if color_symbol in colors:
            # Adiciona uma tupla com a cor e a letra
            result += (colors[color_symbol] + letter.lower())
        else:
            # Para cores que não estão no mapeamento, mas ainda adiciona a letra
            result += ("unknown" + letter.lower())

    return result


driver = webdriver.Chrome()
driver.get("https://mikhad.github.io/wordle/#infinite")

elemento = driver.find_element(By.CLASS_NAME, 'exit')
elemento.click()
row = 0
wait = WebDriverWait(driver, 10)
firstGuess = True
wordCounter = 0
final = 0
while final < 100000:
    if row == 6:
        wordle.resetAll()
        button = wait.until(EC.visibility_of_element_located(
            (By.CLASS_NAME, 'button')))
        svg_element = driver.find_element(By.CLASS_NAME, 'button')
        svg_element.click()
        row = 0
        svg_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "svelte-17ud64h"))
        )

    # Obtém a localização do elemento
        location = svg_element.location
        size = svg_element.size

    # Realiza o clique levemente deslocado para a direita
        actions = ActionChains(driver)
        actions.move_to_element_with_offset(
            svg_element, 20, 0).click().perform()
        row = 0
        firstGuess = True
        wordCounter += 1
        continue
    palavra = wordle.chuteQuatro()
    if firstGuess:
        palavra = "soare"
        firstGuess = False
    if palavra == "flago":
        svg_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "svelte-17ud64h"))
        )


# Realiza o clique levemente deslocado para a direita
        actions = ActionChains(driver)
        actions.move_to_element_with_offset(
            svg_element, 480, 0).click().perform()
        container = driver.find_element(
            By.CSS_SELECTOR, ".overlay.fullscreen.svelte-5i44vt")

        actions = ActionChains(driver)

# Move até a posição do botão e clica no contêiner nessa posição
        actions.move_to_element_with_offset(
            container, 50, 50).click().perform()
        driver.implicitly_wait(10)

# Localize o container principal
        overlay = driver.find_element(
            By.CSS_SELECTOR, '.overlay.popup.visible')

# Dentro do container, encontre o elemento de conteúdo
        content = overlay.find_element(By.CLASS_NAME, 'content')

# Encontre o elemento 'def' dentro do conteúdo
        definition = content.find_element(By.CLASS_NAME, 'def')

# Localize o <h2> dentro do elemento 'def' e obtenha seu texto
        title_element = definition.find_element(By.TAG_NAME, 'h2')
        title_text = title_element.text
        wordle.palavraAdicional(title_text)
        wordle.resetAll()
    # Clica no botão
        row = 0
        firstGuess = True
        wordCounter += 1
        svg_element = driver.find_element(By.CLASS_NAME, 'button')
        svg_element.click()
        continue
    # print(f"CHUTE FEITO: {palavra} \n\n")
    # palavra = input("Digite a palavra: ")
    if palavra == "-1":
        break
    if palavra == "0":
        wordle.resetAll()
        button = wait.until(EC.visibility_of_element_located(
            (By.CLASS_NAME, 'button')))
        svg_element = driver.find_element(By.CLASS_NAME, 'button')
        svg_element.click()
        row = 0
        firstGuess = True
        wordCounter += 1
        continue
    write_word(driver, palavra)
    # time.sleep(3)
    # Analisando a primeira linha (índice 0)
    result = analyze_row_colors(driver, row)
    # Vitória
    if result.count("@") == 5:
        wordle.resetAll()
        svg_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "svelte-17ud64h"))
        )
        actions = ActionChains(driver)
        actions.move_to_element_with_offset(
            svg_element, 20, 0).click().perform()
        row = 0
        firstGuess = True
        wordCounter += 1
        final += 1
        continue
    # Palavra inválida
    if "unknow" in result:
        driver.find_element(By.TAG_NAME, 'body').send_keys("")
        wordle.palavraIncorreta(palavra)
        # print(wordle.chuteQuatro())
        continue
    row += 1
    if result.count("@") != 5 and row == 6:
        wordle.resetAll()
        button = wait.until(EC.visibility_of_element_located(
            (By.CLASS_NAME, 'button')))
        svg_element = driver.find_element(By.CLASS_NAME, 'button')
        svg_element.click()
        row = 0
        svg_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "svelte-17ud64h"))
        )
        location = svg_element.location
        size = svg_element.size
        actions = ActionChains(driver)
        actions.move_to_element_with_offset(
            svg_element, 20, 0).click().perform()
        row = 0
        firstGuess = True
        wordCounter += 1
        continue
    wordle.parseLinha(result)
    wordle.teste()
    # time.sleep(0.5)

    # print(result)

input()
driver.quit()
