from pathlib import Path
import pandas as pd
import streamlit as st
from maintenance import analyze_maintenance
from reporting import create_priority_report
from ai_agent import ask_agent
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title='RailOps AI | Maintenance Analytics', page_icon='🚆', layout='wide')
st.title('🚆 RailOps AI — Maintenance Analytics')
st.caption('Portfolio prototype using synthetic railcar data. Scheduling indicators are not safety assessments.')

sample_path = Path(__file__).parent / 'data' / 'railcars.csv'
upload = st.file_uploader('Upload railcar maintenance CSV (or use sample data)', type='csv')
try:
    source = pd.read_csv(upload if upload is not None else sample_path)
    df = analyze_maintenance(source)
except (ValueError, pd.errors.ParserError, UnicodeDecodeError, FileNotFoundError) as exc:
    st.error(f'Unable to analyze the data: {exc}')
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric('Railcars', len(df))
c2.metric('Overdue', int((df.inspection_status == 'Overdue').sum()))
c3.metric('Due within 14 days', int((df.inspection_status == 'Due Soon').sum()))
c4.metric('On track', int((df.inspection_status == 'On Track').sum()))

st.subheader('Inspection scheduling overview')
st.bar_chart(df.inspection_status.value_counts().reindex(['Overdue', 'Due Soon', 'On Track'], fill_value=0))
status = st.selectbox('Filter inspection status', ['All', 'Overdue', 'Due Soon', 'On Track'])
filtered = df if status == 'All' else df[df.inspection_status == status]
st.dataframe(filtered, width="stretch", hide_index=True)
st.download_button('Download filtered inspection report', filtered.to_csv(index=False).encode('utf-8'), 'railcar_inspection_report.csv', 'text/csv')
st.divider()
st.subheader('Automated priority report')
report = create_priority_report(df)
st.download_button('Download automatic priority report', report, 'railops_priority_report.txt', 'text/plain')
with st.expander('Preview generated report'):
    st.code(report, language='text')

st.divider()
st.subheader('Ask RailOps AI')
st.caption('Uses Gemini function calling to query computed records; requires an eligible API key.')
question = st.text_input('Ask a question', placeholder='Which 5 railcars are most overdue?')
if st.button('Ask AI', type='primary'):
    key = os.getenv('GEMINI_API_KEY', '')
    if not key:
        st.warning('Add GEMINI_API_KEY to your local .env file to enable the AI assistant. The dashboard and report work without it.')
    else:
        try:
            with st.spinner('Analyzing records...'):
                st.write(ask_agent(df, question, key))
        except Exception as exc:
            st.error(f'AI request failed: {exc}')
st.caption('Synthetic data only. This project is not affiliated with TrinityRail.')
