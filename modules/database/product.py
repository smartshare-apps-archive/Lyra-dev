import sys, csv, json, collections

# config current only has column/field mapping information, which will be specific to the import form (of the product csv), e.g. shopify
from config import *
from product_util import *
from modules.payment.stripe_interface import stripe_manager


# load single product by product_id
def loadProduct(product_id, productDatabase):
    try:
        productDatabase.execute(
            "SELECT product_id,stripe_id,VariantSKU,CAST(VariantPrice AS CHAR),VariantCompareAtPrice,VariantInventoryQty,VariantTaxable,VariantWeightUnit,VariantGrams,Title,BodyHTML,Vendor,Type,Tags,Published,ImageSrc,ImageAltText,VariantTypes,resources FROM products WHERE product_id=%s;",
            [product_id])
    except Exception as e:
        print "Exception: ", e
        return None

    productData = productDatabase.fetchone()

    if productData:
        formattedProductData = {}
        for i in range(len(productColumnMappings)):
            formattedProductData[productColumnMappings[i]] = productData[i]
        return formattedProductData
    else:
        return None


# load single product by product_id
def loadProductBySKU(variantSKU, productDatabase):
    variantData = None
    if len(variantSKU.split('-')) == 1:
        productDatabase.execute(
            """SELECT product_id,stripe_id,VariantSKU,CAST(VariantPrice AS CHAR),VariantCompareAtPrice,VariantInventoryQty,VariantTaxable,VariantWeightUnit,VariantGrams,Title,BodyHTML,Vendor,Type,Tags,Published,ImageSrc,ImageAltText,VariantTypes,resources FROM products WHERE VariantSKU=%s;""",
            (variantSKU,))
    else:
        product_id = variantSKU.split('-')[0]
        variantData = loadProductVariantBySKU(variantSKU, productDatabase)
        productDatabase.execute(
            """SELECT product_id,stripe_id,VariantSKU,CAST(VariantPrice AS CHAR),VariantCompareAtPrice,VariantInventoryQty,VariantTaxable,VariantWeightUnit,VariantGrams,Title,BodyHTML,Vendor,Type,Tags,Published,ImageSrc,ImageAltText,VariantTypes,resources FROM products WHERE VariantSKU=%s;""",
            (product_id,))

    productData = productDatabase.fetchone()

    if productData:
        formattedProductData = {}
        for i in range(len(productColumnMappings)):
            formattedProductData[productColumnMappings[i]] = productData[i]

        if variantData:
            for field, value in variantData.iteritems():
                formattedProductData[field] = value

        return formattedProductData
    else:
        return None


def loadProductVariant(variant_id, productDatabase):
    currentQuery = """SELECT variant_id, VariantSKU, product_id, VariantData, VariantPrice, VariantCompareAtPrice, VariantGrams, VariantWeightUnit, VariantInventoryQty,
				      VariantImg, VariantTaxCode, VariantTaxable,VariantWeightUnit,VariantGrams, VariantBarcode, VariantRequiresShipping FROM product_variants WHERE variant_id = %s;"""
    try:
        productDatabase.execute(currentQuery, (variant_id,))
    except Exception as e:
        print "Error: ", e
        return None

    variantData = productDatabase.fetchone()

    # format the variant data for easy access in the templates
    if variantData:
        formattedVariantData = {}
        for i in range(len(variantColumnMappings)):
            formattedVariantData[variantColumnMappings[i]] = variantData[i]
        return formattedVariantData

    else:
        return None


def loadProductVariants(product_id, productDatabase):
    currentQuery = """SELECT variant_id, VariantSKU, product_id, VariantData, VariantPrice, VariantCompareAtPrice, VariantGrams, VariantWeightUnit, VariantInventoryQty,
				      VariantImg, VariantTaxCode, VariantTaxable,VariantWeightUnit,VariantGrams, VariantBarcode, VariantRequiresShipping FROM product_variants WHERE product_id = %s;"""
    try:
        productDatabase.execute(currentQuery, (product_id,))
    except Exception as e:
        print "Error: ", e
        return None

    variantData = productDatabase.fetchall()

    formattedVariantData = []

    # format the variant data for easy access in the templates
    if variantData:
        for i in range(len(variantData)):
            formattedVariantData.append({})
            for j in range(len(variantColumnMappings)):
                formattedVariantData[i][variantColumnMappings[j]] = variantData[i][j]
        return formattedVariantData

    else:
        return []


