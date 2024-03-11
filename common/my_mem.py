"""
参考：https://blog.csdn.net/as604049322/article/details/127573200
https://oomake.com/question/13380887
"""
from ctypes import *

import win32con
from win32gui import FindWindow
from win32process import GetWindowThreadProcessId


DWORD = c_ulong
ULONGLONG = c_ulonglong
kernel32 = cdll.LoadLibrary("kernel32.dll")
GetLastError = kernel32.GetLastError
OpenProcess = kernel32.OpenProcess
VirtualQueryEx = kernel32.VirtualQueryEx
ReadProcessMemory = kernel32.ReadProcessMemory


class MemoryInfo(Structure):
    _fields_ = [
        ("BaseAddress", ULONGLONG),
        ("AllocationBase", ULONGLONG),
        ("AllocationProtect", DWORD),
        ("__alignment1", DWORD),
        ("RegionSize", ULONGLONG),
        ("State", DWORD),
        ("Protect", DWORD),
        ("Type", DWORD),
        ("__alignment2", DWORD),
    ]


def mem_search(pid, text, return_size=512):
    content = text.encode("u8")
    print(f'content={content}')
    process = OpenProcess(win32con.PROCESS_ALL_ACCESS, 0, pid)
    print(f'process={process}')
    mem = MemoryInfo()
    from_addr = 0x0
    max_region_size = 0.5 * 2 ** 30
    while VirtualQueryEx(process, from_addr, byref(mem), sizeof(mem)) != 0:
        if mem.Protect not in (1, 16, 512):
            data_type = c_char * mem.RegionSize
            read_byte = data_type()
            bytes_read = c_ulong(0)
            is_read = ReadProcessMemory(process, from_addr, byref(
                read_byte), mem.RegionSize, byref(bytes_read))
            if is_read:
                position = read_byte.raw.find(content)
                if position != -1:
                    token = read_byte.raw[position +
                                          len(content):position + return_size].decode("u8", "ignore")
                    return token
        from_addr = from_addr + mem.RegionSize
        if mem.RegionSize > max_region_size:
            # 不扫描0.5GB以上的区域
            break


def mem_search2(pid, text, return_size=512):
    content = text.encode("u8")
    print(f'content={content}')
    process = OpenProcess(win32con.PROCESS_ALL_ACCESS, 0, pid)
    print(f'process={process}')
    mem = MemoryInfo()
    from_addr = 0x0
    max_region_size = 0.5 * 2 ** 30
    while VirtualQueryEx(process, from_addr, byref(mem), sizeof(mem)) != 0:
        if mem.Protect not in (1, 16, 512):
            data_type = c_char * mem.RegionSize
            read_byte = data_type()
            bytes_read = c_ulong(0)
            is_read = ReadProcessMemory(process, from_addr, byref(
                read_byte), mem.RegionSize, byref(bytes_read))
            if is_read:
                position = read_byte.raw.find(content)
                while position != -1:
                    token = read_byte.raw[position +
                                          len(content):position + return_size].decode("u8", "ignore")

                    print('================================S============================')
                    print(token)
                    print('================================E============================')
                    position = read_byte.raw.find(content, position + 512)
        from_addr = from_addr + mem.RegionSize
        if mem.RegionSize > max_region_size:
            # 不扫描0.5GB以上的区域
            break


if __name__ == '__main__':
    # 此处是进程不是句柄
    hwnd = FindWindow(None, '道天录')
    print(f'hwnd={hwnd}')
    pid_list = GetWindowThreadProcessId(hwnd)
    print(pid_list)
    for obj in pid_list:
        print(f'pid={obj}')
        mem_search2(obj, '50')
