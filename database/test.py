from DatabaseAdapter import DatabaseAdapter

DB = DatabaseAdapter.Instance()

# DB.addID('qwertyuiop')
# DB.addID('asdfghjkl;')
DB.addID('0987654321')
# DB.removeID('zxcvbnm,./')
print(DB.isInSystem('0987654321'))
# print(DB.isInSystem('asdfghjkl;'))
# print(DB.isInSystem('zxcvbnm,./'))
# print(DB.isInSystem(None))