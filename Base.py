import pymysql

class Base():
    def __init__(self):
        self.conn = pymysql.connect(host="localhost", user="root", password="", database="demo_2", autocommit=True)
        self.cur = self.conn.cursor()

    def select_client(self, login, password):
        sql = "select * from client where login = %s and password = %s"
        self.cur.execute(sql, (login, password))
        return self.cur.fetchone()

    def select_tovar(self, find='', filter = '', sort=''):
        sql = "select * from tovar join category on category.id_category = tovar.id_category join namufact on namufact.id_manufact = tovar.id_manufact join supplier on supplier.id_supplier = tovar.id_supplier where 1 = 1"
        param = []

        if find:
            sql += " and (title like %s or description like %s)"
            param.append(f"%{find}%")
            param.append(f"%{find}%")

        if filter:
            print(filter)
            sql += " and tovar.id_supplier = %s"
            param.append(filter)

        if sort == 1:
            sql += " order by count desc"
        elif sort == 2:
            sql += " order by count asc"

        self.cur.execute(sql, param)
        return self.cur.fetchall()

    def select_category(self):
        sql = "select * from category"
        self.cur.execute(sql)
        return self.cur.fetchall()

    def select_manuract(self):
        sql = "SELECT * FROM namufact"
        self.cur.execute(sql)
        return self.cur.fetchall()

    def select_supplier(self):
        sql = "select * from supplier"
        self.cur.execute(sql)
        return self.cur.fetchall()

    def delete_tovar(self, id):
        try:
            sql = "delete from tovar where id_tovar = %s"
            self.cur.execute(sql, (id, ))
            return True
        except Exception as e:
            print(e)
            return False

    def update_tovar(self, title, photo, desc, category, manuf, supplier, price, unit, count, sale, id):
        try:
            sql = "update tovar set title = %s, photo = %s, description = %s, id_category = %s,  id_manufact = %s,  id_supplier = %s, price = %s,  unit = %s,  count = %s,  sale = %s where id_tovar = %s"
            self.cur.execute(sql, (title, photo, desc, category, manuf, supplier, price, unit, count, sale, id))
            return True
        except Exception as e:
            print(e)
            return False

    def add_tovar(self, title, photo, desc, category, manuf, supplier, price, unit, count, sale):
        try:
            sql = "insert into tovar (title, photo, description , id_category,id_manufact, id_supplier, price, unit, count, sale) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.cur.execute(sql, (title, photo, desc, category, manuf, supplier, price, unit, count, sale))
            return True
        except Exception as e:
            print(e)
            return False