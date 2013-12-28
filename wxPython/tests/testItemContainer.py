"""Unit tests for wx.ItemContainer.

Since wx.ItemContainer is uninstantiable, the tests for 
subclasses are implemented with a "test base-class" of sorts.
        
Methods yet to test:
__init__, GetSelection, GetStrings, GetStringSelection,
Select, SetSelection, SetStringSelection"""

import unittest
import wx

import wxtest

class ItemContainerTest(unittest.TestCase):
    def testConstructorFails(self):
        self.assertRaises(AttributeError, wx.ItemContainer)
        
# -----------------------------------------------------------
    
class ItemContainerBase(unittest.TestCase):
    def setUp(self):
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY)
        self.testControl = None
    
    def tearDown(self):
        self.frame.Destroy()
    
    def testAppend(self):
        """Append, GetCount"""
        items = ['a','b','c','d','e']
        for s,i in zip(items, range(len(items))):
            n = self.testControl.Append(items[i])
            self.assertEquals(i,n)
            self.assertEquals(i+1,self.testControl.GetCount())
                        # count is one more than index
        self.assertEquals(items, self.testControl.GetItems())
    
    def testAppendItems(self):
        """AppendItems, GetItems"""
        one   = ['v','w','x','y','z']
        two   = ['e','d','c','b','a']
        three = ['one','five','nine']
        self.testControl.AppendItems(one)
        self.assertEquals(one, self.testControl.GetItems())
        self.testControl.AppendItems(two)
        self.assertEquals(one+two, self.testControl.GetItems())
        self.testControl.AppendItems(three)
        self.assertEquals(one+two+three, self.testControl.GetItems())
    
    def testClear(self):
        """Clear"""
        self.testControl.AppendItems(['a','b','c'])
        self.assert_(not self.testControl.IsEmpty()) # sanity check
        self.testControl.Clear()
        self.assert_(self.testControl.IsEmpty())
    
    # TODO: clean up this method
    def testClientData(self):
        """SetClientData, GetClientData"""
        self.testControl.AppendItems(['a','b','c','d','e'])
        if wxtest.ASSERTIONS_ON:
            self.assertRaises(wx.PyAssertionError, self.testControl.GetClientData, 0)
        for i in range(self.testControl.GetCount()):
            if i != 0:
                self.assertEquals(None, self.testControl.GetClientData(i))
                # raises exception until one data item added, then returns None
            data = 'data' + str(i)
            self.testControl.SetClientData(i,data)
            self.assertEquals(data, self.testControl.GetClientData(i))
    
    def testDelete(self):
        """Delete"""
        items = ['one','two','three','four','five']
        n = len(items)
        self.testControl.AppendItems(items)
        for i in range(n-1):
            self.testControl.Delete(0)
            items = items[1:]
            self.assertEquals(items[0], self.testControl.GetString(0))
            n -= 1
            self.assertEquals(n, self.testControl.GetCount())
    
    def testDeleteError(self):
        """Delete"""
        # Tests that Delete throws exceptions when given out-of-bound index
        items = ['1','2','3']
        self.testControl.AppendItems(items)
        if wxtest.ASSERTIONS_ON:
            self.assertRaises(wx.PyAssertionError, self.testControl.Delete, self.testControl.GetCount())
            self.assertRaises(wx.PyAssertionError, self.testControl.Delete, -1)
        else:
            self.testControl.Delete(self.testControl.GetCount())
            self.testControl.Delete(-1)
    
    def testEmpty(self):
        """IsEmpty"""
        self.assert_(self.testControl.IsEmpty())
        self.testControl.Append('a')
        self.assert_(not self.testControl.IsEmpty())
    
    def testFindString(self):
        """FindString"""
        items = ['zero','one','two','three']
        self.testControl.AppendItems(items)
        for i in range(len(items)):
            string = items[i]
            index = self.testControl.FindString(string)
            self.assertEquals(i,index)
        self.assertEquals(wx.NOT_FOUND, self.testControl.FindString('seven'))
    
    def testGetSetString(self):
        """SetString, GetString"""
        strings = ['a','b','c','d','e']
        self.testControl.AppendItems(strings)
        for i in range(len(strings)):
            self.testControl.SetString(i, str(i)+strings[i])
            self.assertEquals(str(i)+strings[i], self.testControl.GetString(i))
            
    def testInsert(self):
        """Insert, GetString"""
        init = ['one','two','three','four','five']
        inserts = ['a','b','c','d','e']
        self.testControl.AppendItems(init)
        for i in range(len(inserts)):
            self.testControl.Insert(inserts[i], i)
            self.assertEquals(inserts[i], self.testControl.GetString(i))
    
    def testSetItems(self):
        """SetItems, GetItems"""
        one = ['l','m','n','o','p','q']
        two = ['r','s','t','l','n','e']
        self.testControl.SetItems(one)
        self.assertEquals(one, self.testControl.GetItems())
        self.testControl.SetItems(two)
        self.assertEquals(two, self.testControl.GetItems())
        

if __name__ == '__main__':
    unittest.main(defaultTest="ItemContainerTest")