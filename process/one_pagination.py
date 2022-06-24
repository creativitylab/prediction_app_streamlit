from elasticsearch import Elasticsearch
from pandas import json_normalize
import pandas as pd

username = 'elastic'
password = 'AWbtmGda2Q7BI2bYpdjyF4qd'

es = Elasticsearch(['https://8f9677360fc34e2eb943d737b2597c7b.us-east-1.aws.found.io:9243/'],
                   http_auth=(username, password))


def scroll_page(index, scroll, df, size=10000):
    print('starting pagination')
    es = Elasticsearch(['https://8f9677360fc34e2eb943d737b2597c7b.us-east-1.aws.found.io:9243/'],
                       http_auth=(username, password))
    page = es.search(index=index, scroll=scroll, size=size)
    scroll_id = page['_scroll_id']
    print('scroll_id', scroll_id)
    hits = page['hits']['hits']
    df = df.append(json_normalize(hits))

    while len(hits):
        print('hits ', hits)
        page = es.scroll(scroll_id=scroll_id, scroll=scroll)
        scroll_id = page['_scroll_id']
        hits = page['hits']['hits']
        df = df.append(json_normalize(hits))
    return df


def rename_columns(df):
    """Get es results and rename es columns."""
    df.columns = df.columns.str.replace('_', '')

    for col in df.columns:
        new_col = col.split('.')
        if len(new_col) != 1:
            new_col = new_col[1]
            # print(new_col)
        else:
            new_col = new_col[0]
        df = df.rename(columns={col: new_col})

    return df


df = pd.DataFrame()

pagination_df = scroll_page('brasov-dev', '1m', df)

pagination_df = rename_columns(pagination_df)
pagination_df.to_csv('air_dataset.csv')
# pagination_df=average_per_days(pagination_df)
# # pagination_df = pd.read_csv('last_step_pagination_110422.csv', infer_datetime_format=True)
# clean_data(pagination_df)


#TODO THIS IS THE GOOD ONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!