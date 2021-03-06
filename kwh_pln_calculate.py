import pandas as pd
import requests
import urllib.parse
from datetime import datetime,timedelta
from sqlalchemy import create_engine


IMPULSE_KWH = 1000
RUPIAH_PER_KWH = 1444.70  # R-1/TR 1.301 – 2.200 VA

def run_cron():
    now_date = datetime.now().strftime('%Y-%m-%d')

    yesterday_date = datetime.now() - timedelta(days=1)
    yesterday_date = yesterday_date.strftime('%Y-%m-%d')

    conn = create_engine("postgresql+psycopg2://root:12345678@localhost:5432/plnstats").connect()

    df = pd.read_sql(sql='SELECT color_percentage, created_on from public.home_pln_kwh_sensor where created_on >= \'{yesterday} 00:00:00\' and created_on < \'{currdate} 00:00:00\''.format(yesterday=yesterday_date,currdate=now_date),con=conn)

    df['created_on'] = pd.to_datetime(df.created_on)

    df['created_on'] = df['created_on'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df = df.drop_duplicates(subset=['created_on'])
    df['created_on'] = pd.to_datetime(df.created_on)
    df['hour'] = df['created_on'].dt.strftime('%H')
    df['day'] =  df['created_on'].dt.strftime('%Y-%m-%d')

    list_day = list(df['day'].unique())

    df_summary = pd.DataFrame(columns=['day','hour','sum_impulse','charges_amount'])

    #DETAIL PER HOUR
    for dday in list_day:
        list_hour = list(df[df['day'] == str(dday)]['hour'].unique())
        for y in list_hour:
            wSumKWH = df[(df['day'] == str(dday)) & (df['hour'] == str(y))]
            df_summary = df_summary.append({'hour':y,'day':dday,'sum_impulse':wSumKWH.groupby('hour').count()['day'][0],'charges_amount':(wSumKWH.groupby('hour').count()['day'][0])*RUPIAH_PER_KWH/IMPULSE_KWH},ignore_index=True)

    df_summary.to_sql('home_pln_kwh_hour', schema='public', con=conn, if_exists='append', index=False)
    df_cummary = df_summary[df_summary['day'] == yesterday_date].groupby('day').sum()

    df_cummary.to_sql('home_pln_kwh_summary', schema='public', con=conn, if_exists='append', index=True)


if __name__ == '__main__':
    run_cron()