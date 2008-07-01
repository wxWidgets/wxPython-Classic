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
    virtual ~wxPyObject()
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
    operator PyObject*() const
    {
        Py_INCREF(m_obj);
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

    // Interface for automatic type conversion
    //
    // This is overridden in sequence classes to add an item to a list or tuple.
    virtual void Push(PyObject *obj)
    {
        Take(obj);
    }

    // Return the next item in a sequence.
    // XXX: Use Ok() before Pop()
    virtual PyObject *Pop()
    {
        Py_INCREF(m_obj);
        return m_obj;
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

class wxPySequence: public wxPyObject
{
public:
    wxPySequence()
    {
        m_pos = 0;
    }

    wxPySequence(PyObject *obj): wxPyObject(obj), m_pos(0) {}
    wxPySequence(const wxPyObject &cpy): wxPyObject(cpy), m_pos(0) {}
    const wxPySequence &operator=(PyObject *obj) 
    { 
        Take(obj); 
        return *this;
    }
    const wxPySequence &operator=(const wxPyObject &cpy) 
    { 
        Ref(cpy.Get()); 
        return *this;
    }

    virtual ~wxPySequence() {}

    bool IsSequence() const
    {
        return PySequence_Check(Get()) == 1;
    }

    int Size() const
    {
        return PySequence_Size(Get());
    }

    int GetPos() const
    {
        return m_pos;
    }

    void ResetPos()
    {
        m_pos = 0;
    }

    virtual PyObject *Pop()
    {
        return PySequence_GetItem(Get(), m_pos++);
    }

protected:
    int m_pos;
};

class wxPyTuple: public wxPySequence
{
public:
    wxPyTuple(int len)
    {
        Take(PyTuple_New(len));
    }

    wxPyTuple(PyObject *obj): wxPySequence(obj) {}
    wxPyTuple(const wxPyObject &cpy): wxPySequence(cpy) {}
    const wxPyTuple &operator=(PyObject *obj) 
    { 
        Take(obj); 
        return *this;
    }
    const wxPyTuple &operator=(const wxPyObject &cpy) 
    { 
        Ref(cpy.Get()); 
        return *this;
    }

    virtual ~wxPyTuple() { }

    virtual void Push(PyObject *obj)
    {
        //XXX: no error handling/bounds checking
        PyTuple_SetItem(Get(), m_pos++, obj);
    }
};

class wxPyList: public wxPySequence
{
private:
    enum AddMode {
        ADD_APPEND,
        ADD_SETITEM,
    };

public:
    wxPyList(int len = 0)
    {
        Take(PyList_New(len));

        // If the list is initialized with len > 0 elements, we must use
        // PyList_SetItem() instead of PyList_Append()
        if (len == 0)
            m_mode = ADD_APPEND;
        else
            m_mode = ADD_SETITEM;
    }
    wxPyList(PyObject *obj): wxPySequence(obj), m_mode(ADD_APPEND) {}
    wxPyList(const wxPyObject &cpy): wxPySequence(cpy), m_mode(ADD_APPEND) {}
    const wxPyList &operator=(PyObject *obj) 
    { 
        Take(obj); 
        return *this;
    }
    const wxPyList &operator=(const wxPyObject &cpy) 
    { 
        Ref(cpy.Get()); 
        return *this;
    }

    virtual ~wxPyList() { }

    virtual void Push(PyObject *obj)
    {
        //XXX: no error handling/bounds checking
        switch (m_mode) {
        case ADD_APPEND:
            PyList_Append(Get(), obj);
        case ADD_SETITEM:
            PyList_SetItem(Get(), m_pos, obj);
        }

        m_pos++;
    }

private:
    AddMode m_mode;
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


// Insertion operators perform conversion from C++ to Python
//
inline wxPyObject &operator<<(wxPyObject &po, int i)
{
    po.Push(PyInt_FromLong(i));
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, unsigned int i)
{
    // Make a PyLong object to handle numbers > LONG_MAX
    po.Push(PyLong_FromUnsignedLong(i));
    return po;
}


inline wxPyObject &operator<<(wxPyObject &po, long i)
{
    po.Push(PyInt_FromLong(i));
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, unsigned long i)
{
    // Make a PyLong object to handle numbers > LONG_MAX
    po.Push(PyLong_FromUnsignedLong(i));
    return po;
}

/*
inline wxPyObject &operator<<(wxPyObject &po, size_t i)
{
    po.Push(PyInt_FromLong(i));
    return po;
}
*/

inline wxPyObject &operator<<(wxPyObject &po, bool i)
{
    po.Push(PyBool_FromLong(i));
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, double f)
{
    po.Push(PyFloat_FromDouble(f));
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, float f)
{
    po.Push(PyFloat_FromDouble(f));
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, const wxChar *s)
{
    po.Push(wx2PyString(s));
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, const wxString &s)
{
    po.Push(wx2PyString(s));
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, const wxArrayString &obj)
{
    po.Push(wxArrayString2PyList_helper(obj));
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, wxPyObject obj)
{
    po.Push(obj.Transfer());
    return po;
}

//NOTE: Here, po steals reference to obj.
inline wxPyObject &operator<<(wxPyObject &po, PyObject *obj)
{
    po.Push(obj);
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, const wxVariant &obj)
{
    po.Push(wxVariant_out_helper(obj));
    return po;
}

/*
inline wxPyObject &operator<<(wxPyObject &po, wxObject &obj)
{
    po.Push(wxPyMake_wxObject(&obj, false));
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, wxObject *obj)
{
    po.Push(wxPyMake_wxObject(obj, false));
    return po;
}
*/

//XXX: cast away const
inline wxPyObject &operator<<(wxPyObject &po, const wxObject &obj)
{
    po.Push(wxPyMake_wxObject((wxObject*)&obj, false));
    return po;
}

//XXX: cast away const
inline wxPyObject &operator<<(wxPyObject &po, const wxObject *obj)
{
    po.Push(wxPyMake_wxObject((wxObject*)obj, false));
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, const wxRect *obj)
{
    po.Push(wxPyConstructObject((void*)obj, wxT("wxRect"), 0));
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, const wxRect &obj)
{
    po.Push(wxPyConstructObject((void*)&obj, wxT("wxRect"), 0));
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, const wxKeyEvent &obj)
{
    po.Push(wxPyConstructObject((void*)&obj, wxT("wxKeyEvent"), 0));
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, const wxKeyEvent *obj)
{
    po.Push(wxPyConstructObject((void*)obj, wxT("wxKeyEvent"), 0));
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, const wxColour &obj)
{
    po.Push(wxPyConstructObject((void*)&obj, wxT("wxColour"), 0));
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, const wxFont &obj)
{
    po.Push(wxPyConstructObject((void*)&obj, wxT("wxFont"), 0));
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, const wxColour *obj)
{
    po.Push(wxPyConstructObject((void*)obj, wxT("wxColour"), 0));
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, const wxFont *obj)
{
    po.Push(wxPyConstructObject((void*)obj, wxT("wxFont"), 0));
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, const wxBitmap &obj)
{
    po.Push(wxPyConstructObject((void*)&obj, wxT("wxBitmap"), 0));
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, const wxBitmap *obj)
{
    po.Push(wxPyConstructObject((void*)obj, wxT("wxBitmap"), 0));
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, const wxMouseEvent &obj)
{
    po.Push(wxPyConstructObject((void*)&obj, wxT("wxMouseEvent"), 0));
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, const wxMouseEvent *obj)
{
    po.Push(wxPyConstructObject((void*)obj, wxT("wxMouseEvent"), 0));
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, const wxPoint &obj)
{
    po.Push(wxPyConstructObject((void*)&obj, wxT("wxPoint"), 0));
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, const wxPoint *obj)
{
    po.Push(wxPyConstructObject((void*)obj, wxT("wxPoint"), 0));
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, const wxControl &obj)
{
    po.Push(wxPyConstructObject((void*)&obj, wxT("wxControl"), 0));
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, const wxControl *obj)
{
    po.Push(wxPyConstructObject((void*)obj, wxT("wxControl"), 0));
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, const wxTreeItemId &obj)
{
    po.Push(wxPyConstructObject((void*)&obj, wxT("wxTreeItemId"), 0));
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, const wxTreeItemId *obj)
{
    po.Push(wxPyConstructObject((void*)obj, wxT("wxTreeItemId"), 0));
    return po;
}

// Extractors. Make sure to check Ok() and sequence length (if needed) before extracting.  

// Some helpful functions for the extractors.
//
// Use template functions to avoid ugly casting.
template <class T>
inline void wxPyExtractUint(wxPyObject &pyn, T &out, T tmax) 
{
    if (pyn.Ok() && !PyErr_Occurred()) {
        wxPyObject ro = pyn.Pop();
        unsigned long n = PyLong_AsUnsignedLong(pyn);

        /* PyLong_AsUnsignedLong() checks for overflow for unsigned long */
        if (PyErr_Occurred())
            wxThrowPyException();
        else if (n > tmax) {
            PyErr_SetString(PyExc_OverflowError, "Value too large.");
            wxThrowPyException();
        } else 
            out = n;
    }
}

template <class T>
inline void wxPyExtractInt(wxPyObject &pyn, T &out, T tmin, T tmax) 
{
    if (pyn.Ok() && !PyErr_Occurred()) {
        wxPyObject ro = pyn.Pop();
        long n = PyInt_AsLong(pyn);

        /* PyInt_AsLong() checks for overflow for long */
        if (PyErr_Occurred())
            wxThrowPyException();
        else if (n > tmax) {
            PyErr_SetString(PyExc_OverflowError, "Value too large.");
            wxThrowPyException();
        } else if (n < tmin) {
            PyErr_SetString(PyExc_OverflowError, "Value too small.");
            wxThrowPyException();
        } else 
            out = n;
    }
}

template <class T>
inline void wxPyExtractFloat(wxPyObject &pyn, T &out) 
{
    if (pyn.Ok() && !PyErr_Occurred()) {
        wxPyObject ro = pyn.Pop();
        double n = PyFloat_AsDouble(ro.Get());
        if (PyErr_Occurred())
            wxThrowPyException();
        else
            out = n;
    }
}

template <class T>
inline void wxPyExtractObject(const wxChar *typestr, wxPyObject &pyin, T *&out)
{
    if (pyin.Ok() && !PyErr_Occurred()) {
        T* ptr;
        wxPyObject ro = pyin.Pop();
        if (wxPyConvertSwigPtr(ro.Get(), (void **)&ptr, typestr))
            out = ptr;
        else {
            wxString msg;
            msg.Printf(wxT("Expected %s object."), typestr);
            PyErr_SetString(PyExc_TypeError, msg.mb_str());
            wxThrowPyException();
        }
    }
}

template <class T>
inline void wxPyExtractObjectCopy(const wxChar *typestr, wxPyObject &pyin, T &out)
{
    if (pyin.Ok() && !PyErr_Occurred()) {
        T* ptr;
        wxPyObject ro = pyin.Pop();
        if (wxPyConvertSwigPtr(ro.Get(), (void **)&ptr, typestr))
            out = *ptr;
        else {
            wxString msg;
            msg.Printf(wxT("Expected %s object."), typestr);
            PyErr_SetString(PyExc_TypeError, msg.mb_str());
            wxThrowPyException();
        }
    }
}

inline wxPyObject &operator>>(wxPyObject &po, int &out)
{
    wxPyExtractInt(po, out, INT_MIN, INT_MAX);
    return po;
}

inline wxPyObject &operator>>(wxPyObject &po, unsigned int &out)
{
    wxPyExtractUint(po, out, UINT_MAX);
    return po;
}

inline wxPyObject &operator>>(wxPyObject &po, long &out)
{
    wxPyExtractInt(po, out, LONG_MIN, LONG_MAX);
    return po;
}

inline wxPyObject &operator>>(wxPyObject &po, unsigned long &out)
{
    wxPyExtractUint(po, out, ULONG_MAX);
    return po;
}

inline wxPyObject &operator>>(wxPyObject &po, bool &out)
{
    if (po.Ok() && !PyErr_Occurred()) {
        wxPyObject ro = po.Pop();
        out = PyInt_AsLong(ro.Get());
        if (PyErr_Occurred()) {
            out = false;
            PyErr_Clear();
        }
    }
    return po;
}

inline wxPyObject &operator>>(wxPyObject &po, double &out)
{
    wxPyExtractFloat(po, out);
    return po;
}

inline wxPyObject &operator>>(wxPyObject &po, float &out)
{
    wxPyExtractFloat(po, out);
    return po;
}

inline wxPyObject &operator>>(wxPyObject &po, wxString &out)
{
    if (po.Ok() && !PyErr_Occurred()) {
        wxPyObject ro = po.Pop();

        if (!PyString_Check(ro.Get()) && !PyUnicode_Check(ro.Get()))
            ro = PyObject_Str(ro.Get());
        out = Py2wxString(ro.Get());
    }

    return po;
}

inline wxPyObject &operator>>(wxPyObject &po, wxSize &out)
{
    if (po.Ok() && !PyErr_Occurred()) {
        wxSize *pout = &out;
        wxPyObject ro = po.Pop();
        if (!wxSize_helper(ro.Get(), &pout))
            wxThrowPyException();
    }
    return po;
}

inline wxPyObject &operator>>(wxPyObject &po, wxWindow *&out)
{
    wxPyExtractObject(wxT("wxWindow"), po, out);
    return po;
}

inline wxPyObject &operator>>(wxPyObject &po, wxObject *&out)
{
    wxPyExtractObject(wxT("wxObject"), po, out);
    return po;
}

inline wxPyObject &operator>>(wxPyObject &po, wxColour &out)
{
    wxPyExtractObjectCopy(wxT("wxColour"), po, out);
    return po;
}

inline wxPyObject &operator>>(wxPyObject &po, wxFont &out)
{
    wxPyExtractObjectCopy(wxT("wxFont"), po, out);
    return po;
}

inline wxPyObject &operator>>(wxPyObject &po, wxRect &out)
{
    wxPyExtractObjectCopy(wxT("wxRect"), po, out);
    return po;
}

inline wxPyObject &operator>>(wxPyObject &po, wxBitmap &out)
{
    wxPyExtractObjectCopy(wxT("wxBitmap"), po, out);
    return po;
}

inline wxPyObject &operator>>(wxPyObject &po, wxVisualAttributes &out)
{
    wxPyExtractObjectCopy(wxT("wxVisualAttributes"), po, out);
    return po;
}

#endif
