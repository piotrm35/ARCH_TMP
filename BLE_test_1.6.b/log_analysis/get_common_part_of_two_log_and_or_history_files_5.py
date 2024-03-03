import os


def get_dev_address_list_from_BLE_test_log(log_file_path):
    print('function get_dev_address_list_from_BLE_test_log: ' + log_file_path)
    f = open(log_file_path, mode='r', encoding='utf-8')
    lines_list = f.readlines()
    f.close()
    i = 1
    dev_address_list = []
    for line in lines_list:
        tx_list = line.split(' -> ')
        if len(tx_list) > 1:
##            print(str(i) + ')\t' + line.strip())
            dev_address_list.append(tx_list[1].split(',')[0])
            i += 1
    return dev_address_list


def get_dev_address_list_from_BLE_test_logs(log_file_path_list):
    res_list = []
    for log_file_path in log_file_path_list:
        res_list += get_dev_address_list_from_BLE_test_log(log_file_path)
    return list(set(res_list))


def get_dev_address_list_from_BLEScanner_history(log_file_path):
    print('function get_dev_address_list_from_BLEScanner_history: ' + log_file_path)
    f = open(log_file_path, mode='r', encoding='utf-8')
    lines_list = f.readlines()
    f.close()
    i = 1
    dev_address_list = []
    for line in lines_list:
        tx_list = line.split(',')
        if len(tx_list) == 5 and tx_list[2][2] == ':':
##            print(str(i) + ')\t' + line.strip())
            dev_address_list.append(tx_list[2])
            i += 1
    return dev_address_list


def get_dev_address_list_from_BLEScanner_histories(log_file_path_list):
    res_list = []
    for log_file_path in log_file_path_list:
        res_list += get_dev_address_list_from_BLEScanner_history(log_file_path)
    return list(set(res_list))


def get_dev_address_list_from_Bluetooth_4_0_Scanner_log_CSV(log_file_path):
    print('function get_dev_address_list_from_Bluetooth_4_0_Scanner_log_CSV: ' + log_file_path)
    f = open(log_file_path, mode='r', encoding='utf-8')
    lines_list = f.readlines()
    f.close()
    i = 1
    dev_address_list = []
    for line in lines_list:
        tx_list = line.split(',')
        if len(tx_list) >= 4 and tx_list[3] != 'deviceAddress':
##            print(str(i) + ')\t' + line.strip())
            dev_address_list.append(tx_list[3])
            i += 1
    return dev_address_list


def get_dev_address_list_from_Bluetooth_4_0_Scanner_log_CSVs(log_file_path_list):
    res_list = []
    for log_file_path in log_file_path_list:
        res_list += get_dev_address_list_from_Bluetooth_4_0_Scanner_log_CSV(log_file_path)
    return list(set(res_list))


# this function gets log files paths from subfolders as well
def get_log_path_list(root_folder, extension):      # log_file_paths = get_log_path_list('./', '.TXT')
    res_list = []
    for (dir_path, dir_names, file_names) in os.walk(root_folder):
        res_list += [(dir_path.replace('\\', '/') + '/' + f).replace('//', '/') for f in file_names if os.path.splitext(f)[1].upper() == extension]
    return res_list


#================================================================================================================
# setup:


##dev_address_list_1 = get_dev_address_list_from_BLE_test_log('../arch_log/total_number_dev_logs_02.08.2022-06_40_40_16H.txt')
##dev_address_list_2 = get_dev_address_list_from_BLEScanner_history('../arch_log/OLD_LOGS_without_advertisement_data/BLEScanner History LOG Software Version_v 3.21_08.07.2022_Szrajbera_1p_AM.txt')
##dev_address_list_1 = get_dev_address_list_from_Bluetooth_4_0_Scanner_log_CSV('../arch_log/ble_scan_20220805_095253(1).csv')

log_file_paths = get_log_path_list('../arch_log/07.2022/', '.TXT')
print('log_file_paths = ' + str(log_file_paths))
dev_address_list_1 = get_dev_address_list_from_BLE_test_logs(log_file_paths)
dev_address_list_2 = get_dev_address_list_from_Bluetooth_4_0_Scanner_log_CSV('../arch_log/classic_scan_20220805_124235.csv')


#================================================================================================================


print('\n\n=========================================')
print('common_part_of_two_dev_address_lists:')
print('\n')
common_part_of_two_dev_address_lists = [el for el in dev_address_list_1 if el in dev_address_list_2]
i = 1
for dev_address in common_part_of_two_dev_address_lists:
    print(str(i) + ')\t' + dev_address)
    i += 1


