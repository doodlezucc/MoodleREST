import json
import os
from pathlib import Path
import re
from typing import Any, Dict, List, cast

# Matches single and multiline comments
p_cmnt = r"//.*?$|/\*.*?\*/"

# 1: [new]...
# 2: <FUNCTION_CALL>(
# 3: <boolean>
# 4: <float>
# 5: <int>
# 6: <string>
# 7: <VAR>
# 8: short syntax array "[" 
# 9: comment
r_expression = re.compile(
    fr"(new )?([$\w]+?)\s*\(|(?:(true|false)|(\d+\.\d+)|(\d+)|(?:'(.*?)(?<!\\)')|([\w$\\]+))[,\s\.:;\])]|(\[)|({p_cmnt})",
    flags=re.M|re.S
)
r_array_sep = re.compile(r"=>|,", flags=re.M|re.S)
r_assign_functions = re.compile(r"\$functions\s*=", flags=re.M|re.S)

r_namespace = re.compile(r"^namespace\s*(\S+);", flags=re.M|re.S)
r_class = re.compile(r"^class\s*(\S+)(?:\s+extends\s+(\S+))?\s*{", flags=re.M|re.S)
r_doc = re.compile(r"/\*.*?\*/", flags=re.M|re.S)
r_doc_tag = re.compile(r"@(since|deprecated|todo)\s+(.*?)$", flags=re.M|re.S)
r_semver = re.compile(r"\d+(?:\.\d+)+")

r_param_def = re.compile(r" \* (PARAM_\S+)\W+(.*?)\s*?\*\/.*?define\(.*?,.*?'(.*?)'", flags=re.M|re.S)

def outer_scope(code: str, open = "{", close = "}"):
    # Matches comments first, brackets second
    matches = re.finditer(fr"{p_cmnt}|(\{open}|\{close})", code, flags=re.M|re.S)
    depth = 0
    start = None

    for match in matches:
        if match[1]:
            if match[1] == open:
                depth += 1
                if start is None:
                    start = match.start()
            else:
                depth -= 1
                if depth <= 0:
                    return code[start:match.end()]

class Expression():
    def __init__(self):
        pass

    def resolve(self):
        raise NotImplementedError()

class Primitive(Expression):
    def __init__(self, value):
        super().__init__()
        self.value = value
    
    def __repr__(self):
        if isinstance(self.value, str):
            return f'"{self.value}"'
        return str(self.value)
    
    def resolve(self):
        return self.value

class Reference(Expression):
    def __init__(self):
        super().__init__()
    
    def dereference(self, ctx: dict = None) -> Expression:
        raise NotImplementedError()
    
    def resolve(self):
        return self.dereference().resolve()

class Lookup(Reference):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
    
    def dereference(self, ctx: dict = None) -> Expression:
        if not ctx:
            ctx = prop_lookup
        
        value = ctx[self.name]
        return Primitive(value)
    
    def __repr__(self) -> str:
        return f"var({self.name})"

class Property(Reference):
    def __init__(self, object: Expression, prop: Reference):
        super().__init__()
        self.object = object
        self.prop = prop
    
    def dereference(self, ctx: dict = None) -> Expression:
        if isinstance(self.object, Lookup):
            if not ctx:
                ctx = prop_lookup
            try:
                value = ctx[self.object.name]
                return self.prop.dereference(value)
            except KeyError:
                if isinstance(self.prop, Lookup) and self.prop.name == "class":
                    return Primitive(self.object.name)

        return self.prop
    
    def __repr__(self) -> str:
        return f"{self.object}->{self.prop}"

class Call(Reference):
    def __init__(self, fn: str, params: List[Expression]):
        super().__init__()
        self.fn = fn
        self.params = params
    
    def __repr__(self) -> str:
        return str((self.fn, self.params))

class Constructor(Call):
    def __init__(self, classname: str, params: List[Expression]):
        super().__init__(f"{classname}.new", params)
        self.classname = classname
    
    def __repr__(self) -> str:
        return f"{self.classname}({self.params})"

class PhpArray(Call):
    def __init__(self, entries: Dict[Any, Expression]):
        super().__init__("array", [Primitive(entries)])
        self.entries = entries
        self.is_array = True
        for key in entries:
            if not isinstance(key, int):
                self.is_array = False
                break
        
        self.py = [entries[key] for key in entries] if self.is_array else entries

    def __repr__(self) -> str:
        return str(self.py)
    
    def resolve(self):
        return self.py

