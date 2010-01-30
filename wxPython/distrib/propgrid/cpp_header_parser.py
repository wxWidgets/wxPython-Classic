#
# A very simple and special purpose C++ header parser by Jaakko Salli. Used to
# implement overriddable wxPython virtual functions for wxPropertyGrid.
#
# Any attempt to understand this code may lead to insanity. So, you have been
# warned.
#

import sys, os, os.path, re


class class_obj:
    def __init__(self):
        pass

    def add_function(self, func):
        if func.name in self.func_dict:
            raise ValueError("Class '%s' already had function named '%s' (do we need overloading support yet?)"%(self.name, func.name))

        self.func_list.append(func)
        self.func_dict[func.name] = func

    def find_super_class(self, classes_dict, any_of_these):
        """\
        Tries to find a specific class in one of the super classes.

        classes_dict: dictionary of classes available (should include self).
        any_of_these: One of these is acceptable name of super class.
        """

        for scls in self.base_classes:
            if scls in any_of_these:
                return scls

            try:
                return classes_dict[scls].find_super_class(classes_dict, any_of_these)
            except KeyError:
                pass

        return None

    def find_derived_classes(self, classes_dict, ls=None):
        """\
        Returns list of all classes that have been derived from this class.

        classes_dict: dictionary of classes available (should include self).
        """
        if ls is None:
            ls = []

        bases = self.base_classes

        for ocls in classes_dict.itervalues():
            if self.name in ocls.base_classes:
                ls.append(ocls)
                ocls.find_derived_classes(classes_dict, ls)

        return ls

    def get_all_functions(self, classes_dict, exclude_methods=[]):
        """\
        Returns functions in this class, and also those from all super classes found.

        Returned list is unsorted.

        exclude_methods: List of (classname, funcname) tuples. These won't be
        included (classname can be any superclass).
        """

        def exclude_test(classname, funcname):
            for ex_cls, ex_func in exclude_methods:
                #if classname == 'wxFontProperty':
                #    print (classname, ex_cls, ex_func, funcname)
                #print funcname, ex_func
                if funcname != ex_func:
                    continue
                #if classname == 'wxFontProperty':
                #    print self.find_super_class(classes_dict,[ex_cls])
                if classname == ex_cls or self.find_super_class(classes_dict,[ex_cls]):
                    #print 'Excluded: %s::%s'%(classname, funcname)
                    return True

            return False


        ls_main = [a for a in self.func_list if not exclude_test(self.name, a.name)]
        func_names = self.func_names

        for sclsn in self.base_classes:
            try:
                scls = classes_dict[sclsn]
            except KeyError:
                continue

            ls = scls.get_all_functions(classes_dict, exclude_methods)
            for a in ls:
                n = a.name
                if not (n in func_names) and not (n == sclsn) and not (n[0] == '~'):
                    if not exclude_test(sclsn, n):
                        ls_main.append(a)

        return ls_main

    def is_implemented_in_super_class(self, classes_dict, func_name):
        """\
        Returns True if func_name is implemented in one of the classes
        from which this class derives from.
        """

        for baseclass_name in self.base_classes:
            try:
                baseclass = classes_dict[baseclass_name]
            except KeyError:
                continue

            if func_name in baseclass.func_dict:
                return True

            res = baseclass.is_implemented_in_super_class(classes_dict, func_name)
            if res:
                return True

        return False


