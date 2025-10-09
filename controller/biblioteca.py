from datetime import date, timedelta
import os
import re

class Biblioteca:
    def __init__(self, conn=None):
        self.conn = conn

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

    def _listarUsuarios(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM usuario;
        """)
        resultados = cursor.fetchall()

        print(f"ID | Nome | Matrícula | E-mail")

        for linha in resultados: 
            print(f" {linha[0]} | {linha[1]} | {linha[2]} | {linha[3]}")

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

        print("ID | Retirada | Devolução Prevista | Devolução Real | Status | Livro | Usuário")
        for linha in emprestimos:
            print(f"{linha[0]} | {linha[1]} | {linha[2]} | {linha[3]} | {linha[4]} | {linha[5]} | {linha[6]}")

    def _relatorioDeEmprestimos (self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM emprestimo;
        """)
        resultados = cursor.fetchall()

        print(f"ID | Retirada | Devolução Prevista | Devolução Real | Status | Livro | Usuário")

        for linha in resultados: 
            print(f"{linha[0]} | {linha[1]} | {linha[2]} | {linha[3]} | {linha[4]} | {linha[5]} | {linha[6]}")

    @staticmethod
    def limparTela():
        if os.name == 'nt':
            os.system('cls')
        else: 
            os.system('clear')
