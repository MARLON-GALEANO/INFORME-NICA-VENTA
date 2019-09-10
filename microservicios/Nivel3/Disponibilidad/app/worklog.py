class Worklog:

    def __init__(self, dbcon, logger):
        self._dbcon=dbcon
        self._logger=logger

    def save_location(self, **kwargs):
        sql = """
        insert into location 
            (country, city, active) 
            values ('{}','{}','{}')
        """.format(
                kwargs['country'],
                kwargs['city'],
                kwargs['active'])
        cur = self._dbcon.connection.cursor()
        cur.execute(sql)
        self._dbcon.connection.commit()
        cur.close()
        self._logger.info(sql)

    def update_location(self, **kwargs):
        sql = """
        update location set active='{}' where country='{}' and city='{}'; 
        """.format(
                kwargs['active'],
                kwargs['country'],
                kwargs['city'])
        cur = self._dbcon.connection.cursor()
        rv = cur.execute(sql)
        self._dbcon.connection.commit()
        cur.close()
        self._logger.info(sql)
        return rv

    def obtain_location(self, country, city):
        sql = """
        select * from location where country='{}' and city='{}';
        """.format(country, city)
        cur = self._dbcon.connection.cursor()
        cur.execute(sql)
        rv = cur.fetchall()
        cur.close()
        self._logger.info(rv)
        return rv

