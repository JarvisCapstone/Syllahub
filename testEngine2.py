from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:r9qi8nPF@127.0.0.1/Syllahub')
conn = engine.connect()
result = conn.execute("select email from user")

for row in result:
    print(row['email'])
