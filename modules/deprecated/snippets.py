#get dem records

self.productDatabase.execute("SELECT COUNT(product_id) FROM products");
nProducts = self.productDatabase.fetchone()[0]
