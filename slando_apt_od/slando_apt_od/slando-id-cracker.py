import sqlite3

def main():
    connection = sqlite3.connect('/home/bepec/.db/slando.db')
    cursor = connection.cursor()
    cursor.execute('select id, num from offers')
    table = cursor.fetchall()
    unsorted_dict = { row[1]:row[0] for row in table }

    sorted_nums = sorted([row[1] for row in table])

    sorted_table = [(num, unsorted_dict[num]) for num in sorted_nums]
    print(sorted_table)

    diff_dict = dict()
    for i in range(1, len(sorted_table)-1):
        if sorted_table[i][1] < sorted_table[i-1][1]:
            print("{0} < {1}".format(sorted_table[i], sorted_table[i-1]))
        diff = sorted_table[i][0] - sorted_table[i-1][0]
        diff_dict[diff] = (sorted_table[i-1], sorted_table[i])

    diff_sorted_table = [(diff, diff_dict[diff]) for diff in sorted(diff_dict.keys())]

    for diff in reversed(diff_sorted_table): print(diff)

    code = make_code()
    print((num, code[num]) for num in range(0, code))

def to_num(id):
    result = 0
    
def make_code():
    nums = range('0', chr(ord('9')+1))
    big = range('A', chr(ord('Z')+1))
    small = range('a', chr(ord('z')+1))
    return nums[:] + big[:] + small[:]
   

if '__main__': main()

