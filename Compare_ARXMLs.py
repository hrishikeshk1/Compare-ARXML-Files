import read_arxml as ra
import xlwings as xw
import xml.etree.cElementTree as treepackage

pink = (255, 192, 203)
grey = (128, 128, 128)
green = (144, 238, 144)

file_1 = input('Enter the path to the first file:')
file_2 = input('Enter the path to the second file:')
enums_allowed = input('Include the comparison of enums? (y/n)')
SaveAs = input('Enter a name for the output file')

root_1 = treepackage.parse(file_1).getroot()
root_2 = treepackage.parse(file_2).getroot()
root_dir = [root_1, root_2]

def insights(old_messages, new_messages):
    book_obj = xw.Book()
    sheet_obj = book_obj.sheets[0]

    for i in range(len(old_messages)):
        sheet_obj.range('A' + str(i+2)).value = old_messages[i].name
    for i in range(len(new_messages)):
        sheet_obj.range('B' + str(i+2)).value = new_messages[i].name
    pass

def sidebysideattrs(sheet_obj, old_messages, new_messages, i, x, j, y, iter):
    sheet_obj.range('D' + str(iter)).value = old_messages[i].signals[x].length
    sheet_obj.range('E' + str(iter)).value = new_messages[j].signals[y].length
    if  old_messages[i].signals[x].length != new_messages[j].signals[y].length:
        sheet_obj.range('E' + str(iter)).color = pink

    #Initial Value comparison
    sheet_obj.range('F' + str(iter)).value = old_messages[i].signals[x].initial_value
    sheet_obj.range('G' + str(iter)).value = new_messages[j].signals[y].initial_value
    if  old_messages[i].signals[x].initial_value != new_messages[j].signals[y].initial_value:
        sheet_obj.range('G' + str(iter)).color = pink

    #Offset comparison
    sheet_obj.range('H' + str(iter)).value = old_messages[i].signals[x].offset
    sheet_obj.range('I' + str(iter)).value = new_messages[j].signals[y].offset
    if  old_messages[i].signals[x].offset != new_messages[j].signals[y].offset:
        sheet_obj.range('I' + str(iter)).color = pink

    #Resolution comparison
    sheet_obj.range('J' + str(iter)).value = old_messages[i].signals[x].resolution
    sheet_obj.range('K' + str(iter)).value = new_messages[j].signals[y].resolution
    if  old_messages[i].signals[x].resolution != new_messages[j].signals[y].resolution:
        sheet_obj.range('K' + str(iter)).color = pink

    #Range comparison
    try:
        sheet_obj.range('L' + str(iter)).value = old_messages[i].signals[x].range[0]
        sheet_obj.range('M' + str(iter)).value = new_messages[j].signals[y].range[0]
        if  old_messages[i].signals[x].range[0] != new_messages[j].signals[y].range[0]:
            sheet_obj.range('M' + str(iter)).color = pink
        sheet_obj.range('N' + str(iter)).value = old_messages[i].signals[x].range[1]
        sheet_obj.range('O' + str(iter)).value = new_messages[j].signals[y].range[1]

        if  old_messages[i].signals[x].range[1] != new_messages[j].signals[y].range[1]:
            sheet_obj.range('O' + str(iter)).color = pink
    except:
        sheet_obj.range('L' + str(iter)).value = "Not Applicable"
        sheet_obj.range('M' + str(iter)).value = "Not Applicable"
        sheet_obj.range('N' + str(iter)).value = "Not Applicable"
        sheet_obj.range('O' + str(iter)).value = "Not Applicable"
        sheet_obj.range('L' + str(iter)).color = grey
        sheet_obj.range('M' + str(iter)).color = grey
        sheet_obj.range('N' + str(iter)).color = grey
        sheet_obj.range('O' + str(iter)).color = grey
        #print(f'Range comparison failed - {old_messages[i].signals[x].data_type} - {old_messages[i].signals[x].name}')

    #Unit comparison
    sheet_obj.range('P' + str(iter)).value = old_messages[i].signals[x].unit
    sheet_obj.range('Q' + str(iter)).value = new_messages[j].signals[y].unit
    if  old_messages[i].signals[x].unit != new_messages[j].signals[y].unit:
        sheet_obj.range('Q' + str(iter)).color = pink

    #Data type comparison
    sheet_obj.range('R' + str(iter)).value = old_messages[i].signals[x].data_type
    sheet_obj.range('S' + str(iter)).value = new_messages[j].signals[y].data_type
    if  old_messages[i].signals[x].data_type != new_messages[j].signals[y].data_type:
        sheet_obj.range('S' + str(iter)).color = pink

    #Start position comparison
    sheet_obj.range('T' + str(iter)).value = old_messages[i].signals[x].start_position
    sheet_obj.range('U' + str(iter)).value = new_messages[j].signals[y].start_position
    if  old_messages[i].signals[x].start_position != new_messages[j].signals[y].start_position:
        sheet_obj.range('U' + str(iter)).color = pink

    #Identifier comparison
    sheet_obj.range('V' + str(iter)).value = old_messages[i].ID
    sheet_obj.range('W' + str(iter)).value = new_messages[j].ID
    if  old_messages[i].ID != new_messages[j].ID:
        sheet_obj.range('W' + str(iter)).color = pink

    #Enumeration comparison
    if enums_allowed == 'y':
        sheet_obj.range('X' + str(iter)).value = old_messages[i].signals[x].enum_str
        sheet_obj.range('Y' + str(iter)).value = new_messages[j].signals[y].enum_str

