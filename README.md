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

## 3. Referências
Leitura de dados para web scraping:
 * [nveenverma](https://github.com/nveenverma) com base em seu tutorial: [scraping stack overflow](https://medium.com/@nveenverma/web-scraping-tutorial-project-scraping-stack-overflow-e28bb139fc3b)

 * [iampawan](https://gist.github.com/iampawan) com base no passo a passo disponibilizado no youtube: [Scraping Stack Overflow Using Python Tutorial | Beautiful Soup](https://www.youtube.com/watch?v=EolFGrohtzw)

 * [Web Scrape with Python & case studies](https://www.analyticsvidhya.com/blog/2017/07/web-scraping-in-python-using-scrapy/)

 * [Tweepy for beginners](https://towardsdatascience.com/tweepy-for-beginners-24baf21f2c25)

Vetorização e criação de índice
 * [Vetorização com scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)
 * [Building a simple inverted index using NLTK](https://nlpforhackers.io/building-a-simple-inverted-index-using-nltk/)

Passo a passo na construção de uma engine de busca
* [NLP Search Engine](https://www.kaggle.com/amitkumarjaiswal/nlp-search-engine)
* [Deangela Neves](https://github.com/deangelacgn) com base em seu tutorial: [How to Build a Search Engine](https://medium.com/@deangelaneves/how-to-build-a-search-engine-from-scratch-in-python-part-1-96eb240f9ecb) 
* [Writing a simple Inverted Index in Python](https://medium.com/@fro_g/writing-a-simple-inverted-index-in-python-3c8bcb52169a)

Front-end
* [cyclone-pk](https://github.com/cyclone-pk/pythonandflutter) com base em seu tutorial:[How To Link Python Script (FILE) With Flutter](https://www.youtube.com/watch?v=LXB3gap6P8k&t=21s)