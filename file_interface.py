import os
import json
import base64
from glob import glob


class FileInterface:
    def __init__(self):
        os.chdir('files/')

    def list(self,params=[]):
        try:
            filelist = glob('*.*')
            return dict(status='OK',data=filelist)
        except Exception as e:
            return dict(status='ERROR',data=str(e))

    def get(self,params=[]):
        try:
            filename = params[0]
            if (filename == ''):
                return None
            fp = open(f"{filename}",'rb')
            isifile = base64.b64encode(fp.read()).decode()
            return dict(status='OK',data_namafile=filename,data_file=isifile)
        except Exception as e:
            return dict(status='ERROR',data=str(e))
        
    def upload(self, params=[]):
        try:
            file_name = params[0]
            file_data_base64 = params[1]
            with open(file_name, 'wb') as f:
                f.write(base64.b64decode(file_data_base64.encode()))
            return dict(status='OK', data=f'{file_name} berhasil diupload')
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def delete(self, params=[]):
        try:
            file_name = params[0]
            os.remove(file_name)
            return dict(status='OK', data=f'{file_name} berhasil dihapus')
        except Exception as e:
            return dict(status='ERROR', data=str(e))


if __name__=='__main__':
    f = FileInterface()
    print(f.list())
    print(f.get(['pokijan.jpg']))
    print(f.upload(['contoh.txt', base64.b64encode(b'halo dunia').decode()]))
    print(f.delete(['contoh.txt']))
