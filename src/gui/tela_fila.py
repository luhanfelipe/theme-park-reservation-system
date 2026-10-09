import customtkinter as ctk

class TelaFila(ctk.CTkFrame):
    def __init__(self, master, servico, comando_voltar):
        super().__init__(master)
        self.servico = servico

        self.btn_voltar = ctk.CTkButton(self, text="⬅ Voltar", width=70, fg_color="transparent", border_width=1, command=comando_voltar)
        self.btn_voltar.place(x=15, y=15)

        # --- TÍTULO ---
        self.lbl_titulo = ctk.CTkLabel(self, text="Fila Virtual - Entrada", font=("Arial", 20, "bold"))
        self.lbl_titulo.pack(pady=10)

        # --- FORMULÁRIO ---
        self.frame_form = ctk.CTkFrame(self)
        self.frame_form.pack(pady=20, padx=20, anchor="center")

        self.entry_cpf = ctk.CTkEntry(self.frame_form, placeholder_text="CPF do Visitante", width=200)
        self.entry_cpf.grid(row=0, column=0, padx=15, pady=10)
        self.entry_cpf.bind("<KeyRelease>", self.limitar_cpf)

        # NOVIDADE: Adicionamos o "command=self.atualizar_lista_fila" para atualizar a tela se você mudar a atração!
        self.combo_atracao = ctk.CTkComboBox(self.frame_form, values=["Nenhuma atração cadastrada"], width=220, command=self.atualizar_lista_fila)
        self.combo_atracao.grid(row=0, column=1, padx=15, pady=10)

        self.btn_adicionar = ctk.CTkButton(self.frame_form, text="Adicionar à Fila", command=self.entrar_na_fila)
        self.btn_adicionar.grid(row=1, column=0, columnspan=2, pady=20)

        self.lbl_mensagem = ctk.CTkLabel(self.frame_form, text="", text_color="green")
        self.lbl_mensagem.grid(row=2, column=0, columnspan=2)

        # --- NOVIDADE: VISUALIZAÇÃO DA FILA (O QUE FALTAVA!) ---
        self.lbl_lista = ctk.CTkLabel(self, text="Fila Atual da Atração:", font=("Arial", 16, "bold"))
        self.lbl_lista.pack(pady=(20, 0))

        self.frame_lista = ctk.CTkScrollableFrame(self, height=250, fg_color="transparent")
        self.frame_lista.pack(pady=10, padx=20, fill="both", expand=True)

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
            self.atualizar_lista_fila() # NOVIDADE: Já mostra a fila da primeira atração ao abrir a tela

    def entrar_na_fila(self):
        cpf = self.entry_cpf.get()
        nome_atracao = self.combo_atracao.get()

        if not cpf or nome_atracao == "Nenhuma atração cadastrada":
            self.lbl_mensagem.configure(text="Preencha o CPF e escolha uma atração válida!", text_color="red")
            return

        cpf_limpo = "".join(filter(str.isdigit, cpf))
        
        if len(cpf_limpo) != 11:
            self.lbl_mensagem.configure(text="Erro: O CPF precisa ter exatos 11 números!", text_color="red")
            return
            
        cpf_formatado = f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"

        msg = self.servico.adicionar_visitante_na_fila(cpf_formatado, nome_atracao)
        
        if "Erro" in msg:
            self.lbl_mensagem.configure(text=msg, text_color="red")
        else:
            self.lbl_mensagem.configure(text=msg, text_color="green")
            self.entry_cpf.delete(0, 'end')
            self.atualizar_lista_fila() # NOVIDADE: Atualiza a listagem assim que a pessoa entra com sucesso!

    def atualizar_lista_fila(self, escolha=None):
        nome_atracao = self.combo_atracao.get()
        
        # Limpa os cartões antigos
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        if nome_atracao == "Nenhuma atração cadastrada":
            return

        atracoes = self.servico.listar_atracoes()
        for a in atracoes:
            if a.nome == nome_atracao:
                fila_atual = a.fila_virtual.listar_fila()
                
                if not fila_atual:
                    lbl_vazio = ctk.CTkLabel(self.frame_lista, text="A fila está vazia no momento. Pode entrar!", font=("Arial", 16, "italic"), text_color="gray")
                    lbl_vazio.pack(pady=30)
                else:
                    for posicao, pessoa in enumerate(fila_atual, 1):
                        card = ctk.CTkFrame(self.frame_lista, corner_radius=10, border_width=1, border_color="#3a3a3a")
                        card.pack(pady=5, padx=10, fill="x")
                        
                        lbl_pos = ctk.CTkLabel(card, text=f"{posicao}º", font=("Arial", 18, "bold"), text_color="#1f6aa5", width=40)
                        lbl_pos.pack(side="left", padx=15, pady=10)
                        
                        # --- A MELHORIA: Lê os dados DIRETOS do objeto! ---
                        nome_visitante = pessoa.nome
                        tipo_passe_visitante = str(pessoa.tipo_passe).upper()
                        
                        lbl_nome = ctk.CTkLabel(card, text=nome_visitante, font=("Arial", 16))
                        lbl_nome.pack(side="left", padx=10, pady=10)
                        
                        # Avalia o passe diretamente da variável
                        if "VIP" in tipo_passe_visitante:
                            lbl_vip = ctk.CTkLabel(card, text="★ VIP", font=("Arial", 14, "bold"), text_color="#ffd700")
                            lbl_vip.pack(side="right", padx=20, pady=10)
                        elif "ANUAL" in tipo_passe_visitante:
                            lbl_anual = ctk.CTkLabel(card, text="🎟️ ANUAL", font=("Arial", 14, "bold"), text_color="#32cd32")
                            lbl_anual.pack(side="right", padx=20, pady=10)
                        else:
                            lbl_normal = ctk.CTkLabel(card, text="Normal", font=("Arial", 12), text_color="gray")
                            lbl_normal.pack(side="right", padx=20, pady=10)
                break