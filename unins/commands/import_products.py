
import itertools
import logbook

class ProductImporter:
    log = logbook.Logger('unins.product_import')

    def __init__(self, insales_api, unleashed_api, db_connection):
        self.insales_api = insales_api
        self.unleashed_api = unleashed_api
        self.db = db

    def import_all(self):
        for p in self.iter_api_products():
            self.log.info("{0}", p['title'])

    def iter_api_products(self):
        for page in itertools.count(1):
            self.log.info("Fetching products (page {0})...", page)
            products = self.insales_api.get_products(page=page)
            self.log.info("... got {0} products", len(products))
            if not products:
                return
            for p in products:
                yield p
