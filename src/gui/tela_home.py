import customtkinter as ctk

class TelaHome(ctk.CTkFrame):
    def __init__(self, master, servico):

        super().__init__(master, fg_color="transparent")
        self.servico = servico

        # Cores da Paleta Magia Premium
        COR_CARD = "#252836"       # Mesma cor do menu lateral para criar harmonia
        COR_DOURADO = "#FFD700" 
        COR_VERDE = "#1B921B"
        COR_AZUL = "#3873AD"
        COR_TEXTO = "#FFFFFF"      # Branco para títulos
        COR_TEXTO_SEC = "#A0A0A0"  # Cinza claro para subtítulos

        # Título da Dashboard
        self.lbl_titulo = ctk.CTkLabel(self, text="🎢 Bem-Vindos ao Sistema do Parque", font=("Arial", 24, "bold"), text_color=COR_TEXTO)
        self.lbl_titulo.pack(pady=(20, 30))

        # --- FRAME DOS CARDS (GRID HORIZONTAL) ---
        self.frame_cards = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_cards.pack(pady=10, padx=20, fill="x")
        
        # Configurar as colunas para terem o mesmo tamanho (weight=1)
        self.frame_cards.grid_columnconfigure((0, 1, 2), weight=1)

        # 1. CARD VISITANTES

        COR_FUNDO_VIDRO = "#2A2D3E"
        COR_BORDA_NEON = "#5A52D5"

        # Usamos a COR_CARD para destacar o cartão do fundo
        card_visitantes = ctk.CTkFrame(
            self.frame_cards, 
            corner_radius=15, 
            fg_color=COR_FUNDO_VIDRO,
            border_width=1,
            border_color=COR_BORDA_NEON
        )
        card_visitantes.grid(row=0, column=0, padx=10, sticky="nsew")
        
        lbl_tit_vis = ctk.CTkLabel(card_visitantes, text="👤 Visitantes Cadastrados", font=("Arial", 14, "bold"), text_color=COR_TEXTO_SEC)
        lbl_tit_vis.pack(pady=(15, 5))
        
        self.lbl_num_visitantes = ctk.CTkLabel(card_visitantes, text="0", font=("Arial", 48, "bold"), text_color=COR_AZUL)
        self.lbl_num_visitantes.pack(pady=(0, 15))

        # 2. CARD ATRAÇÕES
        card_atracoes = ctk.CTkFrame(
            self.frame_cards, 
            corner_radius=15, 
            fg_color=COR_FUNDO_VIDRO,
            border_width=1,
            border_color=COR_BORDA_NEON
        )
        card_atracoes.grid(row=0, column=1, padx=10, sticky="nsew")
        
        lbl_tit_atr = ctk.CTkLabel(card_atracoes, text="✨ Atrações Cadastradas", font=("Arial", 14, "bold"), text_color=COR_TEXTO_SEC)
        lbl_tit_atr.pack(pady=(15, 5))
        
        self.lbl_num_atracoes = ctk.CTkLabel(card_atracoes, text="0", font=("Arial", 48, "bold"), text_color=COR_VERDE)
        self.lbl_num_atracoes.pack(pady=(0, 15))

        # 3. CARD STATUS
        card_status = ctk.CTkFrame(
            self.frame_cards, 
            corner_radius=15, 
            fg_color=COR_FUNDO_VIDRO,
            border_width=1,
            border_color=COR_BORDA_NEON
        )
        card_status.grid(row=0, column=2, padx=10, sticky="nsew")
        
        lbl_tit_status = ctk.CTkLabel(card_status, text="⚙️ Status da Operação", font=("Arial", 14, "bold"), text_color=COR_TEXTO_SEC)
        lbl_tit_status.pack(pady=(15, 5))
        
        self.lbl_status = ctk.CTkLabel(card_status, text="Ativo", font=("Arial", 36, "bold"), text_color=COR_DOURADO)
        self.lbl_status.pack(pady=(5, 15))

      # --- FRAME CENTRAL ---
        self.frame_central = ctk.CTkFrame(self, corner_radius=15, fg_color=COR_CARD, border_width=1, border_color="#5A52D5")
        self.frame_central.pack(pady=30, padx=20, fill="both", expand=True)
        
        # Divide o frame central em duas partes (Esquerda e Direita)
        self.frame_central.grid_columnconfigure(0, weight=1)
        self.frame_central.grid_columnconfigure(1, weight=1)
        self.frame_central.grid_rowconfigure(0, weight=1)

        # LADO ESQUERDO: Capacidade do Parque

        frame_esq = ctk.CTkFrame(self.frame_central, fg_color="transparent")
        frame_esq.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        lbl_titulo_esq = ctk.CTkLabel(frame_esq, text="📊 Capacidade do Parque", font=("Arial", 18, "bold"), text_color=COR_TEXTO)
        lbl_titulo_esq.pack(pady=(10, 20))
        
        # barra de progresso
        self.barra_capacidade = ctk.CTkProgressBar(frame_esq, orientation="horizontal", height=20, progress_color=COR_DOURADO)
        self.barra_capacidade.pack(fill="x", padx=20)
        self.barra_capacidade.set(0.0)
        
        self.lbl_detalhe_cap = ctk.CTkLabel(frame_esq, text="0 / 500 Visitantes Máx.", font=("Arial", 14), text_color=COR_TEXTO_SEC)
        self.lbl_detalhe_cap.pack(pady=10)

        # LADO DIREITO: Resumo das Filas

        frame_dir = ctk.CTkFrame(self.frame_central, fg_color="transparent")
        frame_dir.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        lbl_titulo_dir = ctk.CTkLabel(frame_dir, text="Filas Mais Longas", font=("Arial", 18, "bold"), text_color=COR_TEXTO)
        lbl_titulo_dir.pack(pady=(10, 10))
        
        self.frame_mini_filas = ctk.CTkScrollableFrame(frame_dir, fg_color="transparent", height=150)
        self.frame_mini_filas.pack(fill="both", expand=True)

        # Chama a função para preencher os números reais
        self.atualizar_dashboard()

    def atualizar_dashboard(self):
        # 1. Atualiza o número de visitantes e a barra de capacidade
            try:
                visitantes = self.servico.listar_visitantes()
                total_visitantes = len(visitantes)
                self.lbl_num_visitantes.configure(text=str(total_visitantes))
                
                # Atualiza a barra de capacidade
                capacidade_maxima = 500
                percentagem = total_visitantes / capacidade_maxima
                self.barra_capacidade.set(percentagem)
                self.lbl_detalhe_cap.configure(text=f"{total_visitantes} / {capacidade_maxima} Visitantes Máx.")
            except:
                self.lbl_num_visitantes.configure(text="0")
                self.barra_capacidade.set(0)

            # 2. Atualiza os números das atrações
            try:
                atracoes = self.servico.listar_atracoes()
                self.lbl_num_atracoes.configure(text=str(len(atracoes)))
                
                # Limpa as filas antigas
                for widget in self.frame_mini_filas.winfo_children():
                    widget.destroy()
                    
                # Cria a listagem de filas ativas
                if not atracoes:
                    lbl_vazio = ctk.CTkLabel(self.frame_mini_filas, text="Nenhuma atração registada.", text_color="#A0A0A0")
                    lbl_vazio.pack(pady=20, anchor="w", padx=10)
                else:
                    # Ordena as atrações pela quantidade de pessoas na fila (maior para menor)
                    atracoes_ordenadas = sorted(atracoes, key=lambda a: len(a.fila_virtual.listar_fila()), reverse=True)
                    
                    # lista ordenada para desenhar os cartões
                    for a in atracoes_ordenadas:
                        tamanho_fila = len(a.fila_virtual.listar_fila())
                        
                        mini_card = ctk.CTkFrame(self.frame_mini_filas, fg_color="transparent")
                        mini_card.pack(fill="x", pady=5, anchor="w")

                        # Determina se a atração é de prioridade ou comum e ajusta o texto e a cor da tag
                        if hasattr(a, 'aceita_prioridade') and a.aceita_prioridade:
                            texto_tag = "(Prioridade)"
                            cor_tag = "#FFD700" # Dourado
                        else:
                            texto_tag = "(Comum)"
                            cor_tag = "#666666" # Cinza
                        
                        texto_atracao = f"{a.nome}"
                        lbl_nome = ctk.CTkLabel(mini_card, text=texto_atracao, font=("Arial", 14, "bold"), text_color="#FFFFFF")
                        lbl_nome.pack(side="left", padx=(10, 5))
                        
                        lbl_tag = ctk.CTkLabel(mini_card, text=texto_tag, font=("Arial", 12), text_color=cor_tag)
                        lbl_tag.pack(side="left", padx=(0, 5))
                        
                        texto_espera = f"{tamanho_fila} à espera"
                        cor_texto = "#FFD700" if tamanho_fila > 0 else "#A0A0A0" 
                        lbl_espera = ctk.CTkLabel(mini_card, text=texto_espera, font=("Arial", 14), text_color=cor_texto)
                        lbl_espera.pack(side="right", padx=(5, 10))
                        
            except Exception as e:
                print(f"Erro ao atualizar filas: {e}")
                self.lbl_num_atracoes.configure(text="0")