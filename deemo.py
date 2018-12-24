import os
import glob
import fsb5

def is_valid(char):
    try:
        #Lazy ASCII checking
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
	
def get_real_name(file_name):
    with open(file_name, "rb") as fp:
        # Some file start at 0x1004 instead of 0x1005
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
            return None

        fp.seek(start_pos)
        real_name = fp.read(offset)
        return real_name



source_dir = "Data"
destination_dir = "Out"

if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

#Songs are compressed into FSB5 files and named some_string.resource
#Song name is in file with the same as the file above, but without .resource
res_file_list = glob.glob(os.path.join(source_dir, "*.resource"))
for res_file in res_file_list:
    if ("sharedasset" in res_file):
        continue

    #Get real name
    name_file = res_file.split(".")[0]
    real_name = get_real_name(name_file)
    if (real_name is None):
        continue
	
    #Extract FSB5
    with open(res_file, 'rb') as fp:
        fsb = fsb5.FSB5(fp.read())
        
    audio_data = fsb.samples[0]
    
    #Check extension
    ext = fsb.get_sample_extension()
    if (ext is not "mp3"):
        continue
    
    #Build audio save path
    audio_path = os.path.join(destination_dir, real_name.decode("ascii").strip())
    while (os.path.isfile(audio_path)):
        audio_path += "d"
        
    audio_path = audio_path + "." + ext
    
    print("{} > {}".format(res_file, audio_path))
    
    #Write audio file
    with open(audio_path, 'wb') as fp:
        rebuilt_sample = fsb.rebuild_sample(audio_data)
        fp.write(rebuilt_sample)    