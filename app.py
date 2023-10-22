import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from janome.tokenizer import Tokenizer
from collections import Counter

st.title("議案書審議分析")

uploaded_file = st.file_uploader("Excelファイルをアップロードしてください", type=["xlsx"])

#font_path = 'ipaexg.ttf'

# Matplotlibのフォント設定
plt.rcParams['font.family'] = 'Yu Gothic'

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"エラー: {e}")
    else:

        filter_column = '種別'

        # フィルタリングする種別を選択
        filter_values = st.multiselect("フィルタリングする種別を選択してください", df[filter_column].unique())

        # 選択した種別のデータをフィルタリング
        filtered_df = df[df[filter_column].isin(filter_values)]

        # 選択したカラム内のテキストデータを結合
        text = " ".join(filtered_df['内容（要約）'].astype(str))

        # 形態素分析
        tokenizer = Tokenizer()
        tokens = [token.base_form for token in tokenizer.tokenize(text) if token.part_of_speech.split(',')[0] not in ['助詞', '助動詞', '副詞', '動詞', '形容詞'] and token.base_form not in ['、', '？', 'の', ' ']]
        analyzed_text = " ".join(tokens)


        # ワードクラウドを生成
        wordcloud = WordCloud(
            max_words=200, 
            width=400,
            height=400, 
            background_color="white",  # 背景を白に設定
            #font_path=font_path
            font='Yu Gothic'
        ).generate(analyzed_text)

        # ワードクラウドを表示
        st.subheader("ワードクラウド")
        plt.figure(figsize=(4, 4))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        st.pyplot(plt)

        # 語数の棒グラフを生成（上位10語、昇順）
        st.subheader("語数グラフ")
        word_counts = Counter(tokens)
        # カウントを昇順でソート
        sorted_word_counts = dict(sorted(word_counts.items(), key=lambda item: item[1]))
        words, counts = zip(*sorted_word_counts.items())
        top_words = words[-10:]  # 上位10語を選択
        top_counts = counts[-10:]
        plt.figure(figsize=(10, 6))
        plt.barh(top_words, top_counts)
        st.pyplot(plt)