# loads a variant by it's SKU
def loadProductVariantBySKU(VariantSKU, productDatabase):
    currentQuery = """SELECT variant_id, VariantSKU, product_id, VariantData, VariantPrice, VariantCompareAtPrice, VariantGrams, VariantWeightUnit, VariantInventoryQty,
				      VariantImg, VariantTaxCode, VariantTaxable,VariantWeightUnit,VariantGrams, VariantBarcode, VariantRequiresShipping FROM product_variants WHERE VariantSKU = %s;"""
    try:
        productDatabase.execute(currentQuery, (VariantSKU,))
    except Exception as e:
        print "Error: ", e
        return None

    variantData = productDatabase.fetchone()

    # format the variant data for easy access in the templates
    if variantData:
        formattedVariantData = {}
        for i in range(len(variantColumnMappings)):
            formattedVariantData[variantColumnMappings[i]] = variantData[i]
        return formattedVariantData

    else:
        return None


# load all products and parse columns into dictionary format for easy hashing
def loadAllProducts(productDatabase):
    formattedProductList = collections.OrderedDict()

    # select all products in database, including variants
    productDatabase.execute(
        """SELECT product_id,stripe_id,VariantSKU,CAST(VariantPrice AS CHAR),VariantCompareAtPrice,VariantInventoryQty,VariantTaxable,VariantWeightUnit,VariantGrams,Title,BodyHTML,Vendor,Type,Tags,Published,ImageSrc,ImageAltText,VariantTypes,resources FROM products;""")

    productList = productDatabase.fetchall()

    for i in range(len(productList)):
        currentProductID = str(productList[i][0])
        formattedProductList[currentProductID] = {}  # create a new dictionary for each product

        # go through the list of key names (set in config.py file) and assign values to their respective keys
        for j in range(len(productColumnMappings)):
            formattedProductList[currentProductID][productColumnMappings[j]] = productList[i][j]

    return formattedProductList


# load all product variants and parses them columns into dictionary format for easy hashing
def loadAllProductVariants(formattedProductList, productDatabase):
    formattedVariantList = collections.OrderedDict()

    for product_id, product in formattedProductList.iteritems():
        currentProductVariants = loadProductVariants(product_id, productDatabase)
        if currentProductVariants is not None:
            formattedVariantList[product_id] = currentProductVariants

    return formattedVariantList


def loadCollection(collectionID, productDatabase):
    try:
        productDatabase.execute(
            "SELECT collection_id,Title,BodyHTML,CollectionImageSrc,Published,Conditions,Strict,URL,Meta,PageTitle,Template,resources FROM collections WHERE collection_id=%s;",
            (collectionID,));
    except Exception as e:
        return None

    collection = productDatabase.fetchone()

    if collection:
        formattedCollection = {}
        for i in range(len(collectionColumnMappings)):
            formattedCollection[collectionColumnMappings[i]] = collection[i]

        return formattedCollection


# loads a list of collections for the product collections page
def loadCollections(productDatabase):
    try:
        productDatabase.execute(
            "SELECT collection_id,Title,BodyHTML,CollectionImageSrc,Published,Conditions,Strict,URL,Meta,PageTitle,Template,resources FROM collections;")
    except Exception as e:
        return None
    collectionList = productDatabase.fetchall()

    if collectionList:
        formattedCollectionList = []

        for i in range(len(collectionList)):
            formattedCollectionList.append({})
            for j in range(len(collectionColumnMappings)):
                formattedCollectionList[i][collectionColumnMappings[j]] = collectionList[i][j]
        return formattedCollectionList
    else:
        return None


def loadProductsByID(productIDList, productDatabase):
    placeholders = ','.join(['%s' for _ in productIDList])
    q = "SELECT product_id,stripe_id,VariantSKU,CAST(VariantPrice as char),VariantCompareAtPrice,VariantInventoryQty,VariantTaxable,VariantWeightUnit,VariantGrams,Title,BodyHTML,Vendor,Type,Tags,Published,ImageSrc,ImageAltText,VariantTypes,resources FROM products WHERE product_id IN (%s);" % placeholders

    try:
        productDatabase.execute(q, productIDList)
    except Exception as e:
        print "Couldn't retreive product data: ", e
        return None

    productList = productDatabase.fetchall()

    if productList:
        formattedProductList = {}
        for i in range(len(productList)):
            currentProductID = str(productList[i][0])
            formattedProductList[currentProductID] = {}  # create a new dictionary for each product

            # go through the list of key names (set in config.py file) and assign values to their respective keys
            for j in range(len(productColumnMappings)):
                formattedProductList[currentProductID][productColumnMappings[j]] = productList[i][j]

        return formattedProductList
    else:
        return None


