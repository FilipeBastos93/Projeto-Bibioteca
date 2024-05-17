import sqlite3

class BancoDeDados:
    def __init__(self, nome_banco='biblioteca.db'):
        self.nome_banco = nome_banco

    def criar_tabela(self):
        conn = sqlite3.connect(self.nome_banco)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                autor TEXT,
                local_origem TEXT,
                emprestado_para TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def adicionar_livro(self, livro):
        conn = sqlite3.connect(self.nome_banco)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO livros (nome, autor, local_origem, emprestado_para)
            VALUES (?, ?, ?, ?)
        ''', (livro.nome, livro.autor, livro.local_origem, livro.emprestado_para))
        conn.commit()
        conn.close()

    # Métodos para listar, editar e excluir livros aqui...

# Exemplo de uso:
if __name__ == "__main__":
    db = BancoDeDados()
    db.criar_tabela()
