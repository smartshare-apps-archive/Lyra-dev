import sqlite3, sys, csv, json, collections

from product import *
from product_util import *
from customer import *
from event import *
from order_util import *

import resources
import config


# grabs the main navigation categories, which can themselves have submenus
# this allows for dynamic navigation bars
def getNavCategories(cursor):
    query = "SELECT Name, Data FROM store WHERE Type='nav_bar_link'"
    cursor.execute(query)

    nav_links = cursor.fetchall()

    nav_dict = {}
    if nav_links:
        for nav_link in nav_links:
            nav_dict[nav_link[0]] = nav_link[1].split(',')
    return nav_dict


def createNavCategory(nav_category, nav_data, database):
    newCategory = nav_category
    insert_type = "nav_bar_link"
    data_string = "resource_id:" + str(nav_data["resource_id"]) + ",type:" + nav_data["type"]

    currentQuery = "INSERT INTO store(Name, Type, Data) VALUES(%s,%s,%s);"

    try:
        database.execute(currentQuery, (newCategory, insert_type, data_string,))
    except Exception as e:
        print "Error: ", e
        return False


def updateNavData(navData, database):
    for nav_category, nav_data in navData.iteritems():
        if (navData[nav_category]["action"] == "delete"):
            deleteQuery = "DELETE FROM store WHERE Name=%s;"

            try:
                database.execute(deleteQuery, (nav_category,))
            except Exception as e:
                print "Error: ", e
                return False

            continue
        elif (navData[nav_category]["action"] == "insert"):

            resource_id = resources.createResource(nav_data["data"], "local_link", database)
            nav_data["resource_id"] = resource_id

            result = createNavCategory(nav_category, nav_data, database)
            print "Result: ", result
            continue

        resourceQuery = "UPDATE resources SET resource_uri=%s WHERE resource_id=%s;"

        new_resource_uri = nav_data["data"]
        resource_id = nav_data["resource_id"]
        initial_category = nav_data["initial_category"]
        print "initial category:", initial_category
        print "New: ", new_resource_uri, ":", resource_id

        try:
            database.execute(resourceQuery, (new_resource_uri, resource_id,))
        except Exception as e:
            print "Error: ", e
            return False

        resourceQuery = "UPDATE store SET Name=%s WHERE NAME=%s;"

        try:
            database.execute(resourceQuery, (nav_category, initial_category,))
        except Exception as e:
            print "Error: ", e
            return False


# grabs the main footer categories, which can themselves have submenus
# this allows for dynamic footers
def getFooterCategories(database):
    currentQuery = "SELECT Name, Data FROM store WHERE Type='footer_link';"

    try:
        database.execute(currentQuery)
    except Exception as e:
        print e
        return None

    footer_links = database.fetchall()
    # print nav_links
    if footer_links:
        footer_dict = {footer_link[0]: footer_link[1] for footer_link in footer_links}

        for footer_category, footer_data in footer_dict.iteritems():
            footer_dict[footer_category] = footer_data.split(',')

        return footer_dict
    else:
        return {}


def createFooterCategory(footer_category, footer_data, database):
    newCategory = footer_category
    insert_type = "footer_link"
    data_string = "resource_id:" + str(footer_data["resource_id"]) + ",type:" + footer_data["type"]

    currentQuery = "INSERT INTO store(Name, Type, Data) VALUES(%s,%s,%s);"

    try:
        database.execute(currentQuery, (newCategory, insert_type, data_string,))
    except Exception as e:
        print "Error: ", e
        return False


