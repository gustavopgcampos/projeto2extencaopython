import mysql.connector
from datetime import date
import os

# falta colocar classe livro, usuario e empréstimo
# lembrar de retirar essas informações quando fizer push para o github


class Livro:
    def __init__(self, id, titulo, autor, ano, isbn, status):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.isbn = isbn
        self.status = status

class Biblioteca:
    # classe contrutora responsável pela conexão com o banco
    def __init__(self, conn=None):
        self.conn = conn

    # classe responsável por pesquisar o nome do usuário pelo email
    def _pesquisarUsuarioPeloNome(self, nome):
        cursor = self.conn.cursor()
        sql = "SELECT * FROM usuario WHERE nome = %s"
        cursor.execute(sql, (nome, ))
        resultadoPesquisa = cursor.fetchall()

        print(resultadoPesquisa)

        if not resultadoPesquisa:
            print("Nenhum usuário com esse nome foi encontrado!")
            return 
        
        print("O usuário foi encontrado, abaixo estão algumas informações dele!")
        print(f"Nome do usuario | Matrícula do usuário | E-mail do usuário")
        for linha in resultadoPesquisa:
            print(f"{linha[1]} | {linha[2]} | {linha[3]}")

    def _listarUsuarios(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM usuario;
        """)
        resultados = cursor.fetchall()

        print(f"Nome do usuario | Matrícula do usuário | E-mail do usuário")
        
        for linha in resultados:
            print(f"{linha[1]} | {linha[2]} | {linha[3]}")

    def _listarLivros(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM livro;
        """)
        resultados = cursor.fetchall()

        print(f"Título do livro | Autor do livro | Ano do livro | ISBN do livro | Status do livro")

        for linha in resultados: 
            print(f"{linha[1]} | {linha[2]} | {linha[3]} | {linha[4]} | {linha[5]}")

    def _listarEmprestimos(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM emprestimo;
        """)
        resultados = cursor.fetchall()
        for linha in resultados: 
            print(linha)

    def _adicionarLivro(self, titulo, autor, ano, isbn, stats):
        cursor = self.conn.cursor()
        sql = "INSERT INTO livro (titulo, autor, ano, isbn, stats) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (titulo, autor, ano, isbn, stats))
        self.conn.commit()

    def _adicionarUsuario(self, nome, matricula, email):
        cursor = self.conn.cursor()
        sql = "INSERT INTO usuario (nome, matricula, email) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nome, matricula, email))
        self.conn.commit()

    def _adicionarEmprestimo(self, data_retirada, data_devolucao_prevista, data_revolucao_real, stats, livro_id, usuario_id):
        cursor = self.conn.cursor()
        sql = "INSERT INTO emprestimo (data_retirada, data_devolucao_prevista, data_revolucao_real, stats, livro_id, usuario_id) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (data_retirada, data_devolucao_prevista, data_revolucao_real, stats, livro_id, usuario_id))
        self.conn.commit()

    @staticmethod
    def limparTela():
        if os.name == 'nt':
            os.system('cls')
        else: 
            os.system('clear')
    
    
opcao = 0

biblioteca1 = Biblioteca(conn=conn)

while opcao != 7:
    print("1 - Adicionar um usuário")
    print("2 - Listar os usuários")
    print("3 - Adicionar um livro")
    print("4 - Listar os livros")
    print("5 - Procurar usuário pelo nome")
    print("6 - Limpar tela do console")
    print("7 - Sair")
    opcao = int(input("digite aqui sua opcao:"))

    if opcao == 1:
        # pega os valores de nome, matricula e email digitados e insere para o usuário
        nome = input("Digite o nome do usuário:")
        matricula = input("Digite a matrícula:")
        email = input("Digite o e-mail:")

        biblioteca1._adicionarUsuario(nome, matricula, email)

        print(f"O usuário {nome} foi inserido com sucesso!\n")

    elif opcao == 2: 
        # lista todos os usuários que estiverem criados no banco
        biblioteca1._listarUsuarios()

    elif opcao == 3:
        # pega os valores de titulo, autor, ano, isbn, status e adiciona ao banco
        titulo = input("Digite o título do livro:")
        autor = input("Digite o autor do livro:")
        ano = input("Digite o ano de lançamento do livro:")
        isbn = input("Digite aqui o ISBN do livro:")
        status = 1

        biblioteca1._adicionarLivro(titulo, autor, ano, isbn, status)

        print(f"O livro {titulo} foi inserido com sucesso!\n")
    elif opcao == 4:
        # lista todos os livros que estiverem criados no banco
        biblioteca1._listarLivros()
    elif opcao == 5:
        nome_buscado = input("Digite aqui o nome do usuário para saber se ele existe:")
        biblioteca1._pesquisarUsuarioPeloNome(nome_buscado)
    elif opcao == 6:
        Biblioteca.limparTela()




# biblioteca1._adicionarLivro("Pequeno Principe", "Autor Desconhecido", 1975, "8522031452", True)
# biblioteca1._adicionarUsuario("usuario1", "a101", "usuario1@email.com")
# biblioteca1._adicionarEmprestimo("")
# biblioteca1._listarLivros()
# biblioteca1._listarUsuarios()
# biblioteca1._listarEmprestimos()