import os
import re
import sys
from datetime import datetime
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox import firefox_binary
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.safari.webdriver import WebDriver as SafariDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


def registrar(
    iteracao: int,
    contagem_sequencia: int,
    mensagem: str,
    parametro_ultimo_numero: str = "0",
    qtd_ocorrencias_numero: int = 0,
):
    print(
        f"i={iteracao}|d={datetime.now()}|n={parametro_ultimo_numero}|q={qtd_ocorrencias_numero}|c={contagem_sequencia}|m={mensagem}"
    )


def run(parametro_ultimo_numero: str, qtd_ocorrencias_numero: int):

    print("Iniciando...")
    print(f"parametro_ultimo_numero: {parametro_ultimo_numero}")
    print(f"qtd_ocorrencias_numero: {qtd_ocorrencias_numero}")

    # sleep(1)

    # with open("src/config.txt", "r") as f:
    #     x = f.readlines()

    # user = x[0]
    # password = x[1]

    while True:
        """
        Esse loop terá uma segunda iteração somente se a página ficar offline
        Abaixo há outro loop para cada alteração do número na tela
        """

        print("Carregando navegador embarcado")

        # browser = FirefoxBinary("geckodriver")
        # browser = webdriver.Firefox()
        # browser = webdriver.Safari()
        driver = webdriver.Chrome()
        driver.get("https://app.deriv.com")

        print("Pegando o botão de login")
        btn_login = WebDriverWait(driver, 30).until(
            expected_conditions.presence_of_element_located(
                (By.ID, "dt_login_button")
            )
        )
        btn_login.click()

        # sleep(4)

        # print("Pegando o campo de usuário")
        # txtEmail = driver.find_element_by_id("txtEmail")
        # txtEmail.send_keys(user)

        # print("Pegando o campo de senha")
        # txtPass = driver.find_element_by_id("txtPass")
        # txtPass.send_keys(password)

        # sleep(10)

        # try:
        #     print("Pegando o botão de login")
        #     driver.find_element_by_name("login").click()
        # except:
        #     pass

        # sleep(10)

        # print("Pegando o botão do menu principal")
        # driver.find_element_by_id("underlying_component").click()

        # sleep(10)

        # print("Pegando o botão de apostas")
        # driver.find_element_by_class_name("synthetic_index").click()

        # sleep(3)

        # print("Pegando o elemento 100 index")
        # driver.find_element_by_id("R_100").click()

        # sleep(3)

        # print("Pegando tipo de aposta")
        # driver.find_element_by_class_name("contract_current").click()

        # sleep(2)

        # print("Pegando o elemnto combina/difere")
        # contract_subtypes = driver.find_elements_by_class_name("sub ")

        # for contract in contract_subtypes:
        #     if contract.text == "Combina/Difere":
        #         contract.click()
        #         break

        # print("Configurando o tick")
        # duration_amount = driver.find_element_by_id("duration_amount")
        # duration_amount.send_keys(Keys.CONTROL + "a")
        # duration_amount.send_keys(Keys.DELETE)
        # duration_amount.send_keys("1")

        # print("Altere a conta se necessário, aguardando 30 segundos")
        # sleep(30)

        # # INICIO DA LOGICA DE JOGADAS

        # ultimo_numero = ""
        # contagem_sequencia = 0
        # quantidade_numeros_iguais = 0
        # maximo_quantidade_numeros_iguais = 500

        # iteracoes = 0
        # qtd_ganhos = 0

        # while True:
        #     num_novo = "".join(
        #         re.findall(r"[0-9]+", driver.find_element_by_id("spot").text)
        #     )

        #     # Variável de controle para saber se houve compra durante o loop
        #     comprou = False

        #     if num_novo != ultimo_numero:
        #         ultimo_numero = num_novo
        #         iteracoes += 1

        #         # Var de controle para saber se a página travou e precisa ser reaberta
        #         quantidade_numeros_iguais = 0

        #         if num_novo[6:] == parametro_ultimo_numero:

        #             contagem_sequencia += 1

        #             registrar(
        #                 iteracoes,
        #                 contagem_sequencia,
        #                 num_novo,
        #                 parametro_ultimo_numero,
        #                 qtd_ocorrencias_numero,
        #             )

        #             if contagem_sequencia >= int(qtd_ocorrencias_numero):
        #                 registrar(
        #                     iteracoes,
        #                     contagem_sequencia,
        #                     "clicar em comprar",
        #                     parametro_ultimo_numero,
        #                     qtd_ocorrencias_numero,
        #                 )
        #                 comprou = True

        #                 purchase_button_bottom = driver.find_element_by_id(
        #                     "purchase_button_bottom"
        #                 )
        #                 purchase_button_bottom.click()

        #                 sleep(10)  # Aguarda o texto Esse contrato ganhou aparecer

        #                 contract_purchase_heading = driver.find_element_by_id(
        #                     "contract_purchase_heading"
        #                 )
        #                 result: str = contract_purchase_heading.text
        #                 registrar(
        #                     iteracoes,
        #                     contagem_sequencia,
        #                     result,
        #                     parametro_ultimo_numero,
        #                     qtd_ocorrencias_numero,
        #                 )

        #                 if result == "Esse contrato ganhou":
        #                     qtd_ganhos += 1

        #                 sleep(3)

        #                 registrar(
        #                     iteracoes,
        #                     contagem_sequencia,
        #                     "clicar em fechar",
        #                     parametro_ultimo_numero,
        #                     qtd_ocorrencias_numero,
        #                 )
        #                 close_confirmation_container = driver.find_element_by_id(
        #                     "close_confirmation_container"
        #                 )
        #                 close_confirmation_container.click()

        #                 registrar(
        #                     iteracoes,
        #                     contagem_sequencia,
        #                     f"Qtd ganhos: {qtd_ganhos}",
        #                     parametro_ultimo_numero,
        #                     qtd_ocorrencias_numero,
        #                 )
        #         else:
        #             if contagem_sequencia > 0:
        #                 contagem_sequencia = 0
        #                 registrar(
        #                     iteracoes,
        #                     contagem_sequencia,
        #                     "Contagem zerada",
        #                     parametro_ultimo_numero,
        #                     qtd_ocorrencias_numero,
        #                 )

        #     else:
        #         quantidade_numeros_iguais += 1

        #         if quantidade_numeros_iguais >= maximo_quantidade_numeros_iguais:
        #             registrar(
        #                 iteracoes,
        #                 contagem_sequencia,
        #                 "A página está inativa, abortando robô",
        #                 parametro_ultimo_numero,
        #                 qtd_ocorrencias_numero,
        #             )
        #             continue

        #     if comprou:
        #         contagem_sequencia = 0

        #     sleep(0.1)


if __name__ == "__main__":
    # Recebe o ultimo numero do parametro
    try:
        parametro_ultimo_numero = sys.argv[1]
    except:
        parametro_ultimo_numero = input("Digite o ultimo numero: ")

    try:
        qtd_ocorrencias_numero = int(sys.argv[2])
    except:
        qtd_ocorrencias_numero = int(input("Digite a quantidade de ocorrencias: "))

    # Executa a função configurando o bot
    run(parametro_ultimo_numero, qtd_ocorrencias_numero)
