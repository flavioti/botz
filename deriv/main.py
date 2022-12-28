import logging
import os
import re
import sys
from datetime import datetime
from time import sleep
from typing import Union

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox import firefox_binary
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxWebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.safari.webdriver import WebDriver as SafariDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DerivBase:
    def get_driver(self) -> Union[ChromeWebDriver, FirefoxWebDriver]:
        """
        Retorna o driver com base na configuração
        """

        logger.info(f"Loading driver: {settings.driver}")
        if settings.driver == "chrome":
            return webdriver.Chrome()
        else:
            raise NotImplemented(settings.driver)

    def do_login(self, user: str, password: str):
        btn_login: WebElement = WebDriverWait(self.driver, 30, 0.1).until(
            expected_conditions.presence_of_element_located((By.ID, "dt_login_button"))
        )
        btn_login.click()

        logger.info("Pegando o campo de usuário")
        txtEmail: WebElement = WebDriverWait(self.driver, 30, 0.1).until(
            expected_conditions.presence_of_element_located((By.ID, "txtEmail"))
        )
        txtEmail.send_keys(user)

        logger.info("Pegando o campo de senha")
        txtPass: WebElement = WebDriverWait(self.driver, 30, 0.1).until(
            expected_conditions.presence_of_element_located((By.ID, "txtPass"))
        )
        txtPass.send_keys(password)

        eleLogin: WebElement = WebDriverWait(self.driver, 30, 0.1).until(
            expected_conditions.presence_of_element_located((By.NAME, "login"))
        )
        eleLogin.click()

    def do_close_modal(self):
        logger.info("Aguarda o modal aparecer")
        WebDriverWait(self.driver, 30, 0.1).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, "dc-modal"))
        )

        logger.info("Deleta o modal")
        self.driver.execute_script(
            """
            var modal = document.getElementsByClassName('dc-modal')[0];
            modal.parentNode.removeChild(modal);
            """
        )

        logger.info("banners propaganda")
        while True:
            try:
                element: WebElement = WebDriverWait(
                    driver=self.driver,
                    timeout=5,
                    poll_frequency=0.5,
                    ignored_exceptions=[TimeoutException],
                ).until(
                    expected_conditions.presence_of_element_located(
                        (By.CLASS_NAME, "notification-banner__close-icon")
                    )
                )
                if element:
                    element.click()
                else:
                    break
            except:
                break

        logger.info("banners web trade")
        try:
            element: WebElement = WebDriverWait(
                driver=self.driver,
                timeout=5,
                poll_frequency=0.5,
                ignored_exceptions=[TimeoutException],
            ).until(
                expected_conditions.presence_of_element_located(
                    (By.CLASS_NAME, "notification__close-button")
                )
            )
            if element:
                element.click()
        except:
            pass

    def open_url(self):
        raise NotImplemented("Implement on base class")


