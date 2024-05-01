from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

tentativas = 3

pg = Tk()

class Tabela():
    def limpar_tela(self):
        self.cod_entry.delete(0, END)
        self.produto_entry.delete(0, END)
        self.preco_entry.delete(0, END)
        self.promocao_entry.delete(0, END)
        self.estoque_entry.delete(0, END)

    def conectar_bd(self):
        self.conn = sqlite3.connect('petshop.db')
        self.cursor = self.conn.cursor()
        print('Banco de dados conectado')

    def desconectar_bd(self):
        self.conn.close();
        print('Banco de dados desconectado')

    def tabela(self):
        self.conectar_bd()
        self.cursor.execute("""
                    create table if not exists produtos(
                        cod integer primary key autoincrement,
                        produto varchar(30) not null, 
                        preco INTEGER(10),
                        promocao CHARVAR(10),
                        estoque INTEGER(10)
                    );        
                """)
        self.conn.commit();
        print('banco de dados criado')
        self.desconectar_bd()
    def variaveis(self):
        self.cod = self.cod_entry.get()
        self.produto = self.produto_entry.get()
        self.preco = self.preco_entry.get()
        self.promocao = self.promocao_entry.get()
        self.estoque = self.estoque_entry.get()

    def add_produto(self):
        self.variaveis()
        self.conectar_bd()
        self.cursor.execute('''insert into produtos(produto, preco, promocao, estoque)
       values(?, ?, ?, ?)''', (self.produto, self.preco, self.promocao, self.estoque))
        self.conn.commit()
        self.desconectar_bd()
        self.selecionar_lista()
        self.limpar_tela()

    def selecionar_lista(self):
        self.listaProdutos.delete(*self.listaProdutos.get_children())
        self.conectar_bd()
        lista = self.cursor.execute('''select cod, produto, preco, promocao, estoque from produtos
        order by cod asc;''')
        for i in lista:
            self.listaProdutos.insert('', END, values=i)
        self.desconectar_bd()

    def buscar_produto(self):
        self.conectar_bd()
        self.listaProdutos.delete(*self.listaProdutos.get_children())

        self.produto_entry.insert(END, '%')
        nome = self.produto_entry.get()
        self.cursor.execute(
            """ select cod, produto, preco, promocao, estoque from produtos 
        where produto like '%s' order by produto asc """ % nome)
        buscanome = self.cursor.fetchall()
        for i in buscanome:
            self.listaProdutos.insert("", END, values=i)
        self.limpar_tela()
        self.desconectar_bd()

    def doubleclick(self, event):
        self.limpar_tela()
        self.listaProdutos.selection()
        for n in self.listaProdutos.selection():
            c1, c2, c3, c4, c5 = self.listaProdutos.item(n, 'values')
            self.cod_entry.insert(END, c1)
            self.produto_entry.insert(END, c2)
            self.preco_entry.insert(END, c3)
            self.promocao_entry.insert(END, c4)
            self.estoque_entry.insert(END, c5)

    def deletar_produto(self):
        self.variaveis()
        self.conectar_bd()
        self.cursor.execute('''delete from produtos where cod = ? ''', (self.cod))
        self.conn.commit()
        self.desconectar_bd()
        self.limpar_tela()
        self.selecionar_lista()

    def alterar_produto(self):
        self.variaveis()
        self.conectar_bd()
        self.cursor.execute('''update produtos set produto = ?, preco = ?, promocao = ?, estoque = ? where cod = ?''',
                            (self.produto, self.preco, self.promocao,  self.estoque, self.cod))
        self.conn.commit()
        self.desconectar_bd()
        self.selecionar_lista()
        self.limpar_tela()