def updateFooterData(footerData, database):
    for footer_category, footer_data in footerData.iteritems():
        if (footerData[footer_category]["action"] == "delete"):
            deleteQuery = "DELETE FROM store WHERE Name=%s AND Type='footer_link';"

            try:
                database.execute(deleteQuery, (footer_category,))
            except Exception as e:
                print "Error: ", e
                return False
            continue

        elif (footerData[footer_category]["action"] == "insert"):

            resource_id = resources.createResource(footer_data["data"], "local_link", database)
            footer_data["resource_id"] = resource_id

            result = createFooterCategory(footer_category, footer_data, database)
            print "Result: ", result
            continue

        resourceQuery = "UPDATE resources SET resource_uri=%s WHERE resource_id=%s;"

        new_resource_uri = footer_data["data"]
        resource_id = footer_data["resource_id"]
        initial_category = footer_data["initial_category"]
        print "initial category:", initial_category
        print "New: ", new_resource_uri, ":", resource_id

        try:
            database.execute(resourceQuery, (new_resource_uri, resource_id,))
        except Exception as e:
            print "Error: ", e
            return False

        resourceQuery = "UPDATE store SET Name=%s WHERE NAME=%s AND Type='footer_link';"

        try:
            database.execute(resourceQuery, (footer_category, initial_category,))
        except Exception as e:
            print "Error: ", e
            return False


def getPageData(page_id, database):
    currentQuery = "SELECT Data FROM store WHERE Type='page_data' AND Name=%s;"

    try:
        database.execute(currentQuery, (page_id,))
    except Exception as e:
        print "Error: ", e
        return None

    page_data = database.fetchone()
    if page_data:
        return page_data[0]


def getPage(page_id, cursor):
    query = "SELECT Data FROM store WHERE Type='%s' AND Name='%s'"

    def get_result(store_type):
        # TODO: Check for SQL injections
        cursor.execute(query % (store_type, page_id))
        result = cursor.fetchone()
        return result[0] if result else ''

    page = dict(
        page_id=page_id,
        content=get_result('page_data'),
        template=get_result('page_template'),
        type=get_result('page_type'),
        title=get_result('page_title'),
        sections=get_result('page_sections'),
        section_data=get_result('page_section_data')
    )

    return page


def getPageIDs(database):
    currentQuery = "SELECT CONVERT(Data USING utf8) FROM store  WHERE Type='page_id';"

    try:
        database.execute(currentQuery)
    except Exception as e:
        print "Error getting pages: ", e

    page_id_list = database.fetchall()

    if page_id_list:
        return list(page_id[0] for page_id in page_id_list)
    else:
        return None


def getPages(database):
    currentQuery = "SELECT Data FROM store WHERE Type='page_id';"

    try:
        database.execute(currentQuery)
    except Exception as e:
        print "Error: ", e

    pageList = database.fetchall()
    if pageList:
        pages = {}
        for page in pageList:
            page = page[0]
            pages[page] = {}
            currentQuery = "SELECT Data FROM store WHERE Type='page_data' AND Name=%s;"
            try:
                database.execute(currentQuery, (page,))
                pages[page]["content"] = database.fetchone()[0]
            except:
                pages[page]["content"] = ""

            currentQuery = "SELECT Data FROM store WHERE Type='page_template' AND Name=%s;"
            try:
                database.execute(currentQuery, (page,))
                pages[page]["template"] = database.fetchone()[0]
            except:
                pages[page]["template"] = ""

            currentQuery = "SELECT Data FROM store WHERE Type='page_type' AND Name=%s;"
            try:
                database.execute(currentQuery, (page,))
                pages[page]["type"] = database.fetchone()[0]
            except:
                pages[page]["type"] = ""

            currentQuery = "SELECT Data FROM store WHERE Type='page_title' AND Name=%s;"
            try:
                database.execute(currentQuery, (page,))
                pages[page]["title"] = database.fetchone()[0]
            except:
                pages[page]["title"] = ""

            currentQuery = "SELECT Data FROM store WHERE Type='page_sections' AND Name=%s;"
            try:
                database.execute(currentQuery, (page,))
                pages[page]["sections"] = database.fetchone()[0]
            except:
                pages[page]["sections"] = ""

            currentQuery = "SELECT Data FROM store WHERE Type='page_section_data' AND Name=%s;"
            try:
                database.execute(currentQuery, (page,))
                pages[page]["section_data"] = database.fetchone()[0]
            except:
                pages[page]["section_data"] = ""

        return pages

    else:
        return None


