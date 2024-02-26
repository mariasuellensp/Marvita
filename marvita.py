import time
import tkinter

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import customtkinter

# -------INTERFACE--------#


# Seleciona a estilização da janela
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# Cria a janela e sua resolução

# ----------JANELA DE INTERFACE-----------#

window = customtkinter.CTk()
window.resizable(False, False)
window.geometry("300x300")
window.title("Marvita")


def enviar_usuario(usuario):
    with open("usuario.txt", "w") as arquivo:
        arquivo.write(f"{usuario}")
    print("Informações enviadas com sucesso!" + usuario)


def enviar_senha(senha):
    with open("senha.txt", "w") as arquivo:
        arquivo.write(f"{senha}")
    print("Informações enviadas com sucesso!" + senha)


def enviar_nometecnico(nometecnico):
    with open("nometecnico.txt", "w") as arquivo:
        arquivo.write(f"{nometecnico}")
    print("Informações enviadas com sucesso!" + nometecnico)


# Cria um função clique que esta estanciada como Login
def clique():
    user_1 = txt_user.get()
    password_1 = txt_password.get()
    nometecnico_1 = txt_nometecnico.get()
    enviar_usuario(user_1)
    enviar_senha(password_1)
    enviar_nometecnico(nometecnico_1)

    # Volta informação pro usuário que os dados foram coletados
    tkinter.messagebox.showinfo("Informação", "Os dados foram coletados com sucesso!")
    window.destroy()


# Define os atributos do campo de texto
text = customtkinter.CTkLabel(window, text="Robo Fecha Chamado")
text.pack(padx=10, pady=10)

# Define os atributos do campo Usuário
txt_user = customtkinter.CTkEntry(window, placeholder_text="Usuário Ocomon")
txt_user.pack(padx=10, pady=10)

# Define os atributos do campo Senha
txt_password = customtkinter.CTkEntry(window, placeholder_text="Senha", show="*")
txt_password.pack(padx=10, pady=10)

# Define os atributos do campo nome do tecnico
txt_nometecnico = customtkinter.CTkEntry(window, placeholder_text="Nome do técnico")
txt_nometecnico.pack(padx=10, pady=10)

# Define os atributos do botão logar
button = customtkinter.CTkButton(window, text="Iniciar Robô", command=clique)
button.pack(padx=10, pady=10)

window.mainloop()

with open("usuario.txt", "r") as arquivo_usuarios:
    usuario = arquivo_usuarios.readlines()

# Lê o conteúdo do arquivo de senhas
with open("senha.txt", "r") as arquivo_senhas:
    senha = arquivo_senhas.readlines()

with open("nometecnico.txt", "r") as arquivo_tecnico:
    tecnico = arquivo_tecnico.readlines()

# ----------ROBÔ-----------#


# Configurações do ChromeDriver
chrome_options = webdriver.ChromeOptions()

# Inicializa o driver do Chrome
driver = webdriver.Chrome(options=chrome_options)

# Maximiza a tela/pagina.
driver.maximize_window()

# URL do ocomon para iniciar o robô
driver.get("http://servicedesk.tmkt.servicos.mkt/ocomon/index.php")

# Aguarda o idLogin estar disponível para logar no ocomon, tempo máximo de resposta: 20 segundos
# Aumentado o tempo de espera para no máximo 20 segundos
wait = WebDriverWait(driver, 20)
username_field = wait.until(EC.element_to_be_clickable((By.ID, "idLogin")))

# Preenche o campo de usuário com o usuário Ocomon
username_field.send_keys(usuario)

# Localiza o campo de senha
password_field = driver.find_element(By.ID, "idSenha")

# Preenche o campo de senha
password_field.send_keys(senha)

# Localiza o botão de login pelo nome da classe
login_button = driver.find_element(
    By.CLASS_NAME, "blogin")

# Cliqua no botão de login
login_button.click()

# printa no console caso o login for bem sucedido.
print("Login bem-sucedido!")

# Redireciona para a pagina de fechar chamados
url_fechar_chamados = "http://servicedesk.tmkt.servicos.mkt/ocomon/ocomon/geral/abertura.php"
driver.get(url_fechar_chamados)
print("Foi acessado URL de fechar chamados")

# Identifica o body na pagina de fechar chamados
xpath_inicio_html_body = "/html/body/*"

# Esperar até que o elemento body seja visível, tempo máximo de resposta: 10 segundos
elemento = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, xpath_inicio_html_body))
)

