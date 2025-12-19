import uuid 
from datetime import date, timedelta, datetime
from collections import deque
import heapq

class Biblioteca:
    
    def __init__(self, nome: str):
        self.library_name = nome
        self.livros_biblioteca = []
        self.usuarios_biblioteca = []
        self.livros_emprestados = deque()
        
    def cadastrar_livro(self, livro):
        if livro in self.livros_biblioteca:
            print("Este livro já esta presente em nossa biblioteca, tente outro livro.")
            return

        self.livros_biblioteca.append(livro)
        print(f"Livro {livro.book_title} adicionado com sucesso na biblioteca: {self.library_name}")

        
    def cadastrar_usuarios(self, usuario):
        if usuario.user_id in self.usuarios_biblioteca:
            print("Este usuário já esta cadastrado em nossa biblioteca.")
            return

        self.usuarios_biblioteca.append(usuario)
        print(f"Usuário {usuario.user_name} adicionado com sucesso na biblioteca: {self.library_name}")
        
    def emprestar_livro(self, usuario, livro):
        if usuario not in self.usuarios_biblioteca:
            print("Você não está cadastrado em nossa biblioteca ainda! primeiro cadastre-se para emprestar livros!")
            return
        
        if len(usuario.livros_emprestados) >= 3:
            print("Você já atingiu o limite de livros que pode emprestar!")
            return
        
        if not livro in self.livros_biblioteca:
            print("Este livro não consta em nossa biblioteca!")
            return
        
        if livro in usuario.livros_emprestados:
            print("Você já emprestou esse livro!")
            return
        
        if livro.disponivel == False:
            print("Este livro já foi emprestado por outro usuário!")
            return
        
        usuario.livros_emprestados.append(livro)
        usuario.quantidade_vezes_emprestou += 1
        livro.quantidade_vezes_emprestado += 1
        data_devolução = {
            "livro_emprestado" : livro,
            "data_emprestado" : datetime.today(),
            "data_devolução" : datetime.today() + timedelta(days=3)
        }
        self.marcar_livro_indisponivel(livro)
        self.livros_emprestados.append(data_devolução)
        print(f"Usuário {usuario.user_name} emprestou o livro: {livro.book_title}")
        
    def marcar_livro_como_disponivel(self, livro) -> bool:
        if not livro in self.livros_biblioteca:
            print("Este livro não consta em nossa biblioteca!")
            return

        livro.disponivel = True
        
    def marcar_livro_indisponivel(self, livro) -> bool:
        if not livro in self.livros_biblioteca:
            print("Este livro não consta em nossa biblioteca!")
            return
    
        livro.disponivel = False
        
    def devolver_livro(self, usuario, livro):
        if usuario not in self.usuarios_biblioteca:
            print("Você não está cadastrado em nossa biblioteca ainda! primeiro cadastre-se para emprestar livros!")
            return
        
        if len(usuario.livros_emprestados) <= 0:
            print("Você não emprestou nenhum livro para pensar em devolver!")
            return
        
        if not livro in self.livros_biblioteca:
            print("Este livro não consta em nossa biblioteca!")
            return

        if livro not in usuario.livros_emprestados:
            print("Você não emprestou esse livro!")
            return
        
        dias_atrasado = self.verificar_data_devolucao(livro)
        multa = 0
        if dias_atrasado >= 1:
            multa = 1 * dias_atrasado
        
        if multa:
            print("Você devolveu o livro com", dias_atrasado, "dia(s) de atraso. Portanto deverá pagar uma multa de R${0:.2f}".format(multa))
        usuario.livros_emprestados.remove(livro)
        self.marcar_livro_como_disponivel(livro) 
        for registro in list(self.livros_emprestados):
            if registro["livro_emprestado"] == livro:
                self.livros_emprestados.remove(registro)
                break
        print(f"Usuário {usuario.user_name} devolveu o livro: {livro.book_title}")

    def verificar_data_devolucao(self, livro) -> int:
        for registro in self.livros_emprestados:
            if registro["livro_emprestado"] == livro:
                dia_devolucao = registro["data_devolução"]
                diferenca = datetime.today() - dia_devolucao
                return diferenca.days if diferenca.days >= 1 else 0
        print("Este livro não foi emprestado por ninguém!")
        return None
    
    def relatorio(self):
        if not self.livros_emprestados:
            print("Não há livros emprestados para relatórios.")
            return

        for livro in self.livros_emprestados:
            dias_atrasado = self.verificar_data_devolucao(livro["livro_emprestado"])
            if dias_atrasado <= 0:
                continue
            livro_real = livro["livro_emprestado"]
            print(f"Livro {livro_real.book_title} está atrasado!")
        
        top_tres_livros_mais_emprestados = heapq.nlargest(3, [e["livro_emprestado"] for e in self.livros_emprestados], key=lambda x: x.quantidade_vezes_emprestado)
        print("\n===== LIVROS MAIS EMPRESTADOS =====")
        for livro_mais_emprestado in top_tres_livros_mais_emprestados:
            print(f"Título: {livro_mais_emprestado.book_title} | Autor: {livro_mais_emprestado.author} | Quantidade de vezes que foi emprestado: {livro_mais_emprestado.quantidade_vezes_emprestado}")
        
        print("\n===== USUÁRIOS QUE MAIS EMPRESTAM =====")
        top_tres_usuarios_que_mais_emprestam = heapq.nlargest(3, self.usuarios_biblioteca, key=lambda x : x.quantidade_vezes_emprestou)
        for top_usuario in top_tres_usuarios_que_mais_emprestam:
            print(f"Nome do usuário: {top_usuario.user_name} | Quantidade de vezes que emprestou: {top_usuario.quantidade_vezes_emprestou}")
            