# grabs basic page type data
def getPageTypes(database):
    currentQuery = "SELECT Name,Data FROM store WHERE Type='page_type_template';"
    try:
        database.execute(currentQuery)
    except Exception as e:
        print "Error: ", e
        return False

    pageTypes = database.fetchall()
    if pageTypes:
        formattedPageTypes = {}
        for page_type in pageTypes:
            page_id = page_type[0]
            formattedPageTypes[page_id] = {}
            page_data = page_type[1].split('<split>')
            for data_field in page_data:
                data_field = data_field.split('=')
                formattedPageTypes[page_id][data_field[0]] = data_field[1]

        return formattedPageTypes


# grabs all template data
def getPageTemplates(database):
    currentQuery = "SELECT Name,Data FROM store WHERE Type='template';"
    try:
        database.execute(currentQuery)
    except Exception as e:
        print "Error: ", e
        return False

    pageTemplates = database.fetchall()
    if pageTemplates:
        formattedPageTemplates = {}
        for page_template in pageTemplates:
            template_id = page_template[0]
            formattedPageTemplates[template_id] = {}
            template_data = filter(lambda t: t != '', page_template[1].split('<split>'))
            for data_field in template_data:
                data_field = data_field.split('=')
                formattedPageTemplates[template_id][data_field[0]] = data_field[1]

        return formattedPageTemplates


# grabs all section template data
def getSectionTemplates(database):
    currentQuery = "SELECT Name,Data FROM store WHERE Type='section_template';"
    try:
        database.execute(currentQuery)
    except Exception as e:
        print "Error: ", e
        return False

    sectionTemplates = database.fetchall()
    if sectionTemplates:
        formattedSectionTemplates = {}
        for section_template in sectionTemplates:
            section_id = section_template[0]
            formattedSectionTemplates[section_id] = {}

            section_data = filter(lambda t: t != '', section_template[1].split('<split>'))
            for data_field in section_data:
                data_field = data_field.split('=')
                formattedSectionTemplates[section_id][data_field[0]] = data_field[1]

        return formattedSectionTemplates


# grabs template data
def loadTemplateData(template_id, cursor):
    query = "SELECT Data FROM store WHERE Type='template' AND Name='%s'"
    # TODO: Check for SQL injections
    cursor.execute(query % template_id)

    template_data = cursor.fetchone()
    formattedTemplateData = {}

    if template_data:
        template_data = template_data[0]

        template_data = filter(lambda t: t != '', template_data.split('<split>'))
        for data_field in template_data:
            key, value = data_field.split('=')
            formattedTemplateData[key] = value

    return formattedTemplateData


def loadSectionTemplate(section_id, cursor):
    query = "SELECT Data FROM store WHERE Type='section_template' AND Name='%s'"
    # TODO: Check for SQL injections
    cursor.execute(query % section_id)
    result = cursor.fetchone()

    return result[0] if result else None


# grabs template data
def loadTypeTemplateData(template_id, database):
    query = "SELECT Data FROM store WHERE Type='page_type_template' AND Name='%s'"
    # TODO: Check for SQL injections
    database.execute(query % template_id)

    result = database.fetchone()
    if result:
        formattedTemplateData = {}
        template_data = filter(lambda t: t != '', result[0].split('<split>'))
        for data_field in template_data:
            key, value = data_field.split('=')
            formattedTemplateData[key] = value

        return formattedTemplateData


