import sqlite3 as sql

go = True
valid = False

def main():
    global valid

    create_db()

    print_menu()
    while go:
        print()
        if valid:
            print('To view menu, enter "m"')
        valid = False
        while valid != True:
            selection = input('What would you like to do? ').lower()
            validate(selection)
        print()
        use_selection(selection)


def create_db():
    execute_sql('create table if not exists jugglers (name text, record integer)')


def execute_sql(string):
    cnct = sql.connect('juggler_db.sqlite')
    cnct.execute(string)
    cnct.commit()
    cnct.close()


def execute_sql_with_parameters(string, parameter_one, parameter_two):
    cnct = sql.connect('juggler_db.sqlite')
    cnct.execute(string, (parameter_one, parameter_two))
    cnct.commit()
    cnct.close()


def print_menu():
    print('Available options:')
    print('(A)dd a new record holder')
    print('(S)earch for a record by holder\'s name')
    print('(U)pdate the record')
    print('(D)elete a record holder')
    print('(Q)uit')


def validate(selection):
    global valid
    valid_options = ['m', 'a', 's', 'u', 'd', 'q']

    for option in valid_options:
        if selection == option:
            valid = True
    if valid != True:
        print('Invalid selection. Please try again.')


def use_selection(selection):
    if selection == 'm':
        print_menu()
    if selection == 'a':
        add_juggler()
    if selection == 's':
        search_jugglers()
    if selection == 'u':
        update_juggler()
    if selection == 'd':
        delete_juggler()
    if selection == 'q':
        quit()


def add_juggler():
    name = input('Juggler\'s name: ').upper()
    record = get_record()
    execute_sql_with_parameters('insert into jugglers values (?, ?)', name, record)


def search_jugglers():
    try:
        cnct = sql.connect('juggler_db.sqlite')
        name = input('Juggler\'s name: ').upper()
        record = cnct.execute('select * from jugglers where name = ?', (name, )).fetchone()[1]
        print('Juggler\'s record: ' + str(record))
        cnct.close()
    except TypeError:
        print('No juggler with that name.')


def update_juggler():
    name = input('Juggler\'s name: ').upper()
    record = get_record()
    deleted = execute_sql_with_parameters('update jugglers set record = ? where name = ?', record, name)
    if deleted != 1:
        print('No juggler with that name.')


def delete_juggler():
    cnct = sql.connect('juggler_db.sqlite')
    name = input('Juggler\'s name: ').upper()
    deleted = cnct.execute('delete from jugglers where name = ?', (name, ))
    if deleted != 1:
        print('No juggler with that name.')
    else:
        print('Deleted juggler: ' + name)
    cnct.commit()
    cnct.close()


def get_record():
    while True:
        try:
            record = int(input('Juggler\'s record: '))
            break;
        except ValueError:
            print('Please input an integer.')
    return record


def quit():
    global go
    go = False


main()
