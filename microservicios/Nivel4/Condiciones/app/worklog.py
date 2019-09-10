class Worklog:

    def __init__(self, dbcon, logger):
        self._dbcon=dbcon
        self._logger=logger

    def get_price(self, sku):
        sql = """
        select price, description from product where sku="{}";
        """.format(sku)
        cur = self._dbcon.connection.cursor()
        cur.execute(sql)
        rv = cur.fetchall()
        cur.close()
        self._logger.info(rv)
        return rv

    def obtain_product(self, **kwargs):
        sql = """
        select description, price from product 
        inner join location on location.country='{}' 
        and location.city='{}' and product.sku='{}'
        """.format(
                kwargs['country'],
                kwargs['city'],
                kwargs['sku'])
        cur = self._dbcon.connection.cursor()
        cur.execute(sql)
        rv = cur.fetchall()
        cur.close()
        self._logger.info(rv)
        return rv

    def obtain_condition(self, country, city, sku, weather):
        sql = """
        select rules.variation, product.description, product.price from rules 
        inner join product on product.sku=rules.sku 
        where rules.country='{}' 
        and rules.city='{}' 
        and rules.sku='{}' 
        and rules.max_condition >= '{}' 
        and rules.min_condition <= '{}';
        """.format(country, city, sku, weather, weather)
        cur = self._dbcon.connection.cursor()
        cur.execute(sql)
        rv = cur.fetchall()
        cur.close()
        self._logger.info(sql)
        return rv

