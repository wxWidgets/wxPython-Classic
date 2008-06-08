#ifndef _RAIIHELPERS_H_
#define _RAIIHELPERS_H_

// RAII Helpers -- C++ wrappers to aid in exception safety and convenience.
//
// RAII (Resource Acquisition Is Initialization):
// Release resources automatically in the destructor if acquired before.
//
// For further information:
// http://wiki.wxpython.org/GSoC2008/RecognizingPythonCallbackExceptions
//
// XXX: make sure to include wxPython.h or wxPython_int.h before this file.
// 


// wxPyThreadBlocker -- Safe GIL handling

enum wxPTB_BlockType
{
    wxPTB_INIT_BLOCK,
    wxPTB_INIT_UNBLOCK
};

class wxPyThreadBlocker
{
public:
    wxPyThreadBlocker(wxPTB_BlockType bt = wxPTB_INIT_BLOCK) 
    {
        if (bt == wxPTB_INIT_BLOCK)
            Block();
        else
            m_is_blocked = false;
    }

    ~wxPyThreadBlocker() 
    { 
        if (m_is_blocked)
            Unblock(); 
    }

    bool IsBlocked() const 
    { 
        return m_is_blocked; 
    }

    void Block() 
    {
        //XXX: wxASSERT unsafe here? wxASSERT(m_is_blocked == false);
        m_state = wxPyBeginBlockThreads(); 
        m_is_blocked = true;
    }

    void Unblock() 
    { 
        //XXX: wxASSERT unsafe here? wxASSERT(m_is_blocked == true);
        wxPyEndBlockThreads(m_state); 
        m_is_blocked = false;
    }

private:
    bool m_is_blocked;
    wxPyBlock_t m_state;
};

// wxPyObject -- deal with PyObjects conveniently in C++

class wxPyObject
{
public:
    wxPyObject() 
    { 
        m_obj = NULL; 
        m_borrowed = true;
    }

    // We don't know if the GIL is held during destruction, so lock explicitly.
    // GILState API locks support recursion (if needed).
    ~wxPyObject()
    {
        wxPyBlock_t st = wxPyBeginBlockThreads();
        Decref();
        wxPyEndBlockThreads(st);
    }

    // Take PyObject* on construction. 
    // Assume that a Python API function already INCREFed the object for us.
    wxPyObject(PyObject *obj)
    {
        m_obj = obj;
        m_borrowed = false;
    }

    // INCREF wxPyObject on construction. 
    wxPyObject(const wxPyObject &cpy)
    {
        m_obj = cpy.m_obj;
        m_borrowed = false;
        Incref();
    }

    // Take PyObject* on assignment. 
    // Assume that a Python API function already INCREFed the object for us.
    const wxPyObject &operator=(PyObject *obj)
    {
        Take(obj);
        return *this;
    }

    // INCREF wxPyObject on assignment. 
    const wxPyObject &operator=(const wxPyObject &cpy)
    {
        Ref(cpy.m_obj);
        return *this;
    }

    //XXX: Don't rely on this to pass a wxPyObject as a vararg! Use Get() instead.
    operator PyObject*()
    {
        return m_obj;
    }

    bool Ok() const
    {
        return m_obj != NULL;
    }

    // Borrow a reference to obj -- avoid DECREF in destructor.
    void Borrow(PyObject *obj)
    {
        if (obj != m_obj) {
            Decref();
            m_obj = obj; 
            m_borrowed = true;
        }
    }

    // Add a new reference to obj.
    void Ref(PyObject *obj)
    {
        if (obj != m_obj) {
            Decref();
            m_obj = obj; 
            m_borrowed = false;
            Incref();
        }
    }

    // Assume obj was INCREFed for us.
    void Take(PyObject *obj)
    {
        if (obj != m_obj) {
            Decref();
            m_obj = obj; 
            m_borrowed = false;
        }
    }

    PyObject *Get() const
    {
        return m_obj;
    }

    // Convert to borrowed, to transfer reference to list, tuple, etc.
    // Avoid DECREF in destructor.
    PyObject *Transfer()
    {
        m_borrowed = true;
        return m_obj;
    }

    // Shorthand for Transfer() and Clear().
    PyObject *Remove()
    {
        PyObject *ret = m_obj;
        m_obj = NULL;
        m_borrowed = true;
        return ret;
    }

    // Perform DECREF if m_borrowed == false, set m_obj to NULL. 
    void Clear()
    {
        Decref();
    }

private:
    void Decref()
    {
        if (!m_borrowed)
            Py_XDECREF(m_obj);
        m_obj = NULL;
    }

    void Incref()
    {
        Py_XINCREF(m_obj);
    }

private:
    bool m_borrowed;
    PyObject *m_obj;
};

inline bool operator==(const wxPyObject &lhs, const wxPyObject &rhs)
{
    return lhs.Get() == rhs.Get();
}

inline bool operator==(const wxPyObject &lhs, PyObject *rhs)
{
    return lhs.Get() == rhs;
}

inline bool operator==(PyObject *lhs, const wxPyObject &rhs)
{
    return lhs == rhs.Get();
}

inline bool operator!=(const wxPyObject &lhs, const wxPyObject &rhs)
{
    return lhs.Get() != rhs.Get();
}

inline bool operator!=(const wxPyObject &lhs, PyObject *rhs)
{
    return lhs.Get() != rhs;
}

inline bool operator!=(PyObject *lhs, const wxPyObject &rhs)
{
    return lhs != rhs.Get();
}
#endif
