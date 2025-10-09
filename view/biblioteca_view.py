import re
from controller.biblioteca import Biblioteca
from model.conexao import conn

def email_matches (email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.fullmatch(regex, email): 
        return True
    else:
        return False

opcao = 0
biblioteca1 = Biblioteca(conn=conn)

while opcao != 12:
    print("1 - Adicionar um usuário")
    print("2 - Adicionar um livro")
    print("3 - Listar os livros")
    print("4 - Listar os usuários")
    print("5 - Procurar livros por ano")
    print("6 - Procurar livros por título")
    print("7 - Registrar empréstimo")
    print("8 - Registrar devolução")
    print("9 - Listar empréstimos ativos")
    print("10 - Limpar tela do console")
    print("11 - Gerar relatórios de empréstimos")
    print("12 - Sair")
    opcao = int(input("Digite aqui sua opcao:"))

    biblioteca1.limparTela()

    # adicionar um usuário
    if opcao == 1:
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
        
    # adicionar um livro
    elif opcao == 2: 
        titulo = input("Digite o título do livro:")
        autor = input("Digite o autor do livro:")
        ano = input("Digite o ano de lançamento do livro:")
        isbn = input("Digite aqui o ISBN do livro:")
        status = 1

        biblioteca1._adicionarLivro(titulo, autor, ano, isbn, status)
        print(f"O livro {titulo} foi inserido com sucesso!\n")

    # listar os livros disponíveis
    elif opcao == 3:
        Biblioteca.limparTela()
        biblioteca1._listarLivros()
        input("Pressione Enter para continuar...")
        Biblioteca.limparTela()
        
    # listas os usuários do sistema
    elif opcao == 4:
        Biblioteca.limparTela()
        biblioteca1._listarUsuarios()
        input("Pressione Enter para continuar...")
        Biblioteca.limparTela()

    # procurar livros por ano    
    elif opcao == 5:
        ano = input("Digite aqui o ano para efetuar a busca:")
        biblioteca1._pesquisarLivroPorAno(ano)
        input("Pressione Enter para continuar...")
        Biblioteca.limparTela()

    # procurar livros por título
    elif opcao == 6:
        titulo = input("Digite aqui o título para efetuar a busca:")
        biblioteca1._pesquisarLivroPorTitulo(titulo)
        input("Pressione Enter para continuar...")
        Biblioteca.limparTela()

    # registrar empréstimos
    elif opcao == 7:
        livro = int(input("Digite o ID do livro a ser inserido no empréstimo:"))
        usuario = int(input("Digite o ID do usuário a ser inserido no empréstimo:"))

        biblioteca1._adicionarEmprestimo(livro, usuario)
        input("Pressione Enter para continuar...")
        Biblioteca.limparTela()

    # registrar devolução
    elif opcao == 8: 
        livro = int(input("Digite o ID do livro a ser devolvido:"))
        biblioteca1._registrarDevolucao(livro)
        input("Pressione Enter para continuar...")
        Biblioteca.limparTela()
    
    # listar os empréstimos que estão ativos no momento
    elif opcao == 9: 
        Biblioteca.limparTela()
        biblioteca1._listarEmprestimosAtivos()
        input("Pressione Enter para continuar...")
        Biblioteca.limparTela()

    # limpar tela do console
    elif opcao == 10: 
        Biblioteca.limparTela()

    # retornar relatório dos empréstimos realizados (histórico)
    elif opcao == 11:
        Biblioteca.limparTela()
        biblioteca1._relatorioDeEmprestimos()
        input("Pressione Enter para continuar...")
        Biblioteca.limparTela()

