#!/usr/bin/env python3

#import math

'''
Part 1

You make a map (your puzzle input) of the open squares (.) and trees (#) you can see
e.g.
..##.......
#...#...#..
.#....#..#.

Due to something you read about once involving arboreal genetics and biome stability,
the same pattern repeats to the right many times

You start on the open square (.) in the top-left corner and need to reach the bottom (below the bottom-most row on your map)
Start by counting all the trees you would encounter for the slope right 3, down 1

Starting at the top-left corner of your map and following a slope of right 3 and down 1, how many trees would you encounter?


### Parse input file
1. Generate list of lists for each row in input data
- (i.e. each nested list = row from input data)
- Replace tree with 1 & open space with 0 (as integers)
---- Want to count number of trees, so with this can do a simple sum each time a coordinate has a tree
'''

input_file = open("data/day_3.txt","r")

#list of strings, where each string corresponds to row
data = input_file.readlines()
#print(data)

#remove newline characters from each string in x
data = [x.rstrip('\n') for x in data]
#print(data)

#Replace '.' (open square) & '#' (tree) with '0' and 1 respectively
#As want to count when hit tree, if it's 1 then I can do a simple sum when iterate other data
data_replaced = [x.replace('.', '0').replace('#','1') for x in data]
#print(data_replaced)


# Convert each row to be a list of individual positions/characters ('coordinates')
nested_data = [list(row) for row in data_replaced]
#print(nested_data)

#Convert '0' & '1' characters in each nested list to integer
nested_data = [list(map(int, row)) for row in nested_data]
#print(nested_data)

'''
Thoughts...

Pattern provided in put file repeats to the right multiple times for each row
Along 3, down 1

After a few rows, would reach end of provided input - need to duplicate rows (pattern repeats) so can reach bottom of map
2. Widen each row/list as necessary to reach end of map

- Would be cool to try to do extension as few times as possible

i.e. if move along 3, down 1 and have pattern of length 10
for the first 3 rows, I don't need to extend the pattern

To do this, need to know
---- Number of rows (i.e. length of list)
---- Number of positions in provided data (length of rows/nested list)
--------(this should be same for each row from eyeballing but will double check)
'''

# How many rows?
n_rows = len(nested_data)
print("number of rows in input data: {}".format(n_rows))

# How many positions in each row (check all the same too...)
# expect all values to be the same...

row_lengths = list(set([len(row) for row in nested_data]))

if len(row_lengths) != 1:
    print("rows/lines in input data have different widths")
else:
    print("all rows/lines in input data have the same width")
    row_lengths = row_lengths[0]

print("row/line width: {}".format(row_lengths))

'''
Number of rows is 323 (i.e. will go right 3, down 1 322 times)
Rows have 31 positions - starting at 1, moving + 3 every time
Every 10 rows, will have to add another duplicate of pattern

if have index (row, column) starting at (0,0)
(1,3)
(2,6)

when reach (9,30) will have to repeat


https://stackoverflow.com/questions/33046980/duplicating-a-list-n-number-of-times?rq=1
Then perform a map of nested_data + list of same index, telling how many times to copy the contents of nested list

e.g.
nested = [[1,2], [3,4]]
n_duplicate = [1,2] #don't copy [1,2], repeat [3,4] once

list(map(duplicate, nested, n_duplicate))
[[1, 2, 3], [4, 5, 6, 4, 5, 6]]

To programatically get n_duplicate, I need to know
number of rows/length of list
width of rows/length of nested list

To work out how many times will need to repeat each pattern need to know
- starting index/position
- number of rows jump each time (in this case 1)
- number of 'columns' jump each time (in this case 3)

So number of times to copy a pattern of length 31 when jump 1 row, 3 columns at a time, starting at (0,0) (top left)

= (length of row) - 1 / col_start_index + column_jump
= 31 - 1 / 0 + 3
== 10

if don't want to multiply, need to assign index for that row in list to 1
i.e. for first 10 rows, don't want to multiply,
In our example where start at 0,0
want indexes 0 - 9 to all be 1, then 10 - 19 2, 20 - 29 3 etc.

If started a 2nd row (1,0)
want rows 1 - 11 (indexes 0 - 10) to be 1 i.e want 11  of 1

i.e. for each number of minimum copies required, assuming starting row & column position of row_index_start
row_index_start + number_col_jumps_per_copy
i.e. this is the number of rows that don't want to copy (assign value of 1)

e.g.
start at 1st row (index 0)
can do 10 jumps before need to replicate pattern
0 + 10
= 10 rows that don't want to duplicate
therefore want to create initial list of 10 1s

init_idx_n_pattern_copies = [1,1,1,1,1,1,1,1,1,1] # ten 1s, i.e. first ten rows will not be copied

then need to extend list with 10 of n_copies, with n_copies increasing by 1 every 10 iterations
e.g.
n_col_jumps_per_pattern_copy = 10
n_copies = 2

Number of times need to make a copy will be upper bound by the number of rows in data
i.e. want my list of n_copies of patterns to make to be of length number of rows)
e.g. for current example, where 323 rows & start at row 1, will be going right 322 times

If need to copy every 10 iterations


'''




