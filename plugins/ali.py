import requests,json,re,shutil

request_uri = "https://gpsfront.aliexpress.com/queryGpsProductAjax.do?widget_id=5101049&limit=31&currency=&numTopProducts=4"
productList = {}


class lyra_utility(object):

	def __init__(self):
		pass


	def download_product_image(self, product):
		print "Downloading image for: ", product["product_title"], ":", product["product_id"], "\n"
		
		file_url = product["image_uri"]

		response = requests.get(file_url, stream=True)

		with open(product["product_id"] + '.jpg', 'wb') as out_file:
			shutil.copyfileobj(response.raw, out_file)
		
		del response




	def run(self):
		print "Attempting to scrape page: ", request_uri , "\n"
		
		nProducts = 0
		maxProducts = 184

		while(nProducts < maxProducts):
			r = requests.get(request_uri)

			parsed_response = json.loads(r.text)
			for shop in parsed_response["shops"]:
				shop_products = shop["products"]
				for productData in shop_products:

					currentProduct = productData["productTitle"]

					if currentProduct not in productList:
						print "Grabbing new product: ", currentProduct

						productList[currentProduct] = {}
						productList[currentProduct]["product_id"] = str(productData["productId"])
						productList[currentProduct]["product_title"] = productData["productTitle"]

						for key, value in productData.iteritems():
							if key == "productImage":
								productList[currentProduct]["image_uri"] = "https://" + value[2:]
								self.download_product_image(productList[currentProduct])
							elif key == "maxPrice":
								productList[currentProduct]["max_price"] = float(value[4:])
			

			nProducts = len(productList)
			print "Total products scraped thus far: ", nProducts

		print "Scraped: ", nProducts



def main():
	aliTest = lyra_utility()
	aliTest.run()

if __name__ == "__main__":main()