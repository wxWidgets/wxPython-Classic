template0 = """
#define PYCALLBACK_0_VOID(PCLASS, CBNAME)     \\
    B_PYCALLBACK_0_VOID(CBNAME, CBNAME, PCLASS::CBNAME())

#define PYCALLBACK_0_VOID_CONST(PCLASS, CBNAME) \\
    B_PYCALLBACK_0_VOID_CONST(CBNAME, CBNAME, PCLASS::CBNAME())

#define PYCALLBACK_0_VOID_PURE(CBNAME)            \\
    B_PYCALLBACK_0_VOID_PURE(CBNAME, CBNAME)

#define PYCALLBACK_0_VOID_PURE_CONST(CBNAME)          \\
    B_PYCALLBACK_0_VOID_PURE_CONST(CBNAME, CBNAME)

#define PYCALLBACK_0_EXTRACT(PCLASS, RETTYPE, RETINIT, CBNAME)              \\
    B_PYCALLBACK_0(RETTYPE, CBNAME, CBNAME,                                 \\
                RETTYPE RETINIT,                                            \\
                ro >> rval,                                                 \\
                rval = PCLASS::CBNAME(),                                    \\
                rval)                                                   

#define PYCALLBACK_0_EXTRACT_CONST(PCLASS, RETTYPE, RETINIT, CBNAME)        \\
    B_PYCALLBACK_0_CONST(RETTYPE, CBNAME, CBNAME,                           \\
                RETTYPE RETINIT,                                            \\
                ro >> rval,                                                 \\
                rval = PCLASS::CBNAME(),                                    \\
                rval)                                                   

#define PYCALLBACK_0_EXTRACT_PURE(RETTYPE, RETINIT, CBNAME)                 \\
    B_PYCALLBACK_0_PURE(RETTYPE, CBNAME, CBNAME,                            \\
                RETTYPE RETINIT,                                            \\
                ro >> rval,                                                 \\
                rval)

#define PYCALLBACK_0_EXTRACT_PURE_CONST(RETTYPE, RETINIT, CBNAME)           \\
    B_PYCALLBACK_0_PURE_CONST(RETTYPE, CBNAME, CBNAME,                      \\
                RETTYPE RETINIT,                                            \\
                ro >> rval,                                                 \\
                rval)

// -
#define IMP_PYCALLBACK_0_VOID(CLASS, PCLASS, CBNAME)     \\
    B_PYCALLBACK_0_VOID(CLASS::CBNAME, CBNAME, PCLASS::CBNAME())

#define IMP_PYCALLBACK_0_VOID_CONST(CLASS, PCLASS, CBNAME) \\
    B_PYCALLBACK_0_VOID_CONST(CLASS::CBNAME, CBNAME, PCLASS::CBNAME())

#define IMP_PYCALLBACK_0_VOID_PURE(CLASS, CBNAME)            \\
    B_PYCALLBACK_0_VOID_PURE(CLASS::CBNAME, CBNAME)

#define IMP_PYCALLBACK_0_VOID_PURE_CONST(CLASS, CBNAME)          \\
    B_PYCALLBACK_0_VOID_PURE_CONST(CLASS::CBNAME, CBNAME)

#define IMP_PYCALLBACK_0_EXTRACT(CLASS, PCLASS, RETTYPE, RETINIT, CBNAME)       \\
    B_PYCALLBACK_0(RETTYPE, CLASS::CBNAME, CBNAME,                              \\
                RETTYPE RETINIT,                                                \\
                ro >> rval,                                                     \\
                rval = PCLASS::CBNAME(),                                        \\
                rval)                                                   

#define IMP_PYCALLBACK_0_EXTRACT_CONST(CLASS, PCLASS, RETTYPE, RETINIT, CBNAME)\\
    B_PYCALLBACK_0_CONST(RETTYPE, CLASS::CBNAME, CBNAME,                       \\
                RETTYPE RETINIT,                                               \\
                ro >> rval,                                                    \\
                rval = PCLASS::CBNAME(),                                       \\
                rval)                                                   

#define IMP_PYCALLBACK_0_EXTRACT_PURE(CLASS, RETTYPE, RETINIT, CBNAME)      \\
    B_PYCALLBACK_0_PURE(RETTYPE, CLASS::CBNAME, CBNAME,                     \\
                RETTYPE RETINIT,                                            \\
                ro >> rval,                                                 \\
                rval)

#define IMP_PYCALLBACK_0_EXTRACT_PURE_CONST(CLASS, RETTYPE, RETINIT, CBNAME)\\
    B_PYCALLBACK_0_PURE_CONST(RETTYPE, CLASS::CBNAME, CBNAME,               \\
                RETTYPE RETINIT,                                            \\
                ro >> rval,                                                 \\
                rval)
"""