def get_n_copies_list(init_row_index = 0, init_col_index = 0, row_jump = 1, col_jump = 3, row_length = 31, list_length = 323):
    '''
    return list of length list_length, where each value corresponds to number of times need to copy pattern/list
    index matches rows of data list and number of times want to copy that pattern
    '''

    # How many times can i jump columns before it falls outside width of row in list?
    # = (length of row) - 1 / col_start_index + column_jump

    n_col_jumps_per_copy = (row_length - 1) / (init_col_index + col_jump)
    n_col_jumps_per_copy = round(n_col_jumps_per_copy)
    print("this is how many col jumps can do before needing extra copy of pattern: {}".format(n_col_jumps_per_copy))


    # Don't want to multiply first n rows in list,
    # before & including row index start first n cols where and where pattern will fit inside column jump
    copies_list = [1] * row_jump * (init_row_index + n_col_jumps_per_copy)
    print("this is initial copies list - initial rows that don't need to be copied {}".format(copies_list))

    # init_copies_list covers the first n rows where don't want to copy & column jump index will remain within width of pattern
    # now want rows with corresponding index to have their pattern copied enough times to for col_index to reach bottom of list
    # Starting at copying pattern once, will update every n_col_jumps_per_copy
    n_copies = 2

    #copies_list will go up until the next value to added will correspond to index of row need to multiply
    while len(copies_list) <= list_length:
        # copies_list will go up until the next value to added will correspond to index of row need to multiply
        # but row jump may mean that skip a row i.e. don't need it to be copied

        idx_sequence = [n_copies]
        rows_to_skip = [1] * (row_jump - 1)
        idx_sequence.extend(rows_to_skip)

        idx_sequence = idx_sequence * n_col_jumps_per_copy
        copies_list.extend(idx_sequence)

        #Next batch of columns will need to have additional copy of pattern made
        n_copies +=1

    #While loop means that copies_list could end up having indexes for rows not in data set
    #If copies list > list_length, need to trim the difference from copies_list

    if len(copies_list) == list_length:

        return copies_list

    else:
        n_to_trim = len(copies_list) - list_length
        copies_list = copies_list[:-n_to_trim]

        #sanity check lengths are identical
        if len(copies_list) == list_length:

            return copies_list

        else:
            raise Exception("You've messed up somewhere...")



row_n_copies_list = get_n_copies_list()
print(len(row_n_copies_list))
print(row_n_copies_list)



def duplicate_pattern(row_list, n):
    '''

    '''
    return row_list * n


# Matching indexes of nested_data & row_n_copies_list to copy pattern minimum number of times
cp_nested_data = list(map(duplicate_pattern, nested_data, row_n_copies_list))

print([len(nested) for nested in cp_nested_data])

