import csv
from database import criar_conexao
from file_operations import fazer_backup, EXPORT_DIR

def adicionar_livro(titulo, autor, ano_publicacao, preco):
    fazer_backup()
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO livros (titulo, autor, ano_publicacao, preco)
        VALUES (?, ?, ?, ?)
    ''', (titulo, autor, ano_publicacao, preco))
    conn.commit()
    conn.close()
    print("Livro adicionado com sucesso!")

def exibir_livros():
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livros')
    livros = cursor.fetchall()
    conn.close()
    
    if not livros:
        print("Nenhum livro cadastrado.")
    else:
        for livro in livros:
            print(f"ID: {livro[0]}, Título: {livro[1]}, Autor: {livro[2]}, Ano: {livro[3]}, Preço: R${livro[4]:.2f}")

def atualizar_preco(id, novo_preco):
    fazer_backup()
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('UPDATE livros SET preco = ? WHERE id = ?', (novo_preco, id))
    if cursor.rowcount == 0:
        print("Livro não encontrado.")
    else:
        print("Preço atualizado com sucesso!")
    conn.commit()
    conn.close()

def remover_livro(id):
    fazer_backup()
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM livros WHERE id = ?', (id,))
    if cursor.rowcount == 0:
        print("Livro não encontrado.")
    else:
        print("Livro removido com sucesso!")
    conn.commit()
    conn.close()

def buscar_por_autor(autor):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livros WHERE autor LIKE ?', (f'%{autor}%',))
    livros = cursor.fetchall()
    conn.close()
    
    if not livros:
        print("Nenhum livro encontrado para este autor.")
    else:
        for livro in livros:
            print(f"ID: {livro[0]}, Título: {livro[1]}, Autor: {livro[2]}, Ano: {livro[3]}, Preço: R${livro[4]:.2f}")

def exportar_para_csv():
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livros')
    livros = cursor.fetchall()
    conn.close()

    csv_path = EXPORT_DIR / 'livros_exportados.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['ID', 'Título', 'Autor', 'Ano de Publicação', 'Preço'])
        csv_writer.writerows(livros)
    
    print(f"Dados exportados para {csv_path}")

def importar_de_csv():
    csv_path = EXPORT_DIR / 'livros_exportados.csv'
    if not csv_path.exists():
        print("Arquivo CSV não encontrado.")
        return

    fazer_backup()
    conn = criar_conexao()
    cursor = conn.cursor()

    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Pular o cabeçalho
        for row in csv_reader:
            cursor.execute('''
                INSERT INTO livros (titulo, autor, ano_publicacao, preco)
                VALUES (?, ?, ?, ?)
            ''', (row[1], row[2], int(row[3]), float(row[4])))

    conn.commit()
    conn.close()
    print("Dados importados com sucesso!")

def menu():
    while True:
        print("\n=== Sistema de Gerenciamento de Livraria ===")
        print("1. Adicionar novo livro")
        print("2. Exibir todos os livros")
        print("3. Atualizar preço de um livro")
        print("4. Remover um livro")
        print("5. Buscar livros por autor")
        print("6. Exportar dados para CSV")
        print("7. Importar dados de CSV")
        print("8. Fazer backup do banco de dados")
        print("9. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            titulo = input("Título do livro: ")
            autor = input("Autor do livro: ")
            ano = int(input("Ano de publicação: "))
            preco = float(input("Preço do livro: "))
            adicionar_livro(titulo, autor, ano, preco)
        elif opcao == '2':
            exibir_livros()
        elif opcao == '3':
            id = int(input("ID do livro: "))
            novo_preco = float(input("Novo preço: "))
            atualizar_preco(id, novo_preco)
        elif opcao == '4':
            id = int(input("ID do livro a ser removido: "))
            remover_livro(id)
        elif opcao == '5':
            autor = input("Nome do autor: ")
            buscar_por_autor(autor)
        elif opcao == '6':
            exportar_para_csv()
        elif opcao == '7':
            importar_de_csv()
        elif opcao == '8':
            fazer_backup()
        elif opcao == '9':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")