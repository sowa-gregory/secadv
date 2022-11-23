import requests
import base64
import os
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

MAIN_URL = "https://www.assaabloy.com/group/en/about-us/product-security/security-advisory"
HID_URL = "https://www.hidglobal.com"


def expanded_raise_for_status(res):
    """
    Take a "requests" response object and expand the raise_for_status method to return more helpful errors
    @param res:
    @return: None
    """
    try:
        res.raise_for_status()
    except HTTPError as e:
        if res.text:
            raise HTTPError(e.request.url, res.text)
        else:
            raise e
    return


def dequote(a):
    a = a[a.find("\"")+1:]
    return a[:a.find("\"")-1]


def processHID(sess, link):
    res = sess.get(link)
    soup = BeautifulSoup(res.text, features="lxml")
    out = soup.find("div", attrs={"class": "field__item"}).find(
        "a").attrs["href"]
    link = HID_URL+out
    print(link, end="")
    return sess.get(link)


def main():
    sess = requests.Session()
    res = sess.get(MAIN_URL)
    expanded_raise_for_status(res)

    soup = BeautifulSoup(res.text, features="lxml")
    content = base64.b64decode(
        soup.find("gw-group-text-and-media-centered").attrs["content"])

    soup = BeautifulSoup(content,  features="lxml")
    tab = soup.select("tr > td > a ")
    links = [i.attrs["href"] for i in tab]

    cnt = 1
    for link in links:
        print(str(cnt)+"/"+str(len(links))+" ", end="")
        cnt += 1
        link = dequote(link)
        if(link.startswith(HID_URL)):
            res = processHID(sess, link)
        else:
            res = sess.get(link)
            print(link, end="")
        if(res.status_code == 200):
            print(bcolors.OKGREEN + " OK" + bcolors.ENDC)
        else:
            print(bcolors.FAIL+" "+str(res.status_code)+bcolors.ENDC)

print(bcolors.HEADER+bcolors.BOLD+"Security Advisory Checker v1.1"+bcolors.ENDC, end="")
print(" - running as UID:"+str(os.getuid())+bcolors.ENDC)
print()
main()