class func_obj:
    def __init__(self):
        pass

    def construct_impl_head(self, **kwargs):
        """\
            Constructs first line of function implementation,
            eg. "int classname::funcname(arg1, arg2)".
        """
        args_str_nodefs = ', '.join(['%s %s'%(a[0],a[1]) for a in self.arguments])
        func_post_decl = ''
        if 'const' in self.flags:
            func_post_decl = ' const'

        class_name = kwargs.get('class_name', self.owner.name)
        func_name = kwargs.get('func_name', self.name)

        return '%s %s::%s(%s)%s'%(self.retval, class_name, func_name, args_str_nodefs, func_post_decl)

    def construct_decl(self, **kwargs):
        func_post_decl = ''
        if 'const' in self.flags:
            func_post_decl = ' const'
        func_pre_decl = ''
        if 'virtual' in self.flags:
            func_pre_decl = 'virtual '

        ss = []
        for arg in self.arguments:
            if len(arg) > 2 and arg[2]:
                ss.append('%s %s=%s'%arg)
            ss.append('%s %s'%arg[:2])
        args_str = ', '.join(ss)

        func_name = kwargs.get('func_name', self.name)

        return '%s%s %s(%s)%s;'%(func_pre_decl, self.retval, func_name, args_str, func_post_decl)


def parse_macro(macro_dict, macro_def, macro_code):
    """\
    macro_def contains macro name and args.
    """
    args = macro_def[macro_def.find('(')+1:-1].split(',')
    args = [s.strip() for s in args]
    name = macro_def[:macro_def.find('(')].strip()

    macro_dict[name] = (args,macro_code)


def parse_macros(macros):
    parsed_macros = {}

    for k,v in macros.iteritems():
        parse_macro(parsed_macros, k, v)

    return parsed_macros


def process_and_run_macros(s, include_paths=[], custom_macros={}, process_macros=True, resolve_macros=True, is_swig=False):
    ss = []

    parsed_macros = parse_macros(custom_macros)

    if not is_swig:
        reDefine = re.compile('#\s*define\s+(\w+)',re.I)
    else:
        reDefine = re.compile('%\s*define\s+(\w+)',re.I)

    reMacro = re.compile('([\w]+)\s*[(]',re.I|re.M)

    pos = 0
    chunk_start = 0
    mdef_start = len(s)

    while 1:
        m = reMacro.search(s, pos)
        if m:
            m_start = m.start()
        else:
            m_start = len(s)

        if process_macros:
            mdef = reDefine.search(s, pos)
            if mdef:
                mdef_start = mdef.start()
            else:
                mdef_start = len(s)

        if mdef_start < m_start:
            # Found macro definition next
            m = mdef

            parens_pos = s.find('(',m.end())
            macro_code_start = m.end()
            if parens_pos >= 0:
                pre_p = s[m.end():parens_pos]
                if not pre_p or pre_p.isspace():
                    parens_end = find_balanced_parenthesis(s, parens_pos)
                    #macro_args_list = [s_.strip() for s_ in s[parens_pos+1:parens_end].split(',')]
                    macro_code_start = parens_end+1

            macro_name_and_args = s[m.start(1):macro_code_start].strip()

            if is_swig:
                macro_code_end = s.find('%enddef',macro_code_start)
                macro_code = s[macro_code_start:macro_code_end].strip()+'\n'
                macro_code_end += 7
            else:
                # Macro ends at the end of a line without '\' at its end
                macro_parts = []
                p_ls = macro_code_start
                while 1:
                    p_le = s.find('\n',p_ls)
                    if p_le >= 0:
                        p_slash = s.rfind('\\',p_ls,p_le)
                        if p_slash >= 0:
                            pb = s[p_slash+1:p_le]
                            if not pb or pb.isspace():
                                # Yep, it continue
                                macro_parts.append(s[p_ls:p_slash-1].rstrip())
                        else:
                            # Not found
                            macro_parts.append(s[p_ls:p_le].rstrip())
                            macro_code_end = p_le
                            break
                    else:
                        p_le = len(s)
                        macro_parts.append(s[p_ls:p_le].rstrip())
                        macro_code_end = p_le
                        break

                    p_ls = p_le + 1

                macro_code = '\n'.join(macro_parts)
                macro_code_end += 1


            parse_macro(parsed_macros, macro_name_and_args, macro_code)
            print '-- MACRO --'
            print macro_name_and_args
            print macro_code

            ss.append(s[chunk_start:mdef_start])
            chunk_start = macro_code_end
            pos = macro_code_end

        elif m:
            # Found potential macro expansion next

            macro_name = m.group(1)
            macro_args,macro_str = parsed_macros.get(macro_name,(None,None))
            if macro_str is None:
                pos = m.end()
                continue

            pos = m.start()
            ss.append(s[chunk_start:pos])

            macro_end_pos = find_balanced_parenthesis(s, m.end()-1)

            #print m.end()
            #print macro_end_pos

            args = s[m.end():macro_end_pos].split(',')
            args = [s_.strip() for s_ in args]

            i = 0
            for rarg in macro_args:
                uarg = args[i]
                macro_str = re.compile('\\b%s\\b'%rarg,re.M).sub(uarg, macro_str)
                i += 1

            ss.append(macro_str)
            #print 'Adding %i chars from macro'%len(ss[-1])

            pos = macro_end_pos + 1
            chunk_start = pos

        else:
            break


    if not ss:
        return s

    ss.append(s[chunk_start:len(s)])
    #print 'Adding %i chars'%len(ss[-1])

    return ''.join(ss)

