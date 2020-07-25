import sqlite3 as sq
import pandas as pd

df = pd.read_csv(r'C:\Users\vsuha\Downloads\my-diner-food-master\my-diner-food-master\the-diner-dinner.csv',
                 engine='python')
conn = sq.connect('the_diner_dinner.db')
c = conn.cursor()
c.execute('''DROP TABLE IF EXISTS the_diner_dinner''')
conn.commit()
df.to_sql('the_diner_dinner', conn, if_exists='replace', index=False)

