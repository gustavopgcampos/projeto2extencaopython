import mysql.connector
import os
import re
from datetime import date, timedelta
from dotenv import load_dotenv


load_dotenv()

conn = mysql.connector.connect (
    host=os.getenv("DB_HOST"), 
    user=os.getenv("DB_USER"), 
    password=os.getenv("DB_PASSWORD"), 
    database=os.getenv("DB_DATABASE")
)

class Livro:
    def __init__(self, id, titulo, autor, ano, isbn, status):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.isbn = isbn
        self.status = status

class Usuario: 
    def __init__(self, id, nome, matricula, email):
        self.id = id
        self.nome = nome
        self.matricula = matricula
        self.email = email
        

class Biblioteca:
    # classe contrutora responsável pela conexão com o banco
    def __init__(self, conn=None):
        self.conn = conn

    # método responsável por pesquisar livro por titulo || ano
    def _pesquisarLivroPorAno(self, ano):
        try:
            cursor = self.conn.cursor()
            sql = "SELECT * FROM livro WHERE ano = %s"
            cursor.execute(sql, (ano, ))
            resultadoPesquisa = cursor.fetchall()
        
            if not resultadoPesquisa:
                print("Não foi encontrado nenhum livro referente ao ano.")
            else: 
                print(str(resultadoPesquisa))

        except Exception as error:
            print("Error", error)

    def _pesquisarLivroPorTitulo(self, titulo):
        cursor = self.conn.cursor()
        sql = "SELECT * FROM livro WHERE titulo = %s"
        cursor.execute(sql, (titulo, ))
        resultadoPesquisa = cursor.fetchall()

        if not resultadoPesquisa:
            print("Não foi encontrado nenhum livro referente ao título.")
        else: 
            print(resultadoPesquisa)

    def _listarLivros(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM livro;
        """)
        resultados = cursor.fetchall()

        print(f" ID | Título do livro | Autor do livro | Ano do livro | ISBN do livro | Status do livro")

        for linha in resultados: 
            print(f" {linha[0]} | {linha[1]} | {linha[2]} | {linha[3]} | {linha[4]} | {linha[5]}")

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

    def _adicionarEmprestimo(self, livro_id, usuario_id):

        data = date.today()
        dataPrevista = data + timedelta(days=7)
        status = "N"
        status_yes = "Y"

        cursor = self.conn.cursor()
        sqla = "SELECT * FROM emprestimo WHERE usuario_id = %s AND stats = %s"
        cursor.execute(sqla, (usuario_id, status_yes, ))
        res = cursor.fetchone()

        if res is None:
            cursor = self.conn.cursor()
            sql3 = "SELECT stats FROM livro WHERE id = %s"
            cursor.execute(sql3, (livro_id, ))
            resultado = cursor.fetchone()

            resultado_string = ''.join(resultado)

            # quando adiciona um empréstimo coloca o status do empréstimo para Y e do livro para N
            if resultado_string == "Y": 
                cursor = self.conn.cursor()
                sql = "INSERT INTO emprestimo (data_retirada, data_devolucao_prevista, stats, livro_id, usuario_id) VALUES (%s, %s, %s, %s, %s)"
                sql2 = "UPDATE livro SET stats = %s WHERE id = %s"
                cursor.execute(sql, (data, dataPrevista, status_yes, livro_id, usuario_id, ))
                cursor.execute(sql2, (status, livro_id, ))
                self.conn.commit()
            elif resultado_string == "N": 
                print("O livro já está em outro empréstimo")
        else: 
            print("O usuário já possui um empréstimo ativo!") 
            

    def _registrarDevolucao(self, livro):
        data = date.today()
        status = "Y"
        status_no = "N"

        cursor = self.conn.cursor()
        sql = "SELECT stats FROM livro WHERE id = %s"
        cursor.execute(sql, (livro, ))
        resultados = cursor.fetchone()
        resultado_string = ''.join(resultados)
 
        if resultado_string == "N":
            # ao registrar uma devolucao preciso voltar o status do livro para Y e registrar a data de devolução do empréstimo
            cursor = self.conn.cursor()
            sql = "UPDATE livro SET stats = %s WHERE id = %s"
            sql2 = "UPDATE emprestimo SET stats = %s WHERE livro_id = %s"
            sql3 = "UPDATE emprestimo SET data_devolucao_real = %s WHERE livro_id = %s AND stats = %s"
            cursor.execute(sql, (status, livro))
            cursor.execute(sql3, (data, livro, status, ))
            cursor.execute(sql2, (status_no, livro, ))
            self.conn.commit()

            print("livro devolvido com sucesso!")
        else: 
            print("O livro citado não se encontra em um empréstimo!")

    # arrumar para listar apenas os emprestimos que estão com Y (ativos)
    def _listarEmprestimosAtivos(self): 
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT e.id, e.data_retirada, e.data_devolucao_prevista, e.data_devolucao_real, 
                e.stats, l.titulo, u.nome
            FROM emprestimo e
            INNER JOIN livro l ON e.livro_id = l.id
            INNER JOIN usuario u ON e.usuario_id = u.id
            WHERE e.stats = 'Y'
        """)
        emprestimos = cursor.fetchall()

        print("ID | Retirada | Prevista | Devolução Real | Status | Livro | Usuário")
        for linha in emprestimos:
            print(f"{linha[0]} | {linha[1]} | {linha[2]} | {linha[3]} | {linha[4]} | {linha[5]} | {linha[6]}")

    @staticmethod
    def limparTela():
        if os.name == 'nt':
            os.system('cls')
        else: 
            os.system('clear')
    