# load products meeting certain collection conditions
def loadProductsInCollection(collectionConditions, collectionStrict, productDatabase):
    productSetList = []

    print "Trying to load products that match: ", collectionConditions

    if len(collectionConditions) == 0:
        return None

    for condition_id, condition in collectionConditions.iteritems():
        conditionType = condition["type"]
        conditionValue = condition["value"]
        conditionRule = condition["rule"]

        if conditionValue == "":
            productSetList.append(set([]))
            continue

        conditionRule = condition["rule"]

        # find products that match the title conditions
        if conditionType == "Title":
            q = "SELECT product_id FROM products WHERE Title LIKE CONCAT('%%', %s, '%%');"
            try:
                productDatabase.execute(q, (conditionValue.lower(),))
            except Exception as e:
                print "Error getting products by title: ", e
                return None

            products = productDatabase.fetchall()

            if products:
                products = [product[0] for product in products]
                productSet = set(products)
                productSetList.append(productSet)
            else:
                productSetList.append(set([]))


        # find products that match the tag conditions
        elif conditionType == "Tag":
            if conditionRule == "=":
                q = "SELECT product_id FROM products WHERE Tags REGEXP CONCAT('[,]?', %s, '[,]?');"

            try:
                productDatabase.execute(q, (conditionValue.lower(),))
            except Exception as e:
                print "Error getting products by tag: ", e
                return None

            products = productDatabase.fetchall()

            if products:
                products = [product[0] for product in products]
                productSet = set(products)
                productSetList.append(productSet)
            else:
                productSetList.append(set([]))


        # find products that match the tag conditions
        elif conditionType == "Type":
            if conditionRule == "=":
                q = "SELECT product_id FROM products WHERE Type = %s;"

            try:
                productDatabase.execute(q, (conditionValue,))
            except Exception as e:
                print "Error getting products by type: ", e
                return None

            products = productDatabase.fetchall()

            if products:
                products = [product[0] for product in products]
                productSet = set(products)
                productSetList.append(productSet)
            else:
                productSetList.append(set([]))


        # find products that match the tag conditions
        elif conditionType == "Price":

            # conditionValue = float(conditionValue)
            print "price value: ", conditionValue

            if conditionRule == "=":
                q = "SELECT product_id FROM products WHERE VariantPrice = %s;"
            elif conditionRule == ">":
                q = "SELECT product_id FROM products WHERE VariantPrice > %s;"
            elif conditionRule == "<":
                q = "SELECT product_id FROM products WHERE VariantPrice < %s;"
            elif conditionRule == "<=":
                q = "SELECT product_id FROM products WHERE VariantPrice <= %s;"
            elif conditionRule == ">=":
                q = "SELECT product_id FROM products WHERE VariantPrice <= %s;"

            try:
                productDatabase.execute(q, (conditionValue,))
            except Exception as e:
                print "Error getting products by price: ", e
                return None

            products = productDatabase.fetchall()

            if products:
                products = [product[0] for product in products]
                productSet = set(products)
                productSetList.append(productSet)
            else:
                productSetList.append(set([]))

    if len(productSetList) > 0:
        if collectionStrict:
            return list(set.intersection(*productSetList))
        else:
            return list(set.union(*productSetList))
    else:
        return []


def saveProductTags(product_id, product_tags, productDatabase):
    currentQuery = "UPDATE products SET Tags=%s WHERE product_id=%s;"

    try:
        productDatabase.execute(currentQuery, (product_tags, product_id,))
    except Exception as e:
        print "Error: ", e
        return None

    return True


