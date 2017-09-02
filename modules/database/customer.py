import sqlite3, sys, csv, json, collections

# config current only has column/field mapping information, which will be specific to the import form (of the product csv), e.g. shopify
from config import *
from product import *
from order import *


# from product_util import *



def loadCustomer(customer_id, database):
    currentQuery = "SELECT customer_id,user_id,Email,Phone,ShippingFirstName,ShippingLastName,ShippingAddress1,ShippingAddress2,ShippingCity,ShippingState,ShippingPostalCode,ShippingCountry,BillingFirstName,BillingLastName,BillingAddress1,BillingAddress2,BillingCity,BillingState,BillingPostalCode,BillingCountry,Company,TotalSpent,LastOrder,accepts_marketing FROM customers WHERE customer_id = %s;"

    try:
        database.execute(currentQuery, (customer_id,))
    except Exception as e:
        print "Error: ", e
        return None

    customer = database.fetchone()

    if customer:
        formattedCustomerData = {}
        for i in range(len(customerColumnMappings)):
            formattedCustomerData[customerColumnMappings[i]] = customer[i]

        return formattedCustomerData


def loadAllCustomers(database):
    currentQuery = "SELECT customer_id,user_id,Email,Phone,ShippingFirstName,ShippingLastName,ShippingAddress1,ShippingAddress2,ShippingCity,ShippingState,ShippingPostalCode,ShippingCountry,BillingFirstName,BillingLastName,BillingAddress1,BillingAddress2,BillingCity,BillingState,BillingPostalCode,BillingCountry,Company,TotalSpent,LastOrder,accepts_marketing FROM customers ORDER BY customer_id DESC;"

    try:
        database.execute(currentQuery)
    except Exception as e:
        print "Error: ", e
        return None

    customers = database.fetchall()
    if customers:
        formattedCustomers = collections.OrderedDict()
        for customer in customers:
            currentCustomer = {}
            for i in range(len(customerColumnMappings)):
                currentCustomer[customerColumnMappings[i]] = customer[i]
            customer_id = currentCustomer["customer_id"]

            formattedCustomers[customer_id] = currentCustomer

        return formattedCustomers
    else:
        return {}


def saveCustomerData(customerData, database):
    fieldUpdates = ""

    for field, value in customerData.iteritems():
        # ensures that data types are preserved properly
        if field == "customer_id":
            customer_id = int(value)
            continue
        if customerFieldMapping[field] == "TEXT":
            fieldUpdates += (field + "=\"" + value + "\",")
        elif customerFieldMapping[field] == "INTEGER":
            fieldUpdates += (field + "=" + str(value) + ",")
        elif customerFieldMapping[field] == "REAL":
            fieldUpdates += (field + "=" + str(value) + ",")
        else:
            fieldUpdates += (field + "=\"" + value + "\",")

    fieldUpdates = fieldUpdates[:-1]  # remove the last comma
    currentQuery = "UPDATE customers SET %s WHERE customer_id =" % fieldUpdates  # pop in the fieldUpdates for this query

    currentQuery += "%s;"

    try:
        database.execute(currentQuery, (customer_id,))  # run current query
    except Exception as e:
        print "Exception:", e


def createCustomer(customer_info, order_details, database, user_data=None):
    fieldList = ""
    valueList = ""

    for field, value in customer_info.iteritems():
        if value == "":
            continue

        if customerFieldMapping[field] == "TEXT":
            value = "'" + value + "'"
        elif customerFieldMapping[field] == "INTEGER" or customerFieldMapping[field] == "REAL":
            value = value
        else:
            value = "'" + value + "'"

        fieldList += field + ","
        valueList += value + ","

    fieldList = fieldList[:-1]
    valueList = valueList[:-1]

    currentQuery = "INSERT INTO customers(%s) VALUES(%s);" % (fieldList, valueList)

    try:
        database.execute(currentQuery)
    except Exception as e:
        print "Error: ", e
        return None

    try:
        database.execute("SELECT LAST_INSERT_ID();")
    except Exception as e:
        print "Exception: ", e

    customer_id = database.fetchone()
    if customer_id:
        return customer_id[0]


def updateCustomer(customer_id, order_details, database):
    customer_data = loadCustomer(customer_id, database)
    totalSpent = customer_data["TotalSpent"]

    if totalSpent is not None:
        newTotalSpent = float(totalSpent) + float(order_details["OrderTotal"])
    else:
        newTotalSpent = float(order_details["OrderTotal"])

    currentQuery = "UPDATE customers SET TotalSpent=%s, LastOrder=%s WHERE customer_id=%s;"

    order_id = order_details["order_id"]

    try:
        database.execute(currentQuery, (newTotalSpent, order_id, customer_id,))
    except Exception as e:
        print "Error: ", e
        return None


# bulk functions

def bulkDeleteCustomers(customer_id_list, database):
    customer_id_list = map(int, customer_id_list)

    placeholder = '%s'
    placeholders = ','.join(placeholder for unused in customer_id_list)

    currentQuery = "DELETE FROM customers WHERE customer_id IN(%s);" % placeholders

    try:
        database.execute(currentQuery, customer_id_list)
    except Exception as e:
        print "Error: ", e
        return False

    return True
