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

# Localizar o host do Shadow DOM
WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located)
shadow_host = driver.find_element(By.CSS_SELECTOR, '#container > div')
shadow_root = driver.execute_script('return arguments[0].shadowRoot', shadow_host)

shadow_host2 = shadow_root.find_element(By.CSS_SELECTOR, 'div:nth-child(1) > div.SportsBookRouterstyled__RoutesWrapper-sc-iwc66s-0 > main > div > div > div.Kironstyled__VirtualTableTennisContainer-sc-jvy8h9-1 > div.Kironstyled__VirtualEventListWrapper-sc-jvy8h9-7 > div > div:nth-child(4) > div:nth-child(2)')
print(shadow_host2.text)

driver.quit()