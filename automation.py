RESULT_ROOT = 'results'

from string import Template
import re
import os



#### PARSING ####

def course(path='src'):
    entity = 'course'
    files = os.listdir(path)
    files = [os.path.join( path, f ) for f in files]
    files = [f  for f in files if os.path.isfile(f) and f.endswith('.py') ]
    children = lessons = map(lesson, files)
    return locals()
    
def lesson(path):
    entity = 'lesson'
    name = os.path.split( path )[-1]
    code = open(path).read()
    
    task_codes = code.split("###TASK:")
    intro = task_codes.pop(0)

    children = tasks = map(task, task_codes)
    return locals()

def task(task_code):
    entity = 'task'
    lines = task_code.split("\n")
    name = lines.pop(0)

    children = placeholders = []
    for nr, line in enumerate(lines):
        p = placeholder( line )
        if p['match']:
            placeholders.append( p )
            lines[nr] = p['result_line'] 
            p['line_nr'] = nr
    
    result_code = '\n'.join( lines )
    
    return locals()
    
    
# def subtask():
    # pass

def placeholder(line):
    entity = 'placeholder'
    re_placeholder = re.compile(r"###PLACEHOLDER:(.*?)--\>(.+)")
    
    match = re_placeholder.search(line)
    if match:
        expected, replaced = match.group(1).strip(), match.group(2).strip()
        result_line = re.sub(re_placeholder, "" , line)  # clear directive from code
        offset_in_line = result_line.find( expected )
        result_line = result_line.replace( expected, replaced )
    
    return locals()
    

#### RENDERING ####

def render_with_children( info , templates ):
    if info['entity'] != 'placeholder':
        rendered_children_list = [render_with_children(child, templates)       for child in info['children'] ]
        # rendered_children_list = map( lambda x: render_with_children(x, templates),  info['children'] )
        info['rendered_children'] = "\n".join( rendered_children_list )  # recursion

    tpl =  templates[ info['entity']  ] # todo: could be singleton
    result = tpl.safe_substitute( info )

    return result

def save(fname, content, dirpath=""):
    dirpath = os.path.join( RESULT_ROOT, dirpath )
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    if isinstance( content, (list, tuple)):
        content = "\n".join( content )  # try to be smart

    with open( os.path.join( dirpath, fname), 'w') as f:
        f.write( content )

def init_placeholders_DEPRECATED():
    code = open('src.py').read()
    
    tasks = code.split("###TASK:")
    intro = tasks.pop(0)

    results = []
    for nr, t in enumerate( tasks ):
        name, code = t.split("\n", 1)
        
        def apply_placeholder(code):
            re_placeholder = re.compile(r"###PLACEHOLDER:(.*?)--\>(.+)")
            result_code =  re.sub(re_placeholder, "" , code)
            
            for match in re_placeholder.finditer(code):
                # print (match)
                global expected
                expected, replace = match.group(1).strip(), match.group(2).strip()
                result_code = result_code.replace( expected, replace )
            return result_code
        
        result_lines = [ apply_placeholder(line) for  line in code.split('\n') ]
        result_code = '\n'.join( result_lines )
            
        
        print("#"*10, name, "#"*10)
        print(result_code)

        results.append( result_code )
        
        path = 'result_lesson/task%s' % nr
        if not os.path.exists(path):
            os.makedirs(path)
    
        with open(  os.path.join( path, "task.py" )  , 'w') as f:
            f.writelines( [intro, result_code] )
        
        
        make_test_file(path=path, human_nr=nr+1, name=name, expected=expected, extra_args="")
        
    # for testing / overview
    with open("result.py", 'w') as f:
        f.writelines( [intro] + results )

def render_course_tree( info ):
    # for course in info:
        course = info
        course['name'] = 'Demo'
        course['description'] = 'demo'
        for lnr, lesson in enumerate( course['children'] ):
            # print (lnr)
            lesson['nr'] = lnr+1
            
            for tnr, task in enumerate ( lesson['children'] ):
                # make_test_file(path=path, human_nr=nr+1, name=name, expected=expected, extra_args="")
                # print("  ", tnr )
                task['nr'] = tnr+1
                
                # task['code_html_escaped'] = ...
                for phnr, placeholder in enumerate( task['children'] ):
                    # print("    ", phnr)
                    placeholder.setdefault('extra_args', '')
                    placeholder['nr'] = phnr
                    placeholder['human_nr'] = phnr+1

                    # TODO
                    
                    lines_before = task['lines'][:  placeholder['line_nr'] ] 
                    lines_before.insert(0, lesson['intro'] )
                    lines_before.append( placeholder['result_line'] [ : placeholder['offset_in_line'] ] ) 
                    content_before = "\n".join( lines_before )
                    placeholder['offset'] = len(content_before)
                    placeholder['length'] = len( placeholder['replaced'] )

                    print ( ' -> '.join( map(str,   [ lesson.get('name'), task.get('name'), placeholder.get('name') ] )))


                dirpath = path = os.path.join("lesson%s" % lesson['nr'],

                                              "task%s" % task['nr']   )
                tests_content = render_with_children( task , templates=test_tpls  )
                save('tests.py', tests_content , dirpath=dirpath )
                save('task.py', lesson['intro']+"\n"+task['result_code'] , dirpath=dirpath )






                # make_test_file(path, placeholder)

def make_test_file(path, **task):
    test_tpl = Template(open("tpl/tests.py").read())
    
    test_code = test_tpl.substitute( task )
                
    with open( os.path.join( RESULT_ROOT, path, "tests.py"), 'w') as f:
        f.write(test_code)
                
    


if __name__ == "__main__":
    info = course( )
    from pprint import pprint
    pprint( info )

    # TEST course files tree rendering: task.py , test.py

    test_tpls = dict(

task=Template("""
from test_helper import run_common_tests, failed, passed, get_answer_placeholders
from test_helper import check_placeholder

#### task: $name
def test_answer_placeholders():
    placeholders = get_answer_placeholders()

$rendered_children

if __name__ == '__main__':
    run_common_tests()
    test_answer_placeholders()       # TODO: uncomment test call

"""),

placeholder=Template("""
    check_placeholder(placeholders[$nr], '$expected'
                      ,human_nr=$human_nr
                      $extra_args
                      )
""")
    )


    render_course_tree( info )

    # TEST study_project rendering
    study_project_templates = {}
    for fname in os.listdir('tpl/study_project'):
        if fname.endswith(".xml"):
            study_project_templates[fname[:-4]] = Template(open(os.path.join("tpl/study_project", fname)).read())


    content = render_with_children( info, study_project_templates )
    save("study_project.xml", content)


    # TODO move files to new place...
    print("OK")
    
