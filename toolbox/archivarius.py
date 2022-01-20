import os
import time
import zipfile as zp

def make_file_timestamp(ms: float) -> 'timestamp: str':
    return dt.datetime.fromtimestamp(ms).strftime('%Y%m%d_%H%m')
    
def archivarius(dir_to_clean: str, days_old: int, delete_files: bool=False, compress_files: bool=False) -> None:
    processed_counter = 0
    deleted_counter = 0
    compressed_counter = 0
    
    dir_to_clean = os.path.abspath(dir_to_clean)
    print(dir_to_clean)
    
    times_list = []
    
    # init vars for compression
    if compress_files == True:
        compress_dir = dir_to_clean + '/archived'
        os.makedirs(compress_dir, exist_ok=True)
        tmp_zip_path = f'{compress_dir}/tmp.zip'
        try:
            os.remove(tmp_zip_path)
        except FileNotFoundError:
            pass
    
                        
    for file_name in os.listdir(dir_to_clean):
        file_path = dir_to_clean + '/' + file_name
        
        if os.path.isdir(file_path) == True:
            continue

        last_modified = os.path.getmtime(file_path)
        times_list.append(last_modified)

        days_ago = (time.time() - last_modified) / 60 / 60 / 24
        if days_ago > days_old:
            # COMPRESS
            if compress_files == True:
                with zp.ZipFile(tmp_zip_path, 'a', compression=zp.ZIP_BZIP2, compresslevel=9) as myzip:
                    # ZIP_DEFLATED - more fast, but less efficient compression
                    myzip.write(file_path, arcname=file_name)

                compressed_counter += 1

            # DELETE
            if delete_files == True:
                os.remove(file_path)
                deleted_counter += 1

        processed_counter += 1
        
    # rename Zip file to final one
    if compress_files == True:
        min_ts = make_file_timestamp(min(times_list))
        max_ts = make_file_timestamp(max(times_list))
        final_zip_path = f'{compress_dir}/period_{min_ts}_{max_ts}.zip'
        os.rename(tmp_zip_path, final_zip_path)
        
   # abs_dir = '/'.join(os.path.abspath(file).split('/')[:-1])
    
    print('Processed directory: %s'%dir_to_clean)
    print('Total files in directory: %i'%len(os.listdir(dir_to_clean)))
    print('='*30)
    print('Processed files: %i'%processed_counter)
    print('Compressed files: %i'%compressed_counter)
    print('Deleted files: %i'%deleted_counter)
