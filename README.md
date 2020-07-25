# 🤓 Ferramenta de busca 🔎📚 
Ferramenta de busca utilizando como base de dados o stackoverflow

## 1. Objetivo
* Capturar as perguntas mais frequentes sobre Python no [stackoverflow](https://stackoverflow.com/questions/)

* Armazenar para cada pergunta: link, breve descrição da pergunta, quantidade de votos e visualizações, pergunta completa, resposta com melhor avaliação

* Criar ferramenta de busca considerando como base a arquitetura:

![](https://github.com/sielerod/search_stackoverflow/blob/master/pictures/Arquitetura.PNG)

Para isto, será necessário:

* Web scrapping para captura de dados do stackoverflow


* Tratamento de dados 
   
   ![](https://github.com/sielerod/search_stackoverflow/blob/master/pictures/logica_texto.PNG)
      
* Indexação
    
    ![](https://github.com/sielerod/search_stackoverflow/blob/master/pictures/Ranqueamento.PNG)

* Criação de modelo

* Armazenamento e recuperação da informação

* Interface para consulta e recuperação de dados


## 2. Inspiração 🤔💭
Trabalho proposto pelo prof [Howard Roatti](https://github.com/hroatti) com base em suas [referências de estudo sobre NLP](https://github.com/hroatti/Python)

## 3. Como executar a ferramenta de busca

1) Necessário que bibliotecas / ferramentas abaixo tenham sido instaladas:

    Streamlit

    import numpy as np 

    import pandas as pd

    import requests 

    from requests.exceptions import HTTPError

    from bs4 import BeautifulSoup

    from time import sleep

    import json

    import re

    import string

    import unidecode

    import nltk

    nltk.download('punkt')

    nltk.download('stopwords')

    from nltk.stem import SnowballStemmer

    from nltk.tokenize import word_tokenize

    from nltk.tokenize import RegexpTokenizer

    from nltk.corpus import stopwords

    from operator import itemgetter


2) Baixe os arquivos abaixo e execute os .py

    stackoverflow_tags.csv

    read_stackoverflow.py
    
    search_stackoverflow.py

3) Execute o Streamlit

    ´streamlit run search_stackoverflow.py´

4) Realize as pesquisas utilizando a língua inglesa


## 4. Referências
Leitura de dados para web scraping:
 * [scraping stack overflow](https://medium.com/@nveenverma/web-scraping-tutorial-project-scraping-stack-overflow-e28bb139fc3b) by [nveenverma](https://github.com/nveenverma)

 * [Scraping Stack Overflow Using Python Tutorial | Beautiful Soup](https://www.youtube.com/watch?v=EolFGrohtzw) by [iampawan](https://gist.github.com/iampawan)

 * [Web Scrape with Python & case studies](https://www.analyticsvidhya.com/blog/2017/07/web-scraping-in-python-using-scrapy/)

 * [Tweepy for beginners](https://towardsdatascience.com/tweepy-for-beginners-24baf21f2c25)

Vetorização e criação de índice
 * [Vetorização com scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)
 * [Building a simple inverted index using NLTK](https://nlpforhackers.io/building-a-simple-inverted-index-using-nltk/)

Passo a passo na construção de uma engine de busca
* [NLP Search Engine](https://www.kaggle.com/amitkumarjaiswal/nlp-search-engine)
* [How to Build a Search Engine](https://medium.com/@deangelaneves/how-to-build-a-search-engine-from-scratch-in-python-part-1-96eb240f9ecb) by [Deangela Neves](https://github.com/deangelacgn) 
* [Writing a simple Inverted Index in Python](https://medium.com/@fro_g/writing-a-simple-inverted-index-in-python-3c8bcb52169a)

Front-end
* [How to write Web apps using simple Python for Data Scientists?](https://towardsdatascience.com/how-to-write-web-apps-using-simple-python-for-data-scientists-a227a1a01582)
* [Streamlit 101: An in-depth introduction](https://towardsdatascience.com/streamlit-101-an-in-depth-introduction-fc8aad9492f2)
* [Guia para criar flutter Search Bar](https://blog.usejournal.com/change-app-bar-in-flutter-with-animation-cfffb3413e8a) e [código no github](https://github.com/NishantDesai1306/flutter_search_bar_transition) by [NishantDesai1306](https://github.com/NishantDesai1306)

* [flutter Search Bar](https://github.com/rodolfoggp/search_app_bar) by [rodolfoggp](https://github.com/rodolfoggp)

* [How To Link Python Script (FILE) With Flutter](https://www.youtube.com/watch?v=LXB3gap6P8k&t=21s) by [cyclone-pk](https://github.com/cyclone-pk/pythonandflutter)


## 5. Melhorias

* Scraping para atualização da lista de tags disponíveis no stackoverflow de [stackexchange](https://data.stackexchange.com/stackoverflow/query/381621) 

* Armazenar resultado de pesquisas em arquivo local para recuperação, sem novo scraping caso já tenhamos as tags da pesquisa

* Correção de erros em consultas com poucos resultados. 

* Melhorar apresentação dos resultados
        Apresentação do título com clicable link

* Suportar pesquisas em português