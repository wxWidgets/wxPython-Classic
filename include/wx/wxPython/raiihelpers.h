#ifndef _RAIIHELPERS_H_
#define _RAIIHELPERS_H_


// 
enum BlockType
{
    PTB_INIT_BLOCK,
    PTB_INIT_UNBLOCK
};
class wxPyThreadBlocker
{
public:
    wxPyThreadBlocker(BlockType bt = PTB_INIT_BLOCK) 
    {
        if (bt == PTB_INIT_BLOCK)
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

//TODO: could use operator==, etc 
class wxPyObject
{
public:
    wxPyObject() 
    { 
        m_obj = NULL; 
        m_borrowed = true;
    }

    ~wxPyObject()
    {
        // We don't know if the GIL is held during destruction, so lock explicitly.
        // GILState API locks support recursion (if needed).
        wxPyBlock_t st = wxPyBeginBlockThreads();
        Decref();
        wxPyEndBlockThreads(st);
    }

    wxPyObject(PyObject *obj)
    {
        m_obj = obj;
        m_borrowed = false;
    }

    wxPyObject(const wxPyObject &cpy)
    {
        m_obj = cpy.m_obj;
        m_borrowed = false;
        Incref();
    }

    const wxPyObject &operator=(PyObject *obj)
    {
        Take(obj);
        return *this;
    }

    const wxPyObject &operator=(const wxPyObject &cpy)
    {
        Ref(cpy.m_obj);
        return *this;
    }

    bool Ok() const
    {
        return m_obj != NULL;
    }

    void Borrow(PyObject *obj)
    {
        if (obj != m_obj) {
            Decref();
            m_obj = obj; 
            m_borrowed = true;
        }
    }

    void Ref(PyObject *obj)
    {
        if (obj != m_obj) {
            Decref();
            m_obj = obj; 
            m_borrowed = false;
            Incref();
        }
    }

    // Obj already increfed
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
    PyObject *Transfer()
    {
        m_borrowed = true;
        return m_obj;
    }

    PyObject *Remove()
    {
        PyObject *ret = m_obj;
        m_obj = NULL;
        m_borrowed = true;
        return ret;
    }

    void Clear()
    {
        Decref();
    }

private:
    void Decref()
    {
        //if (m_obj)
            //printf("borrowed %d, ob_refcnt %d\n", m_borrowed, m_obj->ob_refcnt);
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

#endif
