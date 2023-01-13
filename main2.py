from ctypes import alignment, sizeof
from os import system
from tkinter import font
import PySimpleGUI as sg 

ARQUIVO_FLORES = "flores.pkl" 

flores = {}
#============================== Persistência ======================================

def carrega_arquivo_com_pickle(): 
    import pickle
    import os
    global flores
    global notas_alunos
    if not os.path.exists(ARQUIVO_FLORES):
        grava_arquivo_com_pickle()
    arquivo_flores = open(ARQUIVO_FLORES, 'rb')
    flores = pickle.load(arquivo_flores)


def grava_arquivo_com_pickle(): 
    import pickle
    arquivo_flores = open(ARQUIVO_FLORES, 'wb')
    pickle.dump(flores, arquivo_flores)

# Menu Principal 

def menu_principal():
    layout = [[sg.Text("Opções", font=("Arial 14 bold"), pad=(0,10), expand_x= True)], 
              [sg.Button("Adicionar Produto", key="cadastrar", size=(40, 2))],
              [sg.Button("Listar", key="listar", size=(40, 2))],
              [sg.Button("Pesquisar", key="buscar", size=(40, 2))],
              [sg.Button("Limpar", key="limpar", size=(40, 2))]]

    janela = sg.Window("Sistema Floricultura Fina Flor", layout, text_justification="center") 
    botao, valores = janela.read() 
    janela.close() 

    return botao

# Cadastrar Produtos 

def cadastra(): 
    layout = [[sg.Text("Cadastrar", font=("Arial 14 bold"), pad=(0,10), expand_x= True, justification="center")],  
              [sg.Text("Código/SKU:", size= (18,1)), sg.Input(key="sku", size=(28,1))], # O SKU é formado por um código utilizado pelos varejistas para identificarem as mercadorias armazenadas de modo rápido e simplificado.
              [sg.Text("Título:", size= (18,1)), sg.Input(key="titulo", size=(28,1))],
              [sg.Text("Preço:", size= (18,1)), sg.Input(key="preco", size=(28,1))],
              [sg.Text("Categoria:", size= (18,1)),sg.Input(key="categoria", size=(28,1))],
              [sg.Button("Cadastrar", key="cadastra", size=(21,1)), sg.Button("Cancelar", key="cancela", size=(21,1))]]
    
    janela = sg.Window("Cadastrar Produto", layout) 
    botao, dados_floricultura = janela.read() 
    janela.close()

    if botao == "cadastra": 
        sku_floricultura = dados_floricultura.pop("sku") 
        try:
            sku_floricultura = int(sku_floricultura)         
            if sku_floricultura not in flores.keys():  
                flores[sku_floricultura] = dados_floricultura  
            else:
                sg.Popup("Já existe um aluno com esta matrícula") 
        except ValueError:
            sg.Popup("Valor invalido, digite um número") 
    elif botao != "cancela": 
        raise SystemExit 

# Mostrar produtos

def mostra_produto(sku):  
    while True:
        produtos = flores.get(sku)

        if produtos is None:
            layout = [[sg.Text("Produto não encontrado!")],
                      [sg.Button("OK", key="ok", size=(18, 1))]]
            janela = sg.Window("Alerta", layout)
            botao, valores = janela.read()
            janela.close()
            return False

        #Cria a tela e espera um botão ser apertado
        layout = [[sg.Text("Código/SKU: {}".format(sku), size=(40,1))],
                [sg.Text("Título: {}".format(flores["titulo"]), size=(40,1))],
                [sg.Text("Preço: {}".format(flores["preco"]), size=(40,1))],
                [sg.Text("Categoria {}".format(flores["categoria"]), size=(40,1))],
                [sg.Button("Alterar", key="altera", size=(12,1)), sg.Button("Excluir", key="exclui", size=(11,1)), sg.Button("Voltar", key="volta", size=(12,1))]
                ]
        janela = sg.Window("Produto:", layout)
        botao, valores = janela.read()
        janela.close()

        if botao =="altera":
            altera(sku)
        elif botao == "exclui":
            exclui_produto(sku)
            break 
        elif botao == "volta":
            break
        else: 
            raise SystemExit

# Alterar produto

def altera(sku):  
    layout = [[sg.Text("Alterar")],
              [sg.Button("Alterar Produto", key="altera_produto", size=(18,1)), ]]
    janela = sg.Window("Alterar", layout)
    botao, valores = janela.read()
    janela.close()

    if botao == "altera_produto":
        altera_produto(sku)


