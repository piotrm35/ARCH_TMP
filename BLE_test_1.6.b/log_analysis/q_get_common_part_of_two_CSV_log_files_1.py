import os


def get_dev_address_list_from_Bluetooth_4_0_Scanner_log_CSV(log_file_path):
    print('get_dev_address_list: ' + log_file_path)
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

# Android:
LOG_FOLDER_1 = '/storage/emulated/0/TMP/scan_log_test_1/'
LOG_FOLDER_2 = '/storage/emulated/0/TMP/scan_log_test_2/'
# Windows:
##LOG_FOLDER_1 = '../arch_log/scan_log_test_1/'
##LOG_FOLDER_2 = '../arch_log/scan_log_test_2/'

log_file_paths_1 = get_log_path_list(LOG_FOLDER_1, '.CSV')
log_file_paths_2 = get_log_path_list(LOG_FOLDER_2, '.CSV')
##print('log_file_paths_1 = ' + str(log_file_paths_1))
##print('\n\n')
##print('log_file_paths_2 = ' + str(log_file_paths_2))
dev_address_list_1 = get_dev_address_list_from_Bluetooth_4_0_Scanner_log_CSVs(log_file_paths_1)
dev_address_list_2 = get_dev_address_list_from_Bluetooth_4_0_Scanner_log_CSVs(log_file_paths_2)


#================================================================================================================


print('\n\n=========================================')
print('common_part_of_two_dev_address_lists:')
print('\n')
common_part_of_two_dev_address_lists = [el for el in dev_address_list_1 if el in dev_address_list_2]
i = 1
for dev_address in common_part_of_two_dev_address_lists:
    print(str(i) + ')\t' + dev_address)
    i += 1


