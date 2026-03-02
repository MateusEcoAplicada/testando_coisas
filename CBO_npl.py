import fitz  # faça o pip install PyMuPDF
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import pandas as pd

def nuvem_palavras(texto, max_palavras=100):
    
    nuvem_palavras = WordCloud(width=800, height=500, max_font_size=110, max_words=max_palavras).generate(texto)
    plt.figure(figsize=(15, 10))
    plt.imshow(nuvem_palavras, interpolation='bilinear')
    plt.axis('off')
    plt.show()


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

def remover_entre_palavras(texto, palavra_inicio, palavra_fim):
    """Remove tudo que aparece entre palavra_inicio e palavra_fim (versão otimizada com regex)"""
    # Escapa caracteres especiais das palavras
    palavra_inicio_escaped = re.escape(palavra_inicio)
    palavra_fim_escaped = re.escape(palavra_fim)
    
    # Padrão: palavra_inicio + qualquer coisa + palavra_fim
    # DOTALL permite . capturar quebras de linha; non-greedy para capturar o primeiro palavra_fim
    padrao = palavra_inicio_escaped + r'.*?' + palavra_fim_escaped
    
    # Substitui mantendo apenas palavra_inicio + palavra_fim
    resultado = re.sub(padrao, palavra_inicio + palavra_fim, texto, flags=re.DOTALL)
    
    return resultado

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
caminho = r"C:/Users/MATEUS/Desktop/ITI/testando_coisas/livro1.pdf"
livro_string = pdf_para_string(caminho, pular_paginas=23)

# Remove tudo entre 'PARTICIPANTES DA DESCRIÇÃO' e 'CÓDIGO'
participantes = 'PARTICIPANTES DA DESCRIÇÃO'
cod = 'CÓDIGO'

livro_string = remover_entre_palavras(livro_string, participantes, cod)


# Agora 'livro_string' está sem o conteúdo entre as palavras especificadas
#print(livro_string[:100000]) # Imprime os primeiros 100000 caracteres

#print(livro_string[livro_string.find(participantes):livro_string.find(participantes) + 1000])  # Imprime os próximos 1000 caracteres após encontrar a palavra-chave

#Encontra valores entre 'DESCRIÇÃO SUMÁRIA' e 'FORMAÇÃO E EXPERIÊNCIA'
descricao_sumaria = 'DESCRIÇÃO SUMÁRIA'
formacao_experiencia = 'FORMAÇÃO E EXPERIÊNCIA'
condicoes_gerais = 'CONDIÇÕES GERAIS DE EXERCÍCIO'
titulo = 'TÍTULO'

# Extrai TODAS as ocorrências
titulos = buscar_todas_entre_palavras(livro_string, titulo, descricao_sumaria)
descricoes = buscar_todas_entre_palavras(livro_string, descricao_sumaria, formacao_experiencia)
formacoes = buscar_todas_entre_palavras(livro_string, formacao_experiencia, condicoes_gerais)

# Encontra o tamanho máximo para criar o dataframe
max_len = max(len(titulos), len(descricoes), len(formacoes))

# Completa as listas com None para manter o tamanho igual
titulos += [None] * (max_len - len(titulos))
descricoes += [None] * (max_len - len(descricoes))
formacoes += [None] * (max_len - len(formacoes))

# Criar dataframe com os dados
df = pd.DataFrame({
    'titulo': titulos,
    'descricao': descricoes,
    'formacao': formacoes
})

print(df)
print("\n" + "="*50)
print(f"Total de títulos encontrados: {len([x for x in titulos if x])}")
print(f"Total de descrições encontradas: {len([x for x in descricoes if x])}")
print(f"Total de formações encontradas: {len([x for x in formacoes if x])}")
print("="*50)
df.to_csv('dados_extraidos.csv', index=False)