def run_macros(s, macros, is_swig = False):
    return process_and_run_macros(s, custom_macros=macros, process_macros=False, resolve_macros=False, is_swig=is_swig)


def find_balanced_parenthesis(s, pos, cs = '(', ce = ')'):
    """\
    Finds balanced parenthesis end.
    """

    if s[pos] != cs:
        raise ValueError('pos must start at "%s"'%cs)

    balance = 1

    pos += 1

    while 1:
        spos = s.find(cs, pos)
        if spos < 0:
            spos = len(s)
        epos = s.find(ce, pos)
        if epos < 0:
            epos = len(s)

        if epos <= spos:
            balance -= 1
            if balance == 0:
                return epos
            pos = epos + 1
        else:
            balance += 1
            pos = spos + 1


def purge_comments(s):
    s2 = []

    pos = 0

    while 1:
        p1 = s.find('//', pos)
        p2 = s.find('/*', pos)
        if p1 >= 0 and (p1 < p2 or p2 < 0):
            # Line-comment is next
            s2.append(s[pos:p1])
            p3 = s.find('\n',p1)
            if p3 < 0:
                break
            s2.append('\n')
            pos = p3+1
        elif p2 >= 0:
            # Block-comment is next
            s2.append(s[pos:p2])
            p3 = s.find('*/',p2)
            if p3 < 0:
                break
            pos = p3+2
        else:
            break

    if not s2:
        return s

    s2.append(s[pos:len(s)])

    return ''.join(s2)


def normalize_type(s):
    """\
    Normalizes type string.
    """
    while s.find('  ') >= 0:
        s = s.replace('  ',' ')

    s = s.replace(' *','*').replace(' &','&')

    return s.strip()


def split_argument_list(s, start_pos=-1, def_vals=False):
    """\
    Splits argument list string into list of (type,name) tuples.

    start_pos: starting position of parenthesis-enclosed
    argument list (ie. pos must be at starting parens).
    If this arg is given, return value is tuple (arguments,end_pos)
    instead.

    def_vals: if true, third string, default value, is
    added to the argument tuples.
    """
    if not s:
        return []

    if start_pos >= 0:
        end_pos = find_balanced_parenthesis(s, start_pos)
        s = s[start_pos+1:end_pos]

    arg_strings = s.split(',')

    arguments = []

    for s in arg_strings:
        s = s.strip()
        p1 = s.rfind('=')
        if p1 >= 0:
            defval = s[p1+1:].strip()
            s = s[:p1].strip()
        else:
            defval = ''
        p1 = s.rfind(' ')
        p2 = s.rfind('*')
        p3 = s.rfind('&')
        if p2 > p1:
            p1 = p2
        if p3 > p1:
            p1 = p3
        p1 += 1
        s0 = s[:p1]
        s1 = s[p1:].replace('[]','')

        if not s0 and s1:
            s0 = s1
            s1 = ''

        s0 = normalize_type(s0)

        # Normalize type names

        if not def_vals:
            arguments.append((s0,s1))
        else:
            arguments.append((s0,s1,defval))

    if len(arguments) == 1 and arguments[0][0] == '' and arguments[0][1] == '':
        return []

    if start_pos >= 0:
        return (arguments,end_pos)

    return arguments



