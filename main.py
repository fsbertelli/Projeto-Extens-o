import streamlit as st
import pandas as pd

def main():
    st.title('🥦 Gerador de Tabela Nutricional 🍝')
    st.header('🥦 Gerador de Tabela Nutricional 🍝')
    left, middle = st.columns(2, vertical_alignment="center")
    left.subheader("Projeto de Extensão")
    middle.subheader('ADS Unip 2024')

    df = pd.read_excel('Taco-4a-Edicao.xlsx', sheet_name='CMVCol taco3', engine='openpyxl')
    for col in df.columns[1:]:  
        df[col] = pd.to_numeric(df[col], errors='coerce')

    alimentos = df['Alimentos'].unique()
    selected_alimentos = st.multiselect('Selecione os ingredientes 👇', alimentos, placeholder = "Selecione uma opção")
    quantidades = {}
    resultados = pd.DataFrame()

    for alimento in selected_alimentos:
        quantidade = st.number_input(f'Insira a quantidade em gramas para {alimento.replace(',', '')}:', min_value=0, step=1)
        quantidades[alimento] = quantidade
        alimento_df = df[df['Alimentos'] == alimento]
        if not alimento_df.empty:
            proporcao = quantidade / 100
            valores_proporcionais = alimento_df.iloc[:, 1:] * proporcao  
            valores_proporcionais['Alimentos'] = alimento  
            resultados = pd.concat([resultados, valores_proporcionais], ignore_index=True)

    if st.button('Gerar etiqueta'):
        soma_valores = resultados.sum(numeric_only=True)
        st.subheader("Informações Nutricionais")
        selected_alimentos_formatados = [alimento.replace(',', '') for alimento in selected_alimentos]
        st.write(f"Ingredientes: {', '.join(selected_alimentos_formatados)}")
        st.write("Valor Energético: {:.2f} kcal".format(soma_valores.get('Calorias', 0)))
        st.write("Carboidratos: {:.2f} g".format(soma_valores.get('Carboidrato', 0)))
        st.write("Proteínas: {:.2f} g".format(soma_valores.get('Proteína', 0)))
        st.write("Gorduras Totais: {:.2f} g".format(soma_valores.get('Lipídeos', 0)))
        st.write("Fibra Alimentar: {:.2f} g".format(soma_valores.get('Fibra Alimentar', 0)))
        st.write("Sódio: {:.2f} mg".format(soma_valores.get('Sódio', 0)))
        st.dialog("title", width="small")

        
    st.caption("Autores :sunglasses:")
    st.caption("Felipe Bertelli dos Santos, Fernanda Melo, Jean Lucas Gomes Gama, Rony Siqueira da Silva, Tiago gonzaga da Silva, Marcos Antonio do Carmo Alves")

if __name__ == '__main__':
    main()