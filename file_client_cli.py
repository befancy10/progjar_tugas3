import socket
import json
import base64
import logging

server_address=('0.0.0.0',7777)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        # Look for the response, waiting until socket is done (no more data)
        data_received="" #empty string
        while True:
            #socket does not receive all data at once, data comes in part, need to be concatenated at the end of process
            data = sock.recv(16)
            if data:
                #data is not empty, concat with previous content
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                # no more data, stop the process by break
                break
            
        logging.warning(f"Raw response:\n{data_received}")
        
        # at this point, data_received (string) will contain all data coming from the socket
        # to be able to use the data_received as a dict, need to load it using json.loads()
        hasil = json.loads(data_received)
        logging.warning("data received from server:")
        return hasil
    except Exception as e:
        # logging.warning("error during data receiving")
        logging.warning(f"error during data receiving: {e}")
        return False


def remote_list():
    command_str=f"LIST"
    hasil = send_command(command_str)
    # if (hasil['status']=='OK'):
    if hasil and isinstance(hasil, dict) and hasil.get('status') == 'OK':
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    command_str=f"GET {filename}"
    hasil = send_command(command_str)
    # if (hasil['status']=='OK'):
    if hasil and isinstance(hasil, dict) and hasil.get('status') == 'OK':
        #proses file dalam bentuk base64 ke bentuk bytes
        namafile= hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        fp = open(namafile,'wb+')
        fp.write(isifile)
        fp.close()
        return True
    else:
        print("Gagal")
        return False
    
def remote_upload(file_path):
    try:
        with open(file_path, 'rb') as f:
            file_data = f.read()
        file_data_base64 = base64.b64encode(file_data).decode()
        file_name = file_path.split('/')[-1]
        command_str = f"UPLOAD {file_name} {file_data_base64}"
        result = send_command(command_str)
        print(result['data'])
        return result['status'] == 'OK'
    except Exception as e:
        print(f"Error: {e}")
        return False

def remote_delete(file_name):
    command_str = f"DELETE {file_name}"
    result = send_command(command_str)
    print(result['data'])
    return result['status'] == 'OK'


if __name__=='__main__':
    server_address=('127.0.0.1',6666)
    remote_list()
    remote_get('donalbebek.jpg')
    remote_list()
    remote_upload('contoh_upload.txt')
    remote_list()
    remote_delete('contoh_upload.txt')
    remote_list()