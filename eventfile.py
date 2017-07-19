"""
Some tools for reading and writing event files.
The file format is simply a JSON header, then
a null byte, and then the raw event data.
"""

import io
import json
from typing import Dict, Tuple


def write_header(outp: io.RawIOBase, header: Dict) -> None:
    """ Writes a header to the file.  The header must be a python dict
        that is convertable to JSON.

        After calling this, you can just write the events to the file.
    """
    dumped = json.dumps(header)
    encoded = dumped.encode('utf-8')
    outp.write(encoded)
    outp.write(b'\x00')


def read_event_file(inp: io.RawIOBase) -> Tuple[Dict, bytes]:
    """ Reads an event file, and returns the header (as a python dict)
        and the data (as bytes).

        TODO: This reads the whole file into memory.  It might be
        better to only read the header, if this causes problems later
        with large files.
    """
    file_bytes = inp.read()
    zero_pos = file_bytes.index(b'\x00')
    header_bytes = file_bytes[:zero_pos]
    header_str = header_bytes.decode('utf-8')
    header = json.loads(header_str)
    data = file_bytes[zero_pos+1:]
    return header, data


def main():
    """ Test everything """
    with open("test.bin", "wb") as outp:
        header = {'data': 1}
        write_header(outp, header)

        data = b'\x61\x62\x63\x00\x01\0x2\x03'
        f.write(data)

    with open("test.bin", "rb") as inp:
        header, data = read_event_file(inp)

        print(header)
        print(data)


if __name__ == '__main__':
    main()
