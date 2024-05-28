import re
from collections import defaultdict
from seleniumbase import Driver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from a_selenium2df import get_df
from PrettyColorPrinter import add_printer
import numpy as np


add_printer(1)


def obter_dataframe(query="*"):
    df = pd.DataFrame()
    while df.empty:
        df = get_df(
            driver,
            By,
            WebDriverWait,
            expected_conditions,
            queryselector=query,
            with_methods=True,
        )
    return df

driver = Driver(uc=True)
driver.get("https://br.betano.com/sport/futebol/brasil/brasileirao-serie-a/10016/")
df = obter_dataframe(query='div')


df_filtered  = df.loc[df.aa_className.str.contains('vue-recycle-scroller__item-view', na=False)]

def transformar_texto(texto):
    partes = texto.split('\n')
    data = partes[0].replace("\\", "")  # Remover a barra invertida
    data = data.replace("/", "-")  # Substituir a barra por um traço para evitar problemas de escape no JSON
    return {
        'data': data,
        'hora': partes[1],
        'equipes': f"{partes[2]} x {partes[3]}",
        'local': partes[4] if partes[4] != '1' else "Em local neutro",
        'Odd N1': partes[5],
        'Odd NX': partes[6],
        'Odd N2': partes[7]
    }


if not df_filtered.empty:
    # Extraia e transforme o texto
    texto_transformado = df_filtered['aa_innerText'].apply(transformar_texto)
    
    # Converta para um DataFrame
    texto_df = pd.DataFrame(texto_transformado.tolist())
    
    # Salve o DataFrame resultante em um arquivo JSON
    texto_df.to_json('Odds.json', orient='records', indent=4, force_ascii=False)
    print("Dados salvos em 'Odds.json'")
else:
    print("Nenhuma linha encontrada com a classe especificada")