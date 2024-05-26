import oracledb


def getConnection():
    try:
        connection = oracledb.connect('Login/Senha@oracle.fiap.com.br/ORCL')
        print("Conexao realizada com sucesso!", connection.version)
    except Exception as e:
        print(f"Erro na conexao: {e}")
    return connection

def verif_tabela(tabela):
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT 1 FROM {tabela} WHERE ROWNUM = 1")
        return True
    except:
        return False
    finally:
        cursor.close()
        conn.close()

def create_table_cliente():
    try:
        conn = getConnection()
        cursor = conn.cursor()
        sqlCreateTable = """CREATE TABLE CLIENTE(
        NOME VARCHAR2(50),
        EMAIL VARCHAR2(50),
        CPF VARCHAR2(50) PRIMARY KEY,
        TELEFONE VARCHAR2(50),
        CEP VARCHAR2(50),
        ESTADO VARCHAR2(50),
        CIDADE VARCHAR2(50),
        BAIRRO VARCHAR2(50),
        ENDERECO VARCHAR2(50),
        NUMERACAO VARCHAR2(10),
        COMPLEMENTO VARCHAR2(50)
        )"""
        cursor.execute(sqlCreateTable)
        conn.commit()
        print("Table created successfully")
    except oracledb.DatabaseError as e:
        print("Failed to create table", e)
    finally:
        if (conn):
            cursor.close()
            conn.close()
        

def create_table_bike():
    try:
        conn = getConnection()
        cursor = conn.cursor()
        sqlCreateTable = """CREATE TABLE BIKE(
        MODELO VARCHAR2(50),
        NUMERO_SERIE VARCHAR2(50) PRIMARY KEY,
        LANCAMENTO NUMBER,
        VALOR NUMBER,
        CPF VARCHAR2(50),
        FOREIGN KEY (CPF) REFERENCES CLIENTE(CPF)
        )"""
        cursor.execute(sqlCreateTable)
        print("Table created successfully")
    except oracledb.DatabaseError as e:
        print("Failed to create table", e)
    finally:
        if (conn):
            cursor.close()
            conn.close()

def create_table_acessorio():
    try:
        conn = getConnection()
        cursor = conn.cursor()
        sqlCreateTable = """CREATE TABLE ACESSORIO(
        ACESSORIO VARCHAR2(50),
        VALOR NUMBER,
        NUMERO_SERIE VARCHAR2(50),
        FOREIGN KEY (NUMERO_SERIE) REFERENCES BIKE(NUMERO_SERIE) ON DELETE CASCADE
        )"""
        cursor.execute(sqlCreateTable)
        print("Table created successfully")
    except oracledb.DatabaseError as e:
        print("Failed to create table", e)
    finally:
        if (conn):
            cursor.close()
            conn.close()

def insert_cliente(dados):
    conn = getConnection()
    cursor = conn.cursor()
    sql_query = "INSERT INTO CLIENTE (NOME, EMAIL, CPF, TELEFONE, CEP, ESTADO, CIDADE, BAIRRO, ENDERECO, NUMERACAO, COMPLEMENTO) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)"
    data = (
        dados['Nome'], 
        dados['Email'], 
        dados['Cpf'], 
        dados['Telefone'], 
        dados['Cep'], 
        dados['Estado'], 
        dados['Cidade'], 
        dados['Bairro'], 
        dados['Endereço'],
        dados['Numeracao'], 
        dados['Complemento']
    )
    try:
        cursor.execute(sql_query, data)
        conn.commit()
        print("Registro inserido com sucesso")
    finally:
        cursor.close()
        conn.close()

def insert_bike(dados, CPF):
    conn = getConnection()
    cursor = conn.cursor()
    sql_query = "INSERT INTO BIKE (MODELO, NUMERO_SERIE, LANCAMENTO, VALOR, CPF) VALUES (:1, :2, :3, :4, :5)"
    data = (
        dados['Modelo'], 
        dados['Numero_Serie'],  
        dados['Lancamento'], 
        dados['Valor'],
        CPF
        )
    try:
        cursor.execute(sql_query, data)
        conn.commit()
        print("Registro inserido com sucesso")
    finally:
        cursor.close()
        conn.close()

