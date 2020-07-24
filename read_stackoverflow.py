import numpy as np 
import pandas as pd
import requests # Coleta de conteúdo em Webpage
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup as bs # Scraping webpages
from time import sleep
import json
import re #biblioteca para trabalhar com regular expressions - regex
import string
import unidecode
import nltk
#nltk.download('punkt')
#nltk.download('stopwords')
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from operator import itemgetter

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>|&[.*?]')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

#remove todas as pontuações e retorna lista de palavras
def clean_text (text):
    text = text.translate(str.maketrans('', '', string.punctuation)) #remove todas as pontuações: '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    text = text.replace('\n',' ').strip() 
    text = text.lower()
    text = unidecode.unidecode(text)
    return text

def read_stackoverflow_overview(tags=[], tab='Frequent', pages=5):
  link = 'https://stackoverflow.com/questions'
  selector='question-summary'
  
  if tags:
    tags_link = '/tagged/'
    pre=''
    for t in tags:
      tags_link += str(pre) + t
      pre = '+or+' 
    link += tags_link

  link += '?tab='+tab

  questions_text = ''
  soup_selection = []
  for page in range(1,pages+1):
    page_link = '&page='+str(page)

    try:
      request = requests.get(link+page_link)
      request.raise_for_status()
      try:
        soup = bs(request.text, 'html.parser')
        soup_selection.append(soup.select('.'+selector))
      except: print ("Could not transform to soup object by selecting ",selector)
    except HTTPError:
      print ("Could not download page ", page)

    sleep(0.05)

  return soup_selection

def questions_overview(questions_overview_raw):
  questions_overview = { 'questions':[]}

  for soups in questions_overview_raw:
    for soup in soups:
      title = soup.select_one('.question-hyperlink').getText()
      link = 'https://stackoverflow.com'+soup.select_one('.question-hyperlink').get('href')
      summary = soup.select_one('.excerpt').getText()
      vote_count =  soup.select_one('.vote-count-post').getText()
      answers_count = soup.select_one('.answered-accepted')
      answers_count = re.sub('\D','',answers_count.getText('')) if answers_count else '0'
      views =  re.sub('views','',soup.select_one('.views').attrs['title'])
      views = re.sub(',','',views)
      tags = []
      for tag in soup.select('.post-tag'): tags.append(tag.getText())

      questions_overview['questions'].append({
          'title': title,
          'link': link,
          'summary': summary,
          'vote_count': int(vote_count),
          'answers_count': int(answers_count),
          'views': int(views),
          'tags': tags,
          'full_question': '',
          'best_answer': '',
      })

  questions_df = pd.DataFrame(questions_overview['questions'])
  
  return questions_df

def read_question_detail(questions_df):
  
  idx = 0
  for link in questions_df['link']:
    question = []
    answer = []
    try:
      request = requests.get(link)
      request.raise_for_status()
      try:
        soup = bs(request.text, 'html.parser')
        questions_df['full_question'][idx] = soup.find("div", {"id": "question"}).select_one('.post-text').getText()
        questions_df['best_answer'][idx] = soup.find("div", {"id": "answers"}).select_one('.post-text').getText()

      except: 
        print ("Could not transform to soup object by selecting")

    except HTTPError:
      print ("Could not download page")

    idx += 1

    sleep(0.05)

  return questions_df

def stackoverflow_vocabulary(questions_df):
    docs_stem_words = []
    vocabulary = {}
    stop_words = stopwords.words('english')
    #stop_words.append(['could', 'would', 'might', 'can', 'should'])
    snowball_stemmer = SnowballStemmer("english")

    for index in range(len(questions_df)):
        text = questions_df['title'][index] + questions_df['full_question'][index] + questions_df['best_answer'][index] 
        tokentext = word_tokenize(clean_text(text))
        stem_words  = [snowball_stemmer.stem(word) for word in tokentext if not word in stop_words and len(word) > 2 and word not in string.punctuation]
        docs_stem_words.append(stem_words)

        #Inicializa vocabulário sem repetição de palavras
        for word in stem_words:
            vocabulary[word] = 0

    #Contabiliza ocorrência de cada palavra em todos os documentos
    for words in docs_stem_words:
        for word in words:
            vocabulary[word] += 1
    
    return vocabulary, docs_stem_words


#Criar índice invertido para viabilizar buscas
def create_InvertedIndex(vocabulary, docs_stem_words): 
    invertedList = dict()
    for term in vocabulary:
        invertedList[term] = list()
        index = 0
        for stem_words in docs_stem_words:
            frequencia = 0
            for word in stem_words:
                if word == term:
                    frequencia += 1
            if frequencia > 0:
                invertedList[term].append([index, frequencia])
            index += 1
            invertedList[term].sort(key=itemgetter(1), reverse=True)

    # Serialize data into file:
    json.dump(invertedList, open( "stackoverflow_InvertedIndex.json", 'w' ) )

    return

