import pandas as pd
import psycopg2

class DBManager:
    def __init__(self, db_config):
        self.db_config = db_config

    def execute_query(self, query):
        """
        전달된 SQL 쿼리를 실행하고 결과를 DataFrame으로 반환.
        :param query: str - 실행할 SQL 쿼리
        :return: DataFrame - SQL 실행 결과
        """
        try:
            conn = psycopg2.connect(**self.db_config)
            df = pd.read_sql_query(query, conn)  # 쿼리 실행

            # 동일한 air id 가진 행 중에서 fare가 최소인 행만 남김
            min_fare_idx  = df.groupby(['air_id', 'fetched_date'])['fare'].idxmin()
            grouped_df = df.loc[min_fare_idx]

            # 'is_layover'가 True인 행 제거
            grouped_df = grouped_df[grouped_df['is_layover'] != True]

            return grouped_df
        
        except Exception as e:
            print(f"데이터 로드 오류: {e}")
            
        finally:
            conn.close()
