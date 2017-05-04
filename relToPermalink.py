import os
import re
import requests
"""
Program to search through all markdown files in the repo, and look for links in the form:
(*)[<relative link>]:perm
"""


base_github_url = "https://github.com/hgarrereyn/Th3g3ntl3man-CTF-Writeups/tree/dev/"
shortened_github_url = base_github_url[len("https://github.com"):] + 'blob/'
check_files_ending_in = ".md"
reSearch = re.compile("(\[.*?\]\(.*?\):perm)")
imgEndings = ['.png','.jpg','.jpeg','.gif']

def main():
    exclude = ['.git','picoCTF_2017','PACTF_2017']
    for root, dirs, files in os.walk('.', topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude]
        for f in files:
            if(f.endswith(check_files_ending_in)):
                fcontents = open(root+'/'+f).read()
                matches = reSearch.findall(fcontents)
                if(len(matches)>0):
                    print(("Found %s links to update in " + root+'/'+f) % len(matches))
                    for match in matches:
                        # Convert these to permalinks
                        path = match[match.index('(')+1:match.index(')')]
                        useRaw = False
                        for ending in imgEndings:
                            if(path.endswith(ending)):
                                useRaw = True
                                break
                        URL = ""
                        if(path[0]=='/'):
                            URL = base_github_url + path[1:]
                        elif(path[:4] == 'http'):
                            print(path + " is a URL, trying to convert it anyway...")
                            URL = path
                        else:
                            URL =  base_github_url + root + '/' + path
                        githubURL = convertURLtoPermalink(URL)
                        if(useRaw):
                            githubURL = githubURL + "?raw=true"
                        newMatch = match.replace(path,githubURL)[:-5]
                        print("converting %s to %s" % (match,newMatch))
                        fcontents = fcontents.replace(match,newMatch)
                    open(root+'/'+f,'w').write(fcontents)


def convertURLtoPermalink(URL):
    #print(URL)
    r = requests.get(URL)
    text = r.text
    #print(text)
    cutdownText = text[:text.index("class=\"d-none js-permalink-shortcut\" data-hotkey=\"y\">Permalink</a>")]
    cutdownText = cutdownText[cutdownText.rindex("<a href=\"")+9:-2]
    return "https://github.com" + cutdownText

main()
