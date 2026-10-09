import customtkinter as ctk
from src.services.parque_service import ParqueService
from src.gui.tela_visitante import TelaVisitante
from src.gui.tela_atracao import TelaAtracao
from src.gui.tela_fila import TelaFila
from src.gui.tela_login import TelaLogin
from src.gui.tela_home import TelaHome

class AppParque(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.servico = ParqueService()
        self.title("Sistema de Reservas - Parque Temático")
        self.geometry("900x600")
        
        # Agora dividimos a tela em 3 colunas
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0) # Coluna 0: Barra Fina (Nunca estica)
        self.grid_columnconfigure(1, weight=0) # Coluna 1: Menu Retrátil (Estica e encolhe)
        self.grid_columnconfigure(2, weight=1) # Coluna 2: Tela Principal (Ocupa o resto)

        self.menu_visivel = False # Começa avisando o Python que o menu tá escondido no login

        # --- BARRA LATERAL FINA (Sempre visível após o login) ---
        self.frame_fino = ctk.CTkFrame(self, width=50, corner_radius=0)
        
        # Botão Hambúrguer usando o símbolo ☰ do teclado!
        self.btn_hamburguer = ctk.CTkButton(self.frame_fino, text="☰", width=40, height=40, font=("Arial", 24), fg_color="transparent", command=self.alternar_menu)
        self.btn_hamburguer.pack(pady=10)

        # --- FRAME MENU (Expansível) ---
        self.frame_menu = ctk.CTkFrame(self, width=200, corner_radius=0)

        self.label_logo = ctk.CTkLabel(self.frame_menu, text="Menu Parque", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_logo.grid(row=0, column=0, padx=20, pady=(20, 30))

        self.btn_home = ctk.CTkButton(self.frame_menu, text="Início (Dashboard)", command=self.abrir_tela_home)
        self.btn_home.grid(row=1, column=0, padx=20, pady=10)

        self.btn_cadastrar_visitante = ctk.CTkButton(self.frame_menu, text="Cadastrar Visitante", command=self.abrir_tela_visitante)
        self.btn_cadastrar_visitante.grid(row=2, column=0, padx=20, pady=10)

        self.btn_cadastrar_atracao = ctk.CTkButton(self.frame_menu, text="Cadastrar Atração", command=self.abrir_tela_atracao)
        self.btn_cadastrar_atracao.grid(row=3, column=0, padx=20, pady=10)

        self.btn_fila_virtual = ctk.CTkButton(self.frame_menu, text="Fila Virtual", command=self.abrir_tela_fila)
        self.btn_fila_virtual.grid(row=4, column=0, padx=20, pady=10)

        # --- FRAME PRINCIPAL ---
        self.frame_principal = ctk.CTkFrame(self, corner_radius=10)
        # Na hora do Login, a tela principal ocupa as 3 colunas de ponta a ponta!
        self.frame_principal.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")

        # Inicia direto na tela de login
        self.abrir_tela_login()

    # --- A MÁGICA DE ABRIR E FECHAR O MENU ---
    def alternar_menu(self):
        if self.menu_visivel:
            self.frame_menu.grid_remove() # Oculta o menu (a tela principal estica pra esquerda)
            self.menu_visivel = False
        else:
            self.frame_menu.grid(row=0, column=1, sticky="nsew") # Mostra o menu de volta
            self.menu_visivel = True
    # ------------------------------------------

    def abrir_tela_login(self):
        self.limpar_frame_principal()
        tela = TelaLogin(self.frame_principal, self.liberar_acesso_sistema)
        tela.pack(fill="both", expand=True)

    def liberar_acesso_sistema(self):
        self.limpar_frame_principal()
        
        # Mostra a barra fina com o ☰ na primeira coluna
        self.frame_fino.grid(row=0, column=0, sticky="nsew")
        
        # Mostra o menu inteiro na segunda coluna
        self.frame_menu.grid(row=0, column=1, sticky="nsew")
        self.menu_visivel = True
        
        # Empurra a tela principal para a terceira coluna
        self.frame_principal.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")
        
        self.abrir_tela_home()

    def limpar_frame_principal(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

    def abrir_tela_home(self):
        self.limpar_frame_principal()
        tela = TelaHome(self.frame_principal, self.servico)
        tela.pack(fill="both", expand=True)

    def abrir_tela_visitante(self):
        self.limpar_frame_principal()
        tela = TelaVisitante(self.frame_principal, self.servico, self.abrir_tela_home)
        tela.pack(fill="both", expand=True)

    def abrir_tela_atracao(self):
        self.limpar_frame_principal()
        tela = TelaAtracao(self.frame_principal, self.servico, self.abrir_tela_home)
        tela.pack(fill="both", expand=True)

    def abrir_tela_fila(self):
        self.limpar_frame_principal()
        tela = TelaFila(self.frame_principal, self.servico, self.abrir_tela_home)
        tela.pack(fill="both", expand=True)

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    app = AppParque()
    app.mainloop()