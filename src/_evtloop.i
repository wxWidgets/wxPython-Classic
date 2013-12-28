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
// TODO:
//   * wxPyEventLoop that virtualizes all the methods
//   * Add wxEventLoopSource when MSW gets an implementation    
//---------------------------------------------------------------------------
%newgroup

%{
#include <wx/evtloop.h>
%}

class wxEventLoopBase
{
public:
    // wxEventLoopBase();    *** It's an ABC, can't instantiate
    virtual ~wxEventLoopBase();

    // use this to check whether the event loop was successfully created before
    // using it
    virtual bool IsOk() const;

    // returns true if this is the main loop
    bool IsMain() const;
    
    // start the event loop, return the exit code when it is finished
    virtual int Run();

    // is the event loop running now?
    virtual bool IsRunning() const;

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

    // implement this to wake up the loop: usually done by posting a dummy event
    // to it (can be called from non main thread)
    virtual void WakeUp();

    // idle handling
    // -------------

    // make sure that idle events are sent again
    virtual void WakeUpIdle();

        // this virtual function is called  when the application
        // becomes idle and normally just sends wxIdleEvent to all interested
        // parties
        //
        // it should return true if more idle events are needed, false if not
    virtual bool ProcessIdle();


        // process all currently pending events right now
        //
        // it is an error to call Yield() recursively unless the value of
        // onlyIfNeeded is true
        //
        // WARNING: this function is dangerous as it can lead to unexpected
        //          reentrancies (i.e. when called from an event handler it
        //          may result in calling the same event handler again), use
        //          with _extreme_ care or, better, don't use at all!
    bool Yield(bool onlyIfNeeded = false);
    virtual bool YieldFor(long eventsToProcess);

        // returns true if the main thread is inside a Yield() call
    virtual bool IsYielding() const;

        // returns true if events of the given event category should be immediately
        // processed inside a wxApp::Yield() call or rather should be queued for
        // later processing by the main event loop
    virtual bool IsEventAllowedInsideYield(wxEventCategory cat) const;

    
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
    wxEventLoopActivator(wxEventLoopBase *evtLoop);
    ~wxEventLoopActivator();
};
 

//---------------------------------------------------------------------------
