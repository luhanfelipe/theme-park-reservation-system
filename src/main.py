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
        
        # Definimos as cores aqui em cima para ser fácil mudar no futuro
        COR_FUNDO_APP = "#1F1D2B"
        COR_MENU = "#252836"
        COR_BOTAO_ROXO = "#6C63FF"
        COR_HOVER_ROXO = "#5A52D5" 
        COR_VERMELHO = "#C9302C"
        COR_HOVER_VERMELHO = "#AC2925"

        # Aplica a cor de fundo escura à janela inteira do programa
        self.configure(fg_color=COR_FUNDO_APP)

        # Configuração das 3 colunas principais do sistema
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        self.menu_visivel = False 

        # --- BARRA LATERAL FINA ---
        # Aplicamos a cor do menu para parecer uma extensão natural
        self.frame_fino = ctk.CTkFrame(self, width=50, corner_radius=0, fg_color=COR_MENU)
        
        self.btn_hamburguer = ctk.CTkButton(self.frame_fino, text="☰", width=40, height=40, font=("Arial", 24), fg_color="transparent", hover_color=COR_FUNDO_APP, command=self.alternar_menu)
        self.btn_hamburguer.pack(pady=10)

        # --- FRAME DO MENU LATERAL (A barra que abre e fecha) ---
        self.frame_menu = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color=COR_MENU)

        self.label_logo = ctk.CTkLabel(self.frame_menu, text="Menu Parque", font=ctk.CTkFont(size=20, weight="bold"), text_color="#FFFFFF")
        self.label_logo.grid(row=0, column=0, padx=20, pady=(20, 30))

        # --- BOTÕES DE NAVEGAÇÃO ---
        self.botoes_menu = []
        
        self.btn_home = ctk.CTkButton(
            self.frame_menu, text="Início (Dashboard)", 
            fg_color=COR_BOTAO_ROXO, hover_color=COR_HOVER_ROXO, 
            command=lambda: self.abrir_tela_home(btn=self.btn_home)
        )
        self.btn_home.grid(row=1, column=0, padx=20, pady=10)
        self.botoes_menu.append(self.btn_home)

        self.btn_cadastrar_visitante = ctk.CTkButton(
            self.frame_menu, text="Cadastrar Visitante", 
            fg_color="transparent", hover_color=COR_HOVER_ROXO, 
            command=lambda: self.abrir_tela_visitante(btn=self.btn_cadastrar_visitante)
        )
        self.btn_cadastrar_visitante.grid(row=2, column=0, padx=20, pady=10)
        self.botoes_menu.append(self.btn_cadastrar_visitante)

        self.btn_cadastrar_atracao = ctk.CTkButton(
            self.frame_menu, text="Cadastrar Atração", 
            fg_color="transparent", hover_color=COR_HOVER_ROXO, 
            command=lambda: self.abrir_tela_atracao(btn=self.btn_cadastrar_atracao)
        )
        self.btn_cadastrar_atracao.grid(row=3, column=0, padx=20, pady=10)
        self.botoes_menu.append(self.btn_cadastrar_atracao)

        self.btn_fila_virtual = ctk.CTkButton(
            self.frame_menu, text="Fila Virtual", 
            fg_color="transparent", hover_color=COR_HOVER_ROXO, 
            command=lambda: self.abrir_tela_fila(btn=self.btn_fila_virtual)
        )
        self.btn_fila_virtual.grid(row=4, column=0, padx=20, pady=10)
        self.botoes_menu.append(self.btn_fila_virtual)

        # --- BOTÃO DE LOGOUT ---
        # Usa o vermelho de alerta para indicar uma ação destrutiva (sair)
        self.btn_logout = ctk.CTkButton(self.frame_menu, text="Sair da Sessão", fg_color=COR_VERMELHO, hover_color=COR_HOVER_VERMELHO, command=self.fazer_logout)
        
        self.frame_menu.grid_rowconfigure(5, weight=1)
        self.btn_logout.grid(row=6, column=0, pady=20, padx=20, sticky="s")

        # --- FRAME PRINCIPAL ---
        self.frame_principal = ctk.CTkFrame(self, corner_radius=10, fg_color=COR_FUNDO_APP)
        self.frame_principal.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")

        # Dispara o carregamento do login
        self.abrir_tela_login()

    def atualizar_botao_ativo(self, botao_selecionado):
        # 1. Pinta todos os botões de transparente primeiro (Desliga todos)
        for btn in self.botoes_menu:
            btn.configure(fg_color="transparent")
        
        # 2. Pinta apenas o botão que clicámos de roxo (Liga o correto)
        if botao_selecionado:
            botao_selecionado.configure(fg_color="#6C63FF")
    
    # MENU ---
    def alternar_menu(self):
        if self.menu_visivel:
            self.frame_menu.grid_remove() # Oculta o menu (a tela principal estica pra esquerda)
            self.menu_visivel = False
        else:
            self.frame_menu.grid(row=0, column=1, sticky="nsew") # Mostra o menu de volta
            self.menu_visivel = True

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

    def abrir_tela_home(self, btn=None):
        self.limpar_frame_principal()
        tela = TelaHome(self.frame_principal, self.servico)
        tela.pack(fill="both", expand=True)
        if btn: self.atualizar_botao_ativo(btn)

    def abrir_tela_visitante(self, btn=None):
        self.limpar_frame_principal()
        tela = TelaVisitante(self.frame_principal, self.servico, self.abrir_tela_home)
        tela.pack(fill="both", expand=True)
        if btn: self.atualizar_botao_ativo(btn)

    def abrir_tela_atracao(self, btn=None):
        self.limpar_frame_principal()
        tela = TelaAtracao(self.frame_principal, self.servico, self.abrir_tela_home)
        tela.pack(fill="both", expand=True)
        if btn: self.atualizar_botao_ativo(btn)

    def abrir_tela_fila(self, btn=None):
        self.limpar_frame_principal()
        tela = TelaFila(self.frame_principal, self.servico, self.abrir_tela_home)
        tela.pack(fill="both", expand=True)
        if btn: self.atualizar_botao_ativo(btn)

    ##-- Logout temporário apenas para ilustração, futuramente será arrumado com a implementação do banco --
    def fazer_logout(self):
            # 1. Esconde as duas barras laterais do sistema
            self.frame_menu.grid_remove() 
            self.frame_fino.grid_remove()
            self.menu_visivel = False
            
            # 2. Devolve o frame principal para o centro, ocupando a tela toda (as 3 colunas)
            self.frame_principal.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")
            
            # 3. Chama a função que você já tem para desenhar a TelaLogin!
            self.abrir_tela_login()

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    app = AppParque()
    app.mainloop()