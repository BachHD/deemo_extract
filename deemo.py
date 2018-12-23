import os
import glob

def is_valid(char):
    try:
        char_dec = ord(char)
        if (48 <= char_dec <= 57 or
            65 <= char_dec <= 90 or
            97 <= char_dec <= 122 or
            char_dec == 46 or
            char_dec == 95 or
            char_dec == 32):
            return True
    except:
        pass
    return False

data_dir = "Data"
file_list = glob.glob(os.path.join(data_dir, "*"))

for file_name in file_list:
    if ((".resource" in file_name) or
            ("sharedasset" in file_name)):
        continue

    with open(file_name, "rb") as fp:
        fp.seek(0x1004)
        if (is_valid(fp.read(1))):
            start_pos = 0x1004
        else:
            start_pos = 0x1005

        fp.seek(start_pos)
        offset = 0
        while (is_valid(fp.read(1))):
            offset += 1

        if (offset < 1):
            continue

        fp.seek(start_pos)
        real_name = fp.read(offset)
        new_path = os.path.join(data_dir, real_name.decode("ascii").strip())
        while (os.path.isfile(new_path)):
            new_path += "d"
        print("{} > {}".format(file_name, new_path))
        os.rename(file_name, new_path)