prop_lookup = {}

def read_scope(s: str, pos: List[int], open="(", close=")"):
    start = s.index(open, pos[0])
    scope = outer_scope(s[start:], open, close)
    pos[0] = start + len(scope)
    return scope

def read_expression(s: str, pos: List[int]):
    match = r_expression.search(s, pos=pos[0])
    if match:
        pos[0] = match.end() - 1

        result = None
        
        if match[1]:
            result = Constructor(match[2], read_array(read_scope(s, pos)))
        elif match[2]:
            if match[2] != "array":
                result = Call(match[2], read_array(read_scope(s, pos)))
            else:
                result = read_array(read_scope(s, pos))
        elif match[3]:
            result = Primitive(True if match[3] == "true" else False)
        elif match[4]:
            result = Primitive(float(match[4]))
        elif match[5]:
            result = Primitive(int(match[5]))
        elif match[6]:
            result = Primitive(match[6])
        elif match[7]:
            result = Lookup(match[7])
        elif match[8]:
            result = read_array(read_scope(s, pos, open="[", close="]"))
        elif match[9]:
            # Match is comment, continue looking
            return read_expression(s, pos)
        
        try:
            last = s[pos[0]]
            if last in ".:":
                result = Property(result, read_expression(s, pos))
        finally:
            return result
    
    # raise ValueError(f'Unable to find expression in "{s[pos[0]:]}"')

def read_array(s: str):
    defs = dict()
    count = 0
    pos = [1]
    expr = read_expression(s, pos)
    while expr is not None:
        sep = r_array_sep.search(s, pos=pos[0])
        if sep is not None and sep[0] == "=>":
            defs[expr.resolve()] = read_expression(s, pos)
        else:
            defs[count] = expr
            count += 1 # todo(?) update count with integer keys
        
        expr = read_expression(s, pos)
    
    return PhpArray(defs)

class DocTags():
    def __init__(self, since: str = None, deprecated: str = None, todo: str = None):
        self.since = since
        self.deprecated = deprecated
        self.todo = todo
    
    def __repr__(self) -> str:
        return f'Docs({self.since}, {self.deprecated}, {self.todo})'

def parse_docs(docs: str):
    tags = dict()

    for match in r_doc_tag.finditer(docs):
        tag = match[1]
        comment = match[2]
        tags[tag] = comment
    
    return DocTags(tags.get("since"), tags.get("deprecated"), tags.get("todo"))

def find_docs(classdef: str, method: str):
    fn = re.search(f"function {method}" + r"\(.*?{", classdef)
    if not fn:
        return DocTags()
    
    try:
        previous_bracket = classdef.rindex("}", 0, fn.start())
        matches = r_doc.finditer(classdef, previous_bracket, fn.start())
        *_, docs = matches
        return parse_docs(docs[0])
    except ValueError:
        return DocTags()

def extract_classes(file: Path, lookup: dict):
    with file.open("r", -1, "utf-8", errors="replace") as f:
        content = f.read()

        space = r_namespace.search(content)
        prefix = f"{space[1]}\\" if space else ""

        for match in r_class.finditer(content):
            name = match[1]
            key = prefix + name
            lookup[key] = outer_scope(content[(match.end() - 1):])

def make_class_lookup(root: Path):
    lookup = dict()

    files = list(root.rglob("*.php"))
    num = len(files)
    numf = float(num)
    count = 0
    for file in files:
        count += 1
        if count % 100 == 0:
            percent = "{0:.1%}".format(count / numf)
            print(f"Finding classes... {percent} ({count}/{num})")
        extract_classes(file, lookup)
    
    return lookup

def extract_function_info(spec: PhpArray, class_defs: Dict[str, str], cwd: Path):
    # Some $functions don't have methodnames and default to "execute()"
    try:
        method = cast(str, spec.entries["methodname"].resolve())
    except KeyError:
        method = "execute"

    classid = cast(str, spec.entries["classname"].resolve())
    if classid.startswith("\\"):
        classid = classid[1:]
    
    classid = classid.replace("\\\\", "\\")
    definition = class_defs[classid]

    # print(f"Looking for {method} in {classid}")
    return_docs = find_docs(definition, f"{method}_returns")
    return return_docs

