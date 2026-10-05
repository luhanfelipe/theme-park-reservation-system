import customtkinter as ctk
from src.services.parque_service import ParqueService
from src.gui.tela_visitante import TelaVisitante

class AppParque(ctk.CTk):
    """Representa a janela principal do sistema do parque."""
    def __init__(self):
        super().__init__()

        # Inicializa o serviço responsável pelas regras do sistema.
        self.servico = ParqueService()

        # Configurações da Janela
        self.title("Sistema de Reservas - Parque Temático")
        self.geometry("900x600")
        
        # Grid layout (1 linha, 2 colunas: Menu lateral e Área de conteúdo)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- FRAME LATERAL (Menu) ---
        self.frame_menu = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.frame_menu.grid(row=0, column=0, sticky="nsew")
        self.frame_menu.grid_rowconfigure(5, weight=1)

        self.label_logo = ctk.CTkLabel(self.frame_menu, text="Menu Parque", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_logo.grid(row=0, column=0, padx=20, pady=(20, 30))

        self.btn_cadastrar_visitante = ctk.CTkButton(self.frame_menu, text="Cadastrar Visitante", command=self.abrir_tela_visitante)
        self.btn_cadastrar_visitante.grid(row=1, column=0, padx=20, pady=10)

        self.btn_cadastrar_atracao = ctk.CTkButton(self.frame_menu, text="Cadastrar Atração", command=self.abrir_tela_atracao)
        self.btn_cadastrar_atracao.grid(row=2, column=0, padx=20, pady=10)

        self.btn_fila_virtual = ctk.CTkButton(self.frame_menu, text="Fila Virtual", command=self.abrir_tela_fila)
        self.btn_fila_virtual.grid(row=3, column=0, padx=20, pady=10)

        # --- FRAME PRINCIPAL (Onde o conteúdo vai aparecer) ---
        self.frame_principal = ctk.CTkFrame(self, corner_radius=10)
        self.frame_principal.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.label_boas_vindas = ctk.CTkLabel(self.frame_principal, text="Bem-vindo ao Sistema do Parque!", font=("Arial", 24))
        self.label_boas_vindas.pack(expand=True)

    # Métodos para limpar a tela principal e carregar a nova (serão implementados depois)
    def limpar_frame_principal(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

    def abrir_tela_visitante(self):
        self.limpar_frame_principal()

        tela = TelaVisitante(self.frame_principal, self.servico)
        tela.pack(fill="both", expand=True) # Faz a tela ocupar todo o espaço

    def abrir_tela_atracao(self):
        self.limpar_frame_principal()
        ctk.CTkLabel(self.frame_principal, text="Tela de Cadastro de Atrações (Em breve)", font=("Arial", 18)).pack(pady=20)

    def abrir_tela_fila(self):
        self.limpar_frame_principal()
        ctk.CTkLabel(self.frame_principal, text="Tela da Fila Virtual (Em breve)", font=("Arial", 18)).pack(pady=20)

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark") # Pode ser "Light" ou "System"
    app = AppParque()
    app.mainloop()