_temp_fns = []

def get_temp_filename(ext='tmp'):
    global _temp_fns

    num = 1
    while 1:
        fn = 'tempfile%i.%s'%(num,ext)
        if not os.path.isfile(fn):
            _temp_fns.append(fn)
            return fn
        num += 1


def cleanup():
    global _temp_fns

    for fn in _temp_fns:
        try:
            os.remove(fn)
        except:
            pass


def preprocess(header_content, include_paths):

    # Let's use a genu-wine C pre-processor
    # We'll use VC on Win32, GCC on Unix (latter is TODO)

    pp_fn = get_temp_filename('h')
    src_fn = get_temp_filename('cpp')
    f = file(src_fn,'wt')
    f.write(header_content)
    f.close()
    pp_cmd_line = 'cl /EP %s %s > %s'%(' '.join(['/I%s'%a for a in include_paths]),src_fn,pp_fn)
    print pp_cmd_line
    if os.system(pp_cmd_line) != 0:
        global _temp_fns
        _temp_fns.remove(pp_fn)
        _temp_fns.remove(src_fn)
        return None

    try:
        f = file(pp_fn,'rt')
    except OSError:
        return None

    s = f.read()
    f.close()

    return s


def parse_header(header_content, include_paths, custom_macros={}):

    classes = {}

    header_content = preprocess(header_content, include_paths)
    if header_content is None:
        return None

    reClassDecl = re.compile('^[\s\w]*class([\s\w:,]+){',re.M)
    reScopeDecl = re.compile('^\s*([a-z]+):',re.M)  # 'public', 'private' etc.
    rePreprocDecl = re.compile('^#\s*([a-zA-Z]+)[ \t]*([^\n]*)\n',re.M)  # 'public', 'private' etc.
    reFuncDecl = re.compile('([\w\s*&]+) ([~\w]+)\s*[(]',re.I|re.M)  # 'public', 'private' etc.
    rePureDecl = re.compile('\s*=\s*0\s*;',re.I|re.M)  # = 0;

    pos = 0

    while 1:
        m = reClassDecl.search(header_content, pos)
        if not m:
            break

        pos = m.start()

        base_classes = tuple()

        # Determine class name
        s = m.group(1)
        p1 = s.rfind(':')
        if p1 >= 0:
            base_classes = [a_.split(' ')[-1].strip() for a_ in s[p1+1:].split(',')]
            s = s[:p1]
        s = s.strip()
        p1 = s.rfind(' ') + 1
        class_name = s[p1:]

        if not class_name in classes:
            ls = []
            dict = {}

            cls = class_obj()
            cls.name = class_name
            cls.func_names = func_names = set()
            cls.base_classes = base_classes
            cls.func_list = ls
            cls.func_dict = dict

            classes[class_name] = cls
        else:
            cls = classes[class_name]
            ls = cls.func_list
            dict = cls.func_dict

        # Find class end
        class_end_pos = find_balanced_parenthesis(header_content, m.end()-1, '{', '}')

        scope = 'private'

        # Preprocessor #if stack
        pp_if_stack = []

        # Find scopes, pre-processor conditionals, and function declarations
        while 1:
            m_func = reFuncDecl.search(header_content, pos, class_end_pos)
            if m_func:
                func_pos = m_func.start()
            else:
                func_pos = len(header_content)

            m_scope = reScopeDecl.search(header_content, pos, class_end_pos)
            if m_scope:
                scope_pos = m_scope.start()
            else:
                scope_pos = len(header_content)

            m_preproc = rePreprocDecl.search(header_content, pos, class_end_pos)
            if m_preproc:
                preproc_pos = m_preproc.start()
            else:
                preproc_pos = len(header_content)

            if scope_pos < preproc_pos:
                if func_pos < scope_pos:
                    do_what = 0
                else:
                    do_what = 1
            else:
                if func_pos < preproc_pos:
                    do_what = 0
                else:
                    do_what = 2

            if do_what == 0 and m_func:
                func_pre_str = m_func.group(1).strip()
                func_name = m_func.group(2)
                #print func_pre_str, func_name

                # Find argument list in decl
                arg_start = m_func.end()-1
                arg_end = find_balanced_parenthesis(header_content, arg_start)
                arg_start += 1

                flags = set()

                # Need to extend declaration to include 'const' etc.,
                # but exclude pure virtual definition.
                p1 = header_content.find('{', arg_end, class_end_pos)
                p2 = header_content.find(';', arg_end, class_end_pos)
                p3 = header_content.find('=', arg_end, class_end_pos)
                p4 = header_content.find(':', arg_end, class_end_pos)  # Constructor only
                p5 = header_content.find('(', arg_end, class_end_pos)
                p6 = header_content.find('}', arg_end, class_end_pos+2)
                #p7 = header_content.find('\n', arg_end, class_end_pos)
                p = p1
                if p < 0:
                    p = len(header_content)

                is_inline = True
                is_func = True

                if p2 >= 0 and p2 < p:
                    is_inline = False
                    p = p2
                if p3 >= 0 and p3 < p:
                    p = p3
                if p4 >= 0 and p4 < p:
                    if func_name == class_name:
                        p = p4
                    else:
                        is_func = False
                if p5 >= 0 and p5 < p:
                    is_func = False
                if p6 >= 0 and p6 < p:
                    is_func = False
                #if p7 >= 0 and p7 < p:
                #    is_func = False  # Likely a non-resolved macro

                if is_inline:
                    flags.add('inline')

                if not is_func:
                    pos = arg_end
                    continue

                func_content = ''

                if p >= 0:
                    decl_end = p

                    if is_inline:
                        func_end_pos = find_balanced_parenthesis(header_content, p1, '{', '}')
                        if func_end_pos >= 0:
                            # Find start of line for {
                            content_start_pos = header_content.rfind('\n', 0, p1)
                            if content_start_pos >= 0 and content_start_pos > arg_end:
                                content_start_pos += 1
                            else:
                                content_start_pos = p1
                            func_content = remove_indent(header_content[content_start_pos:func_end_pos+1])
                    else:
                        func_end_pos = p2
                        if p2 < 0:
                            raise ValueError
                else:
                    decl_end = len(header_content)
                    func_end_pos = decl_end

                pos = func_end_pos + 1

                in_hdr_pos = m_func.start()
                while header_content[in_hdr_pos].isspace():
                    in_hdr_pos += 1

                vp = func_pre_str.find('pyvirtual ')
                if vp >= 0 and (vp == 0 or vp[-1].isspace()):
                    flags.add('pyvirtual')
                    flags.add('virtual')
                else:
                    vp = func_pre_str.find('virtual ')
                    if vp >= 0 and (vp == 0 or vp[-1].isspace()):
                        flags.add('virtual')

                func_decl = header_content[in_hdr_pos:decl_end].replace('pyvirtual','').replace('virtual ','').strip()

                arguments = split_argument_list(header_content[arg_start:arg_end]) #,def_vals=True)

                if func_decl.endswith('const'):
                    flags.add('const')

                m_pd = rePureDecl.search(header_content,decl_end,decl_end+8);
                if m_pd:
                    if m_pd.start() == decl_end:
                        flags.add('pure')

                retval = func_decl[:func_decl.find(func_name)-1]

                fo_ = func_obj()
                fo_.owner = cls
                fo_.name = func_name
                func_names.add(func_name)
                fo_.decl = func_decl
                fo_.retval = retval
                fo_.arguments = arguments
                fo_.scope = scope
                fo_.pp_if_stack = pp_if_stack
                fo_.flags = flags
                fo_.content = func_content

                ls.append( fo_ )
                if not func_name in dict:
                    dict[func_name] = fo_

            elif do_what == 1 and m_scope:
                scope = m_scope.group(1)
                pos = m_scope.end()

            elif do_what == 2 and m_preproc:
                command = m_preproc.group(1)
                params = m_preproc.group(2).strip()
                #print '%s(%s)'%(command,params)

                # Create new list (so copy of each state will be retained)
                pp_if_stack = list(pp_if_stack)

                if command == 'if':
                    pp_if_stack.append(params)
                elif command == 'ifdef':
                    pp_if_stack.append('defined(%s)'%params)
                elif command == 'ifndef':
                    pp_if_stack.append('!defined(%s)'%params)
                elif command == 'else':
                    pp_if_stack[-1] = '!(%s)'%(pp_if_stack[-1])
                elif command == 'elif':
                    # Treat elif as if
                    pp_if_stack[-1] = params
                elif command == 'endif':
                    del pp_if_stack[-1]
                else:
                    print 'WARNING: Unsupport preprocessor command "%s" inside class body.'%command

                #print 'Preprocessor Condition Stack: %s'%pp_if_stack

                pos = m_preproc.end()
            else:
                break

        pos = m.end()


    return classes


