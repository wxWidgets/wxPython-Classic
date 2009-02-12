/////////////////////////////////////////////////////////////////////////////
// Name:        _evtloop.i
// Purpose:     SWIG interface for wxEventLoop
//
// Author:      Robin Dunn
//
// Created:     18-Sept-2004
// RCS-ID:      $Id$
// Copyright:   (c) 2004 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

// Not a %module


//---------------------------------------------------------------------------
// TODO: wxPyEventLoop that virtualizes all the methods...

//---------------------------------------------------------------------------
%newgroup

%{
#include <wx/evtloop.h>
%}

class wxEventLoopBase
{
public:
    // wxEventLoopBase();    *** It's an ABC, can't instantiate
    virtual ~wxEventLoop();

    // use this to check whether the event loop was successfully created before
    // using it
    virtual bool IsOk() const;

    // start the event loop, return the exit code when it is finished
    virtual int Run();

    // exit from the loop with the given exit code
    virtual void Exit(int rc = 0);

    // return true if any events are available
    virtual bool Pending() const;

    // dispatch a single event, return false if we should exit from the loop
    virtual bool Dispatch();

    // same as Dispatch() but doesn't wait for longer than the specified (in
    // ms) timeout, return true if an event was processed, false if we should
    // exit the loop or -1 if timeout expired
    virtual int DispatchTimeout(unsigned long timeout) ;

    // is the event loop running now?
    virtual bool IsRunning() const;

    virtual void WakeUp();
    
    // return currently active (running) event loop, may be NULL
    static wxEventLoopBase* GetActive();

    // set currently active (running) event loop
    static void SetActive(wxEventLoopBase* loop);
};


// class wxEventLoopManual : public wxEventLoopBase
// {
// public:
//     wxEventLoopManual();
// };


class wxGUIEventLoop : public wxEventLoopBase
{
public:
    wxGUIEventLoop();
};



%pythoncode {
    class EventLoop(GUIEventLoop):
        """Class using the old name for compatibility."""
        pass
}



class wxModalEventLoop : public wxGUIEventLoop
{
public:
    wxModalEventLoop(wxWindow *winModal);
};



// This object sets the wxEventLoop given to the ctor as the currently active
// one and unsets it in its dtor, this is especially useful in presence of
// exceptions but is more tidy even when we don't use them
class wxEventLoopActivator
{
public:
    wxEventLoopActivator(wxEventLoop *evtLoop);
    ~wxEventLoopActivator();
};
 

//---------------------------------------------------------------------------
