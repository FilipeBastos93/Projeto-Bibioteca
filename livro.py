class Livro:
    def __init__(self, nome, autor, local_origem=None, emprestado_para=None):
        self.nome = nome
        self.autor = autor
        self.local_origem = local_origem
        self.emprestado_para = emprestado_para
