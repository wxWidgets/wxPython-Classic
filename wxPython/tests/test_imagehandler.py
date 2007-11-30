import wx
print wx.version()

TESTHANDLER= 999
class TestImageHandler(wx.PyImageHandler):
    def __init__(self):
        wx.PyImageHandler.__init__(self)
        self.SetName("TestImageHandler")
        self.SetExtension("tst")
        self.SetMimeType("image/tst")
        self.SetType(TESTHANDLER)
            
    def DoCanRead(self, stream):
        print "DoCanRead"
        return True
    
    def LoadFile(self, image, stream, verbose, index):
        print "LoadFile", type(stream)
        image.Create(10, 10)
    
    def GetImageCount(self, stream):
        print "GetImageCount"
        return 1
                
    def SaveFile(self, image, stream, verbose):
        print "SaveFile", type(stream)
        return True

app= wx.PyApp()

wx.Image.AddHandler(TestImageHandler())

testfile= file("testin.tst", "w")
testfile.close()
image= wx.Image("testin.tst", TESTHANDLER)
image.SaveFile("testout.tst", TESTHANDLER)

