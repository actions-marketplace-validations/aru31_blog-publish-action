import frontmatter
from urllib import request
from devto import devto_create, devto_update
from findfiles import FindFiles
from constants import GITHUB_CODES, API_URLS
from custom_exceptions import UpdationNotImplemented, WrongURLException


class BlogPublishAPI(object):
    def __init__(self, apikey, owner_repo):
        self.content = None
        self.metadata = None
        self.apikey = apikey
        self.owner_repo = owner_repo

    def download_file(self, url, filename):
        try:
            # downloading the file with the same name will override the previous file
            request.urlretrieve(url, "blog.md")
            print(f"Downloading file -> {filename}")
        except Exception as e:
            print(f"Error message : {e}")
            raise WrongURLException(url)

    def parse_md(self):
        """
        parse the .md file to separate body (content) from frontmatter (metadata)
        """

        print("Parsing the markdown file")
        with open("blog.md") as f:
            self.metadata, self.content = frontmatter.parse(f.read())

    def devto_publish(self):
        """
        Dev.to publish
        """

        findfiles = FindFiles(self.owner_repo)

        """
        files sample schema: 
        [
            {'filename': 'test_blog.md', 'url': '....', 'status': 'modified'},
            {...}
        ]
        """
        files = findfiles.useful_files

        # iterating through all the files (list of dictionaries)
        for file_info in files:
            self.download_file(
                url=file_info["url"], filename=file_info["filename"])
            self.parse_md()

            if file_info["status"] == GITHUB_CODES.ADDED:
                devto_create(metadata=self.metadata, content=self.content,
                             apikey=self.apikey, url=API_URLS.DEVTO)
            if file_info["status"] == GITHUB_CODES.MODIFIED:
                # raise UpdationNotImplemented("dev.to")
                devto_update()
