import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="データ軽量化・圧縮アプリ")

st.title("データ軽量化・圧縮アプリ")
st.write("CSVを読み込み、ファイルサイズを劇的に軽くする形式で書き出します。")

# ファイルアップローダー
uploaded_file = st.file_uploader("「**CSVファイルを選択**」", type=["csv"])

if uploaded_file is not None:
    original_name = uploaded_file.name
    original_size = uploaded_file.size / (1024 * 1024)
    
    st.write(f"読み込み元: 「**{original_name}**」 ({original_size:.2f} MB)")
    
    try:
        df = pd.read_csv(uploaded_file)
        
        # 保存形式の選択
        option = st.radio(
            "「**保存形式を選択**」", 
            ["GZIP圧縮CSV (.csv.gz)", "Parquet形式 (.parquet)"]
        )
        
        buffer = io.BytesIO()
        
        if option == "GZIP圧縮CSV (.csv.gz)":
            df.to_csv(buffer, index=False, compression='gzip')
            file_name = original_name + ".gz"
            mime_type = "application/gzip"
        else:
            # Parquet形式（高圧縮・高速読み込み）
            df.to_parquet(buffer, index=False)
            file_name = original_name.replace(".csv", ".parquet")
            mime_type = "application/octet-stream"
            
        output_data = buffer.getvalue()
        new_size = len(output_data) / (1024 * 1024)
        reduction = (1 - new_size / original_size) * 100 if original_size > 0 else 0
        
        st.success("処理が完了しました！")
        st.write(f"処理後サイズ: {new_size:.2f} MB (削減率: {reduction:.1f}%)")
        
        # ダウンロードボタン
        st.download_button(
            label="「**ダウンロード**」",
            data=output_data,
            file_name=file_name,
            mime=mime_type
        )
        
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
