import customtkinter as ctk

class TelaHome(ctk.CTkFrame):
    def __init__(self, master, servico):
        super().__init__(master)
        self.servico = servico

        self.lbl_titulo = ctk.CTkLabel(self, text="Dashboard do Parque", font=("Arial", 24, "bold"))
        self.lbl_titulo.pack(pady=(30, 20))

        # Frame invisível só para organizar os cartões lado a lado
        self.frame_cards = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_cards.pack(pady=20, padx=20, fill="x")
        
        # Grid para dividir a tela no meio (50% pra cada lado)
        self.frame_cards.grid_columnconfigure(0, weight=1)
        self.frame_cards.grid_columnconfigure(1, weight=1)

        # --- CARTÃO DE VISITANTES ---
        self.card_visitantes = ctk.CTkFrame(self.frame_cards, corner_radius=15)
        self.card_visitantes.grid(row=0, column=0, padx=15, pady=10, sticky="nsew")
        
        self.lbl_tit_vis = ctk.CTkLabel(self.card_visitantes, text="Visitantes Cadastrados", font=("Arial", 16))
        self.lbl_tit_vis.pack(pady=(20, 5))
        
        self.lbl_val_vis = ctk.CTkLabel(self.card_visitantes, text="0", font=("Arial", 48, "bold"), text_color="#1f6aa5")
        self.lbl_val_vis.pack(pady=(0, 20))

        # --- CARTÃO DE ATRAÇÕES ---
        self.card_atracoes = ctk.CTkFrame(self.frame_cards, corner_radius=15)
        self.card_atracoes.grid(row=0, column=1, padx=15, pady=10, sticky="nsew")

        self.lbl_tit_atr = ctk.CTkLabel(self.card_atracoes, text="Atrações Cadastradas", font=("Arial", 16))
        self.lbl_tit_atr.pack(pady=(20, 5))
        
        self.lbl_val_atr = ctk.CTkLabel(self.card_atracoes, text="0", font=("Arial", 48, "bold"), text_color="#1f6aa5")
        self.lbl_val_atr.pack(pady=(0, 20))

        # Chama a função para calcular os números na hora que a tela abre
        self.atualizar_estatisticas()

    def atualizar_estatisticas(self):
        # Pede pro gerente as listas completas
        visitantes = self.servico.listar_visitantes()
        atracoes = self.servico.listar_atracoes()

        # Usa a função len() do Python para contar quantas pessoas/brinquedos tem na lista
        total_visitantes = len(visitantes)
        total_atracoes = len(atracoes)

        # Atualiza os números gigantes na tela
        self.lbl_val_vis.configure(text=str(total_visitantes))
        self.lbl_val_atr.configure(text=str(total_atracoes))