def saveProductVendors(vendorData, productDatabase):
    for vendor_id, vendor in vendorData.iteritems():

        q = "INSERT INTO vendors(vendor_id, Name, Phone, URL, Email) VALUES(%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE vendor_id=%s, NAME=%s, Phone=%s, URL=%s, Email=%s;"

        try:
            productDatabase.execute(q, (
            vendor_id, vendor["Name"], vendor["Phone"], vendor["URL"], vendor["Email"], vendor_id, vendor["Name"],
            vendor["Phone"], vendor["URL"], vendor["Email"]))
        except Exception as e:
            print "Error with: ", q
            print "Error updating vendors: ", e
            return False

    return True


# returns a list of product variants given a product id
def findProductVariants(product_id, productDatabase):
    currentQuery = "SELECT variant_id FROM product_variants WHERE product_id = %s;"

    try:
        productDatabase.execute(currentQuery, (product_id,))
    except Exception as e:
        print "Error: ", e
        return None

    variants = productDatabase.fetchall()
    variantIDList = []

    if variants:
        for i in range(len(variants)):
            variantIDList.append(variants[i][0])
        return variantIDList
    else:
        return None


def findTotalProductStock(product_id, productDatabase):
    currentQuery = "SELECT VariantInventoryQty FROM product_variants WHERE product_id=%s;"
    try:
        productDatabase.execute(currentQuery, (product_id,))
    except Exception as e:
        print e

    stockList = productDatabase.fetchall()
    if stockList:
        variantCount = len(stockList)
        totalStock = reduce(lambda x, y: x + y, [int(stock[0]) for stock in stockList])

        return (variantCount, totalStock)


# save changes to product description, title, and other things later on
def saveProductData(productData, productDatabase):
    orderedFields = collections.OrderedDict()
    fieldUpdates = ""

    for field, value in productData.iteritems():
        # ensures that data types are preserved properly
        if field == "product_id":
            product_id = int(value)
            continue
        else:
            orderedFields[field] = value
            fieldUpdates += field + "=%s,"

    fieldUpdates = fieldUpdates[:-1]

    valueList = [value for field, value in orderedFields.iteritems()]
    valueList.append(product_id)

    currentQuery = "UPDATE products SET %s WHERE product_id=" % fieldUpdates  # pop in the fieldUpdates for this query
    currentQuery += "%s;"

    print currentQuery

    try:
        productDatabase.execute(currentQuery, valueList)  # run current query
    except Exception as e:
        print "Exception:", e


def saveProductVariantTypes(product_data, variantTypes, productDatabase):
    currentQuery = """UPDATE products SET VariantTypes=%s WHERE product_id=%s;"""

    formattedVariantTypes = ""

    for variantType, values in variantTypes.iteritems():
        formattedVariantTypes += variantType + ":" + ",".join(values) + ";"

    product_id = product_data["product_id"]

    try:
        productDatabase.execute(currentQuery, (formattedVariantTypes[:-1], product_id,))
    except Exception as e:
        print e

    # delete old variants that are incompatible
    if formattedVariantTypes != "":
        deleteInvalidVariants(product_id, productDatabase)
    else:
        deleteAllVariants(product_id, productDatabase)


def deleteAllVariants(product_id, productDatabase):
    currentQuery = "DELETE FROM product_variants WHERE product_id=%s;"

    try:
        productDatabase.execute(currentQuery, (product_id,))
    except Exception as e:
        print "Exception: ", e


def deleteInvalidVariants(product_id, productDatabase):
    currentQuery = "SELECT VariantTypes FROM products WHERE product_id=%s;"

    try:
        productDatabase.execute(currentQuery, (product_id,))
    except Exception as e:
        print "Exception: ", e

    variantTypes = productDatabase.fetchone()
    if variantTypes:
        variantTypes = variantTypes[0].split(';')

    currentVariantTypes = {}

    for variantType in variantTypes:
        variantType = variantType.split(':')
        option = variantType[0]
        values = variantType[1].split(',')
        currentVariantTypes[option] = values

    variants = loadProductVariants(product_id, productDatabase)

    if variants:
        for variant in variants:
            currentOptions = variant["VariantData"].split(';')
            for option in currentOptions:
                option = option.split(':')
                optionName = option[0]
                optionValue = option[1]
                if optionValue not in currentVariantTypes[optionName]:
                    deleteVariant(variant["variant_id"], productDatabase)
                    continue


