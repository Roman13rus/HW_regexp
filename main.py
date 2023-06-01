import csv
import re
with open("phonebook_raw.csv", 'r', encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

def data_converter(data:list): # функция преобразования Имени, фамилии и отчества и перемешщения их в соответствии с заголовком. так же удаляет дубли
    new_list = []
    for people in contacts_list[1::]:
        if len(people[0].split(' ')) == 3:
            lastname = people[0].split(' ')[0]
            firstname = people[0].split(' ')[1]
            surname = people[0].split(' ')[2]
            people[0], people[1], people[2] = lastname, firstname, surname
        elif len(people[0].split(' ')) == 2:
            lastname = people[0].split(' ')[0]
            firstname = people[0].split(' ')[1].split(' ')[0]
            people[0], people[1] = lastname, firstname
        elif len(people[0].split(' ')) == 1 and len(people[1].split(' ')) == 2:
            lastname = people[0]
            firstname = people[1].split(' ')[0]
            surname = people[1].split(' ')[1]
            people[0], people[1], people[2] = lastname, firstname, surname
        elif len(people[0].split(' ')) == 1:
            people[0] = people[0].split(' ')[0]
        for j in range(len(people)):
            people[j] = telephone_number_converter(people[j])
    name_dict = {}
    for i in range(1, len(contacts_list)):
        if contacts_list[i][0] in name_dict:
            name_dict[contacts_list[i][0]].append(i)
        else:
            name_dict[contacts_list[i][0]] = [i]
    for i in name_dict:
        if len(name_dict[i]) == 2:
            con1, con2 = name_dict[i][0], name_dict[i][1]
            for j in range(len(contacts_list[con1])):
                if contacts_list[con1][j] == '':
                    contacts_list[con1][j] = contacts_list[con2][j]
            new_list.append(contacts_list[con1]) 
        elif len(name_dict[i]) == 1:
            con1 = name_dict[i][0]
            new_list.append(contacts_list[con1])
    new_list.insert(0, contacts_list[0])
    return new_list
def telephone_number_converter(data:str): # описание функции преобразования вида номера телефона(вызывается в data_converter)
    pattern_number = r'(\+7|8|7)?\s*\(?(\d{3})\)?\s*?[-]?(\d{3})[-]?(\d{2})[-]?(\d{2})?\s?'
    pattern_dob = r'\(?(доб.) (\d{4})\)?'
    new_pattern_group_dob = r' \1\2'
    new_pattern_group_number = r'+7(\2)\3-\4-\5'
    new_string_dob = re.sub(pattern_dob, new_pattern_group_dob, data)
    result_string = re.sub(pattern_number, new_pattern_group_number, new_string_dob)
    return result_string
if __name__ == "__main__":
    with open("phonebook.csv", "w", encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(data_converter(contacts_list))