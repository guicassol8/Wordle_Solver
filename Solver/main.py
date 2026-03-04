from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import wordle


debug = False
driver = webdriver.Chrome()
driver.get("http://localhost:5173/")
wait = WebDriverWait(driver, 10)

vitorias = 0
derrotas = 0
partidas = 0
tentativas = 0


def printdebug(string):
    if (debug):
        print(string)


def write_word(word):
    actions = ActionChains(driver)
    actions.send_keys(word).perform()


def get_row_colors(row_index):
    cores = []
    for col in range(5):
        try:
            selector = f"#word{row_index + 1} > div:nth-child({col + 1}) > div"
            tile = driver.find_element(By.CSS_SELECTOR, selector)
            classes = tile.get_attribute("class")

            if "bg-green" in classes:
                cores.append("@")
            elif "bg-yellow" in classes:
                cores.append("$")
            elif "bg-slate-700" in classes or "bg-gray-700" in classes:
                cores.append("#")
            else:
                cores.append("?")
        except:
            cores.append("?")
    return cores


def get_background_color():
    try:
        tile = driver.find_element(By.CSS_SELECTOR, '#root > div')
        classes = tile.get_attribute("class")
        if "bg-green" in classes:
            return "verde"
        elif "bg-red-700" in classes:
            return "vermelho"
        else:
            return "desconhecido"
    except:
        return "erro"


def format_feedback(cores, palavra):
    return ''.join([f"{c}{l}" for c, l in zip(cores, palavra)])


def reset_game():
    actions = ActionChains(driver)
    actions.send_keys(Keys.ENTER).perform()


lostwords = []
count = 0
while True:
    wordle.resetAll()
    chute = "arose"

    for linha in range(6):
        time.sleep(0.3)
        tentativas += 1
        # printdebug(f"\n🟦 Tentativa {linha + 1} | Palavra: {chute}")

        write_word(chute)

        cores = get_row_colors(linha)
        resultado = format_feedback(cores, chute)
        # printdebug(f"🎨 Feedback: {resultado}")

        wordle.parseLinha(resultado)
        wordle.teste()

        background = get_background_color()
        # printdebug(background)

        if background == "verde":
            # printdebug("✅ Vitória!")
            vitorias += 1
            break
        elif background == "vermelho":
            # printdebug("❌ Derrota!")
            word = driver.find_element(
                By.CSS_SELECTOR, "#root > div > div > p.mt-4.text-white.text-lg > span")

            print(word.text)
            lostwords.append(word.text)
            derrotas += 1
            break
        else:
            chute = wordle.chuteQuatro()

    partidas += 1
    count += 1
    print(
        f"\n📊 Estatísticas: {partidas} partidas | {vitorias} vitórias | {derrotas} derrotas | {tentativas} tentativas\n"
    )
    if (count == 8497):
        print(lostwords)
        break

    # printdebug(f"\n📊 Estatísticas: {partidas} partidas | {vitorias} vitórias | {derrotas} derrotas | {tentativas} tentativas\n")

    reset_game()
