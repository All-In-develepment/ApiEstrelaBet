from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configurar o WebDriver do Edge
service = Service(EdgeChromiumDriverManager().install())

driver = webdriver.Edge(service=service)
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': """
Element.prototype._attachShadow = Element.prototype.attachShadow;
Element.prototype.attachShadow = function () {
    return this._attachShadow( { mode: "open" } );
};
"""})
driver.get('https://estrelabet.com/pb#/virtual')

# Aceitar os Cookies
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > app-root > div:nth-child(2) > app-cookie-policy > div > div > div > span > button')))
    accept_button = driver.find_element(By.CSS_SELECTOR, 'body > app-root > div:nth-child(2) > app-cookie-policy > div > div > div > span > button')
    driver.execute_script("arguments[0].click();", accept_button)
    print("Botão de aceitação de cookies clicado.")
    time.sleep(3)
except Exception as e:
    print(f"Erro ao clicar no botão de aceitação de cookies: {e}")

# Localizar o host do Shadow DOM
shadow_host = driver.find_element(By.CSS_SELECTOR, '#container > div')
shadow_root = driver.execute_script('return arguments[0].shadowRoot', shadow_host)

shadow_host2 = shadow_root.find_element(By.CSS_SELECTOR, 'div:nth-child(1) > div.SportsBookRouterstyled__RoutesWrapper-sc-iwc66s-0 > main > div > div > div.Kironstyled__VirtualTableTennisContainer-sc-jvy8h9-1 > div.Kironstyled__VirtualEventListWrapper-sc-jvy8h9-7 > div')

child_elements = shadow_host2.find_elements(By.CLASS_NAME, 'Kironstyled__EventDataContainer-sc-jvy8h9-5')

for game in child_elements:
    game_columns = game.find_elements(By.CLASS_NAME, 'Kironstyled__EventData-sc-jvy8h9-3')
    for col in game_columns:
        if col.text == 'Resultados':
            # Rolando até o elemento 'Resultados'
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", col)
            WebDriverWait(driver, 10).until(EC.visibility_of(col))
            driver.execute_script("arguments[0].click();", col)
            time.sleep(4)

            # Encontrar o container de detalhes do evento dentro do Shadow DOM
            shadow_host3 = shadow_root.find_element(By.CSS_SELECTOR, 'div:nth-child(1) > div.SportsBookRouterstyled__RoutesWrapper-sc-iwc66s-0.fHjhfY > main > div > div > div.Kironstyled__VirtualTableTennisContainer-sc-jvy8h9-1.dYeXtu > div.EventDetailsMarketsstyled__EventDetailsMarketsContainer-sc-qy9han-0.bYqefA')

            # Rolando até o botão 'Resultado Exato' dentro do Shadow DOM
            try:
                exact_results_button = WebDriverWait(shadow_host3, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div:nth-child(8) > div > div > div.EventDetailsMarketBoxstyled__IconsWrapper-sc-p3o2rl-7.ijUPWY > svg'))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", exact_results_button)
                WebDriverWait(driver, 10).until(EC.visibility_of(exact_results_button))
                driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}));", exact_results_button)
                time.sleep(8)  # Aguarde o carregamento da lista de resultados

                # Rolagem para baixo 3 vezes
                for _ in range(3):
                    driver.execute_script("window.scrollBy(0, window.innerHeight);")
                    time.sleep(4)  # Tempo para carregar mais resultados

                last_height = driver.execute_script("return document.body.scrollHeight")

                while True:
                    # Encontre todos os resultados
                    result_elements = shadow_host3.find_elements(By.CSS_SELECTOR, 'div.EventDetailsMarketBoxstyled__EventDetailsMarketWrapperBase-sc-p3o2rl-0.iRpoal > div > div > button.OddBoxVariant0styled__OddBoxButton-sc-1ypym0p-4.copbbS > div > div.OddBoxVariant0styled__OddLabelContent-sc-1ypym0p-0.ejAbYs > span')
                    print(f"Número de elementos de resultado encontrados: {len(result_elements)}")
                    if not result_elements:
                        break

                    # Verificar se os resultados têm a cor de fundo verde
                    for result in result_elements:
                        parent = result.find_element(By.XPATH, '..')
                        background_color = driver.execute_script("return window.getComputedStyle(arguments[0]).backgroundColor;", parent)
                        print(f"Elemento: {result.text}, Background color: {background_color}")
                        if background_color == 'rgb(77, 177, 79)':  # Cor verde identificada
                            print('Resultado exato correto:', result.text)

                    # Rolagem
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)  # Tempo para carregar mais resultados

                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height

            except Exception as e:
                print(f"Erro ao encontrar ou clicar em 'Resultado Exato': {e}")
