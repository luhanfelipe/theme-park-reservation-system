import customtkinter as ctk

class TelaHome(ctk.CTkFrame):
    def __init__(self, master, servico):
        super().__init__(master)
        self.servico = servico

        # --- TÍTULO DO DASHBOARD ---
        self.lbl_titulo = ctk.CTkLabel(
            self, 
            text="📊 Dashboard do Parque", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.lbl_titulo.pack(pady=(25, 15))

        # --- CONTAINER DOS CARDS (GRID DE METRICAS) ---
        self.frame_cards = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_cards.pack(pady=10, padx=20, fill="x")
        
        # Três colunas com pesos iguais
        self.frame_cards.grid_columnconfigure(0, weight=1)
        self.frame_cards.grid_columnconfigure(1, weight=1)
        self.frame_cards.grid_columnconfigure(2, weight=1)

        # --- CARTÃO 1: VISITANTES ---
        self.card_visitantes = ctk.CTkFrame(
            self.frame_cards, 
            corner_radius=12, 
            border_width=1, 
            border_color="#374151"
        )
        self.card_visitantes.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.lbl_tit_vis = ctk.CTkLabel(
            self.card_visitantes, 
            text=" 👤 Visitantes Cadastrados", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#9ca3af"
        )
        self.lbl_tit_vis.pack(pady=(20, 5))
        
        self.lbl_val_vis = ctk.CTkLabel(
            self.card_visitantes, 
            text="0", 
            font=ctk.CTkFont(size=44, weight="bold"), 
            text_color="#38bdf8"
        )
        self.lbl_val_vis.pack(pady=(0, 20))

        # --- CARTÃO 2: ATRAÇÕES ---
        self.card_atracoes = ctk.CTkFrame(
            self.frame_cards, 
            corner_radius=12, 
            border_width=1, 
            border_color="#374151"
        )
        self.card_atracoes.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.lbl_tit_atr = ctk.CTkLabel(
            self.card_atracoes, 
            text="✦ Atrações Cadastradas", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#9ca3af"
        )
        self.lbl_tit_atr.pack(pady=(20, 5))
        
        self.lbl_val_atr = ctk.CTkLabel(
            self.card_atracoes, 
            text="0", 
            font=ctk.CTkFont(size=44, weight="bold"), 
            text_color="#34d399"
        )
        self.lbl_val_atr.pack(pady=(0, 20))

        # --- CARTÃO 3: OPERAÇÃO / STATUS ---
        self.card_status = ctk.CTkFrame(
            self.frame_cards, 
            corner_radius=12, 
            border_width=1, 
            border_color="#374151"
        )
        self.card_status.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.lbl_tit_status = ctk.CTkLabel(
            self.card_status, 
            text=" ⏱ Status da Operação", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#9ca3af"
        )
        self.lbl_tit_status.pack(pady=(20, 5))
        
        self.lbl_val_status = ctk.CTkLabel(
            self.card_status, 
            text="Ativo", 
            font=ctk.CTkFont(size=28, weight="bold"), 
            text_color="#fef08a"
        )
        self.lbl_val_status.pack(pady=(10, 20))

        # --- PAINEL INFORMATIVO INFERIOR ---
        self.frame_info = ctk.CTkFrame(self, corner_radius=12, border_width=1, border_color="#374151")
        self.frame_info.pack(pady=20, padx=30, fill="both", expand=True)

        self.lbl_info_tit = ctk.CTkLabel(
            self.frame_info, 
            text="⚏ Boas-vindas ao Sistema do Parque ⚏", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.lbl_info_tit.pack(pady=(15, 5))

        self.lbl_info_desc = ctk.CTkLabel(
            self.frame_info, 
            text="Utilize o menu lateral para gerenciar os visitantes, cadastrar novas atrações e controlar as filas virtuais com prioridade VIP.", 
            font=ctk.CTkFont(size=13),
            text_color="#9ca3af",
            wraplength=500
        )
        self.lbl_info_desc.pack(pady=(0, 15))

        # Carrega os dados atualizados ao abrir a tela
        self.atualizar_estatisticas()

    def atualizar_estatisticas(self):
        visitantes = self.servico.listar_visitantes()
        atracoes = self.servico.listar_atracoes()

        total_visitantes = len(visitantes)
        total_atracoes = len(atracoes)

        self.lbl_val_vis.configure(text=str(total_visitantes))
        self.lbl_val_atr.configure(text=str(total_atracoes))