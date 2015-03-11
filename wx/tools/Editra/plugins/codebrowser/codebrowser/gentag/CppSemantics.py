""" Simplifed BNF for C++ and possibly for C """

import taglib

from pygments.token import Token

def DebugWrite( msg ):
    """ Conditionally be able to turn on debug messages.
    """
    import syslog

    if ( 1 ):
        syslog.syslog( msg ) 

#--------------------------------------------------------------------------#

class Stack( object ):
    """Stack is a simple wrapper for a list with push and pop exposed.
     """
    def __init__( self ):
        """start with empty stack """
        self._stack = []
 
    def push( self, item ):
        """Add item onto the stack """
        self._stack.append( item )
        
    def pop( self ):
        """Remove item from stack """
        try:
            return self._stack.pop() 
        except IndexError:
            return None

#--------------------------------------------------------------------------#


def NotUsed( *parms ):
    """ This function is used to state to "pylint" that I really
    am not using the variables that I passed in, but it's okay.
    """
    return len( parms )


class CppSemantics( object ):
    """A simplified BNF that will just look for the structures we 
    are interested in.
    """
 
    def __init__( self, rtags ):
        """Setup structure of BNF and initial classes and ids store. 
        """
        self.ids = {}
        self.classes = {}

        self._state = 'start'
        self.rtags = rtags
        self.currentclasstag = None
        self.destructor = False

        self.states = {
            'start': 
                [ 
                ( self.action_match, Token.Keyword, 'class', 'foundClass' ), #
                ( self.action_store, Token.Name, 'nameid', 'varOrfunc' ) 
                ],

            'varOrfunc': 
                [
                ( self.action_AddFunc, 'nameid', Token.Punctuation, 
                    '(', 'haveFuncParms'), #
                ( self.action_match, Token.Operator, ':', 'second'), 
                ( self.action_next_state, 'Endofline' ),
#                ( self.action_addVar, 'nameid', 'start' ),
                ],        
            'Endofline': 
                [
                ( self.action_match, Token.Punctuation, ';', 'start'), 
                ],        
            'second': 
                [
                ( self.action_addClass, 'nameid', Token.Operator, 
                    ':', 'externalMemFunc'), 
                ( self.action_next_state, 'start' ),
                ],        
            'externalMemFunc': 
                [
                ( self.action_destructor, Token.Operator, '~', 
                    'externalMemFunc') , #
                ( self.action_store, Token.Name, 'nameid', 'externalMemFunc' ) ,
                ( self.action_memfunc, 'nameid', Token.Punctuation, 
                    '(', 'haveExternalMemFuncParms'), 
                ],        
            'haveExternalMemFuncParms': 
                [
                ( self.action_match, Token.Punctuation, ')', 
                    'haveExternalMemFuncBodyStart'), 
                ],        

            'haveExternalMemFuncBodyStart': 
                [
                ( self.action_match_push, Token.Punctuation, '{', 
                    'haveExternalMemFuncBody', 'start'),
                ( self.action_next_state, 'start' ),
                ],        

            'haveExternalMemFuncBody': 
                [
                ( self.action_match_push, Token.Punctuation, '{', 
                    'haveExternalMemFuncBody', 'haveExternalMemFuncBody'), 
                ( self.action_match_pop, Token.Punctuation, '}'), 
                ],       
                
                 
            'haveFuncParms': 
                [
                ( self.action_match, Token.Punctuation, ')', 
                    'haveFuncBodyStart'), #
                ],        

            'haveFuncBodyStart': 
                [
                ( self.action_match_push, Token.Punctuation, '{', 
                    'haveFuncBody', 'start'), #
                ( self.action_match, Token.Punctuation, ';', 'start'), #
                ],        

            'haveFuncBody': 
                [
                ( self.action_match_push, Token.Punctuation, '{', 
                    'haveFuncBody', 'haveFuncBody'), #
                ( self.action_match_pop, Token.Punctuation, '}'), #
                ],        


            'foundClass': 
                [
                ( self.action_match_class, Token.Name.Class, 'findParents' ), #
                ],

            'findParents': 
                [
                ( self.action_match, Token.Punctuation, ':', 'classBody' ), #
                ( self.action_match_push, Token.Punctuation, 
                    '{', 'classBodyNext', 'start' ), #
                ],
                    
            'classBody': 
                [
                ( self.action_match_push, Token.Punctuation, 
                    '{', 'classBodyNext', 'start' ), #
                ],        
            'classBodyNext': 
                [
                ( self.action_match_push, Token.Punctuation, '{', 
                    'classBodyNext', 'classBodyNext' ), #
                ( self.action_match_pop,  Token.Punctuation, '}' ), #
                ( self.action_destructor, Token.Operator, '~', 
                    'classBodyNext') , #
                ( self.action_store, Token.Name, 'nameid', 'memfuncorvar' ), #
                ],        
            'memfuncorvar': 
                [
                ( self.action_memfunc, 'nameid', Token.Punctuation, 
                    '(', 'haveMemFuncParms'), # 
                ( self.action_addVar, 'nameid', 'classBodyNext' ),
                ],        
            'haveMemFuncParms': 
                [
                ( self.action_match, Token.Punctuation, ')', 
                    'haveMemFuncBodyStart'), 
                ],        

            'haveMemFuncBodyStart': 
                [
                ( self.action_match_push, Token.Punctuation, '{', 
                    'haveMemFuncBody', 'classBodyNext'), #
                ( self.action_match, Token.Punctuation, ';', 'classBodyNext'), #
                ],        

            'haveMemFuncBody': 
                [
                ( self.action_match_push, Token.Punctuation, '{', 
                    'haveMemFuncBody', 'haveMemFuncBody'), #
                ( self.action_match_pop, Token.Punctuation, '}'), #
                ],        

        }

    def _getState( self ):
        """ Get the current state variable 
        """
        return self._state
        
    def _setState( self, new_state ):
        """ Set the current state, we dubug info when possible 
        """
        #print "State change %s to %s " % ( self._state, new_state)
        self._state = new_state
    
    state = property( _getState, _setState )


    def action_destructor( self, token, value, num, parms ):
        """ Found a destructor, set flag 
        """
        NotUsed( num )
        to_token, to_value, next_state  = parms
        if token == to_token and value == to_value :
            self.state = next_state
            self.destructor = True
            return True
        return False


    def action_next_state( self, token, value, num, parms ):
        """ Just jump to the next state
        """
        NotUsed( num, token, value )
        self.state = parms[0]
        return True


    def action_AddFunc( self, token, value, num, parms ):
        """ Found function, add to rtag, and pop name
        """
        varid, to_token, to_value, next_state  = parms
        if token == to_token and value == to_value :
            self.state = next_state
            fname = self.ids[ varid ].pop()
            self.rtags.AddElement('function', taglib.Function(fname, num))
            return True
        return False

    def _FindClass( self, classname, num ):
        """ Search for classname and return existing rtag
        else add to dict a new rtag.
        """
        
        if ( not self.classes.get( classname, None) ):
            classtag = taglib.Class( classname, num )
            self.classes[ classname ] = classtag
            self.rtags.AddElement('class', classtag)
            return classtag
            
        else:
            return self.classes[ classname ]

    def action_addClass( self, token, value, num, parms ):
        """ Found Class, add to rtag, and pop name
        """
        varid, to_token, to_value, next_state  = parms
        if token == to_token and value == to_value :
            self.state = next_state
            classname = self.ids[ varid ].pop()
            self.currentclasstag = self._FindClass( classname, num )
            return True
        return False


    def action_addVar( self, token, value, num,  parms ):
        """ Variable Class, add to rtag, and pop name
        """
        NotUsed( token, value )
        varid, next_state  = parms
        self.state = next_state
        fname = self.ids[ varid ].pop()

        if ( hasattr( self, 'currentclasstag' ) ):
            self.currentclasstag.AddVariable(
                taglib.Variable(fname, num, self.currentclasstag.GetName() ))
        return True
        


    def action_memfunc( self, token, value, num, parms ):
        """ Found mem func, add to rtag, and pop name
        """
        varid, to_token, to_value, next_state  = parms
        if token == to_token and value == to_value :
            self.state = next_state
            fname = self.ids[ varid ].pop()

            self.currentclasstag.AddMethod(
                taglib.Function(fname, num, self.currentclasstag.GetName() ))
            return True
        return False



    def action_match_push( self, token, value, num, parms ):
        """ If match token, value push state to stack
        """
        NotUsed( num )
        to_token, to_value, next_state, last_state  = parms
        if token == to_token and value == to_value :
            self.state = next_state
            
            mybraces = self.ids.get( "{", Stack() )
            mybraces.push( last_state )
            self.ids["{"] = mybraces
            
            return True
        return False

    def action_match_pop( self, token, value, num, parms ):
        """ If match token, value pop state from stack
        and go to that state
        """
        NotUsed( num )

        to_token, to_value = parms
        if token == to_token and value == to_value :
            mybraces = self.ids.get( "{", Stack() )
            next_state = mybraces.pop()
            self.state = next_state
            return True
        return False

    # match token and value so that you go get the next_state
    def action_match( self, token, value, num, parms ):
        """ If match token, value then move to state
        """
        NotUsed( num )
        to_token, to_value, next_state = parms
        if token == to_token and value == to_value :
            self.state = next_state
            return True
            
        return False

    def action_match_class( self, token, value, num, parms ):
        """ If match token, value then move to state, add class 
        """
        to_token, next_state = parms
        if token == to_token:
            self.state = next_state
            self.currentclasstag = self._FindClass( value, num )
            return True
            
        return False

    def action_store( self, token, value, num,  parms ):
        """ If match token, push id 
        """
        NotUsed( num )
        to_token, varid, next_state = parms
        if ( token == to_token ):
            if ( self.destructor ):
                value = "~" + value
                self.destructor = False
        
            if ( hasattr( self.ids, varid ) ):
                self.ids[varid].append( value )
            else:
                self.ids[varid] = [ value ]
            self.state = next_state 
            return True
            
        return False

    def Feed( self, token, value, num ):
        """ Get next token, value, num and walk through state machine
        """

        current_state = self.state
        

        for idx, step in enumerate( self.states[self.state] ):
            DebugWrite( "%s %s" % (self.state, None) )

            action = step[0]
            parms = step[1:]
            result =  action( token, value, num, parms )
            if ( result ):
                DebugWrite ( "%s:%d ( %s ) => %s" % ( 
                current_state, idx, value, self.state ) )
                break