def email_matches (email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if re.fullmatch(regex, email): 
        return True
    else:
        return False

opcao = 0

biblioteca1 = Biblioteca(conn=conn)

while opcao != 10:
    print("1 - Adicionar um usuário")
    print("2 - Adicionar um livro")
    print("3 - Listar os livros")
    print("3 - Listar os usuários") #
    print("4 - Procurar livros por ano")
    print("5 - Procurar livros por título")
    print("6 - Registrar empréstimo")
    print("7 - Registrar devolução")
    print("8 - Listar empréstimos ativos")
    print("9 - Limpar tela do console")
    print("10 - Gerar relatórios de empréstimos") #
    print("10 - Sair")
    opcao = int(input("Digite aqui sua opcao:"))

    biblioteca1.limparTela()

    if opcao == 1:

        # pega os valores de nome, matricula e email digitados e insere para o usuário
        nome = input("Digite o nome do usuário:")
        matricula = input("Digite a matrícula:")
        email = input("Digite o e-mail:")

        result = email_matches(email)

        if result == False:
            
            print("Ocorreu um erro ao validar o E-mail fornecido, tenha certeza que ele segue esse padrão (email@email.com)")
            input("Pressione Enter para continuar...")
            biblioteca1.limparTela()
        elif result == True:
            biblioteca1._adicionarUsuario(nome, matricula, email)

            print(f"O usuário {nome} foi criado com sucesso!")
            input("Pressione Enter para continuar...")
            biblioteca1.limparTela()
        
    elif opcao == 2: 
        # pega os valores de titulo, autor, ano, isbn, status e adiciona ao banco
        titulo = input("Digite o título do livro:")
        autor = input("Digite o autor do livro:")
        ano = input("Digite o ano de lançamento do livro:")
        isbn = input("Digite aqui o ISBN do livro:")
        status = 1

        biblioteca1._adicionarLivro(titulo, autor, ano, isbn, status)

        print(f"O livro {titulo} foi inserido com sucesso!\n")
        

    elif opcao == 3:
        # lista todos os livros que estiverem criados no banco
        Biblioteca.limparTela()
        biblioteca1._listarLivros()
        input("Pressione Enter para continuar...")
        Biblioteca.limparTela()
        
    elif opcao == 4:
        ano = input("Digite aqui o ano para efetuar a busca:")
        biblioteca1._pesquisarLivroPorAno(ano)
        input("Pressione Enter para continuar...")
        Biblioteca.limparTela()
    elif opcao == 5:
        titulo = input("Digite aqui o título para efetuar a busca:")
        biblioteca1._pesquisarLivroPorTitulo(titulo)
        input("Pressione Enter para continuar...")
        Biblioteca.limparTela()
    elif opcao == 6:
        livro = int(input("Digite o ID do livro a ser inserido no empréstimo:"))
        usuario = int(input("Digite o ID do usuário a ser inserido no empréstimo:"))

        biblioteca1._adicionarEmprestimo(livro, usuario)
        input("Pressione Enter para continuar...")
        Biblioteca.limparTela()
    elif opcao == 7:
        livro = int(input("Digite o ID do livro a ser devolvido:"))
        biblioteca1._registrarDevolucao(livro)
        input("Pressione Enter para continuar...")
        Biblioteca.limparTela()
    elif opcao == 8: 
        Biblioteca.limparTela()
        biblioteca1._listarEmprestimosAtivos()
        input("Pressione Enter para continuar...")
        Biblioteca.limparTela()
    elif opcao == 9: 
        Biblioteca.limparTela()

# biblioteca1._adicionarLivro("Pequeno Principe", "Autor Desconhecido", 1975, "8522031452", True)
# biblioteca1._adicionarUsuario("usuario1", "a101", "usuario1@email.com")
# biblioteca1._adicionarEmprestimo("")
# biblioteca1._listarLivros()
# biblioteca1._listarUsuarios()
# biblioteca1._listarEmprestimos()