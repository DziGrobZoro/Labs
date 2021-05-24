from solution import FileReader

fr = FileReader('test_1.txt')
print('Файл 1: ')
print(fr.file_name)
print(fr.file_content)
print(fr.count_lines())


fr2 = FileReader('test_2.txt')
print('Файл 2: ')
print(fr2.file_name)
print(fr2.file_content)
print(fr2.count_lines())

fr3 = fr + fr2
print('Файл 3: ')
print(fr3.file_name)
print(fr3.file_content)
print(fr3.count_lines())
print(str(fr3))