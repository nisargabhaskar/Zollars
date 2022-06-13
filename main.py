# from typing import TYPE_CHECKING,List
import fastapi as _fastapi

# import schemas as _schemas
# import sqlalchemy.orm as _orm
# import services as _services
import blockchain as _blockchain
import uvicorn
import psycopg2


blockchain = _blockchain.Blockchain()
app = _fastapi.FastAPI()

try:
    connection = psycopg2.connect(
        user="myuser",
        password="blockchain",
        host="127.0.0.1",
        port="5432",
        database="blockchain_database",
    )
    cursor = connection.cursor()
    cursor.execute("select * from information_schema.tables where table_name=%s", ('transaction_history',))
    counter = cursor.rowcount
    if  counter == 0:
        sql = """CREATE TABLE transaction_history(index INT NOT NULL,data CHAR(100),previous_hash CHAR(64),time_stamp CHAR(26),proof INT)"""
        cursor.execute(sql)
        connection.commit()
        postgres_insert_query = """ INSERT INTO transaction_history (index, data  ,previous_hash , time_stamp , proof ) VALUES (%s,%s,%s,%s,%s)"""
        record_to_insert = (1,"000","0","0",1)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()

    postgreSQL_select_Query = "select * from transaction_history"
    cursor.execute(postgreSQL_select_Query)
    transactions = cursor.fetchall()
    for row in transactions:
        if row[0] != 1:
            block = blockchain.mine_block(data = row[1])
            block[" timestamp "]= row[3]
        else:
            block = blockchain._create_block(data = "000", proof = 1, previous_hash ="0", index = 1, timestamp ="0")
            blockchain.chain.append(block)
finally:
    # closing database connection.
    if connection:
        cursor.close()
        connection.close()




@app.post("/add_to_db")
def add_to_db() -> int:
    connection = psycopg2.connect(
        user="myuser",
        password="blockchain",
        host="127.0.0.1",
        port="5432",
        database="blockchain_database",
    )
    cursor = connection.cursor()
    cursor.execute("select * from information_schema.tables where table_name=%s", ('transaction_history',))
    counter = cursor.rowcount
    if  counter == 0:
        sql = """CREATE TABLE transaction_history(index INT NOT NULL,data CHAR(100),previous_hash CHAR(64),time_stamp CHAR(26),proof INT)"""
        cursor.execute(sql)
        connection.commit()
        postgres_insert_query = """ INSERT INTO transaction_history (index, data  ,previous_hash , time_stamp , proof ) VALUES (%s,%s,%s,%s,%s)"""
        record_to_insert = (1,"000","0","0",1)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()

    postgreSQL_select_Query = "select * from transaction_history"
    cursor.execute(postgreSQL_select_Query)
    transactions = cursor.fetchall()
    counter = len(transactions)
    if connection:
        cursor.close()
        connection.close()
    for x in range(counter, len(blockchain.chain)):
        try:
            connection = psycopg2.connect(
                user="myuser",
                password="blockchain",
                host="127.0.0.1",
                port="5432",
                database="blockchain_database",
            )
            cursor = connection.cursor()
            postgres_insert_query = """ INSERT INTO transaction_history (index, data  ,previous_hash , time_stamp , proof ) VALUES (%s,%s,%s,%s,%s)"""
            record_to_insert = (
                blockchain.chain[x]["index"],
                blockchain.chain[x]["data"],
                blockchain.chain[x]["previous_hash"],
                blockchain.chain[x]["timestamp"],
                blockchain.chain[x]["proof"],
            )
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()
        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into transaction_history table", error)

        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
            


@app.post("/mine_block/")
def mine_block(data: str):
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(
            status_code=400, detail="the blockchain is corrupted"
        )
    block = blockchain.mine_block(data=data)
    return block


@app.get("/blockchain/")
def get_blockchain():
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(
            status_code=400, detail="the blockchain is corrupted"
        )
    chain = blockchain.chain
    return chain


@app.get("/previousblock/")
def previous_block():
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(
            status_code=400, detail="the blockchain is corrupted"
        )
    return blockchain.get_previous_block()


@app.get("/validate/")
def validate():
    return blockchain.is_chain_valid()
