import tweepy
import os
import time
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Carregar as credenciais de autenticação
API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# Verifique se as variáveis foram carregadas corretamente
if not all([API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, BEARER_TOKEN]):
    raise ValueError("Uma ou mais credenciais de autenticação não foram encontradas no arquivo .env")

# Configurar a autenticação OAuth 1.0a
auth = tweepy.OAuth1UserHandler(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# Criar o cliente com autenticação OAuth 1.0a
api = tweepy.API(auth)

# Criar o cliente para pesquisa recente de tweets com Bearer Token
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Função para buscar tweets relacionados ao tema
def buscar_tweets(query):
    try:
        # Usar a função search_recent_tweets do cliente correto
        tweets = client.search_recent_tweets(query=query, tweet_fields=['created_at', 'public_metrics'], max_results=1)
        return tweets.data if tweets.data else []
    except tweepy.TooManyRequests as e:
        print("Limite de requisições atingido. Aguardando o tempo de reset...")
        reset_time = int(e.response.headers['x-rate-limit-reset'])  # Obter o tempo de reset
        current_time = time.time()
        wait_time = reset_time - current_time + 5  # Aguardar até o reset, com 5 segundos de folga
        print(f"Aguardando {wait_time} segundos...")
        time.sleep(wait_time)  # Esperar até o reset
        return buscar_tweets(query)  # Tentar novamente após a pausa
    except tweepy.TweepyException as e:
        print(f"Erro ao buscar tweets: {e}")
        return []

# Função para realizar a busca e mostrar o resultado
def realizar_busca():
    query = 'cryptocurrency'  # Palavra-chave para buscar
    tweets = buscar_tweets(query)
    
    if tweets:
        tweet = tweets[0]  # Pega apenas o primeiro tweet encontrado
        print(f"Tweet encontrado de @{tweet.author_id}: {tweet.text}")
        print(f"Visualizações: {tweet.public_metrics['impression_count']}")
    else:
        print("Nenhum tweet encontrado.")

# Realizar a busca e exibir o resultado
realizar_busca()