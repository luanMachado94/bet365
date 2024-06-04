from openai import OpenAI

client = OpenAI()

def get_corner_kick_analysis(match_data):
    prompt = f"""
    Você é um analista de apostas esportivas especializado em fornecer previsões precisas para eventos de futebol. Sua tarefa é analisar os confrontos e fornecer um palpite de escanteios baseado em estatísticas atualizadas, desempenho histórico dos times, condições climáticas, desfalques nas equipes e opiniões de especialistas com foco em escanteios. Para o confronto entre as equipes {match_data}, forneça as seguintes informações em forma de lista tópicos:

    1. Média de escanteios do confronto
    2. Média de finalizações do confronto
    3. Média de chutes a gol do confronto
    4. Total de escanteios esperados

    Certifique-se de que todas as informações são extraídas do site SofaScore e são apresentadas em forma de lista tópicos conforme o formato especificado.
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um analista de apostas esportivas."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )

    return response.choices[0].message.content.strip()

# Exemplo de dados do confronto
match_data = "Corinthias vs Botafogo"

analysis = get_corner_kick_analysis(match_data)
print(analysis)
