

def correct_data(table_row):
	""" 
		This function Concatenates the Product Name into Single String.
		THis is done, so that product name is aligned in a single column.
	"""
	table_with_name = ''
	table_with_price = []
	first_element_array = []
	if len(data_splited[1]) > 5:
	#     table_with_price = table_row[:-4] + table_row[-4:]
		for i in range(len(table_row) - len(table_row[-4:])):
	    		table_with_name += table_row[i] + " "
		first_element_array.insert(0, table_with_name)
		table_with_price = first_element_array + table_row[-4:]
	else:
		table_with_price = table_row
	return table_with_price