template = """
#define PYCALLBACK_%(count)d_VOID(PCLASS, CBNAME, ARGS)     \\
    B_PYCALLBACK_N_VOID(CBNAME, CBNAME, %(count)d, ARGS,    \\
                %(insertion)s, \\
                PCLASS::CBNAME(%(pargs)s))

#define PYCALLBACK_%(count)d_VOID_CONST(PCLASS, CBNAME, ARGS) \\
    B_PYCALLBACK_N_VOID_CONST(CBNAME, CBNAME, %(count)d, ARGS, \\
                %(insertion)s, \\
                PCLASS::CBNAME(%(pargs)s))

#define PYCALLBACK_%(count)d_VOID_PURE(CBNAME, ARGS)            \\
    B_PYCALLBACK_N_VOID_PURE(CBNAME, CBNAME, %(count)d, ARGS,   \\
                %(insertion)s)

#define PYCALLBACK_%(count)d_VOID_PURE_CONST(CBNAME, ARGS)          \\
    B_PYCALLBACK_N_VOID_PURE_CONST(CBNAME, CBNAME, %(count)d, ARGS, \\
                %(insertion)s)

#define PYCALLBACK_%(count)d_EXTRACT(PCLASS, RETTYPE, RETINIT, CBNAME, ARGS)    \\
    B_PYCALLBACK_N(RETTYPE, CBNAME, CBNAME, %(count)d, ARGS,                    \\
                %(insertion)s,  \\
                RETTYPE RETINIT,                                                \\
                ro >> rval,                                                     \\
                rval = PCLASS::CBNAME(%(pargs)s),                               \\
                rval)                                                   

#define PYCALLBACK_%(count)d_EXTRACT_CONST(PCLASS, RETTYPE, RETINIT, CBNAME, ARGS)    \\
    B_PYCALLBACK_N_CONST(RETTYPE, CBNAME, CBNAME, %(count)d, ARGS,                    \\
                %(insertion)s,  \\
                RETTYPE RETINIT,                                               \\
                ro >> rval,                                                    \\
                rval = PCLASS::CBNAME(%(pargs)s),                              \\
                rval)                                                   

#define PYCALLBACK_%(count)d_EXTRACT_PURE(RETTYPE, RETINIT, CBNAME, ARGS)   \\
    B_PYCALLBACK_N_PURE(RETTYPE, CBNAME, CBNAME, %(count)d, ARGS,           \\
                %(insertion)s,  \\
                RETTYPE RETINIT,                                            \\
                ro >> rval,                                                 \\
                rval)

#define PYCALLBACK_%(count)d_EXTRACT_PURE_CONST(RETTYPE, RETINIT, CBNAME, ARGS)   \\
    B_PYCALLBACK_N_PURE_CONST(RETTYPE, CBNAME, CBNAME, %(count)d, ARGS,           \\
                %(insertion)s,  \\
                RETTYPE RETINIT,                                            \\
                ro >> rval,                                                 \\
                rval)

// -
#define IMP_PYCALLBACK_%(count)d_VOID(CLASS, PCLASS, CBNAME, ARGS)     \\
    B_PYCALLBACK_N_VOID(CLASS::CBNAME, CBNAME, %(count)d, ARGS,    \\
                %(insertion)s, \\
                PCLASS::CBNAME(%(pargs)s))

#define IMP_PYCALLBACK_%(count)d_VOID_CONST(CLASS, PCLASS, CBNAME, ARGS) \\
    B_PYCALLBACK_N_VOID_CONST(CLASS::CBNAME, CBNAME, %(count)d, ARGS, \\
                %(insertion)s, \\
                PCLASS::CBNAME(%(pargs)s))

#define IMP_PYCALLBACK_%(count)d_VOID_PURE(CLASS, CBNAME, ARGS)            \\
    B_PYCALLBACK_N_VOID_PURE(CLASS::CBNAME, CBNAME, %(count)d, ARGS,   \\
                %(insertion)s)

#define IMP_PYCALLBACK_%(count)d_VOID_PURE_CONST(CLASS, CBNAME, ARGS)          \\
    B_PYCALLBACK_N_VOID_PURE_CONST(CLASS::CBNAME, CBNAME, %(count)d, ARGS, \\
                %(insertion)s)

#define IMP_PYCALLBACK_%(count)d_EXTRACT(CLASS, PCLASS, RETTYPE, RETINIT, CBNAME, ARGS) \\
    B_PYCALLBACK_N(RETTYPE, CLASS::CBNAME, CBNAME, %(count)d, ARGS,                     \\
                %(insertion)s,  \\
                RETTYPE RETINIT,                                                        \\
                ro >> rval,                                                             \\
                rval = PCLASS::CBNAME(%(pargs)s), \\
                rval)                                                   

#define IMP_PYCALLBACK_%(count)d_EXTRACT_CONST(CLASS, PCLASS, RETTYPE, RETINIT, CBNAME, ARGS)    \\
    B_PYCALLBACK_N_CONST(RETTYPE, CLASS::CBNAME, CBNAME, %(count)d, ARGS,                        \\
                %(insertion)s,  \\
                RETTYPE RETINIT,                                                                 \\
                ro >> rval,                                                                      \\
                rval = PCLASS::CBNAME(%(pargs)s), \\
                rval)                                                   

#define IMP_PYCALLBACK_%(count)d_EXTRACT_PURE(CLASS, RETTYPE, RETINIT, CBNAME, ARGS)    \\
    B_PYCALLBACK_N_PURE(RETTYPE, CLASS::CBNAME, CBNAME, %(count)d, ARGS,                \\
                %(insertion)s,  \\
                RETTYPE RETINIT,                                                        \\
                ro >> rval,                                                             \\
                rval)

#define IMP_PYCALLBACK_%(count)d_EXTRACT_PURE_CONST(CLASS, RETTYPE, RETINIT, CBNAME, ARGS)  \\
    B_PYCALLBACK_N_PURE_CONST(RETTYPE, CLASS::CBNAME, CBNAME, %(count)d, ARGS,              \\
                %(insertion)s,  \\
                RETTYPE RETINIT,                                                            \\
                ro >> rval,                                                                 \\
                rval)
"""


H=10
aset = 'abcdefghijklmnopqrstuvwxyz'

for i in xrange(0,H+1):
    print "//"
    print "// --"
    print "//"

    if i == 0:
        print template0
    else:
        set = aset[:i]
        insertion = 'args << ' + ' << '.join(set)
        pargs = ', '.join(set)
        d = {
                'count': i,
                'insertion': insertion,
                'pargs': pargs,
            }

        print template % d
    
