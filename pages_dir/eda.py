import io
import missingno as msno

import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def app():
    st.title('Custom Data-Explore')
    dataset = st.file_uploader("Upload a dataset", type=["csv"])

    st.sidebar.header('Import a dataset to view the analysis')
    if dataset:
        df = pd.read_csv(dataset)

        rows, columns = df.shape
        st.write('Uploaded dataset has ', rows, ' rows and ', columns, ' columns')
        st.write('First 5 rows of the dataset are: ')

        st.dataframe(df.head())
        with st.expander('View entire dataset'):
            st.dataframe(df)

        all_menu_items = ['Empty Values', 'Descriptive Analysis',
                          'Distribution of Numerical Columns',
                          'Box Plots']

        all_menu_items = st.sidebar.selectbox("Explore the uploaded dataset", all_menu_items)

        if 'Empty Values' in all_menu_items:
            st.subheader('Missing data information')
            if df.isnull().sum().sum() == 0:
                st.write('Your dataset does not have empty values.')
            else:
                res = pd.DataFrame(df.isnull().sum()).reset_index()
                res['Percentage'] = round(res[0] / df.shape[0] * 100, 2)
                res['Percentage'] = res['Percentage'].astype(str) + '%'
                res.rename(columns={'index': 'Column Name', 0: 'Count'}, inplace=True)
                st.dataframe(res)

                msno.bar(df)

                gray_patch = mpatches.Patch(color='gray', label='Data present')
                white_patch = mpatches.Patch(color='white', label='Data absent ')
                plt.legend(handles=[gray_patch, white_patch])

                st.pyplot(plt)

        if 'Detailed Analysis' in all_menu_items:
            st.subheader('Detailed Analysis:')
            st.dataframe(df.describe())

        if 'Histogram' in all_menu_items:
            st.subheader("Select column to plot histogram for:")
            target_column = st.selectbox("", df.columns, index=len(df.columns) - 1)

            fig = px.histogram(df, x=target_column)
            col1, col2, col3 = st.columns([0.5, 2, 0.5])
            col2.plotly_chart(fig)

        numerical_columns = df.select_dtypes(exclude='object').columns

        if 'Distribution of Numerical Columns' in all_menu_items:

            if len(numerical_columns) == 0:
                st.write('There are no numerical columns in the uploaded data.')
            else:
                selected_num_cols = sidebar_selection('Choose columns for Distribution plots:',
                                                      numerical_columns, 'Distribution')
                st.subheader('Distribution of numerical columns')
                i = 0
                while (i < len(selected_num_cols)):
                    col1, col2 = st.columns(2)
                    for j in [col1, col2]:

                        if (i >= len(selected_num_cols)):
                            break

                        fig = px.histogram(df, x=selected_num_cols[i])
                        j.plotly_chart(fig, use_container_width=True)
                        i += 1

        if 'Box Plots' in all_menu_items:
            if len(numerical_columns) == 0:
                st.write('There are no numerical columns in the uploaded data.')
            else:
                selected_num_cols = sidebar_selection('Choose columns for Box plots:', numerical_columns,
                                                      'Box')
                st.subheader('Box plots')
                i = 0
                while (i < len(selected_num_cols)):
                    col1, col2 = st.columns(2)
                    for j in [col1, col2]:

                        if (i >= len(selected_num_cols)):
                            break

                        fig = px.box(df, y=selected_num_cols[i])
                        j.plotly_chart(fig, use_container_width=True)
                        i += 1


def sidebar_selection(massage, arr, key):
    container = st.sidebar.container()
    selected_num_cols = container.multiselect(massage, arr, default=arr[0])

    return selected_num_cols
