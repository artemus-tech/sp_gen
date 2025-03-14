import glob
import os

import constants as const
import dbassets

# Use glob to get a list of directories that match the pattern
counter=0
for directory in glob.glob(f'{const.path_speval}/sp_eval*'):
    if os.path.exists(directory):
        print(f"Processing directory: {directory}")

        # Match all files in the directory using glob (e.g., all files inside the directory)
        files = glob.glob(os.path.join(directory, '*'))  # Match all files in the directory

        # Count the number of files
        file_count = len(files)

        if file_count==1:
            counter+=1
            dbassets.insert_data("sp_eval",data_dict={
                'qmin':0.02,
                'qmax':5.0,
                'qnum':150,
                'src_path':files[0],
                'gen_id':int(os.path.basename(files[0]).replace('.txt',''))
            })
        elif file_count>1:
            raise Exception(f"{file_count}???????")


        else:
            os.rmdir(directory)

        print(f"Total files in {directory}: {file_count}")
    else:
        print(f"Directory {directory} does not exist.")
print(counter)