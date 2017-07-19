""" Tests eventfile.py.  This is also an example of a unittest. """

import unittest
from io import BytesIO

import eventfile


class EventfileTestCase(unittest.TestCase):
    def test_header(self):
        """ Check if we can write and read a header. """
        buf = BytesIO()
        header = {'string': 'Hello', 'number': 1234}
        eventfile.write_header(buf, header)
        buf.seek(0)
        header2, data2 = eventfile.read_event_file(buf)
        self.assertEqual(header, header2)
        self.assertEqual(b'', data2)


    def test_data(self):
        """ Check if we can write and read data after the header. """
        buf = BytesIO()
        header = {'string': 'Hello', 'number': 1234}
        data = b'Hello World'
        eventfile.write_header(buf, header)
        buf.write(data)
        buf.seek(0)
        header2, data2 = eventfile.read_event_file(buf)
        self.assertEqual(header, header2)
        self.assertEqual(data, data2)



if __name__ == '__main__':
    unittest.main()