def updatePageData(page_data, database):
    page_id = page_data["page_id"]

    if "page_title" in page_data:
        page_title = page_data["page_title"]
        currentQuery = "UPDATE store SET Data=%s WHERE NAME=%s AND Type='page_title';"
        try:
            database.execute(currentQuery, (page_title, page_id,))
        except Exception as e:
            print "Error: ", e
            return False

    if "page_template" in page_data:
        page_template = page_data["page_template"]
        currentQuery = "UPDATE store SET Data=%s WHERE NAME=%s AND Type='page_template';"
        try:
            database.execute(currentQuery, (page_template, page_id,))
        except Exception as e:
            print "Error: ", e
            return False

    if "page_type" in page_data:
        page_type = page_data["page_type"]
        currentQuery = "UPDATE store SET Data=%s WHERE NAME=%s AND Type='page_type';"
        try:
            database.execute(currentQuery, (page_type, page_id,))
        except Exception as e:
            print "Error: ", e
            return False

    if "content" in page_data:
        page_content = page_data["content"]

        currentQuery = "UPDATE store SET Data=%s WHERE NAME=%s AND Type='page_data';"
        try:
            database.execute(currentQuery, (page_content, page_id,))
        except Exception as e:
            print "Error: ", e
            return False

    if "sections" in page_data:
        page_sections = ','.join(page_data["sections"])

        print "page sections: ", page_sections
        currentQuery = "UPDATE store SET Data=%s WHERE NAME=%s AND Type='page_sections';"
        try:
            database.execute(currentQuery, (page_sections, page_id))
        except Exception as e:
            print "Error: ", e
            return False


# updates all the section data for a page
def updatePageSectionData(page_section_data, page_id, database):
    currentQuery = "UPDATE store SET Data=%s WHERE NAME=%s AND Type='page_section_data';"
    try:
        database.execute(currentQuery, (page_section_data, page_id,))
    except Exception as e:
        print "Error: ", e
        return False


def createNewPage(page_data, database):
    page_id = page_data["page_id"]
    page_title = "default title"
    page_template = page_data["page_template"]
    page_type = page_data["page_type"]
    page_content = ""

    print "Page ID: ", page_id

    currentQuery = "INSERT INTO store(Name, Data, Type) VALUES(%s,%s,%s);"
    try:
        database.execute(currentQuery, (page_id, page_id, "page_id"))
    except Exception as e:
        print "Error: ", e
        return False

    currentQuery = "INSERT INTO store(Name, Data, Type) VALUES(%s,%s,%s);"
    try:
        database.execute(currentQuery, (page_id, page_title, "page_title"))
    except Exception as e:
        print "Error: ", e
        return False

    currentQuery = "INSERT INTO store(Name, Data, Type) VALUES(%s,%s,%s);"
    try:
        database.execute(currentQuery, (page_id, page_template, "page_template"))
    except Exception as e:
        print "Error: ", e
        return False

    currentQuery = "INSERT INTO store(Name, Data, Type) VALUES(%s,%s,%s);"
    try:
        database.execute(currentQuery, (page_id, page_type, "page_type"))
    except Exception as e:
        print "Error: ", e
        return False

    currentQuery = "INSERT INTO store(Name, Data, Type) VALUES(%s,%s,%s);"
    try:
        database.execute(currentQuery, (page_id, page_content, "page_data"))
    except Exception as e:
        print "Error: ", e
        return False

    currentQuery = "INSERT INTO store(Name, Data, Type) VALUES(%s,%s,%s);"
    try:
        database.execute(currentQuery, (page_id, "content", "page_sections"))
    except Exception as e:
        print "Error: ", e
        return False

    currentQuery = "INSERT INTO store(Name, Data, Type) VALUES(%s,%s,%s);"
    try:
        database.execute(currentQuery, (page_id, "", "page_section_data"))
    except Exception as e:
        print "Error: ", e
        return False


def deletePage(page_id, database):
    currentQuery = "DELETE FROM store WHERE Name=%s AND Type != 'page_type_template';"

    try:
        database.execute(currentQuery, (page_id,))
    except Exception as e:
        print "Error deleting: ", e
        return False