def find_services_php(dirpath: Path):
    return dirpath.rglob("db/services.php")

def extract_from_services(services: Path, cwd: Path, cls_lookup: dict, fns: dict = {}):
    content = services.read_text()

    pos = [r_assign_functions.search(content).end()]
    arr = cast(PhpArray, read_expression(content, pos))

    if not len(arr.entries):
        return fns

    for fn in arr.entries:
        fns[fn] = extract_function_info(arr.entries[fn], cls_lookup, cwd)
    return fns

def extract_all(root: Path, limit = -1):
    print("Reading ALL class definitions")
    cls_lookup = make_class_lookup(root)
    print("Class lookup created. Resolving web service functions...")
    all_services = find_services_php(root)

    wsfns = dict()
    for php in all_services:
        print(php)
        extract_from_services(php, root, cls_lookup, wsfns)
        
        limit -= 1
        if limit == 0:
            break
    
    return wsfns

def extend_with_doc_tags(obj: Dict, tags: DocTags):
    if tags.since:
        obj["since"] = r_semver.search(tags.since)[0]
    if tags.deprecated:
        obj["deprecated"] = r_semver.search(tags.deprecated)[0]
    if tags.todo:
        obj["todo"] = tags.todo

def extend_wsapi(wsapi_file: str, output: str, tags: Dict[str, DocTags]):
    with open(wsapi_file, "r") as f:
        wsapi = json.load(f)
        
        for compname in wsapi:
            component = wsapi[compname]
            for funcname in component:
                try:
                    docs = tags[funcname]
                    fn = component[funcname]
                    extend_with_doc_tags(fn, docs)

                except KeyError:
                    pass
        
        with open(output, "w") as f:
            json.dump(wsapi, f, separators=(',', ':'))

def punctuate(s: str):
    """Ensures a uppercase first letter and a period, exclamation point, question mark or bracket at the end of s."""
    s = s[0].upper() + s[1:]
    if s[-1] in ".!?()[]{}":
        return s
    
    return s + "."

def get_comment_text(comment: str):
    # Remove doc tags and leading comment asterisks
    lines = comment.splitlines()
    out_lines = [""]

    for line in lines:
        trim = line.replace(" *", "").strip()
        if trim.startswith("@"): # skip doc tags
            continue

        if len(trim):
            if trim.startswith("NOTE"):
                out_lines.append("")

            elif len(out_lines[-1]):
                out_lines[-1] += " "
            
            out_lines[-1] += trim
        else:
            out_lines.append("")
        
    return "\n".join(punctuate(line) for line in out_lines)

def read_param_type_defs(root: Path):
    lib_path = "lib/moodlelib.php"
    lib_file = root.joinpath(lib_path)
    contents = lib_file.read_text(errors="ignore")

    matches = r_param_def.finditer(contents)

    params = dict()

    for match in matches:
        const_name = match[1]
        comment = match[2]
        key = match[3]

        if "alias" in comment.lower(): # Skip deprecated alias types
            continue

        tags = parse_docs(comment)
        comment = get_comment_text(comment)

        entry = {
            "id": const_name,
            "comment": comment
        }
        extend_with_doc_tags(entry, tags)

        params[key] = entry
    
    return params

def extract_param_type_defs(moodle_root: Path, output):
    param_defs = read_param_type_defs(moodle_root)
    
    with open(output, "w") as f:
        json.dump(param_defs, f, indent="\t")

def main(extract_param_types = True, extend_api = True):
    os.chdir(os.path.dirname(__file__))

    root = Path("../../../../Moodle-400/server/moodle")
    wsapi_file = "wsapi.json"
    output = "../src/api/moodle-4.0.0.json"
    output_params = "../src/api/params.g.json"

    if extract_param_types:
        print("Extracting available parameter types")
        extract_param_type_defs(root, output_params)

    if extend_api:
        print("Extracting tags...")
        wsfns = extract_all(root)

        print(f"Documentation tags extracted successfully!\n")
        print("Applying tags to generated API Reference...")
        extend_wsapi(wsapi_file, output, wsfns)
    
    print("Done!")

main(extend_api=False)
