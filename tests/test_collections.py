from __future__ import absolute_import
import unittest
from jnius import autoclass, protocol_map


class TestCollections(unittest.TestCase):

    def test_hashset(self):
        hset = autoclass('java.util.HashSet')()
        data = {1,2}
        # add is in both Python and Java
        for k in data:
            hset.add(k)
        # __len__
        print(dir(hset))
        self.assertEqual(len(data), len(hset))
        # __contains__
        for k in data:
            self.assertTrue(k in hset)
        self.assertFalse(0 in hset)
        # __iter__
        for k in hset:
            self.assertTrue(k in data)
        # __delitem__
        for k in data:
            del(hset[k])
            self.assertFalse(k in hset)
        
    def test_hashmap(self):
        hmap = autoclass('java.util.HashMap')()
        data = {1 : 'hello', 2 : 'world'}
        # __setitem__
        for k,v in data.items():
            hmap[k] = v
        # __len__
        self.assertEqual(len(data), len(hmap))
        # __contains__
        for k,v in data.items():
            self.assertTrue(k in hmap)
            self.assertEqual(data[k], hmap[k])
        # __iter__
        for k in hmap:
           self.assertTrue(k in data)
        # __contains__
        self.assertFalse(0 in hmap)
        # __delitem__
        for k in data:
            del(hmap[k])
            self.assertFalse(k in hmap)

if __name__ == '__main__':
    unittest.main()
