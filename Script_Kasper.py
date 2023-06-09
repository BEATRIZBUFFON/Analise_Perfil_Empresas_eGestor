#Importando bibliotecas
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Tratamento de dados:
df = pd.read_excel('parceirosAlan2.xlsx')
df.drop(index=df[df['data_situacao_cadastral'] == '0'].index, inplace=True)
df['data_inicio_atividades'] = pd.to_datetime(df['data_inicio_atividades'], format='%Y%m%d')
df['data_situacao_cadastral'] = pd.to_datetime(df['data_situacao_cadastral'], format='%Y%m%d')

#Distribuição geográfica das empresas por ESTADO e CIDADE
distribuicao_geog = df[['descricao', 'uf']].value_counts()
distribuicao_geog = distribuicao_geog.reset_index()
distribuicao_geog = distribuicao_geog.rename(columns={0: 'quantidade'})
distribuicao_geog.to_excel('Distribuicao_Geografica.xlsx', index=False)

#Quantidade do início das atividades das empresas por ano
inicio_ativ = df['data_situacao_cadastral'].dt.year.value_counts().sort_index()
inicio_ativ = inicio_ativ.reset_index()
inicio_ativ.columns = ['ano', 'quantidade']
inicio_ativ.to_excel('Inicio_Atividades.xlsx', index=False)

df1 = df[['cnae_fiscal', 'cnpj']]

#CNAE Fiscal com maior aparição ​
cnae_fiscal = pd.DataFrame({
   'cnae_fiscal': [6920601, 8550302, 8211300, 4751201, 6319400, 4781400, 1822999,
           7020400, 8599604, 6190699, 8291100, 6204000, 8219999, 8219901,
           1091102, 6920602, 1813001, 9511800, 6201501, 5813100, 1340501,
           7490104, 4789007, 4712100, 7112000, 4619200, 6311900, 5819100,
           6209100, 8599605],
    'descricao':['Atividades de contabilidade',
                 'Ensino de idiomas',
                 'Serviços combinados de escritório e apoio administrativo',
                 'Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados',
                 'Portais, provedores de conteúdo e outros serviços de informação na internet',
                 'Comércio varejista de artigos do vestuário e acessórios',
                 'Reprodução de gravações', 
                 'Atividades de consultoria em gestão empresarial, exceto consultoria técnica específica', 
                 'Treinamento em informática',
                 'Outras atividades de teleatendimento',
                 'Atividades de cobranças e informações cadastrais',
                 'Consultoria em tecnologia da informação', 
                 'Preparação de documentos e serviços especializados de apoio administrativo não especificados anteriormente',
                 'Fotocópias',
                 'Fabricação de sorvetes e outros gelados comestíveis',
                 'Atividades auxiliares da justiça, exceto cartórios',
                 'Impressão de material para uso publicitário',
                 'Reparação e manutenção de equipamentos de comunicação',
                 'Desenvolvimento de programas de computador sob encomenda',
                 'Edição de livros',
                 'Fabricação de tecidos de algodão',
                 'Atividades de intermediação e agenciamento de serviços e negócios em geral, exceto imobiliários',
                 'Comércio varejista de produtos alimentícios em geral ou especializado em produtos alimentícios não especificados anteriormente',
                 'Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns',
                 'Serviços de engenharia',
                 'Representantes comerciais e agentes do comércio de combustíveis, minerais, produtos siderúrgicos e químicos',
                 'Tratamento de dados, provedores de serviços de aplicação e serviços de hospedagem na internet',
                 'Edição de revistas',
                 'Suporte técnico, manutenção e outros serviços em tecnologia da informação', 
                 'Treinamento em desenvolvimento profissional e gerencial']})

df_teste = pd.merge(cnae_fiscal, df1, on='cnae_fiscal')
df_teste = df_teste['descricao'].value_counts()
df_teste = df_teste[df_teste >= 7]
df_teste.to_excel('Cnae_fiscal0.xlsx', index=False)

#CNAE Fiscal secundária com maior aparição ​
cnae_fiscal_sec = df[['cnae_fiscal_secundaria', 'cnpj']]
cnae_fiscal_sec = cnae_fiscal_sec.copy()
cnae_fiscal_sec.loc[:, 'cnae_fiscal_secundaria_list'] = cnae_fiscal_sec['cnae_fiscal_secundaria'].str.split('[,.]')
cnae_fiscal_sec = cnae_fiscal_sec.explode('cnae_fiscal_secundaria_list')
cnae_fiscal_sec.drop('cnae_fiscal_secundaria', axis=1, inplace=True)
cnae_fiscal_sec.rename(columns={'cnae_fiscal_secundaria_list': 'cnae_fiscal_secundaria'}, inplace=True)
cnae_fiscal_sec = cnae_fiscal_sec[['cnpj', 'cnae_fiscal_secundaria']]
cnae_fiscal_sec.dropna(subset=['cnae_fiscal_secundaria'], inplace=True)
cnae_fiscal_sec.to_excel('teste2023.xlsx', index=False)

teste1 = pd.read_excel('teste000.xlsx')
import re
def limpar_codigo(codigo):
    return re.sub(r'[-/]', '', codigo)
teste1['codigo'] = teste1['codigo'].astype(str).apply(limpar_codigo)
print(teste1)
teste_pronto = pd.merge(cnae_fiscal_sec, teste1, left_on='cnae_fiscal_secundaria', right_on='codigo', how='left')
teste_pronto.to_excel('tete0.xlsx', index=False)
teste_pronto = teste_pronto['servico'].value_counts()
teste_pronto = teste_pronto[teste_pronto >= 10]
teste_pronto = teste_pronto.reset_index()
teste_pronto.columns = ['descricao', 'quantidade']
teste_pronto.to_excel('CNAE_Fiscal_Secundária.xlsx', index=False)