class Usuario:
    
    def __init__(self, nome: str, email: str):
        self.user_id = uuid.uuid1()
        self.user_name = nome
        self.email = email
        self.livros_emprestados = deque()
        self.quantidade_vezes_emprestou = 0
    

class Livros:
    
    def __init__(self, titulo: str, autor: str, ano: date):
        self.book_id = uuid.uuid1()
        self.book_title = titulo
        self.author = autor
        self.date_published = ano
        self.disponivel = True
        self.quantidade_vezes_emprestado = 0
    

biblioteca = Biblioteca("Biblioteca Maringá")

us1 = Usuario("Djeffer", "djeffer@teste.com")
us2 = Usuario("Luiz", "luiz@teste.com")
us3 = Usuario("Enrico", "enrico@teste.com")

lvr1 = Livros("Estrela decadente", "Demiurgo", date(2008, 4, 12))
lvr2 = Livros("Arquiteto da Mentira", "Demiurgo", date(2005, 4, 1))
lvr3 = Livros("Artíficie do Cárcere", "Demiurgo", date(2009, 12, 12))
lvr4 = Livros("A Centelha diante da Luz", "Demiurgo", date(2023, 1, 24))

biblioteca.cadastrar_livro(lvr1)
biblioteca.cadastrar_livro(lvr2)
biblioteca.cadastrar_livro(lvr3)
biblioteca.cadastrar_livro(lvr4)

biblioteca.cadastrar_usuarios(us1)
biblioteca.cadastrar_usuarios(us2)
biblioteca.cadastrar_usuarios(us3)

biblioteca.emprestar_livro(us1, lvr1)
biblioteca.emprestar_livro(us1, lvr2)
biblioteca.emprestar_livro(us3, lvr4)
biblioteca.emprestar_livro(us2, lvr3)
biblioteca.devolver_livro(us2, lvr3)
biblioteca.devolver_livro(us1, lvr2)
biblioteca.emprestar_livro(us1, lvr3)

print("="*60)
print("TESTE 1: LIMITES E RESTRIÇÕES")
print("="*60)

us4 = Usuario("Ana", "ana@teste.com")
us5 = Usuario("Pedro", "pedro@teste.com")
us6 = Usuario("Carla", "carla@teste.com")

