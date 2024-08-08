from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Função para configurar o WebDriver
def setup_driver():
    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': """
    Element.prototype._attachShadow = Element.prototype.attachShadow;
    Element.prototype.attachShadow = function () {
        return this._attachShadow( { mode: "open" } );
    };
    """})
    return driver

# Função para aceitar os cookies
def accept_cookies(driver):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > app-root > div:nth-child(2) > app-cookie-policy > div > div > div > span > button')))
        accept_button = driver.find_element(By.CSS_SELECTOR, 'body > app-root > div:nth-child(2) > app-cookie-policy > div > div > div > span > button')
        driver.execute_script("arguments[0].click();", accept_button)
        print("Botão de aceitação de cookies clicado.")
        time.sleep(3)
    except Exception as e:
        print(f"Erro ao clicar no botão de aceitação de cookies: {e}")

# Função para obter o Shadow DOM
def get_shadow_root(driver):
    shadow_host = driver.find_element(By.CSS_SELECTOR, '#container > div')
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', shadow_host)
    return shadow_root

# Função para capturar dados de uma partida
def capture_game_data(driver, shadow_root, game_number, game_id, game_teams):
    print(f"\nResultados para o ID {game_id} e times {game_teams}:")
    
    shadow_host2 = shadow_root.find_element(By.CSS_SELECTOR, 'div:nth-child(1) > div.SportsBookRouterstyled__RoutesWrapper-sc-iwc66s-0 > main > div > div > div.Kironstyled__VirtualTableTennisContainer-sc-jvy8h9-1 > div.Kironstyled__VirtualEventListWrapper-sc-jvy8h9-7 > div')

    # Processar resultados
    child_elements = shadow_host2.find_elements(By.CLASS_NAME, 'Kironstyled__EventDataContainer-sc-jvy8h9-5')

    for game in child_elements:
        game_columns = game.find_elements(By.CLASS_NAME, 'Kironstyled__EventData-sc-jvy8h9-3')
        for col in game_columns:
            if col.text == 'Resultados':
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", col)
                WebDriverWait(driver, 10).until(EC.visibility_of(col))
                driver.execute_script("arguments[0].click();", col)
                time.sleep(4)

                # Novo seletor para "Número Exato de Gols"
                shadow_host3 = shadow_root.find_element(By.CSS_SELECTOR, 'div:nth-child(1) > div.SportsBookRouterstyled__RoutesWrapper-sc-iwc66s-0.fHjhfY > main > div > div > div.Kironstyled__VirtualTableTennisContainer-sc-jvy8h9-1.dYeXtu > div.EventDetailsMarketsstyled__EventDetailsMarketsContainer-sc-qy9han-0.bYqefA')

                try:
                    exact_goals_button = WebDriverWait(shadow_host3, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div:nth-child(7) > div > div > div.EventDetailsMarketBoxstyled__IconsWrapper-sc-p3o2rl-7.ijUPWY > svg'))
                    )
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", exact_goals_button)
                    WebDriverWait(driver, 10).until(EC.visibility_of(exact_goals_button))
                    driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}));", exact_goals_button)
                    time.sleep(8)

                    for _ in range(3):
                        driver.execute_script("window.scrollBy(0, window.innerHeight);")
                        time.sleep(4)

                    last_height = driver.execute_script("return document.body.scrollHeight")

                    while True:
                        result_elements = shadow_host3.find_elements(By.CSS_SELECTOR, 'div.EventDetailsMarketBoxstyled__EventDetailsMarketWrapperBase-sc-p3o2rl-0.iRpoal > div > div > button.OddBoxVariant0styled__OddBoxButton-sc-1ypym0p-4.copbbS > div > div.OddBoxVariant0styled__OddLabelContent-sc-1ypym0p-0.ejAbYs > span')

                        if not result_elements:
                            break

                        for result in result_elements:
                            print(f"Resultado encontrado: {result.text}")

                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(2)

                        new_height = driver.execute_script("return document.body.scrollHeight")
                        if new_height == last_height:
                            break
                        last_height = new_height

                except Exception as e:
                    print(f"Erro ao encontrar ou clicar em 'Número Exato de Gols': {e}")

# Função principal
def main():
    driver = setup_driver()
    driver.get('https://estrelabet.com/pb#/virtual')

    accept_cookies(driver)
    shadow_root = get_shadow_root(driver)

    # Captura de dados do primeiro ID
    try:
        shadow_host2 = shadow_root.find_element(By.CSS_SELECTOR, 'div:nth-child(1) > div.SportsBookRouterstyled__RoutesWrapper-sc-iwc66s-0.fHjhfY > main > div > div > div.Kironstyled__VirtualTableTennisContainer-sc-jvy8h9-1 > div.Kironstyled__VirtualEventListWrapper-sc-jvy8h9-7.cUhgrY > div')

        first_game_id_element = WebDriverWait(shadow_host2, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div:nth-child(1) > div:nth-child(2)'))
        )
        first_game_id = first_game_id_element.text

        first_game_teams_element = shadow_host2.find_element(By.CSS_SELECTOR, 'div:nth-child(1) > div.Kironstyled__EventData-sc-jvy8h9-3.Kironstyled__EventName-sc-jvy8h9-4.eiCTSg.kzvlWP')
        first_game_teams = first_game_teams_element.text

        print(f"Primeiro ID da partida encontrado: {first_game_id}")
        print(f"Times do primeiro ID: {first_game_teams}")

        capture_game_data(driver, shadow_root, "primeiro", first_game_id, first_game_teams)
    except Exception as e:
        print(f"Erro ao capturar dados do primeiro ID: {e}")

    # Fechar o navegador
    driver.quit()

if __name__ == "__main__":
    main()
