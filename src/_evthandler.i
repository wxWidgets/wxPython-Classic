/////////////////////////////////////////////////////////////////////////////
// Name:        _evthandler.i
// Purpose:     SWIG interface for wxEventHandler
//
// Author:      Robin Dunn
//
// Created:     9-Aug-2003
// RCS-ID:      $Id$
// Copyright:   (c) 2003 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

// Not a %module


//---------------------------------------------------------------------------
%newgroup

// wxEvtHandler: the base class for all objects handling wxWindows events
class wxEvtHandler : public wxObject {
public:
    // turn off this typemap
    %typemap(out) wxEvtHandler*;    

    %pythonAppend wxEvtHandler         "self._setOORInfo(self)"
    wxEvtHandler();

    // Turn it back on again
    %typemap(out) wxEvtHandler* { $result = wxPyMake_wxObject($1, $owner); }

    wxEvtHandler* GetNextHandler();
    wxEvtHandler* GetPreviousHandler();
    void SetNextHandler(wxEvtHandler* handler);
    void SetPreviousHandler(wxEvtHandler* handler);

    bool GetEvtHandlerEnabled();
    void SetEvtHandlerEnabled(bool enabled);

    void Unlink();
    bool IsUnlinked() const;

    // process an event right now
    bool ProcessEvent(wxEvent& event);

    // Process an event by calling ProcessEvent and handling any exceptions
    // thrown by event handlers. It's mostly useful when processing wx events
    // when called from C code (e.g. in GTK+ callback) when the exception
    // wouldn't correctly propagate to wxEventLoop.
    bool SafelyProcessEvent(wxEvent& event);

    // This method tries to process the event in this event handler, including
    // any preprocessing done by TryBefore() and all the handlers chained to
    // it, but excluding the post-processing done in TryAfter().
    //
    // It is meant to be called from ProcessEvent() only and is not virtual,
    // additional event handlers can be hooked into the normal event processing
    // logic using TryBefore() and TryAfter() hooks.
    //
    // You can also call it yourself to forward an event to another handler but
    // without propagating it upwards if it's unhandled (this is usually
    // unwanted when forwarding as the original handler would already do it if
    // needed normally).
    bool ProcessEventLocally(wxEvent& event);

    
    void QueueEvent(wxEvent *event);
    
    // add an event to be processed later
    void AddPendingEvent(const wxEvent& event);

    // process all pending events
    void ProcessPendingEvents();

    void DeletePendingEvents();
    
    %extend {
        // Dynamic association of a member function handler with the event handler
        void Connect( int id, int lastId, wxEventType eventType, PyObject* func) {
            bool is_callable = false;
            {
                wxPyThreadBlocker blocker;
                is_callable = PyCallable_Check(func) != 0;
            }
            if (is_callable) {
                self->Connect(id, lastId, eventType,
                              (wxObjectEventFunction)(wxEventFunction)
                              &wxPyCallback::EventThunker,
                              new wxPyCallback(func));
            }
            else if (func == Py_None) {
                self->Disconnect(id, lastId, eventType,
                                 (wxObjectEventFunction)(wxEventFunction)
                                 &wxPyCallback::EventThunker);
            }
            else {
                wxPyBLOCK_THREADS(
                    PyErr_SetString(PyExc_TypeError, "Expected callable object or None."));
            }
        }

        bool Disconnect(int id, int lastId = -1,
                        wxEventType eventType = wxEVT_NULL,
                        PyObject* func = NULL ) {
            if (func && func != Py_None) {
                // Find the current matching binder that has this function
                // pointer and dissconnect that one.  Unfortuneatly since we
                // wrapped the PyObject function pointer in another object we
                // have to do the searching ourselves...
                wxList::compatibility_iterator node = self->GetDynamicEventTable()->GetFirst();
                while (node)
                {
                    wxDynamicEventTableEntry *entry = (wxDynamicEventTableEntry*)node->GetData();
                    if ((entry->m_id == id) &&
                        ((entry->m_lastId == lastId) || (lastId == wxID_ANY)) &&
                        ((entry->m_eventType == eventType) || (eventType == wxEVT_NULL)) &&
                        // FIXME?
                        //((entry->m_fn->IsMatching((wxObjectEventFunction)(wxEventFunction)&wxPyCallback::EventThunker))) &&
                        (entry->m_callbackUserData != NULL))
                    {
                        wxPyCallback *cb = (wxPyCallback*)entry->m_callbackUserData;
                        wxPyBlock_t blocked = wxPyBeginBlockThreads();
                        int result = PyObject_Compare(cb->m_func, func);
                        wxPyEndBlockThreads(blocked); 
                        if (result == 0) {
                            delete cb;
                            self->GetDynamicEventTable()->Erase(node);
                            delete entry;
                            return true;
                        }                        
                    }
                    node = node->GetNext();
                }
                return false;

            }
            else {
                return self->Disconnect(id, lastId, eventType,
                                        (wxObjectEventFunction)
                                        &wxPyCallback::EventThunker);
            }
        }
    }