_type_default_values = {
'void' : '',
'int' : 0,
'long' : 0,
'unsigned int' : 0,
'unsigned long' : 0,
'size_t' : 0,
'double' : 0.0,
'float' : 0.0,
'bool' : 'false',
'BOOL' : 'FALSE',
'wxString' : 'wxEmptyString',
}

def get_default_value_for_type(s):
    defval = _type_default_values.get(s,None);
    if not (defval is None):
        return defval

    if s.endswith('*'):
        return 'NULL'
    else:
        return '%s()'%s


def is_builtin_type(s):
    """\
    Returns true if actualt type, without const, ptr, etc. decorations
    is a C/C++ built-in one (ie. not class/struct).
    """
    cls, flags = parse_type(s)
    if cls in _type_default_values:
        return True
    return False


def is_likely_callback_arg(t):
    if t.endswith('**'):
        return True
    elif t.endswith('*') and t[:-1] in _type_default_values:
        return True

    return False


def parse_type(t):
    """\
    returns (cls,flags), where cls is the class name or built-in type
    name, and flags is set with such possible members as 'ptr', 'ref'
    and 'const', with hopefully obvious meanings.
    """
    flags = set()

    end_pos = len(t)
    p_star = t.find('*')
    p_and = t.find('&')

    if p_star >= 0 and p_star == end_pos-1:
        flags.add('ptr')
        end_pos = p_star;
    elif p_and >= 0 and p_and == end_pos-1:
        flags.add('ref')
        end_pos = p_and;

    start_pos = 0
    p_const = t.find('const')

    if p_const >= 0:
        start_pos = p_const+5
        flags.add('const')

    return (t[start_pos:end_pos].strip(),flags)


def format_type(tcls, tflags):
    """\
    Reverse of parse_type. Can be used to format type names
    into a consistent format.
    """
    if 'const' in tflags:
        const_s = 'const '
    else:
        const_s = ''

    if 'ptr' in tflags:
        ptr_symbol = '*'
    elif 'ref' in tflags:
        ptr_symbol = '&'
    else:
        ptr_symbol = ''

    return'%s%s%s'%(const_s,tcls,ptr_symbol)


def indent(s, n):
    si = n*' '
    s = s.strip().replace('\n','\n%s'%si)
    if s.find(si) != 0:
        s = si + s
    return s

def find_lowest_indent(s_orig):
    ss = s_orig.split('\n')

    lowest_spaces = sys.maxint

    # Find highest starting space count
    for s in ss:
        spaces = 0
        for c in s:
            if not c.isspace():
                break
            spaces += 1

        if spaces < len(s) and spaces < lowest_spaces:
            lowest_spaces = spaces

    return lowest_spaces, ss

def remove_indent(s_orig):
    lowest_indent, ss = find_lowest_indent(s_orig)
    return '\n'.join([s[lowest_indent:] for s in ss])