def setColumnNames(sheet_obj):
    sheet_obj.range('A1').value = "Signal Name"
    sheet_obj.range('B1').value = "Parent in Old File"
    sheet_obj.range('C1').value = "Parent in New File"
    sheet_obj.range('D1').value = "Length(O)"
    sheet_obj.range('E1').value = "Length(N)"
    sheet_obj.range('F1').value = "Initial Value(O)"
    sheet_obj.range('G1').value = "Initial Value(N)"
    sheet_obj.range('H1').value = "Offset(O)"
    sheet_obj.range('I1').value = "Offset(N)"
    sheet_obj.range('J1').value = "Resolution(O)"
    sheet_obj.range('K1').value = "Resolution(N)"
    sheet_obj.range('L1').value = "Lower Limit(O)"
    sheet_obj.range('M1').value = "Lower Limit(N)"
    sheet_obj.range('N1').value = "Upper Limit(O)"
    sheet_obj.range('O1').value = "Upper Limit(N)"
    sheet_obj.range('P1').value = "Unit(O)"
    sheet_obj.range('Q1').value = "Unit(N)"
    sheet_obj.range('R1').value = "Data Type(O)"
    sheet_obj.range('S1').value = "Data Type(N)"
    sheet_obj.range('T1').value = "Start Position(O)"
    sheet_obj.range('U1').value = "Start Position(N)"
    sheet_obj.range('V1').value = "Identifier(O)"
    sheet_obj.range('W1').value = "Identifier(N)"
    sheet_obj.range('X1').value = "Enums(O)"
    sheet_obj.range('Y1').value = "Enums(N)"

