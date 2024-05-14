import os
import pandas as pd

# 读取Excel表格数据
excel_file = "commands.xlsx"
df = pd.read_excel(excel_file, index_col=0)

# 创建系统命令对应的C语言代码文件和函数
def create_c_code(command):
    c_code = f"void systest_{command}(void) {{\n"
    c_code += "    // Your code here\n}\n"
    with open(f"systest_{command}.c", "w") as file:
        file.write(c_code)

# 检查并创建系统命令对应的C语言代码文件和函数
def check_and_create_c_code(command):
    if not os.path.exists(f"systest_{command}.c"):
        create_c_code(command)
    with open(f"systest_{command}.c", "r") as file:
        content = file.read()
        if f"systest_{command}(void)" not in content:
            create_c_code(command)

# 遍历Excel表格中的每一行，检查并创建系统命令对应的C语言代码文件和函数
for command, row in df.iterrows():
    check_and_create_c_code(command)

    # 在对应的C语言文件中添加函数和变量
    with open(f"systest_{command}.c", "r") as file:
        c_code = file.read()
        c_code += f"\nvoid systest_{command}(void) {{\n"
        for col, val in row.items():
            if pd.notnull(val):
                if df.loc['word_type', col] == 'string':
                    c_code += f"    char* {val}; // {col}\n"
                elif df.loc['word_type', col] == 'digital':
                    c_code += f"    int {val}; // {col}\n"
        c_code += "}\n"
    with open(f"systest_{command}.c", "w") as file:
        file.write(c_code)
