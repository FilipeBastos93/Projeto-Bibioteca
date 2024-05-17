import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class BancoDeDados:
    def __init__(self, nome_banco):
        self.conn = sqlite3.connect(nome_banco)
        self.c = self.conn.cursor()
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                autor TEXT NOT NULL,
                local_origem TEXT,
                turma_retirou TEXT
            )
        """)
        self.conn.commit()

    def adicionar_livro(self, nome, autor, local_origem="", turma_retirou=""):
        self.c.execute("""
            INSERT INTO livros (nome, autor, local_origem, turma_retirou)
            VALUES (?, ?, ?, ?)
        """, (nome, autor, local_origem, turma_retirou))
        self.conn.commit()

    def excluir_livro(self, id_livro):
        self.c.execute("DELETE FROM livros WHERE id = ?", (id_livro,))
        self.conn.commit()

    def obter_livros(self):
        self.c.execute("SELECT * FROM livros")
        return self.c.fetchall()

    def obter_livro_por_id(self, id_livro):
        self.c.execute("SELECT * FROM livros WHERE id = ?", (id_livro,))
        return self.c.fetchone()

    def editar_livro(self, id_livro, nome, autor, local_origem="", turma_retirou=""):
        self.c.execute("""
            UPDATE livros
            SET nome=?, autor=?, local_origem=?, turma_retirou=?
            WHERE id=?
        """, (nome, autor, local_origem, turma_retirou, id_livro))
        self.conn.commit()

class BibliotecaApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Biblioteca App")
        self.banco_de_dados = BancoDeDados("biblioteca.db")
        self.create_widgets()
        self.carregar_livros()
        self.root.mainloop()

    def create_widgets(self):
        self.frame_adicionar = ttk.Frame(self.root)
        self.frame_adicionar.pack(padx=10, pady=10)

        lbl_nome = ttk.Label(self.frame_adicionar, text="Nome:")
        lbl_nome.grid(row=0, column=0, padx=5, pady=5)
        self.entry_nome = ttk.Entry(self.frame_adicionar)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        lbl_autor = ttk.Label(self.frame_adicionar, text="Autor:")
        lbl_autor.grid(row=1, column=0, padx=5, pady=5)
        self.entry_autor = ttk.Entry(self.frame_adicionar)
        self.entry_autor.grid(row=1, column=1, padx=5, pady=5)

        lbl_local_origem = ttk.Label(self.frame_adicionar, text="Local de Origem:")
        lbl_local_origem.grid(row=2, column=0, padx=5, pady=5)
        self.entry_local_origem = ttk.Entry(self.frame_adicionar)
        self.entry_local_origem.grid(row=2, column=1, padx=5, pady=5)

        lbl_turma_retirou = ttk.Label(self.frame_adicionar, text="Turma Retirou:")
        lbl_turma_retirou.grid(row=3, column=0, padx=5, pady=5)
        self.entry_turma_retirou = ttk.Entry(self.frame_adicionar)
        self.entry_turma_retirou.grid(row=3, column=1, padx=5, pady=5)

        self.botao_adicionar = ttk.Button(self.root, text="Adicionar Livro", command=self.adicionar_livro)
        self.botao_adicionar.pack(padx=10, pady=5)

        self.lista_livros = ttk.Treeview(self.root)
        self.lista_livros["columns"] = ("ID", "Nome", "Autor", "Local de Origem", "Turma Retirou")
        self.lista_livros.heading("#0", text="", anchor=tk.W)
        self.lista_livros.heading("ID", text="ID", anchor=tk.W)
        self.lista_livros.heading("Nome", text="Nome", anchor=tk.W)
        self.lista_livros.heading("Autor", text="Autor", anchor=tk.W)
        self.lista_livros.heading("Local de Origem", text="Local de Origem", anchor=tk.W)
        self.lista_livros.heading("Turma Retirou", text="Turma Retirou", anchor=tk.W)
        self.lista_livros.pack(padx=10, pady=10)

        self.botao_excluir = ttk.Button(self.root, text="Excluir Livro", command=self.excluir_livro)
        self.botao_excluir.pack(side=tk.LEFT, padx=10, pady=5)

        self.botao_editar = ttk.Button(self.root, text="Editar Livro", command=self.editar_livro)
        self.botao_editar.pack(side=tk.LEFT, padx=10, pady=5)

    def adicionar_livro(self):
        nome = self.entry_nome.get()
        autor = self.entry_autor.get()
        local_origem = self.entry_local_origem.get()
        turma_retirou = self.entry_turma_retirou.get()
        if nome and autor:
            self.banco_de_dados.adicionar_livro(nome, autor, local_origem, turma_retirou)
            self.carregar_livros()
            messagebox.showinfo("Sucesso", "Livro adicionado com sucesso.")
        else:
            messagebox.showerror("Erro", "Preencha pelo menos Nome e Autor do livro.")

    def excluir_livro(self):
        try:
            selected_item = self.lista_livros.selection()[0]
            id_livro = self.lista_livros.item(selected_item)['values'][0]
            self.banco_de_dados.excluir_livro(id_livro)
            self.carregar_livros()
            messagebox.showinfo("Sucesso", "Livro excluído com sucesso.")
        except IndexError:
            messagebox.showerror("Erro", "Selecione um livro para excluir.")

    def editar_livro(self):
        try:
            selected_item = self.lista_livros.selection()[0]
            id_livro = self.lista_livros.item(selected_item)['values'][0]
            livro = self.banco_de_dados.obter_livro_por_id(id_livro)
            if livro:
                # Abrir janela de edição com os detalhes do livro
                self.abrir_janela_edicao(id_livro, livro)
            else:
                messagebox.showerror("Erro", "Livro não encontrado.")
        except IndexError:
            messagebox.showerror("Erro", "Selecione um livro para editar.")

    def abrir_janela_edicao(self, id_livro, livro):
        janela_edicao = tk.Toplevel()
        janela_edicao.title("Editar Livro")

        frame_edicao = ttk.Frame(janela_edicao)
        frame_edicao.pack(padx=10, pady=10)

        lbl_nome = ttk.Label(frame_edicao, text="Nome:")
        lbl_nome.grid(row=0, column=0, padx=5, pady=5)
        entry_nome = ttk.Entry(frame_edicao)
        entry_nome.grid(row=0, column=1, padx=5, pady=5)
        entry_nome.insert(0, livro[1])

        lbl_autor = ttk.Label(frame_edicao, text="Autor:")
        lbl_autor.grid(row=1, column=0, padx=5, pady=5)
        entry_autor = ttk.Entry(frame_edicao)
        entry_autor.grid(row=1, column=1, padx=5, pady=5)
        entry_autor.insert(0, livro[2])

        lbl_local_origem = ttk.Label(frame_edicao, text="Local de Origem:")
        lbl_local_origem.grid(row=2, column=0, padx=5, pady=5)
        entry_local_origem = ttk.Entry(frame_edicao)
        entry_local_origem.grid(row=2, column=1, padx=5, pady=5)
        entry_local_origem.insert(0, livro[3])

        lbl_turma_retirou = ttk.Label(frame_edicao, text="Turma Retirou:")
        lbl_turma_retirou.grid(row=3, column=0, padx=5, pady=5)
        entry_turma_retirou = ttk.Entry(frame_edicao)
        entry_turma_retirou.grid(row=3, column=1, padx=5, pady=5)
        entry_turma_retirou.insert(0, livro[4])

        btn_salvar = ttk.Button(frame_edicao, text="Salvar",
                                 command=lambda: self.salvar_edicao(id_livro, entry_nome.get(), entry_autor.get(),
                                                                   entry_local_origem.get(), entry_turma_retirou.get(),
                                                                   janela_edicao))
        btn_salvar.grid(row=4, column=0, columnspan=2, pady=10)

    def salvar_edicao(self, id_livro, nome, autor, local_origem, turma_retirou, janela_edicao):
        self.banco_de_dados.editar_livro(id_livro, nome, autor, local_origem, turma_retirou)
        self.carregar_livros()
        janela_edicao.destroy()

    def carregar_livros(self):
        self.lista_livros.delete(*self.lista_livros.get_children())
        for livro in self.banco_de_dados.obter_livros():
            self.lista_livros.insert("", "end", values=livro)

if __name__ == "__main__":
    app = BibliotecaApp()