def insights_2(old_messages, new_messages):
    common_signals = []
    book_obj = xw.Book()
    sheet_obj = book_obj.sheets[0]
    setColumnNames(sheet_obj)
    sgn_cnt = 0
    for i in range(len(old_messages)):
        for j in range(len(old_messages[i].signals)):
            found = False
            sheet_obj.range('A' + str(sgn_cnt+2)).value = str(old_messages[i].signals[j].name)
            sheet_obj.range('B' + str(sgn_cnt+2)).value = old_messages[i].name
            working_signal = old_messages[i].signals[j]
            blank_count = 0
            for kl in range(len(new_messages)):
                if found == True:
                    break
                if len(new_messages[kl].signals) > 0:

                    for l in range(len(new_messages[kl].signals)):

                        if new_messages[kl].signals[l].name == working_signal.name:
                            common_signals.append(new_messages[kl].signals[l])
                            sheet_obj.range('C' + str(sgn_cnt + 2)).value = new_messages[kl].name
                            if old_messages[i].name != new_messages[kl].name:
                                sheet_obj.range('C' + str(sgn_cnt + 2)).color = pink
                            else:
                                sheet_obj.range('C' + str(sgn_cnt + 2)).color = green

                            sidebysideattrs(sheet_obj, old_messages, new_messages, i, j, kl, l, sgn_cnt + 2)
                            sgn_cnt += 1
                            found = True
                            break
                        if l == len(new_messages[kl].signals) - 1 and kl == (len(new_messages) - (blank_count + 1)):
                            sheet_obj.range('C' + str(sgn_cnt + 2)).value = "<Signal Not Found>"
                            sheet_obj.range('C' + str(sgn_cnt + 2)).color = grey
                            sgn_cnt += 1
                            found = True
                            break
                else:
                    if kl == len(new_messages) - 1 and found == False:
                        sheet_obj.range('C' + str(sgn_cnt + 2)).value = "<Signal Not Found>"
                        sheet_obj.range('C' + str(sgn_cnt + 2)).color = grey
                        sgn_cnt += 1
                        break

    newly_added = new_messages
    for i in range(len(newly_added)):
        if len(newly_added[i].signals) > 0:
            for j in range(len(newly_added[i].signals)):
                for k in range(len(common_signals)):
                    if newly_added[i].signals[j].name == common_signals[k].name:
                        break
                    elif k == len(common_signals) - 1:
                        sheet_obj.range('A' + str(sgn_cnt + 2)).value = newly_added[i].signals[j].name
                        sheet_obj.range('B' + str(sgn_cnt + 2)).value = "<Signal Not Found>"
                        sheet_obj.range('B' + str(sgn_cnt + 2)).color = grey
                        sheet_obj.range('C' + str(sgn_cnt + 2)).value = newly_added[i].name
                        sgn_cnt += 1

    book_obj.save(SaveAs)


def extract_data(root):
    messages = ra.read_messages(root)
    for i in messages:
        i.getIdentifier(root)
        i.getTriggers(root)
        i.getType(root)
    signals = ra.read_signals(root)
    for sgn in range(len(signals)):
        signals[sgn].get_signal_param1(root)
        signals[sgn].convert_enums_to_string(root)
        signals[sgn].get_signal_unit(root)
        signals[sgn].get_signal_datatype(root)
        signals[sgn].get_start_position_and_mapping(root)
    messages = ra.map_messages_to_signals(messages, signals)
    for i in messages:
        i.sort_signals_by_start_bit(root)
        i.getDirection(root)
        i.getLength(root)
    return messages

messages_A = extract_data(root_1)
messages_B = extract_data(root_2)

#Input and Processing of the second ARXML file ends here:
print("\n\n\n\nCompare begins here:")
print(f'Number of messages in Old ARXML: {len(messages_A)}')
print(f'Number of messages in New ARXML: {len(messages_B)}')

ct_a = 0
for i in range(len(messages_A)):
    ct_a += len(messages_A[i].signals)
#print(ct_a)
ct_b = 0
for j in range(len(messages_B)):
    ct_b += len(messages_B[j].signals)

m_matches = 0
for i in range(len(messages_A)):
    for j in range(len(messages_B)):
        if messages_A[i].name == messages_B[j].name:
            m_matches += 1

print(f'Of which {m_matches} match')

print(f'Number of signals in Old ARXML: {ct_a}')
print(f'Number of signals in New ARXML: {ct_b}')


matches = 0


for i in range(len(messages_A)):
    for j in range(len(messages_B)):
        for k in range(len(messages_A[i].signals)):
            for l in range(len(messages_B[j].signals)):
                if messages_A[i].signals[k].name == messages_B[j].signals[l].name:
                    matches = matches + 1


print(f'Of which {matches} match')

insights_2(messages_A, messages_B)
input()