lvr5 = Livros("O Senhor dos Anéis", "J.R.R. Tolkien", date(1954, 7, 29))
lvr6 = Livros("1984", "George Orwell", date(1949, 6, 8))
lvr7 = Livros("Dom Casmurro", "Machado de Assis", date(1899, 1, 1))
lvr8 = Livros("Harry Potter", "J.K. Rowling", date(1997, 6, 26))
lvr9 = Livros("Clean Code", "Robert Martin", date(2008, 8, 1))
lvr10 = Livros("Python Fluente", "Luciano Ramalho", date(2015, 7, 20))

biblioteca.cadastrar_livro(lvr5)
biblioteca.cadastrar_livro(lvr6)
biblioteca.cadastrar_livro(lvr7)
biblioteca.cadastrar_livro(lvr8)
biblioteca.cadastrar_livro(lvr9)
biblioteca.cadastrar_livro(lvr10)

biblioteca.cadastrar_usuarios(us4)
biblioteca.cadastrar_usuarios(us5)
biblioteca.cadastrar_usuarios(us6)
biblioteca.emprestar_livro(us4, lvr5)
biblioteca.emprestar_livro(us4, lvr6) 
biblioteca.emprestar_livro(us4, lvr7)
biblioteca.emprestar_livro(us4, lvr8) 
biblioteca.emprestar_livro(us5, lvr5) 

print("\n" + "="*60)
print("TESTE 2: MULTAS E ATRASOS")
print("="*60)

lvr_atraso = Livros("Livro Teste Atraso", "Autor Teste", date(2020, 1, 1))
biblioteca.cadastrar_livro(lvr_atraso)
biblioteca.emprestar_livro(us5, lvr_atraso) 

for registro in biblioteca.livros_emprestados:
    if registro["livro_emprestado"] == lvr_atraso:
        # Modificar data de devolução para 5 dias ATRÁS
        registro["data_devolução"] = datetime.today() - timedelta(days=5)
        print("⚠️  Data de devolução modificada para 5 dias atrás")
        break

biblioteca.devolver_livro(us5, lvr_atraso)  

print("\n" + "="*60)
print("TESTE 4: RELATÓRIOS E ESTATÍSTICAS")
print("="*60)

biblioteca.emprestar_livro(us2, lvr5)
biblioteca.emprestar_livro(us3, lvr6)
biblioteca.emprestar_livro(us4, lvr8) 
biblioteca.emprestar_livro(us5, lvr9)
biblioteca.emprestar_livro(us6, lvr10)


biblioteca.devolver_livro(us2, lvr5)
biblioteca.devolver_livro(us3, lvr6)

biblioteca.relatorio()
lvr_atraso2 = Livros("Outro Livro Atrasado", "Autor", date(2021, 1, 1))
biblioteca.cadastrar_livro(lvr_atraso2)
biblioteca.emprestar_livro(us1, lvr_atraso2)

for registro in biblioteca.livros_emprestados:
    if registro["livro_emprestado"] == lvr_atraso2:
        registro["data_devolução"] = datetime.today() - timedelta(days=3)
        break

print("\n📊 RELATÓRIO COM ATRASOS:")
biblioteca.relatorio()


print("\n" + "="*60)
print("TESTE 6: TESTES DE BORDA (EDGE CASES)")
print("="*60)
biblioteca_vazia = Biblioteca("Biblioteca Vazia")
biblioteca_vazia.relatorio()  


biblioteca_vazia.cadastrar_usuarios(Usuario("Teste", "teste@teste.com"))

usuario_sem_livros = Usuario("Sem Livros", "sem@teste.com")
biblioteca.cadastrar_usuarios(usuario_sem_livros)
biblioteca.devolver_livro(usuario_sem_livros, lvr1) 

livro_nunca_emprestado = Livros("Nunca Emprestado", "Autor", date(2024, 1, 1))
biblioteca.cadastrar_livro(livro_nunca_emprestado)
biblioteca.devolver_livro(us1, livro_nunca_emprestado)  