# To check if my functions work correctly, let's try random mix
x = get_n_copies_list(init_row_index = 2, row_jump = 2, col_jump =3)
xl = list(map(duplicate_pattern, nested_data, x))
print([len(nested) for nested in xl])



'''
Now to implement the how many trees do you come across when go 1 down, 3 across

Need to stop when row index is greater than number of rows in column

In order to generalise this to (x,y) row + column jump

suggest make a list of tuples of row and column indexes of positions to access
Then can iterate over these tuples to count number of trees
'''

def get_index_tuple_list(init_row_index = 0, init_col_index = 0, row_jump = 1, col_jump = 3, list_length=323):
    '''
    return list of tuples in format [(row_idx, col_idx)]
    '''

    row_idxs = [idx for idx in range(init_row_index, list_length, row_jump)]

    #column indexes, needs to be same length as row_idxs
    col_idxs = [init_col_index]

    col_index_init = init_col_index

    while len(col_idxs) < len(row_idxs):

        col_index_init += col_jump #next column index
        col_idxs.append(col_index_init)

    if len(col_idxs) != len(row_idxs):
        print("col_idxs length: {}".format(len(col_idxs)))
        print("row_idxs length: {}".format(len(row_idxs)))
        raise Exception("you're being silly")

    else:

        idx_list = list(zip(row_idxs, col_idxs))

        return idx_list


p1_index_tuple_list = get_index_tuple_list()
print(p1_index_tuple_list)

#part 1
pt1_result = sum((cp_nested_data[idx_tuple[0]][idx_tuple[1]] for idx_tuple in p1_index_tuple_list))

print("this is result for part 1: {}".format(pt1_result))


## part two
'''
Determine the number of trees you would encounter if, for each of the following slopes, you start at the top-left corner and traverse the map all the way to the bottom:

Right 1, down 1.
Right 3, down 1. (This is the slope you already checked.)
Right 5, down 1.
Right 7, down 1.
Right 1, down 2.

What do you get if you multiply together the number of trees encountered on each of the listed slopes?
'''

# workflow should be:
#1. n_copies_list
#2. copied_list
#3. index_tuple_list
#4. Sum result

def n_trees_wrapper(list_of_lists, init_row_index = 0, init_col_index = 0, row_jump = 1, col_jump = 3, row_length = 31, list_length = 323):
    '''
    returns integer of n trees encountered
    '''

    n_cp_list = get_n_copies_list(init_row_index, init_col_index, row_jump, col_jump, row_length, list_length)

    cp_l_o_l = list(map(duplicate_pattern, list_of_lists, n_cp_list))

    idx_tup_list = get_index_tuple_list(init_row_index, init_col_index, row_jump, col_jump, list_length)

    n_trees = sum((cp_l_o_l[idx_tuple[0]][idx_tuple[1]] for idx_tuple in idx_tup_list))

    return n_trees


# Right 1, down 1.
# Right 3, down 1. (This is the slope you already checked.)
# Right 5, down 1.
# Right 7, down 1.
# Right 1, down 2.

r1_d1 = n_trees_wrapper(nested_data, init_row_index = 0, init_col_index = 0, row_jump = 1, col_jump = 1)
r3_d1 = n_trees_wrapper(nested_data)
r5_d1 = n_trees_wrapper(nested_data, init_row_index = 0, init_col_index = 0, row_jump = 1, col_jump = 5)
r7_d1 = n_trees_wrapper(nested_data, init_row_index = 0, init_col_index = 0, row_jump = 1, col_jump = 7)
r1_d2 = n_trees_wrapper(nested_data, init_row_index = 0, init_col_index = 0, row_jump = 2, col_jump = 1)

if r3_d1 == pt1_result:
    print("all is well with wrapper")
else:
    raise Exception("wrapper is going wrong")

#multiply together to get pt2 resut
pt2_result = r1_d1 * r3_d1 * r5_d1 * r7_d1 * r1_d2
print("this is pt2 result: {}".format(pt2_result))
