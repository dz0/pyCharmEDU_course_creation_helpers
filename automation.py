import re
import os


def init_placeholders():
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
    from string import Template
    test_tpl = Template(open("tpl/tests.py").read())
    
    test_code = test_tpl.substitute( task )
                
    with open( os.path.join( path, "tests.py"), 'w') as f:
        f.write(test_code)
                
    


if __name__ == "__main__":
    init_placeholders()
