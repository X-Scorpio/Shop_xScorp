import pdms

conn = pdms.connect_db()

pdms.add_product(conn,'Pen',15,45)
pdms.add_product(conn,'Book',25,450)
pdms.add_product(conn,'Cup',5,245)


pdms.add_user(conn, 'test', 'test@xscop.gg', "234")
pdms.add_user(conn, 'test2', 'test2@xscop.gg', "2234")

pds=pdms.get_products(conn)
print(pds)

conn.commit()
conn.close()
