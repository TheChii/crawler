from urllib.request import Request, urlopen

import os

website = "github.com"

directory = input("New folder name: ")

req = Request(website, headers={'User-Agent': 'Mozilla/5.0'})
page_source = urlopen(req).read().decode('utf-8')

def setup():

    parent_dir = os.getcwd()
    path = os.path.join(parent_dir, directory)
    css_path = os.path.join(path, "css")
    js_path = os.path.join(path, "js")


    try:
        os.makedirs(path, exist_ok = True)
        os.makedirs(css_path, exist_ok = True)
        os.makedirs(js_path, exist_ok = True)

        print("Directories created successfully")
    except OSError as error:
        print("Something went wrong creating directories")


kw = ["src=", "href="]

css_files = []
js_files = []

css_names = []
js_names = []

lines = page_source.split("\n")

def get_all():
    for line in lines:
        line = line.replace(" ", "")
        if "stylesheet" in line or "script" in line:
            for keyword in kw:
                if keyword in line:
                    first_pos = line.index(keyword) + len(keyword) + 1
                    end_pos = None
                    if "'" in line[first_pos:]:
                        end_pos =  line[first_pos:].index("'")

                    elif '"' in line[first_pos:]:
                        end_pos = line[first_pos:].index('"')


                    if(keyword == "src="):
                        js_files.append(line[first_pos:(first_pos+end_pos)])
                    else:
                        css_files.append(line[first_pos:(first_pos+end_pos)])

def get_css():
    for line in lines:
        line = line.replace(" ", "")
        if "stylesheet" in line:
            keyword = "href="
            try:
                first_pos = line.index(keyword) + len(keyword) + 1
                end_pos = None
                if "'" in line[first_pos:]:
                    end_pos =  line[first_pos:].index("'")

                elif '"' in line[first_pos:]:
                    end_pos = line[first_pos:].index('"')
                css_files.append(line[first_pos:(first_pos+end_pos)])
            except:
                pass



def get_js():
    for line in lines:
        line = line.replace(" ", "")
        if "scriptsrc=" in line:
            keyword = "src="
            try:
                first_pos = line.index(keyword) + len(keyword) + 1
                end_pos = None
                if "'" in line[first_pos:]:
                    end_pos =  line[first_pos:].index("'")

                elif '"' in line[first_pos:]:
                    end_pos = line[first_pos:].index('"')
                js_files.append(line[first_pos:(first_pos+end_pos)])
            except:
                pass

def ru(n):
	extensions = ["js", "css", "html"]
	pos = None
	ln = None

	for x in extensions:
		if x in n:
			pos = n.index(x)
			ln = len(x)

	return n[0:pos+ln]

def fileName(n):
	if "http" in n:
		for chr in n[::-1]:
			if(chr == "/"):
				stop = len(n) - n[::-1].index(chr)
				return ru(n[stop:])
	else:
		lc = n[::-1].index("/")
		start = len(n)-lc
		return n[start:]

def get_content(fname):
    if "http" in fname:
        req = Request(fname, headers={'User-Agent': 'Mozilla/5.0'})
        print(fname)
        page_source = urlopen(req).read().decode('utf-8')
        return page_source
    else:
        newurl = website + "/" + fname

        print(newurl)
        req = Request(newurl, headers={'User-Agent': 'Mozilla/5.0'})
        page_source = urlopen(req).read().decode('utf-8')
        return page_source

def save_content():
    parent_dir = os.getcwd()
    path = os.path.join(parent_dir, directory)
    css_path = os.path.join(path, "css")
    js_path = os.path.join(path, "js")

    for file in css_files:
        try:
            f_path = css_path + "/"+fileName(file)
            css_files[css_files.index(file)] = fileName(file)
            with open(f_path, "w", encoding='utf-8') as f:
                f.write(get_content(file))
            js_names.append(fileName(file))
        except:
            print(file + " could not be saved ")

    for file in js_files:
        try:
            js_files[js_files.index(file)] = fileName(file)
            f_path = js_path + "/"+fileName(file)
            with open(f_path, "w", encoding='utf-8') as f:
                f.write(get_content(file))
            js_names.append(fileName(file))
        except:
            print(file + "could not be saved")

for x in lines:
    if "head" in x:
        for fn in css_names:
            new_name = css_path + '/' + fn
            new_line = '<link rel="stylesheet" href="{flname}">'.format(flname = fn)
            lines.insert(lines.index("head")+1, new_line)
        for fn in js_names:
            new_name = css_path + '/' + fn
            new_line = '<script src="{fname}"></script>'.format(fname = new_name)
            lines.insert(lines.index("head")+1, new_line)

with open("index.html", "w") as f:
    f.write(lines)
print(lines)
setup()
get_all()
save_content()
