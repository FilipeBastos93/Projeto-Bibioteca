import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class Livro:
    def __init__(self, nome, autor, local_origem=None, emprestado_para=None):
        self.nome = nome
        self.autor = autor
        self.local_origem = local_origem
        self.emprestado_para = emprestado_para

    def salvar_no_banco(self):
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO livros (nome, autor, local_origem, emprestado_para)
            VALUES (?, ?, ?, ?)
        ''', (self.nome, self.autor, self.local_origem, self.emprestado_para))
        conn.commit()
        conn.close()

    @staticmethod
    def listar_livros():
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("SELECT rowid, * FROM livros")
        livros = cursor.fetchall()
        conn.close()
        return livros

    @staticmethod
    def editar_livro(id_livro, nome, autor, local_origem, emprestado_para):
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE livros
            SET nome=?, autor=?, local_origem=?, emprestado_para=?
            WHERE rowid=?
        ''', (nome, autor, local_origem, emprestado_para, id_livro))
        conn.commit()
        conn.close()

    @staticmethod
    def excluir_livro(id_livro):
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM livros WHERE rowid=?", (id_livro,))
        conn.commit()
        conn.close()

class BibliotecaApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Biblioteca App")
        self.geometry("600x400")

        self.create_widgets()
        self.carregar_livros()

    def create_widgets(self):
        # Labels
        lbl_nome = tk.Label(self, text="Nome do livro:")
        lbl_nome.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        lbl_autor = tk.Label(self, text="Autor do livro:")
        lbl_autor.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        lbl_local = tk.Label(self, text="Local de origem:")
        lbl_local.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        lbl_emprestado_para = tk.Label(self, text="Emprestado para:")
        lbl_emprestado_para.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        # Entry fields
        self.entry_nome = tk.Entry(self)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=5)
        self.entry_autor = tk.Entry(self)
        self.entry_autor.grid(row=1, column=1, padx=10, pady=5)
        self.entry_local = tk.Entry(self)
        self.entry_local.grid(row=2, column=1, padx=10, pady=5)
        self.entry_emprestado_para = tk.Entry(self)
        self.entry_emprestado_para.grid(row=3, column=1, padx=10, pady=5)

        # Buttons
        btn_adicionar = tk.Button(self, text="Adicionar Livro", command=self.adicionar_livro)
        btn_adicionar.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        btn_listar = tk.Button(self, text="Listar Livros", command=self.carregar_livros)
        btn_listar.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        btn_excluir = tk.Button(self, text="Excluir Livro", command=self.excluir_livro)
        btn_excluir.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # Lista de livros
        self.lista_livros = ttk.Treeview(self, columns=('Nome', 'Autor', 'Local Origem', 'Emprestado para'))
        self.lista_livros.grid(row=7, column=0, columnspan=2, padx=10, pady=5)
        self.lista_livros.heading('#0', text='ID')
        self.lista_livros.heading('Nome', text='Nome')
        self.lista_livros.heading('Autor', text='Autor')
        self.lista_livros.heading('Local Origem', text='Local Origem')
        self.lista_livros.heading('Emprestado para', text='Emprestado para')
        self.lista_livros.column('#0', width=50)
        self.lista_livros.column('Nome', width=150)
        self.lista_livros.column('Autor', width=100)
        self.lista_livros.column('Local Origem', width=100)
        self.lista_livros.column('Emprestado para', width=150)
        self.lista_livros.bind('<ButtonRelease-1>', self.get_selected_item)

    def adicionar_livro(self):
        nome = self.entry_nome.get()
        autor = self.entry_autor.get()
        local_origem = self.entry_local.get()
        emprestado_para = self.entry_emprestado_para.get()

        livro = Livro(nome, autor, local_origem, emprestado_para)
        livro.salvar_no_banco()

        messagebox.showinfo("Sucesso", "Livro adicionado com sucesso!")
        self.carregar_livros()

    def carregar_livros(self):
        # Limpar lista de livros
        for item in self.lista_livros.get_children():
            self.lista_livros.delete(item)

        # Carregar livros do banco de dados
        livros = Livro.listar_livros()

        if not livros:
            messagebox.showinfo("Info", "Não há livros na biblioteca.")
        else:
            # Adicionar livros à lista
            for livro in livros:
                self.lista_livros.insert('', 'end', text=livro[0], values=(livro[1], livro[2], livro[3], livro[4]))

    def get_selected_item(self, event):
        item = self.lista_livros.selection()[0]
        self.selected_item = self.lista_livros.item(item, 'text')

    def excluir_livro(self):
        try:
            id_livro = self.selected_item
            nome_livro = self.lista_livros.item(id_livro, 'values')[0]

            if messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir o livro '{nome_livro}'?"):
                Livro.excluir_livro(id_livro)
                messagebox.showinfo("Sucesso", "Livro excluído com sucesso!")
                self.carregar_livros()  # Atualizar lista de livros
        except IndexError:
            messagebox.showinfo("Info", "Selecione um livro para excluir.")

if __name__ == "__main__":
    app = BibliotecaApp()
    app.mainloop()
