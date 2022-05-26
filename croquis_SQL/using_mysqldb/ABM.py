#!/usr/bin/python3
"""
final project ORM
"""


import MySQLdb
from sys import argv


if len(argv) > 1:
    conn = MySQLdb.connect(host="localhost",
                           port=3306,
                           user="root",
                           passwd="root",
                           db="DB",
                           charset="utf8")
    cur = conn.cursor()
    print("argumentos: {}".format(argv))
    if argv[1] == "insert":
        cur.execute("SHOW TABLES")
        print(cur.fetchall())
        insert = "INSERT INTO Inventory VALUES (%s, %s, %s, %s)"
        if len(argv) == 3:
             cur.execute(insert, (argv[2], "", "", ""))
        if len(argv) == 4:
            cur.execute(insert, (argv[2], argv[3], "", ""))
        if len(argv) == 5:
            cur.execute(insert, (argv[2], argv[3], argv[4], ""))
        else:
            cur.execute(insert, (argv[2], argv[3], argv[4], argv[5]))
        cur.execute("SELECT * FROM Inventory;")
        print(cur.fetchall())
        conn.commit()
    elif argv[1] == "select":
        if len(argv) == 3:
            print("entre donde tengo q entrar")
            select = "SELECT * FROM Inventory;"
            cur.execute(select, ())
        if len(argv) == 4:
            select = "SELECT %s FROM %s"
            cur.execute(select, (argv[2], argv[3]))
        pr = cur.fetchall()
        for p in pr:
            print(p)
    cur.close()
    conn.close()