print("Foi identificado o body")

# desce o scrow até o fim
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
print("Rolagem até o final da página de fechamento de chamado concluída!")

# após descer o scrow, aguarda ate 10 segundos.
elemento = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, xpath_inicio_html_body))
)

# identifica e clica no botão (<a>) ALL para que todos os chamados da chave sejam visíveis. Caso ALL não esteja na página, ele segue o código.
try:
    botao_all = driver.find_element(By.XPATH, '//a[contains(@href, "FULL=1")]')
    botao_all.click()
    print("Foi clicado em ALL")
except:
    print("Elemento ALL não identificado, código rodando normalmente.")
    # time.sleep(3)

# Váriável que guarda a posição da linha inicial (por default, na chave geral o primeiro chamado sempre iniciará pela linha 2 [tr2])
linha_das_tabelas = 2

# Variável que representa a quantidade de linhas que aparecem no chamado
quantidade_de_linhas = 500
# time.sleep(5)
while linha_das_tabelas <= quantidade_de_linhas:

    # time.sleep(3)

    try:
        try:
            # Tenta encontrar o elemento na tabela 4
            contato_tecnico = driver.find_element(
                By.XPATH, "/html/body/table[4]/tbody/tr[4]/td/table/tbody/tr[%d]/td[3]/b" % linha_das_tabelas)
        except NoSuchElementException:
            # Se não encontrar, tenta na tabela 5
            contato_tecnico = driver.find_element(
                By.XPATH, "/html/body/table[5]/tbody/tr[4]/td/table/tbody/tr[%d]/td[3]/b" % linha_das_tabelas)

        print("O nome do técnico verificado foi: ", contato_tecnico.text)

        # aguarda 5 segundos antes de validar as linhas
        time.sleep(3)

        # estrutura de verificação
        if contato_tecnico.text == tecnico[0]:
            try:
                # Tenta encontrar o elemento na tabela 5
                # acessa dentro do chamado.
                acessar_chamado_a = driver.find_element(
                    By.XPATH, "/html/body/table[5]/tbody/tr[4]/td/table/tbody/tr[%d]/td[4]/a" % linha_das_tabelas)
                acessar_chamado_a.click()

                encerrar_ocorrencia_a = driver.find_element(
                    By.XPATH, "/html/body/a[1]")
                encerrar_ocorrencia_a.click()
                finalizar_chamado_button = driver.find_element(
                    By.CLASS_NAME, "button")
                finalizar_chamado_button.click()

                # Aguarda o alert de chamado fechado aparecer
                WebDriverWait(driver, 60).until(EC.alert_is_present())

                # Mude para o alerta e pressione 'ok'
                driver.switch_to.alert.accept()

            except NoSuchElementException:
                # Tenta encontrar o elemento na tabela 4
                # acessa dentro do chamado.
                acessar_chamado_a = driver.find_element(
                    By.XPATH, "/html/body/table[4]/tbody/tr[4]/td/table/tbody/tr[%d]/td[4]/a" % linha_das_tabelas)
                acessar_chamado_a.click()

                encerrar_ocorrencia_a = driver.find_element(
                    By.XPATH, "/html/body/a[1]")
                encerrar_ocorrencia_a.click()
                finalizar_chamado_button = driver.find_element(
                    By.CLASS_NAME, "button")
                finalizar_chamado_button.click()

                # Aguarda o alert de chamado fechado aparecer
                WebDriverWait(driver, 60).until(EC.alert_is_present())

                # Mude para o alerta e pressione 'ok'
                driver.switch_to.alert.accept()

                # time.sleep()
                print("Foi encontrado o chamado referente ao técnico e clicado dentro do chamado.")

                # decrementa o contator de linha para que seja verificado novamente a linha de chamado que foi fechada. 
                # linha_das_tabelas -= 1

                # Caso o nome do técnico buscado não for encontrado na linha de verificação, ele retornará para o início do looping e validará a linha de baixo.
        else:
            print("Percorrido a linha ", linha_das_tabelas,
                  " e não foi identificado o técnico informado.")
            # time.sleep()

            # incrementa a variável da linha
            linha_das_tabelas += 1

    except NoSuchElementException:
        print("Todos os chamados foram analisados")
        tkinter.messagebox.showinfo("Informação", "Todos os chamados foram analisados!")
        break

    # print("Marvita Finalizada.")
