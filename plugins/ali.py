import requests,json,re,shutil

from lyra_utility import *

request_uri = "https://gpsfront.aliexpress.com/queryGpsProductAjax.do?widget_id=5101049&limit=31&currency=&numTopProducts=4"
productList = {}


class ali_scraper(lyra_utility):
	def __init__(self, inputs):
		super(ali_scraper, self).__init__(inputs)


	def register_inputs(self, inputs):
		#self.log("Registering: " + str(inputs))
		pass

	
	def register_commands(self):
		self.possible_commands = {"run": self.run,
								  "say_hello": self.say_hello
								 }


	def download_product_image(self, product):
		self.log("Downloading image for: " + product["product_title"] + ":" + str(product["product_id"]))
		
		file_url = product["image_uri"]

		response = requests.get(file_url, stream=True)

		with open(product["product_id"] + '.jpg', 'wb') as out_file:
			shutil.copyfileobj(response.raw, out_file)
		
		del response



	def say_hello(self, params):
		self.log("You said: " + params["message"])



	def run(self):
		self.log("Attempting to scrape page: " + request_uri)
		
		nProducts = 0
		maxProducts = 40

		while(nProducts < maxProducts):
			r = requests.get(request_uri)

			parsed_response = json.loads(r.text)
			for shop in parsed_response["shops"]:
				shop_products = shop["products"]
				for productData in shop_products:

					currentProduct = productData["productTitle"]

					if currentProduct not in productList:
						self.log("Grabbing new product: "+ currentProduct)

						productList[currentProduct] = {}
						productList[currentProduct]["product_id"] = str(productData["productId"])
						productList[currentProduct]["product_title"] = productData["productTitle"]

						for key, value in productData.iteritems():
							if key == "productImage":
								productList[currentProduct]["image_uri"] = "https://" + value[2:]
								self.download_product_image(productList[currentProduct])
							elif key == "maxPrice":
								productList[currentProduct]["max_price"] = float(value[4:].replace(',',''))
			

			nProducts = len(productList)
			self.log("Total products scraped thus far: " + str(nProducts))

		self.log("Scraped: " + str(nProducts))



def main():
	inputs = {
		"url":"https://google.com"
	}

	aliTest = ali_scraper(inputs)
	
	#aliTest.run()

if __name__ == "__main__":main()