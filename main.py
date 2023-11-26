from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import requests
def getNavegadorFromURL(url):
    navegador = webdriver.Chrome()
    # 'https://www.nba.com/stats/players/transition?SeasonType=Regular+Season'
    navegador.get(url)
    return navegador
def selectAllPages(navegador):
    xpathSelectAll = '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[3]/div/label/div/select/option[1]'
    return navegador.find_element(By.XPATH, xpathSelectAll).click()
def getElementTHeadTr(navegador):
    xpathHead = '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/thead/tr'
    return navegador.find_element(By.XPATH, xpathHead)
def getElementTBody(navegador):
    xPathTBody = '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody'
    return navegador.find_element(By.XPATH, xPathTBody)

def getSeasonType(url):
    params = requests.utils.urlparse(url).query
    if 'SeasonType' in params:
        season_type_value = params.split('=')[1]
        season_true_value = season_type_value.split('+')[0]
        print("O valor do parâmetro SeasonType é:", season_true_value)
        return season_true_value
    else:
        print("O parâmetro SeasonType não está presente na URL.")

url = 'https://www.nba.com/stats/players/transition?SeasonType=Regular+Season'
navegador = getNavegadorFromURL(url)

valorSeason = getSeasonType(url)

selectAllPages(navegador)

elementoHeadTr = getElementTHeadTr(navegador)

elementoTBody = getElementTBody(navegador)

elementosTrHead = elementoHeadTr.find_elements(By.TAG_NAME, 'th')

# Crie uma lista para armazenar os registros do tbody
dados_tbody = []

# Obtenha todas as linhas (tr) do tbody
linhas_tbody = elementoTBody.find_elements(By.TAG_NAME, 'tr')

# Itere sobre as linhas do tbody
for linha in linhas_tbody:
    # Crie um dicionário para armazenar os valores dos elementos <th> para cada linha
    registro = {}
    # Obtenha todos os elementos <th> da linha
    elementos_td = linha.find_elements(By.TAG_NAME, 'td')
    # Itere sobre os elementos <th> e armazene os valores no dicionário
    for i, th in enumerate(elementos_td):
        nome_coluna = elementosTrHead[i].text
        valor_coluna = th.text
        registro[nome_coluna] = valor_coluna
    # Adicione a identificação da tabela ao registro
    registro['REG/OFFS'] = valorSeason  # Substitua 'Playoffs' pelo nome correto
    # Adicione o registro à lista de dados do tbody
    dados_tbody.append(registro)

# Agora, você tem uma lista (dados_tbody) contendo os registros do tbody, incluindo a identificação da tabela
df = pd.DataFrame(dados_tbody)
print(df)

navegador.quit()