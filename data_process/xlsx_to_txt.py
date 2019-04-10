# encoding: utf-8
# @author: ffz@pku.edu.cn

'''
convert xlsx file to txt file
'''
import xlrd

def txt_from_xlsx(source_file, target_file):
    wb = xlrd.open_workbook(source_file)
    sh = wb.sheet_by_name("SQL Results")
    with open(target_file, "w", encoding="utf-8") as f:
        for rownum in range(sh.nrows):
            onerow =  sh.row_values(rownum)
            f.write("\t".join([onerow[1], onerow[2], onerow[3]]) + "\n")

def clean_txt(source_file, target_file):
    programs_dict ={}
    count = 0
    with open(source_file, "r", encoding="utf-8") as in_f, open(target_file, "w", encoding="utf-8") as out_f:

        for line in in_f:
            if count == 0:
                count += 1
                continue
            if count > 35500:
                break
            line = line.strip().split("\t")
            count += 1
            # print(line)
            if len(line) < 3:
                continue
            if line[0].strip() == "" or line[1].strip()=="" or line[2].strip()=="":
                continue
            value = line[2].strip().strip(line[1].strip())
            if len(value) < 5:
                print(value)
                continue
            if line[0] not in programs_dict:
                programs_dict[line[0]] = set()
                programs_dict[line[0]].add(value)
            else:
                programs_dict[line[0]].add(value)

        print("len_case: ", count)
        print("len_person:", len(programs_dict.keys()))
        for key in programs_dict:
            out_f.write(key + "\t" + "\t".join(list(programs_dict[key])) + "\n")


if __name__ == "__main__":
    txt_from_xlsx("programs.xlsx", "programs.txt")
    clean_txt("programs.txt", "clean_programs.txt")