def altera_produto(sku): 
    produtos = flores[sku]
    layout = [[sg.Text("Alterar Produto", font=("Arial 14 bold"), pad=(0,10), expand_x= True, justification="center")],
              [sg.Text("Código/SKU:", size= (18,1)), sg.Text(sku, size=(28,1))], 
              [sg.Text("Título:", size= (18,1)), sg.Input(default_text = flores["titulo"], key="titulo", size=(28,1))],
              [sg.Text("Preço:", size= (18,1)), sg.Input(default_text = flores["preco"], key="preco", size=(28,1))],
              [sg.Text("Categoria", size= (18,1)),sg.Input(default_text = flores["categoria"], key="categoria", size=(28,1))],
              [sg.Button("Alterar", key="altera", size=(21,1)), sg.Button("Cancelar", key="cancela", size=(21,1))]]
    
    janela = sg.Window("Alterar", layout)
    botao, dados_floricultura = janela.read()
    janela.close()

    if botao == "altera": 
        flores["titulo"] = dados_floricultura["titulo"]
        flores["preco"] = dados_floricultura["preco"]
        flores["categoria"] = dados_floricultura["categoria"]
    elif botao != "cancela":
        raise SystemExit


# Excluir Produtos

def exclui_produto(sku): 
    layout = [[sg.Text("Confirmar exclusão?")],
            [sg.Button("Sim", key="s", size=(16,1)), sg.Button("Não", key="n", size=(16,1))]]
    janela = sg.Window("Pesquisar", layout)
    botao, valores = janela.read()
    janela.close()
    if botao == "s":
        flores.pop(sku)
        sg.Popup("Aluno removido com sucesso!")
    elif botao == "n":
        sg.Popup("Exclusão cancelada")

# Listagem dos produtos

def cria_tabela(sku): 
    matriz = [] 
    for codigo in sku:
        produtos = flores[codigo]
        linha = [codigo, produtos["titulo"], produtos["preco"], produtos["categoria"]]
        matriz.append(linha)
    if len(matriz) == 0: 
        tamanho_automatico = False
    else:
        tamanho_automatico = True
    return sg.Table(matriz, ["Código/SKU", "Título", "Preço", "Categoria"], auto_size_columns= tamanho_automatico, expand_x= True, justification="center")

def lista_produtos(): 
    tabela = cria_tabela(flores.keys()) 
    layout = [[sg.Text("Lista de Produtos", font=("Arial 14 bold"), pad=(0,10), expand_x= True)],
               [tabela],
               [sg.Button("Voltar", key="voltar", expand_x=True)]]

    janela = sg.Window("Lista de Produtos", layout, text_justification="center")
    opcao, valores = janela.read()
    janela.close()

    if opcao != "voltar": 
        raise SystemExit


def busca_na_lista():  
    layout = [[sg.Text("Pesquisar produtos por categoria")],
              [sg.Input(key="categoria", size=(40,1))],
              [sg.Button("Buscar", key="buscar", size=(16,1)), sg.Button("Voltar", key="voltar", size=(16,1))]]
    
    janela = sg.Window("Pesquisar", layout)
    botao, valores = janela.read()
    janela.close()

    if botao == "buscar":
        cat_procurada = valores["categoria"]
        produtos_encontrados = []
        for sku, produtos in flores.items():
            if cat_procurada.lower() in produtos["categoria"].lower():  
                produtos_encontrados.append(sku)
        if len(produtos_encontrados) == 0: 
            sg.Popup("Nenhum produto foi encontrado")
        else: 
            tabela = cria_tabela(produtos_encontrados)
            layout = [[sg.Text("Lista Ordenada", font=("Arial 14 bold"), pad=(0,10), expand_x= True)],
                      [tabela],
                      [sg.Button("Voltar", key="voltar", expand_x=True)]]
            janela = sg.Window("Lista Ordenada", layout, text_justification="center")
            opcao, valores = janela.read()
            janela.close()
            if opcao != "voltar":
                raise SystemExit

def limpa_lista():  
    layout = [[sg.Text("Deseja excluir todos os dados?", size=(40,1))],
              [sg.Button("Sim", key="sim", size=(18,1)), sg.Button("Não", key="não", size=(18,1))]]
    janela = sg.Window("Limpar dados", layout)
    opcao, valores = janela.read()
    janela.close()

    if opcao == 'sim':
        flores.clear()  
        sg.Popup("Todos os itens foram removidos")

# Inicialização do código 

def main():
    sg.theme("GreenMono") 
    carrega_arquivo_com_pickle()
    while True:
        opcao = menu_principal()
        try:
            match opcao:
                case 'cadastrar':  
                    cadastra()
                case 'listar':  
                    lista_produtos()
                case 'limpar':  
                    limpa_lista()
                case 'buscar':  
                    busca_na_lista()
                case _:
                    grava_arquivo_com_pickle()
                    break
        except SystemExit: 
            grava_arquivo_com_pickle()
            exit() 

if __name__ == '__main__':
    main()
