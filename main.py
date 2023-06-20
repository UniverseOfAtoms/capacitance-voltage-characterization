import os
import pandas as pd
from capacitance_voltage import Fitting
downloads_path = os.path.expanduser("C:/Users/amira/Downloads/master teza/cv mjerenja sa semiconductor analyzer/")
file_name1 = "cv_test_187.txt"
file_name2 = "cv_test_200.txt"
file_name3 = "cv_test_250.txt"
file_name4 = "cv_test_288.txt"
file_name5 = "cv_test_300.txt"
file_name6 = "cv_test_321.txt"
file_name7 = "cv_test_350.txt"
file_names = [
    file_name1, file_name2,
    file_name3, file_name4,
    file_name5, file_name6, file_name7
]
dataframes = []
for name in file_names:
    file_path = os.path.join(downloads_path, name)
    with open(file_path, 'r') as file:
        content = file.readlines()
        data = [line.split('\t')for line in content]
        columns = ['Cp_AC', 'Gp_AC', 'DCV_AC', 'F_AC', 'CVU1S']
        dtype = {'Cp_AC': float, 'Gp_AC': float, 'DCV_AC': float, 'F_AC': float, 'CVU1S': int}
        df = pd.DataFrame(data[1:], columns=columns).astype(dtype)
        dataframes.append(df)

c_v = Fitting(dataframes)
#c_v.capacitance_voltage_characteristic()
c_v.plot_1_c2_vs_v()