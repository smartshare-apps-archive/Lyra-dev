# converts a sqlite db dump to a sql file for import into rds server

import re

# re.sub(pattern, repl, string, count=0, flags=0)
# re.search(pattern, string, flags=0)

sql_filters = {
    "create_table": r'CREATE\sTABLE\s\"([A-Za-z]+)\"\s\(',
    "begin_transaction": r'BEGIN\sTRANSACTION;',
    "commit": r'COMMIT;'
}


def filter_line(line):
    for sfilter, rc in sql_filters.iteritems():
        m = re.search(rc, line)

        if m:
            if sfilter == "create_table":
                table_name = m.group(1)
                filtered_line = "CREATE TABLE " + table_name + " (\n"
                return filtered_line

            elif sfilter == "begin_transaction":
                return "\n"
            elif sfilter == "commit":
                return "\n"

    return line


def write_file(f_array, OUT_FILE):
    with open(OUT_FILE, 'w') as fout:
        for line in f_array:
            try:
                fout.write(line)
            except Exception as e:
                print "Error: ", e
                return False

    return True


def lite2sql(IN_FILE):
    with open(IN_FILE) as fin:
        f_array = []
        for line in fin:
            filtered_line = filter_line(line)
            f_array.append(filtered_line)

        return f_array


def main():
    IN_FILE = "t.sql"
    OUT_FILE = "converted_t.sql"

    f_array = lite2sql(IN_FILE)

    r = write_file(f_array, OUT_FILE)

    if r:
        print "File converted successfully."
    else:
        print "There was an error converting this file."


if __name__ == "__main__": main()
