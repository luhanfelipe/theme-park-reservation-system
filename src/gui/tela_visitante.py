import customtkinter as ctk

class TelaVisitante(ctk.CTkFrame):
    def __init__(self, master, servico, comando_voltar):
        super().__init__(master)
        
        # O "master" é o frame_principal lá do main.py
        # O "servico" é o ParqueService que vai salvar os dados nas Listas Encadeadas
        self.servico = servico 

        self.btn_voltar = ctk.CTkButton(self, text="⬅ Voltar", width=70, fg_color="transparent", border_width=1, command=comando_voltar)
        self.btn_voltar.place(x=15, y=15)

        # --- TÍTULO DA TELA ---
        self.lbl_titulo = ctk.CTkLabel(self, text="Cadastro de Visitantes", font=("Arial", 20, "bold"))
        self.lbl_titulo.pack(pady=10)


        # --- REQUISITO: FORMULÁRIO (CREATE) ---
        self.frame_form = ctk.CTkFrame(self)
        self.frame_form.pack(pady=20, padx=20, anchor="center")

        ### Campos de entrada para os dados do visitante
        self.entry_nome = ctk.CTkEntry(self.frame_form, placeholder_text="Nome do Visitante", width=200)
        self.entry_nome.grid(row=0, column=0, padx=15, pady=10)

        self.entry_idade = ctk.CTkEntry(self.frame_form, placeholder_text="Idade", width=200)
        self.entry_idade.grid(row=0, column=1, padx=15, pady=10)

        self.entry_cpf = ctk.CTkEntry(self.frame_form, placeholder_text="CPF (só números)", width=200)
        self.entry_cpf.grid(row=1, column=0, padx=15, pady=10)
        self.entry_cpf.bind("<KeyRelease>", self.limitar_cpf)

        self.entry_data = ctk.CTkEntry(self.frame_form, placeholder_text="Data de Nasc. (ddmmaaaa)", width=200)
        self.entry_data.grid(row=1, column=1, padx=15, pady=10)
        self.entry_data.bind("<KeyRelease>", self.limitar_data)

        self.entry_email = ctk.CTkEntry(self.frame_form, placeholder_text="E-mail", width=200)
        self.entry_email.grid(row=2, column=0, padx=15, pady=10)

        self.combo_passe = ctk.CTkComboBox(self.frame_form, values=["Normal", "VIP", "Passe Anual"], width=200)
        self.combo_passe.grid(row=2, column=1, padx=15, pady=10)
        self.combo_passe.set("Normal")

        self.btn_salvar = ctk.CTkButton(self.frame_form, text="Salvar Visitante", command=self.salvar_visitante)
        self.btn_salvar.grid(row=3, column=0, columnspan=2, pady=20)

        self.lbl_mensagem = ctk.CTkLabel(self.frame_form, text="", text_color="green")
        self.lbl_mensagem.grid(row=4, column=0, columnspan=2, pady=(0, 10))

        # --- LISTAGEM DE VISITANTES
        self.lbl_lista = ctk.CTkLabel(self, text="Visitantes Cadastrados:", font=("Arial", 16, "bold"))
        self.lbl_lista.pack(pady=(20, 0))

        self.frame_lista = ctk.CTkScrollableFrame(self, height=250, fg_color="transparent")
        self.frame_lista.pack(pady=10, padx=20, fill="both", expand=True)

        self.atualizar_lista()

        # Ao abrir a tela, já carrega a lista
        self.atualizar_lista()

    def limitar_cpf(self, event):
        texto = self.entry_cpf.get()
        if len(texto) > 11:
            self.entry_cpf.delete(11, "end") # Apaga tudo do caractere 11 até o final

    def limitar_data(self, event):
        texto = self.entry_data.get()
        if len(texto) > 8:
            self.entry_data.delete(8, "end") # Apaga tudo do caractere 8 até o final

    # --- FLUXO ESPERADO: GUI -> PARQUE_SERVICE ---
    def salvar_visitante(self):
        # 1. Pegar os valores digitados nas caixas de texto
        nome = self.entry_nome.get()
        idade = self.entry_idade.get()
        cpf = self.entry_cpf.get()
        data = self.entry_data.get()
        email = self.entry_email.get()
        passe = self.combo_passe.get()

        # Validação básica
        if not nome or not idade or not cpf:
            self.lbl_mensagem.configure(text="Preencha pelo menos Nome, Idade e CPF!", text_color="red")
            return

        # Deixa só os números pra garantir que não vai bugar
        cpf_limpo = "".join(filter(str.isdigit, cpf))
        data_limpa = "".join(filter(str.isdigit, data))

        # Se digitou os 11 números certinhos, formata o CPF
        if len(cpf_limpo) == 11:
            cpf = f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
        
        # Se digitou os 8 números certinhos (ddmmaaaa), formata a Data
        if len(data_limpa) == 8:
            data = f"{data_limpa[:2]}/{data_limpa[2:4]}/{data_limpa[4:]}"

        # 2. Enviar para o Serviço
        msg = self.servico.cadastrar_visitante(nome, idade, cpf, data, email, passe)
        self.lbl_mensagem.configure(text=msg, text_color="green")

        # 3. Limpar os campos para o próximo cadastro
        self.entry_nome.delete(0, 'end')
        self.entry_idade.delete(0, 'end')
        self.entry_cpf.delete(0, 'end')
        self.entry_data.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.combo_passe.set("Normal")

        # 4. Atualizar a tela de visualização
        self.atualizar_lista()

    def atualizar_lista(self):
            # Limpa os cartões antigos da tela
            for widget in self.frame_lista.winfo_children():
                widget.destroy()

            visitantes = self.servico.listar_visitantes()

            if not visitantes:
                lbl_vazio = ctk.CTkLabel(self.frame_lista, text="Nenhum visitante cadastrado ainda.", font=("Arial", 16, "italic"), text_color="gray")
                lbl_vazio.pack(pady=30)
                return

            for v in visitantes:
                # Cria o fundo do cartão
                card = ctk.CTkFrame(self.frame_lista, corner_radius=10, border_width=1, border_color="#3a3a3a")
                card.pack(pady=5, padx=10, fill="x")

                # --- LINHA SUPERIOR (Nome e Etiqueta do Passe) ---
                frame_topo = ctk.CTkFrame(card, fg_color="transparent")
                frame_topo.pack(fill="x", padx=15, pady=(10, 0)) # Margem em cima

                lbl_nome = ctk.CTkLabel(frame_topo, text=v.nome, font=("Arial", 16, "bold"), text_color="#1e90ff")
                lbl_nome.pack(side="left")

                tipo_passe = str(v.tipo_passe).upper()
                if "VIP" in tipo_passe:
                    lbl_passe = ctk.CTkLabel(frame_topo, text="★ VIP", font=("Arial", 14, "bold"), text_color="#ffd700")
                elif "ANUAL" in tipo_passe:
                    lbl_passe = ctk.CTkLabel(frame_topo, text="🎟️ ANUAL", font=("Arial", 14, "bold"), text_color="#32cd32")
                else:
                    lbl_passe = ctk.CTkLabel(frame_topo, text="Normal", font=("Arial", 12), text_color="gray")
                lbl_passe.pack(side="right")

                # --- LINHA INFERIOR (Todos os dados completos do formulário) ---
                frame_base = ctk.CTkFrame(card, fg_color="transparent")
                frame_base.pack(fill="x", padx=15, pady=(5, 10)) # Margem em baixo
                
                # Junta todas as informações numa string formatada com separadores
                info_texto = f"CPF: {v.cpf}  |  Idade: {v.idade} anos  |  Nasc: {v.data_nascimento}  |  E-mail: {v.email}"
                
                lbl_info = ctk.CTkLabel(frame_base, text=info_texto, font=("Arial", 13), text_color="#a0a0a0")
                lbl_info.pack(side="left")