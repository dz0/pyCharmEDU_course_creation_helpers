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
    code = open(path).read()
    
    intro, *task_codes = code.split("###TASK:")
    
    children = tasks = map(task, task_codes)
    return locals()

def task(task_code):
    entity = 'task'
    name, *lines = task_code.split("\n")
    
    children = placeholders = []
    for nr, line in enumerate(lines):
        p = placeholder( line )
        if p['match']:
            placeholders.append( p )
            lines[nr] = p['result_line'] 
    
    result_code = '\n'.join( lines )
    
    return locals()
    
    
# def subtask():
    # pass

def placeholder(line):
    entity = 'placeholder'
    re_placeholder = re.compile(r"###PLACEHOLDER:(.*?)--\>(.+)")
    
    match = re_placeholder.search(line)
    if match:
        expected, replace = match.group(1).strip(), match.group(2).strip()
        result_line = line.replace( expected, replace )
        result_line = re.sub(re_placeholder, "" , line)  # clear directive from code
    
    return locals()
    

#### RENDERING ####

def render( info ):
    if info['entity'] != 'placeholder':
        rendered_children_list = map( render, info['children'] )
        info['rendered_children'] = "\n".join( rendered_children_list )  # recursion
    tpl = Template( open(  os.path.join("tpl/study_project", info['entity']+'.xml' )).read() )  # todo: could be singleton
    result = tpl.safe_substitute( info )
    return result
    

def out( info ):
    result = render( info )
    
    out_root = '.'
    if not os.path.exists(out_root):
            os.makedirs(out_root)
    with open( os.path.join( out_root, "study_project.xml"), 'w') as f:
        f.write( result )
                
        
def init_placeholders_DEPRECATED():
    code = open('src.py').read()
    
    intro, *tasks = code.split("###TASK:")

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

def make_test_file(path, **task):
    test_tpl = Template(open("tpl/tests.py").read())
    
    test_code = test_tpl.substitute( task )
                
    with open( os.path.join( path, "tests.py"), 'w') as f:
        f.write(test_code)
                
    


if __name__ == "__main__":
    info = course( )
    from pprint import pprint
    pprint( info )
    
    out( info )
    # init_placeholders()
