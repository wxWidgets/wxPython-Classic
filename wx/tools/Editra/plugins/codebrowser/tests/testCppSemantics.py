from unittest import TestCase
from unittest import main as TestMain

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatter import Formatter

# Put package on path
import os
import sys
sys.path.insert(0, os.path.abspath('../codebrowser/gentag'))

from CppSemantics import CppSemantics


class CFormatter(Formatter):

    def format(self, tokensource, outfile):
        line_count = 1
        current_line = []

        # Parse the file into tokens and values
        for ttype, value in tokensource:
            if '\n' in value:
                line_count += value.count('\n')
                continue
            if ( len(value.strip()) != 0 ):
                current_line.append((ttype, value, line_count ))
        self.current_line = current_line
        

class FakeRTags( object ):
    def __init__( self ):
        self.ids = {}
        
    def AddElement( self, elementid, ctags ):
        if elementid in self.ids:
            self.ids [ elementid ].append( ctags )
        else:
            self.ids [ elementid ] = [ ctags ]
            
    def GetClass( self ):
        return self.ids[ 'class' ]

    def GetFunction( self ):
        return self.ids[ 'function' ]


class TestCppSemantics( TestCase ):
    
    def setUp( self ):
        self.lexer = get_lexer_by_name( "cpp", stripnl = False )
        self.formatter = CFormatter()
        
    def testSimpleClass( self ):
        className = "TestClassName"

        code = " class %s { } ;" % className
        highlight( code, self.lexer, self.formatter)
        myRTags = FakeRTags()
        test = CppSemantics( myRTags )
        
        for t,v,num in self.formatter.current_line:
            test.Feed( t,v,num )
        
        self.assertEqual( myRTags.GetClass()[0].name, className, 
        "Class Name did not match %s" % myRTags.GetClass()[0].name )
        
        self.assertEqual( test.state, 'start', 
        "Semantics not in correct state '%s'" % ( test.state ))
        
        
    def testSimpleClass2( self ):
        className = "TestClassName"

        code = " class %s : public BaseClass { } ;" % className
        highlight( code, self.lexer, self.formatter)
        myRTags = FakeRTags()
        test = CppSemantics( myRTags )
        
        for t,v,num in self.formatter.current_line:
            test.Feed( t,v,num )
        
        self.assertEqual( myRTags.GetClass()[0].name, className, 
        "Class Name did not match %s" % myRTags.GetClass()[0].name )

        self.assertEqual( test.state, 'start', 
        "Semantics not in correct state '%s'" % ( test.state ))


    def testSimpleClassWithBlocks( self ):
        className = "TestClassName"

        code = " class %s : public BaseClass { { {} } } ;" % className
        highlight( code, self.lexer, self.formatter)
        myRTags = FakeRTags()
        test = CppSemantics( myRTags )
        
        for t,v,num in self.formatter.current_line:
            test.Feed( t,v,num )
        
        self.assertEqual( myRTags.GetClass()[0].name, className, 
        "Class Name did not match %s" % myRTags.GetClass()[0].name )

        self.assertEqual( test.state, 'start', 
        "Semantics not in correct state '%s'" % ( test.state ))


    def testSimpleFunc( self ):
        funcName = "myFuncName"

        code = " int %s (int count, char* mess ) ;" % funcName
        highlight( code, self.lexer, self.formatter)
        myRTags = FakeRTags()
        test = CppSemantics( myRTags )
        
        for t,v,num in self.formatter.current_line:
            test.Feed( t,v,num )
        
        self.assertEqual( myRTags.GetFunction()[0].name, funcName, 
        "Function Name did not match %s" % myRTags.GetFunction()[0].name )

        self.assertEqual( test.state, 'start', 
        "Semantics not in correct state '%s'" % ( test.state ))



    def testSimpleFuncWithLineIssueGood( self ):
        funcName = "myFuncName"

        code = """#include <stdio.h>



int %s (int count, char* mess ) ;""" % funcName
        highlight( code, self.lexer, self.formatter)
        myRTags = FakeRTags()
        test = CppSemantics( myRTags )
        
        for t,v,num in self.formatter.current_line:
            test.Feed( t,v,num )
        
        #print myRTags.GetFunction()[0].GetLine()
        
        self.assertEqual( myRTags.GetFunction()[0].GetLine(), 5, 
        "Function not found on line 5, but instead on line %s" % myRTags.GetFunction()[0].GetLine() )

        self.assertEqual( test.state, 'start', 
        "Semantics not in correct state '%s'" % ( test.state ))

    def testSimpleFuncWithLineIssueBad( self ):
        funcName = "myFuncName"

        code = """



int %s (int count, char* mess ) ;""" % funcName
        highlight( code, self.lexer, self.formatter)
        myRTags = FakeRTags()
        test = CppSemantics( myRTags )
        
        for t,v,num in self.formatter.current_line:
            test.Feed( t,v,num )
        
        #print myRTags.GetFunction()[0].GetLine()
        
        self.assertEqual( myRTags.GetFunction()[0].GetLine(), 5, 
        "Function not found on line 5, but instead on line %s" % myRTags.GetFunction()[0].GetLine() )

        self.assertEqual( test.state, 'start', 
        "Semantics not in correct state '%s'" % ( test.state ))



    def testSimpleFuncWithBody( self ):
        funcName = "myFuncName"

        code = " int %s (int count, char* mess ) {  } " % funcName
        highlight( code, self.lexer, self.formatter)
        myRTags = FakeRTags()
        test = CppSemantics( myRTags )
        
        for t,v,num in self.formatter.current_line:
            test.Feed( t,v,num )
        
        self.assertEqual( myRTags.GetFunction()[0].name, funcName, 
        "Function Name did not match %s" % myRTags.GetFunction()[0].name )

        self.assertEqual( test.state, 'start', 
        "Semantics not in correct state '%s'" % ( test.state ))


    def testSimpleFuncWithBodyCout( self ):
        funcName = "myFuncName"

        code = """ {  
            cout << "mycount";
        } """ 
        highlight( code, self.lexer, self.formatter)
        myRTags = FakeRTags()
        test = CppSemantics( myRTags )
        
        for t,v,num in self.formatter.current_line:
            test.Feed( t,v,num )
        

        self.assertEqual( test.state, 'start', 
        "Semantics not in correct state '%s'" % ( test.state ))



    def testSimpleFuncWithBodyWithBlocks( self ):
        funcName = "myFuncName"

        code = " int %s (int count, char* mess ) { {} {}  } " % funcName
        highlight( code, self.lexer, self.formatter)
        myRTags = FakeRTags()
        test = CppSemantics( myRTags )
        
        for t,v,num in self.formatter.current_line:
            test.Feed( t,v,num )
        
        self.assertEqual( myRTags.GetFunction()[0].name, funcName, 
        "Function Name did not match %s" % myRTags.GetFunction()[0].name )

        self.assertEqual( test.state, 'start', 
        "Semantics not in correct state '%s'" % ( test.state ))


    def testSimpleMemFunc( self ):
        className = "myclassname"
        funcName = "myFuncName"

        code = """  
        class %s {
        int %s (int count, char* mess ) ;
        };
        """ % ( className, funcName )
        highlight( code, self.lexer, self.formatter)
        myRTags = FakeRTags()
        test = CppSemantics( myRTags )
        
        for t,v,num in self.formatter.current_line:
            test.Feed( t,v,num )
        
        self.assertEqual( myRTags.GetClass()[0].name, className, 
        "Class Name did not match %s" % myRTags.GetClass()[0].name )

        mf = myRTags.GetClass()[0].GetElements()[0]

        self.assertEqual( mf['method'][0].GetName(), funcName, 
        "Function Name %s did not match %s" % (mf['method'][0].GetName(), funcName) )

        self.assertEqual( test.state, 'start', 
        "Semantics not in correct state '%s'" % ( test.state ))


    def testSimpleMemVar( self ):
        className = "myclassname"
        funcName = "myFuncName"
        varName = "MyVarName"


        code = """  
        class %s {
        int %s = 99; 
        int %s (int count, char* mess ) ;
        };
        """ % ( className, varName , funcName)
        highlight( code, self.lexer, self.formatter)
        myRTags = FakeRTags()
        test = CppSemantics( myRTags )
        
        for t,v,num in self.formatter.current_line:
            test.Feed( t,v,num )
        
        self.assertEqual( myRTags.GetClass()[0].name, className, 
        "Class Name did not match %s" % myRTags.GetClass()[0].name )

        mf = myRTags.GetClass()[0].GetElements()[0]

        self.assertEqual( mf['variable'][0].GetName(), varName, 
        "Function Name %s did not match %s" % (mf['variable'][0].GetName(), varName) )

        self.assertEqual( test.state, 'start', 
        "Semantics not in correct state '%s'" % ( test.state ))



    def testSimpleMemFuncDestructor( self ):
        className = "myclassname"
        funcName = "~myDesctructorName"

        code = """  
        class %s {
        int %s (int count, char* mess ) ;
        };
        """ % ( className, funcName )
        highlight( code, self.lexer, self.formatter)
        myRTags = FakeRTags()
        test = CppSemantics( myRTags )
        
        for t,v,num in self.formatter.current_line:
            test.Feed( t,v,num )
        
        self.assertEqual( myRTags.GetClass()[0].name, className, 
        "Class Name did not match %s" % myRTags.GetClass()[0].name )

        mf = myRTags.GetClass()[0].GetElements()[0]

        self.assertEqual( mf['method'][0].GetName(), funcName, 
        "Function Name %s did not match %s" % (mf['method'][0].GetName(), funcName) )

        self.assertEqual( test.state, 'start', 
        "Semantics not in correct state '%s'" % ( test.state ))



    def testSimpleMemFuncWithBody( self ):
        funcName = "myFuncName"
        className = "myclassname"

        code = """  
        class %s {
        int %s (int count, char* mess ) {  }
        };
        """ % ( className, funcName )
        highlight( code, self.lexer, self.formatter)
        myRTags = FakeRTags()
        test = CppSemantics( myRTags )
        
        for t,v,num in self.formatter.current_line:
            test.Feed( t,v,num )
        
        
        self.assertEqual( myRTags.GetClass()[0].name, className, 
        "Class Name did not match %s" % myRTags.GetClass()[0].name )

        mf = myRTags.GetClass()[0].GetElements()[0]

        self.assertEqual( mf['method'][0].GetName(), funcName, 
        "Function Name %s did not match %s" % (mf['method'][0].GetName(), funcName) )
        

        self.assertEqual( test.state, 'start', 
        "Semantics not in correct state '%s'" % ( test.state ))


    def testSimpleMemFuncWithBodyWithBlocks( self ):
        className = "myclassname"
        funcName1 = "myFuncName1"
        funcName2 = "myFuncName2"
        funcName3 = "myFuncName3"

        code =  """  
        class %s {
        int %s (int count, char* mess ) ;
        int %s (int count, char* mess ) {  }
        int %s (int count, char* mess ) { {} {}  } 
        };
        """% ( className, funcName1, funcName2, funcName3 )
        
        
        highlight( code, self.lexer, self.formatter)
        myRTags = FakeRTags()
        test = CppSemantics( myRTags )
        
        for t,v,num in self.formatter.current_line:
            test.Feed( t,v,num )


        self.assertEqual( myRTags.GetClass()[0].name, className, 
        "Class Name did not match %s" % myRTags.GetClass()[0].name )

        mf = myRTags.GetClass()[0].GetElements()[0]

        self.assertEqual( mf['method'][0].GetName(), funcName1, 
        "Function Name %s did not match %s" % (mf['method'][0].GetName(), funcName1) )
        self.assertEqual( mf['method'][1].GetName(), funcName2, 
        "Function Name %s did not match %s" % (mf['method'][1].GetName(), funcName2) )
        self.assertEqual( mf['method'][2].GetName(), funcName3, 
        "Function Name %s did not match %s" % (mf['method'][2].GetName(), funcName3) )

        self.assertEqual( test.state, 'start', 
        "Semantics not in correct state '%s'" % ( test.state ))


    def testMemFuncs( self ):
        className = "myclassname"
        funcName = "myFuncName"

        code =  """  
        class %s {
        int %s (int count, char* mess ) { {} {}  } 
        };
        """% ( className, funcName )
        
        
        highlight( code, self.lexer, self.formatter)
        myRTags = FakeRTags()
        test = CppSemantics( myRTags )
        
        for t,v,num in self.formatter.current_line:
            test.Feed( t,v,num )

        self.assertEqual( myRTags.GetClass()[0].name, className, 
        "Class Name did not match %s" % myRTags.GetClass()[0].name )

        mf = myRTags.GetClass()[0].GetElements()[0]

        self.assertEqual( mf['method'][0].GetName(), funcName, 
        "Function Name %s did not match %s" % (mf['method'][0].GetName(), funcName) )

        self.assertEqual( test.state, 'start', 
        "Semantics not in correct state '%s'" % ( test.state ))

    def testExternalMemFuncs( self ):
        className = "ClassName"
        funcName = "FuncName"

        code =  """  
        int %s::%s (int count, char* mess ) { {} {}  } 
        """% ( className, funcName )
        
        
        highlight( code, self.lexer, self.formatter)
        myRTags = FakeRTags()
        test = CppSemantics( myRTags )
        
        for t,v,num in self.formatter.current_line:
            test.Feed( t,v,num )

        self.assertEqual( myRTags.GetClass()[0].name, className, 
        "Class Name did not match %s" % myRTags.GetClass()[0].name )

        mf = myRTags.GetClass()[0].GetElements()[0]

        self.assertEqual( mf['method'][0].GetName(), funcName, 
        "Function Name %s did not match %s" % (mf['method'][0].GetName(), funcName) )

        self.assertEqual( test.state, 'start', 
        "Semantics not in correct state '%s'" % ( test.state ))


    def testExternalMemFuncDestructor( self ):
        className = "myclassname"
        funcName = "~myDesctructorName"

        code = """  
        void %s::%s( char* param1 ) {
            return param1;
        };
        """ % ( className, funcName )
        highlight( code, self.lexer, self.formatter)
        myRTags = FakeRTags()
        test = CppSemantics( myRTags )
        
        for t,v,num in self.formatter.current_line:
            test.Feed( t,v,num )
        
        self.assertEqual( myRTags.GetClass()[0].name, className, 
        "Class Name did not match %s" % myRTags.GetClass()[0].name )

        mf = myRTags.GetClass()[0].GetElements()[0]

        self.assertEqual( mf['method'][0].GetName(), funcName, 
        "Function Name %s did not match %s" % (mf['method'][0].GetName(), funcName) )

        self.assertEqual( test.state, 'start', 
        "Semantics not in correct state '%s'" % ( test.state ))


    def testExternalMultipleMemFuncs( self ):
        className = "ClassName"
        funcName = "FuncName"
        funcName2 = "FuncName2"

        code =  """  
        int %s::%s (int count, char* mess ) { {} {}  } 
        int %s::%s (int count, char* mess ) {  } 
        """ % ( className, funcName, className, funcName2  )
        
        
        highlight( code, self.lexer, self.formatter)
        myRTags = FakeRTags()
        test = CppSemantics( myRTags )
        
        for t,v,num in self.formatter.current_line:
            test.Feed( t,v,num )

        self.assertEqual( myRTags.GetClass()[0].name, className, 
        "Class Name did not match %s" % myRTags.GetClass()[0].name )

        mf = myRTags.GetClass()[0].GetElements()[0]

        self.assertEqual( len(myRTags.GetClass()), 1, 
        "Too many classes (%d) created." % len(myRTags.GetClass()) )


        self.assertEqual( mf['method'][0].GetName(), funcName, 
        "Function Name %s did not match %s" % (mf['method'][0].GetName(), funcName) )

        self.assertEqual( test.state, 'start', 
        "Semantics not in correct state '%s'" % ( test.state ))


if ( __name__ == "__main__" ):
    TestMain()
    
