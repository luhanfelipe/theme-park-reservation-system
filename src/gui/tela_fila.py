import customtkinter as ctk

class TelaFila(ctk.CTkFrame):
    def __init__(self, master, servico, comando_voltar):
        super().__init__(master)
        self.servico = servico

        # --- BOTÃO VOLTAR ---
        self.btn_voltar = ctk.CTkButton(
            self, 
            text="⬅ Voltar", 
            width=80, 
            height=32,
            fg_color="transparent", 
            border_width=1, 
            border_color="#4b5563",
            hover_color="#374151",
            command=comando_voltar
        )
        self.btn_voltar.place(x=20, y=15)

        # --- TÍTULO DA TELA ---
        self.lbl_titulo = ctk.CTkLabel(
            self, 
            text="⧖ Fila Virtual - Entrada", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.lbl_titulo.pack(pady=(15, 5))

        # LEGENDA DE PRIORIDADES
        self.lbl_legenda = ctk.CTkLabel(
            self,
            text="Ordem de Atendimento: ★ VIP  ➔  🏷 PASSE ANUAL  ➔  NORMAL",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#9ca3af"
        )
        self.lbl_legenda.pack(pady=(0, 10))

        # --- FORMULÁRIO DE ENTRADA ---
        self.frame_form = ctk.CTkFrame(self, corner_radius=12, border_width=1, border_color="#374151")
        self.frame_form.pack(pady=10, padx=20, anchor="center")

        # Campo CPF
        self.lbl_cpf = ctk.CTkLabel(self.frame_form, text="CPF do Visitante:", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_cpf.grid(row=0, column=0, sticky="w", padx=15, pady=(12, 2))
        self.entry_cpf = ctk.CTkEntry(self.frame_form, placeholder_text="00000000000", width=220)
        self.entry_cpf.grid(row=1, column=0, padx=15, pady=(0, 10))
        self.entry_cpf.bind("<KeyRelease>", self.limitar_cpf)

        # Campo Seleção de Atração
        self.lbl_atracao = ctk.CTkLabel(self.frame_form, text="Selecione a Atração:", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_atracao.grid(row=0, column=1, sticky="w", padx=15, pady=(12, 2))
        self.combo_atracao = ctk.CTkComboBox(
            self.frame_form, 
            values=["Nenhuma atração cadastrada"], 
            width=220, 
            command=self.atualizar_lista_fila
        )
        self.combo_atracao.grid(row=1, column=1, padx=15, pady=(0, 10))

        # Botão de Entrada na Fila
        self.btn_adicionar = ctk.CTkButton(
            self.frame_form, 
            text=" + Adicionar à Fila", 
            fg_color="#10b981", 
            hover_color="#059669",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=38,
            width=200,
            command=self.entrar_na_fila
        )
        self.btn_adicionar.grid(row=2, column=0, columnspan=2, pady=(15, 10))

        self.lbl_mensagem = ctk.CTkLabel(self.frame_form, text="", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_mensagem.grid(row=3, column=0, columnspan=2, pady=(0, 10))

        # --- VISUALIZAÇÃO DA FILA ---
        self.lbl_lista = ctk.CTkLabel(self, text="⧖ Fila Atual da Atração", font=ctk.CTkFont(size=16, weight="bold"))
        self.lbl_lista.pack(pady=(15, 5))

        self.frame_lista = ctk.CTkScrollableFrame(self, height=220, fg_color="transparent")
        self.frame_lista.pack(pady=5, padx=20, fill="both", expand=True)

        self.carregar_atracoes()

    def limitar_cpf(self, event):
        texto = self.entry_cpf.get()
        if len(texto) > 11:
            self.entry_cpf.delete(11, "end")

    def carregar_atracoes(self):
        atracoes = self.servico.listar_atracoes()
        if atracoes:
            nomes = [a.nome for a in atracoes]
            self.combo_atracao.configure(values=nomes)
            self.combo_atracao.set(nomes[0])
            self.atualizar_lista_fila()

    def entrar_na_fila(self):
        cpf = self.entry_cpf.get()
        nome_atracao = self.combo_atracao.get()

        if not cpf or nome_atracao == "Nenhuma atração cadastrada":
            self.lbl_mensagem.configure(text="⚠ Preencha o CPF e escolha uma atração válida!", text_color="#f87171")
            return

        cpf_limpo = "".join(filter(str.isdigit, cpf))
        
        if len(cpf_limpo) != 11:
            self.lbl_mensagem.configure(text="⚠ Erro: O CPF precisa ter exatos 11 números!", text_color="#f87171")
            return
            
        cpf_formatado = f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"

        msg = self.servico.adicionar_visitante_na_fila(cpf_formatado, nome_atracao)
        
        if "Erro" in msg:
            self.lbl_mensagem.configure(text=f"⚠ {msg}", text_color="#f87171")
        else:
            self.lbl_mensagem.configure(text=f"✓ {msg}", text_color="#34d399")
            self.entry_cpf.delete(0, 'end')
            self.atualizar_lista_fila()

    def atualizar_lista_fila(self, escolha=None):
        nome_atracao = self.combo_atracao.get()
        
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        if nome_atracao == "Nenhuma atração cadastrada":
            return

        atracoes = self.servico.listar_atracoes()
        for a in atracoes:
            if a.nome == nome_atracao:
                fila_atual = a.fila_virtual.listar_fila()
                
                if not fila_atual:
                    lbl_vazio = ctk.CTkLabel(
                        self.frame_lista, 
                        text="A fila está vazia no momento. Pode entrar!", 
                        font=ctk.CTkFont(size=14, slant="italic"), 
                        text_color="#9ca3af"
                    )
                    lbl_vazio.pack(pady=30)
                else:
                    for posicao, pessoa in enumerate(fila_atual, 1):
                        card = ctk.CTkFrame(self.frame_lista, corner_radius=10, border_width=1, border_color="#374151")
                        card.pack(pady=4, padx=5, fill="x")
                        
                        # Posição na Fila em Destaque
                        lbl_pos = ctk.CTkLabel(
                            card, 
                            text=f" {posicao}º ", 
                            font=ctk.CTkFont(size=14, weight="bold"), 
                            text_color="#38bdf8",
                            fg_color="#1e293b",
                            corner_radius=6,
                            width=35
                        )
                        lbl_pos.pack(side="left", padx=12, pady=8)
                        
                        nome_visitante = pessoa.nome
                        tipo_passe_visitante = str(pessoa.tipo_passe).upper()
                        
                        lbl_nome = ctk.CTkLabel(
                            card, 
                            text=nome_visitante, 
                            font=ctk.CTkFont(size=15, weight="bold"),
                            text_color="#e5e7eb"
                        )
                        lbl_nome.pack(side="left", padx=10, pady=8)
                        
                        # Badges de Prioridade
                        if "VIP" in tipo_passe_visitante:
                            lbl_passe = ctk.CTkLabel(
                                card, 
                                text=" ★ VIP ", 
                                font=ctk.CTkFont(size=12, weight="bold"), 
                                text_color="#fef08a", 
                                fg_color="#854d0e", 
                                corner_radius=6
                            )
                        elif "ANUAL" in tipo_passe_visitante:
                            lbl_passe = ctk.CTkLabel(
                                card, 
                                text=" 🏷 PASSE ANUAL ", 
                                font=ctk.CTkFont(size=12, weight="bold"), 
                                text_color="#bbf7d0", 
                                fg_color="#166534", 
                                corner_radius=6
                            )
                        else:
                            lbl_passe = ctk.CTkLabel(
                                card, 
                                text=" NORMAL ", 
                                font=ctk.CTkFont(size=12), 
                                text_color="#e5e7eb", 
                                fg_color="#374151", 
                                corner_radius=6
                            )
                        lbl_passe.pack(side="right", padx=15, pady=8)
                break