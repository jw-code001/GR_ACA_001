# 로컬에서 실행되는 대화형 RAG(검색 증강 생성) 시스템
# 사용자의 질문을 받으면 
# 1) 벡터 DB에서 관련 정보를 찾고, 
# 2) 그 정보를 Ollama 모델(Llama3 등)에게 전달하여 답변을 생성


# 답변용 모델인 llama3가 설치
# ollama pull llama3
# pip install langchain-ollama langchain-chroma langchain-core

import streamlit as st
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. 초기 설정 (이미 구축된 DB 로드)
def load_rag_system():
    # 이전에 사용한 것과 동일한 임베딩 모델
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    
    # 저장된 폴더 연결
    vectorstore = Chroma(
        persist_directory="./chroma_db_ollama", 
        embedding_function=embeddings
    )
    
    # 검색기(Retriever) 설정: 관련성 높은 3개 조각 가져오기
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    # 답변을 생성할 로컬 LLM (Llama3, Mistral 등 설치된 모델명 입력)
    llm = ChatOllama(model="llama3", temperature=0) 
    
    return retriever, llm

# 2. 프롬프트 구성 (AI에게 역할을 부여합니다)
# 수정된 프롬프트 구성
template = """너는 '포랩'의 데이터를 기반으로 답변하는 전문적인 한국어 어시스턴트야. 
반드시 **한국어(Korean)**로 답변해야 해.

[참고 정보]
{context}

질문: {question}

답변:"""

prompt = ChatPromptTemplate.from_template(template)

# 3. 메인 실행 함수
def main():
    st.set_page_config(page_title="포랩 로컬 챗봇", page_icon="🤖")
    st.title("포랩 데이터 기반 로컬 대화 시스템")
    
    retriever, llm = load_rag_system()

    # RAG 체인 생성
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # 채팅 인터페이스
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if query := st.chat_input("포랩에 대해 궁금한 점을 물어보세요!"):
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):
            with st.spinner("데이터에서 정보를 찾는 중..."):
                response = rag_chain.invoke(query)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()

# streamlit run app.py
# "이 자료를 참고해서(1번), 네가 아는 언어 능력과 상식을 동원해(2번) 자연스럽게 대답함."