def simple_stemming_docs(documents):
    snowball_stemmer = SnowballStemmer("english")
    stop_words = stopwords.words('english')
    #stop_words.append('could', 'would', 'might', 'can', 'should')
    tokens = sum([word_tokenize(clean_text(document)) for document in documents], [])
    stem_words  = [snowball_stemmer.stem(word) for word in tokens if not word in stop_words and len(word) > 2 and word not in string.punctuation]

    return stem_words

def simple_lookup_query(query, invertedList):
    terms = simple_stemming_docs([query])

    docs_index = {}

    for term in terms:
        if term in invertedList.keys():
            docs_index[term] = [index[0] for index in invertedList[term]]
        else:
            docs_index['missingTerm'] = None

    return docs_index

def make_clickable(val):
    return '<a href="{}">{}</a>'.format(val,val)

#dataframe com várias colunas
def make_clickable2(val):
    # target _blank to open new window
    return '<a target="_blank" href="{}">{}</a>'.format(val, val)

def print_search_result(docs_index, questions_df, operator='OR', num_results = 5):
    resultList=[lista[1] for lista in docs_index.items()]

    responseSet = []

    if operator == 'AND' and 'missingTerm' in docs_index.keys():
        resultList = []
    elif 'missingTerm' in docs_index.keys():
        resultList.remove(None)

    if len(resultList) == 1:
        responseSet = resultList[0]

    #Realiza a interseção entre os conjuntos
    for i in range(len(resultList)-1):
        #Operador AND
        if operator == 'AND':
            responseSet.append(list(set(resultList[i]).intersection(resultList[i+1])))
        else:
            #Operador OR
            responseSet.append(list(set(resultList[i]).union(resultList[i+1])))

    print("Foram encontrados ", len(np.unique(responseSet)), " perguntas no stackoverflow compatíveis com a sua busca. Veja as respostas mais relevantes:\n")

    #Monta o Resultado
    #results = pd.DataFrame(columns=['title','link','summary'])
    results = pd.DataFrame(columns=['title','link','summary'],  index=range(len(responseSet)))
    idx=0
    for doc_idx in np.unique(responseSet):
        #results.at[idx,'title'] = questions_df['title'][doc_idx]
        #results.at[idx,'link'] = questions_df['link'][doc_idx]
        #results.at[idx,'summary'] = questions_df['summary'][doc_idx]
        results['title'][idx] = questions_df['title'][doc_idx]
        results['link'][idx] = questions_df['link'][doc_idx]
        results['summary'][idx] = questions_df['summary'][doc_idx]
        idx += 1 

    #results['link'] = results['link'].apply(make_clickable2)

    return results #.style.format({'link': make_clickable2})

def clean_tags (text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation)) #remove todas as pontuações: '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    text = text.replace(',',' ').strip()
    text = " ".join(text.split())
    text = unidecode.unidecode(text)
    text = text.split(' ')
    return text

def remove_invalid_tags(tags, stack_tags):
    valid_tags = []
    [valid_tags.append(tag) for tag in tags if tag in stack_tags]
    return valid_tags

def read_stackoverflow_tags():
    stack_tags = pd.read_csv('stackoverflow_tags.csv')
    stack_tags = stack_tags['tagName'].values.tolist()
    return stack_tags

def refresh_stackoverflow(tags=['python','pandas'],tab='Frequent',pages=2):
    questions_overview_raw = read_stackoverflow_overview(tags,tab='Frequent',pages=2)
    questions_df = questions_overview(questions_overview_raw)
    questions_df = read_question_detail(questions_df)
    vocabulary, docs_stem_words = stackoverflow_vocabulary(questions_df)
    create_InvertedIndex(vocabulary, docs_stem_words)
    return questions_df
'''
if __name__ == '__main__':
    questions_df = refresh_stackoverflow(tags=['tell','flutter'],tab='Frequent',pages=2)
    invertedList = json.load( open( "stackoverflow_InvertedIndex.json" ) )
    searchTerms = input("Digite os termos de busca: ") 
    operator = input("Deseja buscar documentos que contenha todos os termos da busca? (S/N)")

    if operator.lower() == 's': operator = 'AND'
    else: operator = 'OR'

    docs_index = simple_lookup_query(searchTerms,invertedList)

    result = print_search_result(docs_index,questions_df,operator)'''
