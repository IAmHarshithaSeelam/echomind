import csv
import sqlite3


con = sqlite3.connect("jarvis.db")

cursor = con.cursor()

# query =  "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100),path VARCHAR(1000))"
# cursor.execute(query)

# query ="INSERT INTO sys_command VALUES (null,'VS code','C:\\Users\\91830\\AppData\\Local\\Programs\\Microsoft VS Code\\code.exe')"
# cursor.execute(query)
# con.commit()

# query =  "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100),url VARCHAR(1000))"
# cursor.execute(query)

# query ="INSERT INTO web_command VALUES (null,'google','https://www.google.com/search?q=')"
# cursor.execute(query)
# con.commit()

  #detele database
# query = "DELETE FROM web_command WHERE name = 'google'"
# cursor.execute(query)
# con.commit()

   #url delete
# query = "DELETE FROM web_command WHERE url = 'https://www.google.com/search?q=your+query'"
# cursor.execute(query)
# con.commit()

# app_name = "android studio"
# cursor.execute(
#                 'SELECT path FROM sys_command WHERE name IN (?)',(app_name,))
# results = cursor.fetchall()
# print(results[0][0])
            
# cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')

# Specify the column indices you want to import (0-based index)
# Example: Importing the 1st and 3rd columns
# # Read the CSV and extract header
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     header = next(csvreader)  # Read header

#     # Get dynamic indices
#     try:
#         name_index = header.index('First Name')
#         phone_index = header.index('Phone 1 - Value')
#     except ValueError as e:
#         print(f"Column not found in header: {e}")
#         con.close()
#         exit()

#     print(f"Using name_index={name_index}, phone_index={phone_index}")

#     for row_number, row in enumerate(csvreader, start=2):  # start from 2 due to header
#         if len(row) <= max(name_index, phone_index):
#             print(f"Skipped row {row_number} (not enough columns): {row}")
#             continue

#         name = row[name_index].strip()
#         mobile_no = row[phone_index].strip()

#         if not name or not mobile_no:
#             print(f"Skipped row {row_number} (empty name or number): {row}")
#             continue

#         try:
#             cursor.execute(
#                 '''INSERT INTO contacts (name, mobile_no) VALUES (?, ?);''',
#                 (name, mobile_no)
#             )
#             print(f"Inserted row {row_number}: {name}, {mobile_no}")
#         except sqlite3.Error as e:
#             print(f"Error inserting row {row_number}: {e}")

# # Save and close
# con.commit()
# con.close()
# print("Data processing completed successfully and stored in Jarviss.db.")



# single contact adding

# query = "INSERT INTO contacts VALUES (null,'ram mamayya', '9666452224',null)"
# cursor.execute(query)
# con.commit()

# search contacts frpm db
# query = 'mummy'
# query = query.strip().lower()

# cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
# results = cursor.fetchall()
# print(results[0][0])

# =COLUMN(AE1)