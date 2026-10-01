import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="CSV軽量化アプリ")

st.title("CSV軽量化アプリ")
st.write("CSVを読み込み、無駄なデータを削ぎ落として同じ名前で書き出します。")

# ファイルアップローダー
uploaded_file = st.file_uploader("「**CSVファイルを選択**」", type=["csv"])

if uploaded_file is not None:
    # 元のファイル名とサイズを取得
    original_name = uploaded_file.name
    original_size = uploaded_file.size / (1024 * 1024)
    
    st.write(f"読み込み元: 「**{original_name}**」 ({original_size:.2f} MB)")
    
    try:
        # データの読み込み
        df = pd.read_csv(uploaded_file)
        
        # 軽量化処理
        # 1. 文字列の前後にある空白を削除
        str_cols = df.select_dtypes(include=['object']).columns
        for col in str_cols:
            df[col] = df[col].astype(str).str.strip()
        
        # 2. CSVデータとして変換（インデックスなし、小数点以下4桁）
        # ダウンロードさせるためにメモリ上のテキストデータにする
        csv_data = df.to_csv(index=False, float_format='%.4f').encode('utf-8')
        
        # 処理後のサイズを計算
        new_size = len(csv_data) / (1024 * 1024)
        reduction = (1 - new_size / original_size) * 100 if original_size > 0 else 0
        
        st.success("軽量化が完了しました！")
        st.write(f"処理後サイズ: {new_size:.2f} MB (削減率: {reduction:.1f}%)")
        
        # ダウンロードボタン（同じファイル名を指定して書き出し）
        st.download_button(
            label="同じ名前で保存",
            data=csv_data,
            file_name=original_name,
            mime="text/csv"
        )
        
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
