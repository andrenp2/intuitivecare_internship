# import required library and packages
from bs4 import BeautifulSoup
import requests
import re
import os.path
from shutil import make_archive
import time

# start time count
start = time.time()

def getHTMLdocument(url):
    response = requests.get(url)
    return response.text


def download_archives(url, address):
    """
        This function, after requesting access to the site,
        rewrites the desired files to be downloaded.
    """

    response = requests.get(url)
    if response.status_code == requests.codes.OK:
        with open(address, 'wb') as new_archive:
            new_archive.write(response.content)
    else:
        response.raise_for_status()


def attachments_links():
    """
    Function that fetches the download links of each file in the HTML structure,
    which are similar to those determined as parameters in "href" as below

    """

    list_attachments = []
    for link in soup.find_all('a', attrs={'href': re.compile(
            "^https://www.gov.br/ans/pt-br/arquivos/assuntos/consumidor/o-que-seu-plano-deve-cobrir/Anexo")}):
        list_attachments.append(link.get('href'))

    return list_attachments


def dict_mount(list_attachments):
    """
        This function aims to return a dictionary where the name
        and link of the file to be downloaded will be stored.
    """

    dict_urls = {}
    dict_aux = {}
    for i in list_attachments:
        name = i.split('https://www.gov.br/ans/pt-br/arquivos/assuntos/consumidor/o-que-seu-plano-deve-cobrir/')[1]
        link = i
        dict_aux = { name : link }
        dict_urls.update(dict_aux)

    return dict(dict_urls)

def create_directory(name):
    if os.path.isdir(name):
        print("The directory 'output' already exist.")
    else:
        os.mkdir(name)
    return name


if __name__ == "__main__":
    url_to_scrapy = 'https://www.gov.br/ans/pt-br/assuntos/consumidor/o-que-o-seu-plano-de-saude-deve-cobrir-1/o-que-e-o-rol-de-procedimentos-e-evento-em-saude'

    html_document = getHTMLdocument(url_to_scrapy)
    soup = BeautifulSoup(html_document, 'html.parser')

    list_attachments = attachments_links() # search links to download

    dict_urls = dict_mount(list_attachments) # create directory with name and links for each document

    output_dir = create_directory('output') # name of output directory

    for keys, value in dict_urls.items():
        name = keys
        link = value
        name_archive = os.path.join(output_dir,'{}'.format(name))

        download_archives(link, name_archive)

    # compress files
    make_archive('output', 'zip', 'output')
    print("downloaded and compressed files. OK.")

    # end time count
    end = time.time()
    print("Time to execute: {:.2f} s".format(end-start))