# saves a new product to the database
def saveNewProductData(productData, productDatabase):
    currentQuery = "INSERT INTO products(Title, ImageSrc, stripe_id) VALUES(%s, %s, %s);"
    defaultImageID = "1"

    productTuple = (productData["Title"], defaultImageID, productData["stripe_id"])

    try:
        productDatabase.execute(currentQuery, productTuple)
    except Exception as e:
        print "Error creating product: ", e

    try:
        productDatabase.execute("SELECT LAST_INSERT_ID();")
    except Exception as e:
        print "Exception: ", e

    product_id = productDatabase.fetchone()[0]
    currentQuery = """UPDATE products SET VariantSKU=%s WHERE product_id = %s;"""

    try:
        productDatabase.execute(currentQuery, (product_id, product_id,))
    except Exception as e:
        print e

    if product_id:
        return product_id


# saves a new product to the database
def saveNewCollectionData(collectionData, productDatabase):
    currentQuery = "INSERT INTO collections(Title, CollectionImageSrc) VALUES(%s, %s);"
    defaultImageID = "1"

    collectionTuple = (collectionData["Title"], defaultImageID,)

    try:
        productDatabase.execute(currentQuery, collectionTuple)
    except Exception as e:
        print "Error creating product: ", e

    try:
        productDatabase.execute("SELECT LAST_INSERT_ID();")
    except Exception as e:
        print "Exception: ", e

    collection_id = productDatabase.fetchone()[0]

    if collection_id:
        return collection_id


# save a new type of product variant based on variant options specified in product editor
def saveNewVariantData(productData, variantData, productDatabase):
    currentQuery = "INSERT INTO product_variants(product_id, stripe_id, VariantSKU, VariantData, VariantPrice, VariantImg, VariantRequiresShipping, VariantWeightUnit) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"

    formattedVariantData = ""
    formattedVariantSKU = str(productData["product_id"])

    for variantOption, variantValue in variantData["attributes"].iteritems():
        formattedVariantData += variantOption + ":" + variantValue + ";"
        formattedVariantSKU += "-" + variantValue.replace(' ', '-').lower()

    try:
        productDatabase.execute(currentQuery, (
        productData["product_id"], variantData["stripe_id"], formattedVariantSKU, formattedVariantData[:-1],
        productData["VariantPrice"], productData["ImageSrc"], "true", "lb"))
    except Exception as e:
        print "Error: ", e


# save changes from product inventory editor
def saveProductVariantData(variantData, productDatabase):
    orderedFields = collections.OrderedDict()
    fieldUpdates = ""

    for field, value in variantData.iteritems():
        # ensures that data types are preserved properly
        if field == "variant_id":
            variant_id = int(value)
            continue
        else:
            orderedFields[field] = value
            fieldUpdates += field + "=%s,"

    fieldUpdates = fieldUpdates[:-1]

    valueList = [value for field, value in orderedFields.iteritems()]
    valueList.append(variant_id)

    currentQuery = "UPDATE product_variants SET %s WHERE variant_id =" % fieldUpdates  # pop in the fieldUpdates for this query
    currentQuery += " %s;"

    print currentQuery, ":", valueList

    try:
        productDatabase.execute(currentQuery, valueList)  # run current query
    except Exception as e:
        print "Exception:", e
        return False

    return True


# update collection data, including conditions
def saveCollectionData(collectionData, productDatabase):
    orderedFields = collections.OrderedDict()
    fieldUpdates = ""

    for field, value in collectionData.iteritems():
        # ensures that data types are preserved properly
        if field == "collection_id":
            collection_id = int(value)
            continue
        elif field == "Conditions":
            value = formatCollectionConditions(value)
            orderedFields[field] = value
            fieldUpdates += field + "=%s,"
        else:
            orderedFields[field] = value
            fieldUpdates += field + "=%s,"

    fieldUpdates = fieldUpdates[:-1]

    valueList = [value for field, value in orderedFields.iteritems()]
    valueList.append(collection_id)

    currentQuery = "UPDATE collections SET %s WHERE collection_id =" % fieldUpdates  # pop in the fieldUpdates for this query
    currentQuery += " %s;"

    print currentQuery, ":", valueList

    try:
        productDatabase.execute(currentQuery, valueList)  # run current query
    except Exception as e:
        print "Exception:", e


