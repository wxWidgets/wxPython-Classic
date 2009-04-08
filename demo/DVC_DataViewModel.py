
import wx
import wx.dataview as dv

#----------------------------------------------------------------------

# We'll use instaces of these classes to hold our music data. Items in the
# tree will get associated with the coresponding Song or Genre object.

class Song(object):
    def __init__(self, id, artist, title, genre):
        self.id = id
        self.artist = artist
        self.title = title
        self.genre = genre

class Genre(object):
    def __init__(self, name):
        self.name = name
        self.songs = []

#----------------------------------------------------------------------

# This model acts as a bridge between the DataViewCtrl and the music data, and
# organizes it hierarchically, as a collection of Genres, each of which is a
# collection of songs. We derive the class from PyDataViewCtrl, which knows
# how to reflect the C++ virtuals to the Python methods in the derived class.

        
class MyTreeListModel(dv.PyDataViewModel):
    def __init__(self, data, log):
        dv.PyDataViewModel.__init__(self)
        self.data = data
        self.log = log
        
        # The objmapper is an instance of DataViewItemObjectMapper and is used
        # to help associate Python objects with DataViewItem objects. Normally
        # a dictionary is used so any Python object can be used as data nodes.
        # If the data nodes are weak-referencable then the objmapper can use a
        # WeakValueDictionary instead.
        self.objmapper.UseWeakRefs(True)
        
        
    # Report how many columns this model provides data for.
    def GetColumnCount(self):
        return 4

    # All of our columns are strings.  If the model or the renderers
    # in the view are other types then that should be reflected here.    
    def GetColumnType(self, col):
        return 'string'
    
    
    
    def GetChildren(self, parent, children):  
        # The view calls this method to find the children of any node in the
        # control. There is an implicit hidden root node, and any top level
        # items should be reported as children of this node. A List view
        # simply provides all items as children of this hidden root. A Tree
        # view adds additional items as children of the other items, as needed
        # to provide the tree hierachy.
        self.log.write("GetChildren\n")
        
        # If the parent item is invalid then it represents the hidden root
        # item, so we'll use the genre objects as its children and they will
        # end up being the collection of visible roots in our tree.
        if not parent:
            for genre in self.data:
                children.append(self.ObjectToItem(genre))
            return len(self.data)
        
        # Otherwise we'll fetch the python object associated with the parent
        # item and make DV children for each of it's child objects.
        node = self.ItemToObject(parent)
        if isinstance(node, Genre):
            for song in node.songs:
                children.append(self.ObjectToItem(song))
            return len(node.songs)


    def IsContainer(self, item):
        # Return True if the item has children, False otherwise.
        self.log.write("IsContainer\n")
        
        # The hidden root is a container
        if not item:
            return True
        # and the genre objects are containers
        node = self.ItemToObject(item)
        if isinstance(node, Genre):
            return True
        # but everything else (the song objects) are not
        return False    

    
    def GetParent(self, item):
        # Return the item which is this item's parent.
        self.log.write("GetParent\n")
        
        if not item:
            return dv.NullDataViewItem

        node = self.ItemToObject(item)        
        if isinstance(node, Genre):
            return dv.NullDataViewItem
        elif isinstance(node, Song):
            for g in self.data:
                if g.name == node.genre:
                    return self.ObjectToItem(g)
            
        
    def GetValue(self, item, col):
        # Return the string to be displayed for this item and column. We'll
        # just pul the values from the data objects we associated with the
        # items in GetChildren.
        #self.log.write("GetValue\n")
        
        # Fetch the data object for this item.
        node = self.ItemToObject(item)
        if isinstance(node, Genre):
            if col == 0:
                return node.name
            return ""
        elif isinstance(node, Song):
            if col == 0:
                return node.genre
            elif col == 1:
                return node.artist
            elif col == 2:
                return node.title
            else:
                return node.id
        else:
            return ""
        
    
    def SetValue(self, value, item, col):
        self.log.write("SetValue: %s\n" % value)
        
        # We're not allowing edits in column zero (see below) so we just need
        # to deal with Song objects and cols 1, 2 and 3 
        
        node = self.ItemToObject(item)
        if isinstance(node, Song):
            if col == 1:
                node.artist = value
            elif col == 2:
                node.title = value
            elif col == 3:
                node.id = value
    
    

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log, data=None, model=None):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        # Create a dataview control
        self.dvc = dv.DataViewCtrl(self,
                                   style=wx.BORDER_THEME
                                   | dv.DV_ROW_LINES # nice alternating bg colors
                                   #| dv.DV_HORIZ_RULES
                                   | dv.DV_VERT_RULES
                                   | dv.DV_MULTIPLE
                                   )
        
        # Create an instance of our model...
        if model is None:
            self.model = MyTreeListModel(data, log)
        else:
            self.model = model            

        # Tel the DVC to use the model
        self.dvc.AssociateModel(self.model)

        # Define the columns that we want in the view. Notice the 2nd
        # parameter which tells the view which col in the data model to pull
        # values from for each view column.
        self.dvc.AppendTextColumn("Genre",   0, width=80)
        self.dvc.AppendTextColumn("Artist",  1, width=170, mode=dv.DATAVIEW_CELL_EDITABLE)
        self.dvc.AppendTextColumn("Title",   2, width=260, mode=dv.DATAVIEW_CELL_EDITABLE)
        c3 = self.dvc.AppendTextColumn("id", 3, width=40,  mode=dv.DATAVIEW_CELL_EDITABLE)
        c3.Alignment = wx.ALIGN_RIGHT
        
        # Set some additional attributes for the columns
        for c in self.dvc.Columns:
            c.Sortable = True
            c.Reorderable = True

            
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self.dvc, 1, wx.EXPAND)
        
        b1 = wx.Button(self, label="New View", name="newView")
        self.Bind(wx.EVT_BUTTON, self.OnNewView, b1)
        
        self.Sizer.Add(b1, 0, wx.ALL, 5)
        
        
    def OnNewView(self, evt):
        f = wx.Frame(None, title="New view, shared model", size=(600,400))
        TestPanel(f, self.log, model=self.model)
        b = f.FindWindowByName("newView")
        b.Disable()
        f.Show()
        
        
#----------------------------------------------------------------------

def runTest(frame, nb, log):
    # Reuse the music data in the ListCtrl sample, and put it in a
    # hierarchical structure so we can show it as a tree
    import ListCtrl
    musicdata = ListCtrl.musicdata.items()
    musicdata.sort()

    # our data structure will be a collection of Genres, each of which is a
    # collection of Songs
    data = dict()
    for key, val in musicdata:
        song = Song(str(key), val[0], val[1], val[2])
        genre = data.get(song.genre)
        if genre is None:
            genre = Genre(song.genre)
            data[song.genre] = genre
        genre.songs.append(song)
    data = data.values()
                
    win = TestPanel(nb, log, data=data)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>DataViewCtrl with custom DataViewModel</center></h2>

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

