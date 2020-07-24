import streamlit as st
import json
import string
import read_stackoverflow as stack

def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    text = link.split('=')[1]
    return f'<a target="_blank" href="{link}">{text}</a>'

if __name__ == '__main__':

    stack_tags = stack.read_stackoverflow_tags()
    searchTerms = st.text_input('Digite o que deseja buscar no stackoverflow:')
    tags = stack.clean_tags(searchTerms)
    tags = stack.remove_invalid_tags(tags, stack_tags)
    st.write("Tags no stackoverflow",tags)

    operator = 'OR'
    if st.checkbox('Buscar documentos com todos os termos'): operator = 'AND'

    if st.button("Iniciar busca"):
        try:
            questions_df = stack.refresh_stackoverflow(tags,tab='Frequent',pages=2)
        except:
            st.write("Oops... Não conseguimos atualizar os dados do stackoverflow sobre este tema :( ")

        invertedList = json.load(open( "stackoverflow_InvertedIndex.json"))
        docs_index = stack.simple_lookup_query(searchTerms,invertedList)

        #st.write(stack.print_search_result(docs_index,questions_df,operator))
        #results = stack.print_search_result(docs_index,questions_df,operator)

        # link is the column with hyperlinks
        #results['link'] = results['link'].apply(make_clickable)
        #results = results.to_html(escape=False)
        #st.write(results, unsafe_allow_html=True)
        results = stack.print_search_result(docs_index,questions_df,operator)
        st.dataframe(results)




