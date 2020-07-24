import streamlit as st
import json
import string
import read_stackoverflow as stack


if __name__ == '__main__':

    stack_tags = stack.read_stackoverflow_tags()
    searchTerms = st.text_input('Digite o que deseja buscar no stackoverflow:')
    tags = stack.clean_tags(searchTerms)
    tags = stack.remove_invalid_tags(tags, stack_tags)
    st.write("Tags para busca",tags)

    operator = 'OR'
    if st.checkbox('Buscar documentos com todos os termos'): operator = 'AND'

    if st.button("Iniciar busca"):
        questions_df = stack.refresh_stackoverflow(tags,tab='Frequent',pages=5)
        invertedList = json.load(open( "stackoverflow_InvertedIndex.json"))
        docs_index = stack.simple_lookup_query(searchTerms,invertedList)

        #st.write(stack.print_search_result(docs_index,questions_df,operator))
        results = stack.print_search_result(docs_index,questions_df,operator)
        st.write(results.to_html(escape=False, index=False), unsafe_allow_html=True)

