from tkinter import *
from tkinter import Tk, ttk, filedialog 
from PIL import ImageTk, Image, ImageEnhance
import cv2

# Cores
cor1 = "#feffff"
cor2 = "#4fa882"
cor3 = "#38576b"
cor4 = "#403d3d"
cor5 = "#e06636"
cor6 = "#038cfc"

# Configuração da janela
janela = Tk()
janela.title("Conversor de Esboço e Lápis")
janela.geometry('450x550')
janela.configure(bg=cor1)
janela.resizable(width=False, height=False)

# Variáveis globais
imagem_original = None
imagem_convertida = None
caminho_imagem = ""  

# Escolher imagem
def escolher_imagem():
    global imagem_original, caminho_imagem

    caminho_imagem = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
    
    if caminho_imagem:
        imagem_original = Image.open(caminho_imagem)
        imagem_preview = imagem_original.resize((200, 200)) 
        imagem_preview = ImageTk.PhotoImage(imagem_preview)

        # Atualiza o Label
        l_preview_original.configure(image=imagem_preview)
        l_preview_original.image = imagem_preview

# Converter imagem
def converter_imagem(event=None):
    global imagem_original, imagem_convertida, caminho_imagem

    if imagem_original is None or not caminho_imagem:
        return

    r = s_intensidade.get()
    brilho = 1 + (s_brilho.get() - 100) / 100.0
    contraste = 1 + (s_constraste.get() - 100) / 100.0

    # Carregar a imagem corretamente no OpenCV
    imagem_cv = cv2.imread(caminho_imagem)  
    imagem_cv = cv2.cvtColor(imagem_cv, cv2.COLOR_BGR2GRAY)

    # Aplicar efeito de esboço
    blur = cv2.GaussianBlur(imagem_cv, (21, 21), 0)
    sketch = cv2.divide(imagem_cv, blur, scale=r)

    # Converter para PIL
    pil_sketch = Image.fromarray(sketch)

    # Aplicar brilho e contraste
    enhancer_brilho = ImageEnhance.Brightness(pil_sketch)
    pil_sketch = enhancer_brilho.enhance(brilho)

    enhancer_contraste = ImageEnhance.Contrast(pil_sketch)
    pil_sketch = enhancer_contraste.enhance(contraste)

    # Atualiza imagem convertida
    imagem_convertida = pil_sketch
    imagem_preview = imagem_convertida.resize((200, 200))
    imagem_preview = ImageTk.PhotoImage(imagem_preview)

    # Atualiza o Label
    l_preview_convertida.configure(image=imagem_preview)
    l_preview_convertida.image = imagem_preview

# Salvar imagem
def salvar_imagem():
    if imagem_convertida:
        caminho = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("Todos os arquivos", "*.*")])
        if caminho:
            imagem_convertida.save(caminho)

# Layout da interface
frame_top = Frame(janela, width=450, height=50, bg=cor1)
frame_top.pack(pady=5)

frame_preview = Frame(janela, width=450, height=220, bg=cor1)
frame_preview.pack()

frame_controls = Frame(janela, width=450, height=226, bg=cor1)
frame_controls.pack()

# Título
Label(frame_top, text="Conversor para Desenho a Lápis", font=("Arial", 16, "bold"), bg=cor1, fg=cor4).pack()

# Labels de pré-visualização (com largura e altura definidas)
l_preview_original = Label(frame_preview, text="Prévia Original", font=("Arial", 12), bg=cor1, fg=cor3, width=200, height=200)
l_preview_original.place(x=30, y=10)

l_preview_convertida = Label(frame_preview, text="Prévia Convertida", font=("Arial", 12), bg=cor1, fg=cor3, width=200, height=200)
l_preview_convertida.place(x=240, y=10)

# Controles
ttk.Label(frame_controls, text="Intensidade", background=cor1).place(x=10, y=10)
s_intensidade = Scale(frame_controls, command=converter_imagem, from_=50, to=300, orient=HORIZONTAL, length=200, bg=cor1, fg=cor4)
s_intensidade.set(120)
s_intensidade.place(x=10, y=30)

ttk.Label(frame_controls, text="Brilho", background=cor1).place(x=10, y=80)
s_brilho = Scale(frame_controls, command=converter_imagem, from_=50, to=200, orient=HORIZONTAL, length=200, bg=cor1, fg=cor4)
s_brilho.set(100)
s_brilho.place(x=10, y=100)

ttk.Label(frame_controls, text="Contraste", background=cor1).place(x=10, y=150)
s_constraste = Scale(frame_controls, command=converter_imagem, from_=50, to=200, orient=HORIZONTAL, length=200, bg=cor1, fg=cor4)
s_constraste.set(100)
s_constraste.place(x=10, y=170)

# Botões
b_escolher = Button(janela, command=escolher_imagem, text="Escolher imagem", bg=cor6, fg=cor1, font=("Arial", 10), width=15)
b_escolher.place(x=20, y=500)

b_converter = Button(janela, command=converter_imagem, text="Converter imagem", bg=cor2, fg=cor1, font=("Arial", 10), width=15)
b_converter.place(x=160, y=500)

b_salvar = Button(janela, command=salvar_imagem, text="Salvar imagem", bg=cor5, fg=cor1, font=("Arial", 10), width=15)
b_salvar.place(x=300, y=500)

# Rodar o programa
janela.mainloop()