    %pythonAppend _setOORInfo   "args[0].this.own(False)";
    %extend {
        void _setOORInfo(PyObject* _self, bool incref=true) {
            if (_self && _self != Py_None) {
                self->SetClientObject(new wxPyOORClientData(_self, incref));
            }
            else {
                wxPyOORClientData* data = (wxPyOORClientData*)self->GetClientObject();
                if (data) {
                    self->SetClientObject(NULL);  // This will delete it too
                }
            }
        }
    }

    %pythoncode {
        def Bind(self, event, handler, source=None, id=wx.ID_ANY, id2=wx.ID_ANY):
            """
            Bind an event to an event handler.

            :param event: One of the EVT_* objects that specifies the
                          type of event to bind,

            :param handler: A callable object to be invoked when the
                          event is delivered to self.  Pass None to
                          disconnect an event handler.

            :param source: Sometimes the event originates from a
                          different window than self, but you still
                          want to catch it in self.  (For example, a
                          button event delivered to a frame.)  By
                          passing the source of the event, the event
                          handling system is able to differentiate
                          between the same event type from different
                          controls.

            :param id: Used to spcify the event source by ID instead
                       of instance.

            :param id2: Used when it is desirable to bind a handler
                          to a range of IDs, such as with EVT_MENU_RANGE.
            """
            assert isinstance(event, wx.PyEventBinder)
            assert handler is None or callable(handler)
            assert source is None or hasattr(source, 'GetId')
            if source is not None:
                id  = source.GetId()
            event.Bind(self, id, id2, handler)              

        def Unbind(self, event, source=None, id=wx.ID_ANY, id2=wx.ID_ANY, handler=None):
            """
            Disconnects the event handler binding for event from self.
            Returns True if successful.
            """
            if source is not None:
                id  = source.GetId()
            return event.Unbind(self, id, id2, handler)              
    }

    %property(EvtHandlerEnabled, GetEvtHandlerEnabled, SetEvtHandlerEnabled, doc="See `GetEvtHandlerEnabled` and `SetEvtHandlerEnabled`");
    %property(NextHandler, GetNextHandler, SetNextHandler, doc="See `GetNextHandler` and `SetNextHandler`");
    %property(PreviousHandler, GetPreviousHandler, SetPreviousHandler, doc="See `GetPreviousHandler` and `SetPreviousHandler`");
    
};

//---------------------------------------------------------------------------
// A class derived from wxEvtHandler that allows the ProcessEvent method to be
// overridden in Python.

%{ // The Python-aware C++ class
class wxPyEvtHandler : public wxEvtHandler
{
    DECLARE_DYNAMIC_CLASS(wxPyEvtHandler)
public:
    wxPyEvtHandler() : wxEvtHandler() {}

    virtual bool ProcessEvent(wxEvent& event)
    {
        bool found;
        bool rval;
        wxString className = event.GetClassInfo()->GetClassName();

        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if ((found = wxPyCBH_findCallback(m_myInst, "ProcessEvent"))) {
            PyObject* arg = wxPyConstructObject((void*)&event, className);
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(O)",arg));
            Py_DECREF(arg);
        }
        wxPyEndBlockThreads(blocked);        
        if (! found)
            rval = wxEvtHandler::ProcessEvent(event);
        return rval;
    }
    
    PYPRIVATE;
};

IMPLEMENT_DYNAMIC_CLASS(wxPyEvtHandler, wxEvtHandler)
%}



// Let SWIG see this class too
DocStr(wxPyEvtHandler,
"The wx.PyEvtHandler class can be used to intercept calls to the
`ProcessEvent` method.  Simply derive a new class from this one,
override ProcessEvent, and then push an instance of the class onto the
event handler chain for a window using `wx.Window.PushEventHandler`.", "");
class wxPyEvtHandler : public wxEvtHandler
{
public:
    %pythonAppend wxPyEvtHandler   "self._setOORInfo(self);" setCallbackInfo(PyEvtHandler)
    wxPyEvtHandler();

    void _setCallbackInfo(PyObject* self, PyObject* _class);    
    
    DocDeclStr(
        virtual bool , ProcessEvent(wxEvent& event),
        "Override this method to intercept the events being sent to the window.
The default implementation searches the event tables and calls event
handler functions if matching event bindings are found.", "");
};

//---------------------------------------------------------------------------
