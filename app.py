import streamlit as st
import pandas as pd
import datetime
import os

# 記録用CSVファイルのパス
CSV_FILE = "model_evaluations.csv"

def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["日時", "コンペ名", "採用モデル", "CV_RMSE", "CV_MAE", "CV_R2"])

def save_data(df):
    df.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")

st.title("モデル評価 記録アプリ")

# 1. 記録入力フォーム
with st.form("record_form"):
    st.subheader("新しい評価を記録")
    
    col1, col2 = st.columns(2)
    with col1:
        compe_name = st.text_input("コンペ名", placeholder="例: お弁当需要予測")
    with col2:
        record_date = st.date_input("日付", datetime.date.today())
        record_time = st.time_input("時間", datetime.datetime.now().time())
        
    model_name = st.text_input("採用モデル", placeholder="例: GBM | 浅い木(深さ2)")
    
    st.write("評価スコア")
    col3, col4, col5 = st.columns(3)
    with col3:
        cv_rmse = st.number_input("CV_RMSE", value=0.0, format="%.4f")
    with col4:
        cv_mae = st.number_input("CV_MAE", value=0.0, format="%.4f")
    with col5:
        cv_r2 = st.number_input("CV_R2", value=0.0, format="%.4f")
    
    submitted = st.form_submit_button("記録を保存")
    
    if submitted:
        if compe_name and model_name:
            dt_str = f"{record_date} {record_time.strftime('%H:%M')}"
            new_record = pd.DataFrame([{
                "日時": dt_str,
                "コンペ名": compe_name,
                "採用モデル": model_name,
                "CV_RMSE": cv_rmse,
                "CV_MAE": cv_mae,
                "CV_R2": cv_r2
            }])
            
            df = load_data()
            # 最新の記録が一番上にくるように結合
            df = pd.concat([new_record, df], ignore_index=True)
            save_data(df)
            st.success("記録を保存しました。")
        else:
            st.error("「コンペ名」と「採用モデル」は入力必須です。")

# 2. 過去の記録表示とダウンロード
st.subheader("記録一覧")
df = load_data()

if not df.empty:
    st.dataframe(df, use_container_width=True)
    
    csv_data = df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button(
        label="📥 記録データをCSVとしてダウンロード",
        data=csv_data,
        file_name="model_evaluations.csv",
        mime="text/csv",
    )
else:
    st.info("まだ記録はありません。")
