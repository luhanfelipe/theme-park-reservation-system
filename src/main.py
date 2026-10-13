import customtkinter as ctk
from src.services.parque_service import ParqueService

# Telas de Login e Cadastro
from src.gui.login.tela_cadastro import TelaCadastro
from src.gui.login.tela_login import TelaLogin

# Telas do Administrador
from src.gui.administrador.tela_home import TelaHome
from src.gui.administrador.tela_atracao import TelaAtracao
from src.gui.administrador.tela_fila import TelaFila

# Telas do Visitante
from src.gui.visitante.tela_reservas import TelaReservas
from src.gui.visitante.tela_minhas_filas import TelaMinhasFilas
from src.gui.visitante.tela_home_visitante import TelaHomeVisitante

class AppParque(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.servico = ParqueService()
        self.title("Sistema de Reservas - Parque Temático")
        self.geometry("1100x650") # Aumentei um pouco para caber melhor os cartões

        # Cores da interface
        COR_FUNDO_APP = "#1F1D2B"
        COR_MENU = "#252836"
        self.COR_BOTAO_ROXO = "#6C63FF"
        COR_HOVER_ROXO = "#5A52D5"
        COR_VERMELHO = "#ef4444"
        COR_HOVER_VERMELHO = "#7f1d1d"

        self.configure(fg_color=COR_FUNDO_APP)

        # Configuração das colunas (Menu Retrátil)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        self.usuario_logado = None
        self.menu_visivel = False
        self.botoes_menu = []

        # --- BARRA LATERAL FINA (Botão Hambúrguer) ---
        self.frame_fino = ctk.CTkFrame(self, width=50, corner_radius=0, fg_color=COR_MENU)
        self.btn_hamburguer = ctk.CTkButton(
            self.frame_fino, text="☰", width=40, height=40, font=("Arial", 24), 
            fg_color="transparent", hover_color=COR_FUNDO_APP, command=self.alternar_menu
        )
        self.btn_hamburguer.pack(pady=10)

        # --- FRAME DO MENU LATERAL (Aberto) ---
        self.frame_menu = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=COR_MENU)
        
        self.label_logo = ctk.CTkLabel(self.frame_menu, text="Menu Parque", font=ctk.CTkFont(size=20, weight="bold"), text_color="#FFFFFF")
        self.label_logo.pack(pady=(30, 20))

        # Sub-frame apenas para guardar os botões dinâmicos (facilita limpar)
        self.frame_botoes = ctk.CTkFrame(self.frame_menu, fg_color="transparent")
        self.frame_botoes.pack(fill="both", expand=True)

        # Botão de Logout fixo em baixo
        self.btn_logout = ctk.CTkButton(
            self.frame_menu, text="Sair da Sessão", fg_color=COR_VERMELHO, 
            hover_color=COR_HOVER_VERMELHO, command=self.fazer_logout
        )
        self.btn_logout.pack(side="bottom", pady=30, padx=20)

        # --- FRAME PRINCIPAL (Onde as telas aparecem) ---
        self.frame_principal = ctk.CTkFrame(self, corner_radius=10, fg_color=COR_FUNDO_APP)
        self.frame_principal.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")

        # Inicia o sistema
        self.abrir_tela_login()

    # ==========================================
    # UTILITÁRIOS DE NAVEGAÇÃO
    # ==========================================
    def alternar_menu(self):
        if self.menu_visivel:
            self.frame_menu.grid_remove()
            self.menu_visivel = False
        else:
            self.frame_menu.grid(row=0, column=1, sticky="nsew")
            self.menu_visivel = True

    def atualizar_botao_ativo(self, botao_selecionado):
        for btn in self.botoes_menu:
            btn.configure(fg_color="transparent")
        if botao_selecionado:
            botao_selecionado.configure(fg_color=self.COR_BOTAO_ROXO)

    def limpar_frame_principal(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

    def criar_botao_menu(self, texto, comando):
        btn = ctk.CTkButton(
            self.frame_botoes, text=texto, fg_color="transparent", 
            text_color="#FFFFFF", hover_color="#5A52D5", anchor="w", 
            command=lambda: comando(btn)
        )
        btn.pack(pady=10, padx=20, fill="x")
        self.botoes_menu.append(btn)
        return btn

    # ==========================================
    # FLUXO DE LOGIN E PERFIS
    # ==========================================
    def abrir_tela_login(self):
        self.limpar_frame_principal()
        tela = TelaLogin(self.frame_principal, self.servico, self.liberar_acesso_sistema, self.abrir_tela_cadastro_publico)
        tela.pack(fill="both", expand=True)

    def abrir_tela_cadastro_publico(self):
        self.limpar_frame_principal()
        tela = TelaCadastro(self.frame_principal, self.servico, self.abrir_tela_login)
        tela.pack(fill="both", expand=True)

    def fazer_logout(self):
        self.frame_menu.grid_remove()
        self.frame_fino.grid_remove()
        self.menu_visivel = False
        self.usuario_logado = None
        
        self.frame_principal.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")
        self.abrir_tela_login()

    def liberar_acesso_sistema(self, perfil, cpf=None):
        self.usuario_logado = {"perfil": perfil, "cpf": cpf}
        self.limpar_frame_principal()

        self.frame_fino.grid(row=0, column=0, sticky="nsew")
        self.frame_menu.grid(row=0, column=1, sticky="nsew")
        self.menu_visivel = True
        self.frame_principal.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")

        self._construir_menu_dinamico()

    def _construir_menu_dinamico(self):
        # Limpa os botões anteriores
        for widget in self.frame_botoes.winfo_children():
            widget.destroy()
        self.botoes_menu.clear()

        perfil = self.usuario_logado["perfil"]

        if perfil == "admin":
            self.label_logo.configure(text="Painel Admin")
            btn_home = self.criar_botao_menu("📊 Dashboard", self.abrir_tela_home)
            self.criar_botao_menu("🎢 Gerir Atrações", self.abrir_tela_atracao)
            self.criar_botao_menu("⧖ Fila Virtual", self.abrir_tela_fila)
            self.abrir_tela_home(btn_home) # Vai direto para a Home

        elif perfil == "visitante":
            self.label_logo.configure(text="Painel Visitante")
            btn_home = self.criar_botao_menu("🏠 Início", self.abrir_tela_home_visitante)
            self.criar_botao_menu("🎡 Reservar Atração", self.abrir_tela_reservas)
            self.criar_botao_menu("📋 Minhas Filas", self.abrir_tela_minhas_filas)
            self.abrir_tela_home_visitante(btn_home) # Vai direto para a Dashboard Visitante

    # ==========================================
    # ROTAS DO ADMINISTRADOR
    # ==========================================
    def abrir_tela_home(self, btn=None):
        self.limpar_frame_principal()
        tela = TelaHome(self.frame_principal, self.servico)
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

    # ==========================================
    # ROTAS DO VISITANTE
    # ==========================================
    def abrir_tela_reservas(self, btn=None):
        self.limpar_frame_principal()
        tela = TelaReservas(self.frame_principal, self.servico, self.usuario_logado["cpf"], self.abrir_tela_home_visitante)
        tela.pack(fill="both", expand=True)
        if btn: self.atualizar_botao_ativo(btn)

    def abrir_tela_minhas_filas(self, btn=None):
        self.limpar_frame_principal()
        tela = TelaMinhasFilas(self.frame_principal, self.servico, self.usuario_logado["cpf"], self.abrir_tela_home_visitante)
        tela.pack(fill="both", expand=True)
        if btn: self.atualizar_botao_ativo(btn)

    def abrir_tela_home_visitante(self, btn=None):
            self.limpar_frame_principal()
            tela = TelaHomeVisitante(self.frame_principal, self.servico, self.usuario_logado["cpf"])
            tela.pack(fill="both", expand=True)
            if btn: self.atualizar_botao_ativo(btn)

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    app = AppParque()
    app.mainloop()