class App(Tabela):
    def __init__(self):
        self.pg = pg
        self.janela()
        self.login()
        pg.mainloop()

    def login_tentativas(self):
        global tentativas
        tentativas -= 1
        if tentativas == 0:
            self.pg.quit()
            messagebox.showerror('Senha incorreta', 'O programa será encerrado por segurança.')
        else:
            messagebox.showerror(f'Senha incorreta', f'Você tem mais {tentativas} tentivas para entrar.')

    def senha(self):
        if self.entrada_senha.get() == 'oxente.bixinhos@2023':
            self.banco()
            self.banco.deiconify()
            self.frames()
            self.widgets_frame1()
            self.tabela_frame2()
            self.tabela()
            self.selecionar_lista()
            self.pg.withdraw()

        else:
            self.login_tentativas()

    def janela(self):
        self.pg.geometry('1280x720')
        self.pg.resizable(FALSE, FALSE)
        self.pg.title('Oxente bixinhos')

    def login(self):
        self.icone = 'Eu.png'
        self.pg.iconbitmap(self.icone)
        self.image = tk.PhotoImage(file = 'login_background.png')
        self.label_image = tk.Label(image = self.image)
        self.label_image.pack()

        self.entrada_senha = Entry(self.pg, show = '*', width = 25)
        self.entrada_senha.place(x = 640, y = 400, anchor = CENTER, height = 25)

        self.botao_login = tk.Button(self.pg, text = 'Confirmar', font=('Oswald', 10), relief='flat', command = self.senha)
        self.botao_login.place(x = 640, y = 450, anchor = CENTER)

    def banco(self):
        self.banco = Toplevel(self.pg)
        self.banco.geometry('1280x720')
        self.banco.resizable(FALSE, FALSE)
        self.banco.title('Oxente bixinhos')
        self.icone = 'Eu.png'
        self.banco.iconbitmap(self.icone)
        self.image = tk.PhotoImage(file='app_background.png')
        self.label_image = tk.Label(self.banco, image=self.image)
        self.label_image.pack()

    def frames(self):
        self.frame1 = Frame(self.banco, bg='#E0E3EF',
                            highlightbackground='#ffde59', highlightthickness=6)
        self.frame1.place(relx=0.6, rely=0.1352, relwidth=0.35, relheight=0.81)

        self.frame2 = Frame(self.banco, bd=10, bg='#E0E3EF',
                            highlightbackground='#0cc0df', highlightthickness=6)
        self.frame2.place(relx=0.037, rely=0.1352, relwidth=0.56, relheight=0.81)

    def widgets_frame1(self):
        self.botao_adicionar = Button(self.frame1, text='Novo', bg='#ffde59', fg='black', font=('Oswald', 11, 'bold'),
                                      command=self.add_produto)
        self.botao_adicionar.place(relx=0.7, rely=0.12, relwidth=0.17, relheight=0.07)

        self.botao_apagar = Button(self.frame1, text='Apagar', bg='#ffde59', fg='black', font=('Oswald', 11, 'bold'),
                                   command=self.deletar_produto)
        self.botao_apagar.place(relx=0.7, rely=0.22, relwidth=0.17, relheight=0.07)

        self.botao_alterar = Button(self.frame1, text='Alterar', bg='#ffde59', fg='black', font=('Oswald', 11, 'bold'),
                                    command=self.alterar_produto)
        self.botao_alterar.place(relx=0.7, rely=0.32, relwidth=0.17, relheight=0.07)

        self.botao_buscar = Button(self.frame1, text='Buscar', bg='#ffde59', fg='black',font=('Oswald', 11, 'bold'),
                                   command=self.buscar_produto)
        self.botao_buscar.place(relx=0.7, rely=0.42, relwidth=0.17, relheight=0.07)

        self.botao_limpar = Button(self.frame1, text='Limpar', bg='#ffde59', fg='black', font=('Oswald', 11, 'bold'),
                                   command=self.limpar_tela)
        self.botao_limpar.place(relx=0.7, rely=0.52, relwidth=0.17, relheight=0.07)


        self.label_cod = Label(self.frame1, text='Código', bg='#E0E3EF', font=('Oswald', 11, 'bold'))
        self.label_cod.place(relx=0.13, rely=0.1)
        self.cod_entry = Entry(self.frame1, relief='groove')
        self.cod_entry.place(relx=0.13, rely=0.15, relwidth=0.4)

        self.label_produto = Label(self.frame1, text='Nome do produto', bg='#E0E3EF', font=('Oswald', 11, 'bold'))
        self.label_produto.place(relx=0.13, rely=0.2)
        self.produto_entry = Entry(self.frame1, relief='groove')
        self.produto_entry.place(relx=0.13, rely=0.25, relwidth=0.4)

        self.label_preco = Label(self.frame1, text='Preço', bg='#E0E3EF', font=('Oswald', 11, 'bold'))
        self.label_preco.place(relx=0.13, rely=0.3)
        self.preco_entry = Entry(self.frame1, relief='groove')
        self.preco_entry.place(relx=0.13, rely=0.35, relwidth=0.4)

        self.label_promocao = Label(self.frame1, text='Promoção', bg='#E0E3EF', font=('Oswald', 11, 'bold'))
        self.label_promocao.place(relx=0.13, rely=0.4)
        self.promocao_entry = Entry(self.frame1, relief='groove')
        self.promocao_entry.place(relx=0.13, rely=0.45, relwidth=0.4)

        self.label_estoque = Label(self.frame1, text='Estoque', bg='#E0E3EF', font=('Oswald', 11, 'bold'))
        self.label_estoque.place(relx=0.13, rely=0.5)
        self.estoque_entry = Entry(self.frame1, relief='groove')
        self.estoque_entry.place(relx=0.13, rely=0.55, relwidth=0.4)


    def tabela_frame2(self):

        self.listaProdutos = ttk.Treeview(self.frame2, height=3, column=("col1", "col2", "col3", "col4", "col5", "col6"))
        self.listaProdutos.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.listaProdutos.heading("#0", text="")
        self.listaProdutos.heading("#1", text="Código")
        self.listaProdutos.heading("#2", text="Produto")
        self.listaProdutos.heading("#3", text="Preço")
        self.listaProdutos.heading("#4", text="Promoção")
        self.listaProdutos.heading("#5", text="Estoque")
        self.listaProdutos.heading("#6", text="")

        self.listaProdutos.column("#0", width=1, anchor=CENTER)
        self.listaProdutos.column("#1", width=50, anchor=CENTER)
        self.listaProdutos.column("#2", width=150, anchor=CENTER)
        self.listaProdutos.column("#3", width=75, anchor=CENTER)
        self.listaProdutos.column("#4", width=75, anchor=CENTER)
        self.listaProdutos.column("#5", width=75, anchor=CENTER)
        self.listaProdutos.column("#6", width=1, anchor=CENTER)


        self.scroolLista = Scrollbar(self.frame2, orient='vertical')
        self.listaProdutos.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.03, relheight=0.85)
        self.listaProdutos.bind('<Double-1>', self.doubleclick)

App()