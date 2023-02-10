import os, django
# 환경 error 발생 시 주석 풀고 진행
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Data_Planet.settings")
# django.setup()

# from apps.models import DataPlatform, Data
import pandas as pd
from io import StringIO
import psycopg2

def run():
    db = psycopg2.connect(
        host='localhost',
        dbname='data_planet_db',
        user='root',
        password='password',
        port=5432
    )

    cursor = db.cursor()
    
    ## DataPlatform 테이블의 데이터가 없는 경우에, DB에 Dump
    cursor.execute('SELECT * FROM "DataPlatform"')
    if cursor.fetchone() is None:
        buffer = StringIO()
        try:
            data_platform = pd.read_csv('data/data_platform.csv') # FIXME: data_platform.csv 파일 경로 위치로 수정하기
            data_platform.to_csv(buffer, index=True, header=False)
            buffer.seek(0)
            cursor.copy_from(buffer, 'DataPlatform', sep=',')
            db.commit()
        except (Exception, psycopg2.DatabaseError) as e:
            print(f"Error: {e}")
            db.rollback()
            cursor.close()
            return 1
        print("copy_from_stringio() done - DataPlatform")
        
    ## Data 테이블의 데이터가 없는 경우에, DB에 Dump
    cursor.execute('SELECT * FROM "Data"')
    if cursor.fetchone() is None:
        buffer = StringIO()
        try:
            data_platform = pd.read_csv('data/total_data.csv', lineterminator='\n') # FIXME: total_data.csv 파일 경로 위치로 수정하기
            data_platform.to_csv(buffer, index=True, header=False)
            buffer.seek(0)
            cursor.copy_from(buffer, 'Data', sep=',')
            db.commit()
        except (Exception, psycopg2.DatabaseError) as e:
            print(f"Error: {e}")
            db.rollback()
            cursor.close()
            return 1
        print("copy_from_stringio() done - Data")

run()