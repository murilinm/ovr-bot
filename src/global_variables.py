"""


"""

global_vars = {}

# Função para criar uma nova pasta
def create_folder(folder_name):
    if folder_name not in global_vars:
        global_vars[folder_name] = {}
        print(f"Pasta '{folder_name}' criada.")
    else:
        print(f"Pasta '{folder_name}' já existe.")

# Função para adicionar ou atualizar uma variável dentro de uma pasta
def set_variable(folder_name, var_name, value):
    if folder_name in global_vars:
        global_vars[folder_name][var_name] = value
        print(f"Variável '{var_name}' definida na pasta '{folder_name}' com valor: {value}")
    else:
        print(f"Pasta '{folder_name}' não existe. Crie a pasta antes de definir uma variável.")

# Função para remover uma variável de uma pasta
def remove_variable(folder_name, var_name):
    if folder_name in global_vars and var_name in global_vars[folder_name]:
        del global_vars[folder_name][var_name]
        print(f"Variável '{var_name}' removida da pasta '{folder_name}'.")
    else:
        print(f"Variável '{var_name}' ou pasta '{folder_name}' não encontrada.")

# Função para obter o valor de uma variável em uma pasta
def get_variable(folder_name, var_name):
    if folder_name in global_vars and var_name in global_vars[folder_name]:
        return global_vars[folder_name][var_name]
    else:
        return f"Variável '{var_name}' ou pasta '{folder_name}' não existe."

# Função para listar todas as variáveis em uma pasta ou todas as pastas
def list_variables(folder_name=None):
    if folder_name:
        if folder_name in global_vars:
            print(f"Variáveis na pasta '{folder_name}':")
            for var_name, value in global_vars[folder_name].items():
                print(f"{var_name}: {value}")
        else:
            print(f"Pasta '{folder_name}' não existe.")
    else:
        if global_vars:
            print("Pastas e variáveis armazenadas:")
            for folder, vars in global_vars.items():
                print(f"Pasta: {folder}")
                for var_name, value in vars.items():
                    print(f"  {var_name}: {value}")
        else:
            print("Nenhuma pasta ou variável armazenada.")

"""
# Exemplo de uso

# Criando pastas
create_folder('config')
create_folder('dados')

# Adicionando variáveis em pastas
set_variable('config', 'versao', '1.0')
set_variable('dados', 'usuario', 'admin')

# Listando variáveis em uma pasta
list_variables('config')

# Acessando uma variável específica
print(f"Versão do sistema: {get_variable('config', 'versao')}")

# Removendo uma variável
remove_variable('dados', 'usuario')

# Listando todas as pastas e variáveis
list_variables()

"""