from django.shortcuts import render
from main.models import Actor, UserSession
from main.populateDB import populate
from main.RS import *
import sqlite3
from openpyxl import Workbook


def populate_database(request):
    (m, g, a)=populate()
    message = 'It has been loaded ' + str(m) + ' movies; ' + str(g) + ' genres; ' + str(a) + ' actors.'
    return render(request, 'base_POPULATEDB.html', {'title': 'End of database load', 'message':message})

def index(request):
    #DELETE ALL UserSession with more than 24 hours since their date_created:
    user = UserSession.objects.get(session_id="1")
    reset_scores(user)
    add_year_score(user)
    add_duration_score(user)
    add_actors_score(user)
    add_genres_score(user)
    add_ratings_score(user)
    add_country_score(user)
    dict_ordered = dict(list(sorted(dictScores[user].items(), key=lambda item: (-item[1])))[:20])
    print(str(dict_ordered))


    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    # Execute a SELECT statement to retrieve data from the table
    c.execute('SELECT name FROM main_genre')

    # Get the column names and data from the cursor object
    data = c.fetchall()

    # Create a new Excel workbook and select the active worksheet
    wb = Workbook()
    ws = wb.active

    # Write the column headers to the first row of the worksheet

    # Write the data to the worksheet
    for row_num, row_data in enumerate(data, 2):
        for col_num, cell_value in enumerate(row_data, 1):
            ws.cell(row=row_num, column=col_num, value=cell_value)

    # Save the workbook to a file
    wb.save('mytable.xlsx')

    # Close the database connection
    conn.close()
    return render(request, 'base_INDEX.html')