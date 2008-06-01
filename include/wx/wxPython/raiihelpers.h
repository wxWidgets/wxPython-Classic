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

// 
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
        Decref();
    }

    void Borrow(PyObject *obj)
    {
        Decref();
        m_obj = obj; 
        m_borrowed = true;
    }

    void Ref(PyObject *obj)
    {
        Decref();
        m_obj = obj; 
        m_borrowed = false;
        Incref();
    }

    // Obj already increfed
    void Take(PyObject *obj)
    {
        Decref();
        m_obj = obj; 
        m_borrowed = false;
    }

    PyObject *Get()
    {
        return m_obj;
    }

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

#endif
