from mongo_connection import conectar_mongo, inserir_dados_no_mongo
from dudu_rapaspadinha3 import setup_driver, accept_cookies, get_shadow_root, capture_game_data
import time
from selenium.webdriver.common.by import By

def realizar_scraping():
    # Configurar o WebDriver e acessar a página
    driver = setup_driver()
    driver.get('https://estrelabet.com/pb/esportes#/virtual')

    # Aceitar cookies
    accept_cookies(driver)

    # Obter o Shadow DOM
    shadow_root = get_shadow_root(driver)

    last_game_ids = set()

    try:
        # Localizar os elementos de jogos
        shadow_host2 = shadow_root.find_element(By.CSS_SELECTOR, 'div:nth-child(1) > div.SportsBookRouterstyled__RoutesWrapper-sc-iwc66s-0.fHjhfY > main > div > div > div.Kironstyled__VirtualTableTennisContainer-sc-jvy8h9-1 > div.Kironstyled__VirtualEventListWrapper-sc-jvy8h9-7.cUhgrY > div')

        game_elements = shadow_host2.find_elements(By.CSS_SELECTOR, 'div.Kironstyled__EventDataContainer-sc-jvy8h9-5')
        for game_element in game_elements:
            game_id = game_element.find_element(By.CSS_SELECTOR, 'div:nth-child(1) > div:nth-child(2)').text
            game_teams = game_element.find_element(By.CSS_SELECTOR, 'div:nth-child(1) > div.Kironstyled__EventData-sc-jvy8h9-3.Kironstyled__EventName-sc-jvy8h9-4.eiCTSg.kzvlWP').text

            if game_id not in last_game_ids:
                last_game_ids.add(game_id)
                
                # Capturar dados do jogo
                game_result = capture_game_data(driver, shadow_root, game_id, game_teams)

                # Conectar ao MongoDB e inserir os dados
                db = conectar_mongo()
                inserir_dados_no_mongo(db, game_id, game_teams, game_result)

                # Saia do loop para evitar múltiplos IDs no mesmo ciclo de scraping
                break

    except Exception as e:
        print(f"Erro ao capturar dados: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    while True:
        realizar_scraping()
        time.sleep(60)  # Ajuste o intervalo para corresponder à duração média dos jogos