def insert_acessorio(dados, Nr_Serie_Bike):
    conn = getConnection()
    cursor = conn.cursor()
    sql_query = "INSERT INTO ACESSORIO(ACESSORIO, VALOR, NUMERO_SERIE) VALUES (:1, :2, :3)"
    data = (
        dados['Acessório'], 
        dados['Valor'],
        Nr_Serie_Bike
    )
    try:
        cursor.execute(sql_query, data)
        conn.commit()
        print("Registro inserido com sucesso")
    finally:
        cursor.close()
        conn.close()

def select_cliente(CPF):
    conn = getConnection()
    cursor = conn.cursor()
    sql_querycliente = """
    SELECT *
    FROM CLIENTE WHERE CLIENTE.CPF = :CPF
    """
    try:
        cursor.execute(sql_querycliente, CPF=CPF)
        results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        result_dict = {}
        for row in results:
            for i, column_name in enumerate(column_names):
                result_dict[column_name.title()] = (row[i])
        return result_dict
    except Exception as e:
        print(f"Erro ao obter o registro: {e}")
    finally:
        cursor.close()
        conn.close()

def select_bike(CPF):
    conn = getConnection()
    cursor = conn.cursor()
    sql_query_bike = """
    SELECT *
    FROM BIKE WHERE BIKE.CPF = :CPF
    """
    try:
        cursor.execute(sql_query_bike, CPF=CPF)
        results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        result_dict = {}
        for row in results:
            for i, column_name in enumerate(column_names):
                result_dict[column_name.title()] = (row[i])
        return result_dict
    except Exception as e:
        print(f"Erro ao obter o registro: {e}")
    finally:
        cursor.close()
        conn.close()

def select_acessorio(numero_serie):
    conn = getConnection()
    cursor = conn.cursor()
    sql_query_acessorio = """
    SELECT *
    FROM ACESSORIO WHERE ACESSORIO.NUMERO_SERIE = :NUMERO_SERIE
    """
    try:
        cursor.execute(sql_query_acessorio, numero_serie=numero_serie)
        results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        result_dict = {}
        for row in results:
            for i, column_name in enumerate(column_names):
                result_dict[column_name.title()] = (row[i])
        return result_dict
    except Exception as e:
        print(f"Erro ao obter o registro: {e}")
    finally:
        cursor.close()
        conn.close()

def select_login(Email, CPF):
    conn = getConnection()
    cursor = conn.cursor()
    sql_querycliente = "SELECT * FROM CLIENTE WHERE EMAIL = :Email AND CPF = :CPF"
    try:
        cursor.execute(sql_querycliente, Email=Email, CPF=CPF)
        results = cursor.fetchall()
        if results:
            return True
    except Exception as e:
        print(f"Erro ao obter o registro: {e}")
    finally:
        cursor.close()
        conn.close()

def update(tabela, item, att, Cpf):
    conn = getConnection()
    cursor = conn.cursor()
    sql_update = f"UPDATE {tabela.upper()} SET {item.upper()} = :att WHERE CPF = :Cpf"
    data = {'att': att, 'Cpf': Cpf}
    try:
        cursor.execute(sql_update, data)
        conn.commit()
        print("Registro atualizado")
    except Exception as e:
        print(f"Erro ao atualizar o registro: {e}")
    finally:
        cursor.close()
        conn.close()

def delete(numero_serie):
    conn = getConnection()
    cursor = conn.cursor()
    sql_delete = "DELETE FROM BIKE WHERE NUMERO_SERIE = :NUMERO_SERIE"
    data = {'NUMERO_SERIE': numero_serie}
    try:
        cursor.execute(sql_delete, data)
        conn.commit()
        print("Registro deletado")
    except Exception as e:
        conn.rollback()
        print(f"Erro ao deletar o registro: {e}")
    finally:
        cursor.close()
        conn.close()