def setDefaultProductImage(product_id, resource_id, productDatabase):
    currentQuery = "UPDATE products SET ImageSrc=%s WHERE product_id=%s;"
    try:
        productDatabase.execute(currentQuery, (resource_id, product_id,))
    except Exception as e:
        print "Exception: ", e
        return None

    return True


def updateProductInventory(product_id, inventory_qty, productDatabase):
    currentQuery = "UPDATE products SET VariantInventoryQty=%s WHERE product_id=%s;"

    try:
        productDatabase.execute(currentQuery, (inventory_qty, product_id,))
    except Exception as e:
        print "Error: ", e
        return None

    return True


def updateProductResources(product_id, resource_id, resource_type, productDatabase):
    currentQuery = "SELECT resources FROM products WHERE product_id=%s;"
    try:
        productDatabase.execute(currentQuery, (product_id,))
    except Exception as e:
        print "Exception: ", e
        return None

    resourceDict = {}

    resources = productDatabase.fetchone()[0]
    if resources:
        resources = filter(lambda r: r != '', resources.split(','))

        for resource in resources:
            resource = resource.split(':')
            if resource[0] in resourceDict:
                resourceDict[resource[0]] += " " + resource[1]
            else:
                resourceDict[resource[0]] = resource[1]

        resourceDict[resource_type] += " " + str(resource_id)
    elif resources is None or resources == "":
        resourceDict[resource_type] = str(resource_id)
        # if this is the first picture they upload, set it to default
        if (resource_type) == "product_image":
            setDefaultProductImage(product_id, resource_id, productDatabase)

    formattedResourceString = ""

    for resource_type, resource_ids in resourceDict.iteritems():
        formattedResourceString += (resource_type + ":" + resource_ids + ",")

    currentQuery = "UPDATE products SET resources=%s WHERE product_id=%s;"
    print "Query:", currentQuery
    try:
        productDatabase.execute(currentQuery, (formattedResourceString, product_id,))
    except Exception  as e:
        print "Exception: ", e
        return None

    return True


def updateProductVariantResources(variant_id, resource_id, productDatabase):
    currentQuery = "UPDATE product_variants SET VariantImg=%s WHERE variant_id=%s;"

    print "Query:", currentQuery
    try:
        productDatabase.execute(currentQuery, (resource_id, variant_id,))
    except Exception  as e:
        print "Exception: ", e
        return None

    return True


def updateCollectionImage(collection_id, resource_id, productDatabase):
    currentQuery = "UPDATE collections SET CollectionImageSrc=%s WHERE collection_id=%s;"

    try:
        productDatabase.execute(currentQuery, (str(resource_id), collection_id,))
    except Exception  as e:
        print "Exception: ", e
        return None

    return True


# deletes a single product from the database
def deleteProduct(product_id, productDatabase):
    try:
        productDatabase.execute("DELETE FROM products WHERE product_id=%s;", (product_id,))
        productDatabase.execute("DELETE FROM product_variants WHERE product_id=%s;", (product_id,))
    except Exception as e:
        print "Exception:", e
        return None

    return True


# deletes a single collection from the database
def deleteCollection(collection_id, productDatabase):
    try:
        productDatabase.execute("DELETE FROM collections WHERE collection_id=%s;", (collection_id,))
    except Exception as e:
        print "Exception:", e
        return None

    return True


# deletes a single variant from the database
def deleteVariant(variant_id, productDatabase):
    currentQuery = "DELETE FROM product_variants WHERE variant_id=%s;"
    try:
        productDatabase.execute(currentQuery, (variant_id,))
    except Exception as e:
        print e
        return None

    return True


def bulkUpdateProducts(productData, productDatabase):
    # iterates through a dictionary of product data and updates product db
    print "attempting to bulk update products."
    # product data is represented as a dictionary of dictionaries, with each field in the main dict representing a different product
    for product_id, currentProductData in productData.iteritems():
        fieldUpdates = ""

        # each subdictionary contains fields correspending to database columns to allow easy indexing and dynamic query building
        for field, value in currentProductData.iteritems():

            # ensures that data types are preserved properly
            if productFieldMapping[field] == "TEXT":
                fieldUpdates += (field + "=\"" + value + "\",")
            elif productFieldMapping[field] == "INTEGER":
                fieldUpdates += (field + "=" + value + ",")
            elif productFieldMapping[field] == "REAL":
                fieldUpdates += (field + "=" + value + ",")
            else:
                fieldUpdates += (field + "=\"" + value + "\",")

        fieldUpdates = fieldUpdates[:-1]  # remove the last comma
        currentQuery = "UPDATE products SET %s WHERE product_id = %s;" % (
        fieldUpdates, product_id)  # pop in the fieldUpdates for this query
        print "q: ", currentQuery
        try:
            productDatabase.execute(currentQuery)  # run current query
        except Exception as e:
            print e


