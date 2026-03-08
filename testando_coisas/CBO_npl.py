import fitz  # faça o pip install PyMuPDF
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import pandas as pd


def pdf_para_string(caminho_pdf, pular_paginas=0):
    texto_completo = ""
    # Abre o documento
    doc = fitz.open(caminho_pdf)
    
    # Itera por todas as páginas, pulando as primeiras se necessário
    for i, pagina in enumerate(doc):
        if i < pular_paginas:
            continue
        # Extrai o texto da página
        texto_completo += pagina.get_text()
    
    return texto_completo


def buscar_entre_palavras(texto, palavra_inicio, palavra_fim):
    """Busca tudo que aparece entre palavra_inicio e palavra_fim"""
    # Escapa caracteres especiais das palavras  

    palavra_inicio_escaped = re.escape(palavra_inicio)
    palavra_fim_escaped = re.escape(palavra_fim)
    
    # Padrão: palavra_inicio + qualquer coisa + palavra_fim
    padrao = palavra_inicio_escaped + r'(.*?)' + palavra_fim_escaped
    
    # Busca usando regex
    resultado = re.search(padrao, texto, flags=re.DOTALL)
    
    if resultado:
        return resultado.group(1).strip()  # Retorna o conteúdo encontrado entre as palavras
    else:
        return None  # Retorna None se não encontrar

def buscar_todas_entre_palavras(texto, palavra_inicio, palavra_fim):
    """Busca TODAS as ocorrências que aparecem entre palavra_inicio e palavra_fim"""
    palavra_inicio_escaped = re.escape(palavra_inicio)
    palavra_fim_escaped = re.escape(palavra_fim)
    
    # Padrão: palavra_inicio + qualquer coisa + palavra_fim
    padrao = palavra_inicio_escaped + r'(.*?)' + palavra_fim_escaped
    
    # Busca todas as ocorrências usando regex
    resultados = re.findall(padrao, texto, flags=re.DOTALL)
    
    # Remove strings vazias e limpa espaços em branco
    resultados = [r.strip() for r in resultados if r.strip()]
    
    return resultados

# Uso
caminho = r"C:\Users\Mateus\Desktop\Faculdade\ITI\ITI_tratamento_dados\testando_coisas\livro1.pdf"
caminho2 = r"C:\Users\Mateus\Desktop\Faculdade\ITI\ITI_tratamento_dados\testando_coisas\livro2.pdf"

livro1_string = pdf_para_string(caminho, pular_paginas=23)
livro2_string = pdf_para_string(caminho2, pular_paginas=9 )  

livro_string = livro1_string  + livro2_string

#Encontra valores entre 'DESCRIÇÃO SUMÁRIA' e 'FORMAÇÃO E EXPERIÊNCIA'
descricao_sumaria = 'DESCRIÇÃO SUMÁRIA'
formacao_experiencia = 'FORMAÇÃO E EXPERIÊNCIA'
condicoes_gerais = 'CONDIÇÕES GERAIS DE EXERCÍCIO'
titulo = 'TÍTULO'

# Extrai TODAS as ocorrências
titulos = buscar_todas_entre_palavras(livro_string, titulo, descricao_sumaria)
descricoes = buscar_todas_entre_palavras(livro_string, descricao_sumaria, formacao_experiencia)

print(titulos[:5])  # Imprime os primeiros 5 títulos encontrados

max_len = max(len(titulos), len(descricoes))

# Completa as listas com None para manter o tamanho igual
titulos += [None] * (max_len - len(titulos))
descricoes += [None] * (max_len - len(descricoes))
# Criar dataframe com os dados
df = pd.DataFrame({
    'titulo': titulos,
    'descricao': descricoes,

})
'''
print(df)
print("\n" + "="*50)
print(f"Total de títulos encontrados: {len([x for x in titulos if x])}")
print(f"Total de descrições encontradas: {len([x for x in descricoes if x])}")
print("="*50)
'''
df.to_csv('dados_extraidos_ambos_livros.csv', index=False)