class DerivR100(DerivBase):
    def __init__(self) -> None:
        super().__init__()
        self.driver = self.get_driver()

    def open_url(self):
        self.driver.get(settings.url)

    def config_demo_account(self):
        WebDriverWait(self.driver, 30, ignored_exceptions=[]).until(
            expected_conditions.presence_of_element_located(
                (By.ID, "dt_core_account-info_acc-info")
            )
        ).click()

        WebDriverWait(self.driver, 30, ignored_exceptions=[]).until(
            expected_conditions.presence_of_element_located(
                (By.ID, "dt_core_account-switcher_demo-tab")
            )
        ).click()

        WebDriverWait(self.driver, 30, ignored_exceptions=[]).until(
            expected_conditions.presence_of_element_located(
                (By.CLASS_NAME, "acc-switcher__id")
            )
        ).click()

    def do_config_r100(self):
        logger.info("Volatilidade")
        volatility_element_name = "cq-symbol-select-btn"
        sleep(1)
        WebDriverWait(
            self.driver,
            30 + 10,
            ignored_exceptions=[
                StaleElementReferenceException,
            ],
        ).until(
            expected_conditions.presence_of_element_located(
                (By.CLASS_NAME, volatility_element_name)
            )
        ).click()

        sleep(1)
        WebDriverWait(self.driver, 30 + 10).until(
            expected_conditions.presence_of_element_located(
                (By.CLASS_NAME, "sc-mcd__item--R_100")
            )
        ).click()

        logger.info("seletor de modalidade (combina/difere)")
        sleep(1)
        WebDriverWait(self.driver, 30 + 10).until(
            expected_conditions.presence_of_element_located(
                (By.CLASS_NAME, "contract-type-widget__display")
            )
        ).click()

        logger.info("Clica no combina/difere")
        sleep(1)
        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located(
                (By.ID, "dt_contract_match_diff_item")
            )
        ).click()

        tick_0 = (
            "/html/body/div[1]/div/div/div/div[4]/div/fieldset[3]/div[2]/div[1]/span[1]"
        )

        logger.info("ticks")
        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located((By.XPATH, tick_0))
        ).click()

        logger.info("entrada")
        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located(
                (By.ID, "dc_stake_toggle_item")
            )
        ).click()

        logger.info("valor")
        element = WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located((By.ID, "dt_amount_input"))
        )

        while len(element.get_attribute("value")) > 0:
            element.send_keys(Keys.BACK_SPACE)

        element.send_keys("1")

        logger.info("foo")

    def play(self):
        ultimo_numero = ""
        contagem_sequencia = 0
        quantidade_numeros_iguais = 0
        maximo_quantidade_numeros_iguais = 500

        iteracoes = 0
        qtd_ganhos = 0

        while True:
            sleep(0.1)
            element = WebDriverWait(self.driver, 30 + 10).until(
                expected_conditions.presence_of_element_located(
                    (By.CLASS_NAME, "cq-animated-price")
                )
            )

            num_novo = element.text

            # Variável de controle para saber se houve compra durante o loop
            comprou = False

            if num_novo != ultimo_numero:
                logger.info(num_novo)
                ultimo_numero = num_novo
                iteracoes += 1

                # Var de controle para saber se a página travou e precisa ser reaberta
                quantidade_numeros_iguais = 0

                if num_novo[-1:] == str(parametro_ultimo_numero):
                    contagem_sequencia += 1

                    if contagem_sequencia >= int(qtd_ocorrencias_numero):
                        comprou = True

                    # logger.info("clica em difere")
                    WebDriverWait(self.driver, 30).until(
                        expected_conditions.presence_of_element_located(
                            (By.CLASS_NAME, "btn-purchase__info")
                        )
                    ).click()

                    sleep(10)  # Aguarda o texto Esse contrato ganhou aparecer

            #             contract_purchase_heading = driver.find_element_by_id(
            #                 "contract_purchase_heading"
            #             )
            #             result: str = contract_purchase_heading.text
            #             registrar(
            #                 iteracoes,
            #                 contagem_sequencia,
            #                 result,
            #                 parametro_ultimo_numero,
            #                 qtd_ocorrencias_numero,
            #             )

            #             if result == "Esse contrato ganhou":
            #                 qtd_ganhos += 1

            #             sleep(3)

            #             registrar(
            #                 iteracoes,
            #                 contagem_sequencia,
            #                 "clicar em fechar",
            #                 parametro_ultimo_numero,
            #                 qtd_ocorrencias_numero,
            #             )
            #             close_confirmation_container = driver.find_element_by_id(
            #                 "close_confirmation_container"
            #             )
            #             close_confirmation_container.click()

            #             registrar(
            #                 iteracoes,
            #                 contagem_sequencia,
            #                 f"Qtd ganhos: {qtd_ganhos}",
            #                 parametro_ultimo_numero,
            #                 qtd_ocorrencias_numero,
            #             )
            #     else:
            #         if contagem_sequencia > 0:
            #             contagem_sequencia = 0
            #             registrar(
            #                 iteracoes,
            #                 contagem_sequencia,
            #                 "Contagem zerada",
            #                 parametro_ultimo_numero,
            #                 qtd_ocorrencias_numero,
            #             )

            else:
                quantidade_numeros_iguais += 1
            #     if quantidade_numeros_iguais >= maximo_quantidade_numeros_iguais:
            #         registrar(
            #             iteracoes,
            #             contagem_sequencia,
            #             "A página está inativa, abortando robô",
            #             parametro_ultimo_numero,
            #             qtd_ocorrencias_numero,
            #         )
            #         continue

            if comprou:
                contagem_sequencia = 0

            sleep(0.1)


if __name__ == "__main__":
    parametro_ultimo_numero = settings.parametro_ultimo_numero
    qtd_ocorrencias_numero = settings.qtd_ocorrencias_numero

    r100 = DerivR100()
    r100.open_url()
    r100.do_login(settings.user, settings.password)
    r100.do_close_modal()
    r100.config_demo_account()
    r100.do_config_r100()
    r100.play()

    logger.info("finished")