def bulkUpdateVariants(variantData, productDatabase):
    # iterates through a dictionary of product data and updates product db

    # variant data is represented as a dictionary of dictionaries, with each field in the main dict representing a different product
    for variant_id, currentVariantData in variantData.iteritems():
        fieldUpdates = ""

        # each subdictionary contains fields correspending to database columns to allow easy indexing and dynamic query building
        for field, value in currentVariantData.iteritems():

            # ensures that data types are preserved properly
            if variantFieldMapping[field] == "TEXT":
                fieldUpdates += (field + "=\"" + value + "\",")
            elif variantFieldMapping[field] == "INTEGER":
                fieldUpdates += (field + "=" + value + ",")
            elif variantFieldMapping[field] == "REAL":
                fieldUpdates += (field + "=" + value + ",")
            else:
                fieldUpdates += (field + "=\"" + value + "\",")

        fieldUpdates = fieldUpdates[:-1]  # remove the last comma
        currentQuery = "UPDATE product_variants SET %s WHERE variant_id = %s;" % (
        fieldUpdates, variant_id)  # pop in the fieldUpdates for this query

        print currentQuery
        try:
            productDatabase.execute(currentQuery)  # run current query
        except Exception as e:
            print e


def bulkUpdateCollections(collectionData, productDatabase):
    # iterates through a dictionary of collection data and updates product db

    # collection data is represented as a dictionary of dictionaries, with each field in the main dict representing a different product
    for collection_id, currentCollectionData in collectionData.iteritems():
        fieldUpdates = ""

        # each subdictionary contains fields correspending to database columns to allow easy indexing and dynamic query building
        for field, value in currentCollectionData.iteritems():

            # ensures that data types are preserved properly
            if collectionFieldMapping[field] == "TEXT":
                fieldUpdates += (field + "=\"" + value + "\",")
            elif collectionFieldMapping[field] == "INTEGER":
                fieldUpdates += (field + "=" + value + ",")
            elif collectionFieldMapping[field] == "REAL":
                fieldUpdates += (field + "=" + value + ",")
            else:
                fieldUpdates += (field + "=\"" + value + "\",")

        fieldUpdates = fieldUpdates[:-1]  # remove the last comma
        currentQuery = "UPDATE collections SET %s WHERE collection_id = %s;" % (
        fieldUpdates, collection_id)  # pop in the fieldUpdates for this query

        print currentQuery
        try:
            productDatabase.execute(currentQuery)  # run current query
        except Exception as e:
            print e


# sets all products in the list of product ids to either published or hidden (based on value="true" or "false")
def bulkPublish(value, product_id_list, productDatabase):
    product_id_list = map(int, product_id_list)

    placeholder = "%s"
    placeholders = ','.join(placeholder for _ in product_id_list)

    currentQuery = "UPDATE products SET Published=%s"
    currentQuery += " WHERE product_id IN(%s)" % (placeholders)

    values = [value] + product_id_list

    try:
        productDatabase.execute(currentQuery, values)
    except Exception as e:
        print e


# deletes a product and all of it's variants from the database
def bulkDelete(products, productDatabase):
    products = map(int, products)
    placeholder = "%s"
    fullProductList = []

    for i in range(len(products)):
        productData = loadProduct(products[i], productDatabase)
        variantIDList = findProductVariants(products[i], productDatabase)
        if variantIDList:
            fullProductList += variantIDList

    if fullProductList != []:
        placeholders = ','.join(placeholder for unused in fullProductList)
        currentQuery = "DELETE FROM products WHERE product_id IN (%s);" % placeholders
        values = fullProductList
    else:
        placeholders = ','.join(placeholder for unused in products)
        currentQuery = "DELETE FROM products WHERE product_id IN (%s);" % placeholders
        values = products

    try:
        productDatabase.execute(currentQuery, values)
    except Exception as e:
        print e
