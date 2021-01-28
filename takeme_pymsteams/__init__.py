""" MS Teams Module """

# System Imports
import json

# 3rd Party Imports
import pymsteams
import requests
import shareplum

class SharePointService:
    DIGEST_HEADER_KEY = 'X-RequestDigest'
    DOC_LIB = 'Shared Documents'

    def __init__(self, share_point_site: str, site_name: str, user_name: str, password: str):
        """
        Constructor
        """
        self.__session = requests.Session()
        self.__session.headers.update({ 'User-Agent': 'python_bite/v1' })
        self.__session.headers.update({ 'Accept': 'application/json;odata=verbose' })
        self.__session.cookies = shareplum.Office365(
            share_point_site=share_point_site,
            username=user_name,
            password=password
        ).GetCookies()
        self.__api_url = '{share_point_site}/sites/{site_name}/_api'.format(
            share_point_site=share_point_site,
            site_name=site_name
        )
        self.__share_point_site = share_point_site

    def __get_form_digest(self) -> str:
        """
        Get form digest value.
        """
        url = '{api_url}/contextinfo'.format(api_url=self.__api_url)
        response = self.__session.post(url=url, data='')
        json_body = json.loads(response.text)
        try: 
            return json_body['d']['GetContextWebInformation']['FormDigestValue']
        except Exception as err: 
            print(str(err))
        return ''

    def upload(self, file_name: str) -> str:
        """
        Upload the specified file to the document library.
        """
        with open(file_name, 'rb+') as fp:
            if self.DIGEST_HEADER_KEY not in self.__session.headers:
                form_digest = self.__get_form_digest()
                if form_digest != '':
                    self.__session.headers.update({ self.DIGEST_HEADER_KEY: self.__get_form_digest() })
            try: 
                response = self.__session.post( 
                    url="{}/web/GetFolderByServerRelativeUrl('{}')/Files/add(url='{}',overwrite=true)".format(
                        self.__api_url,
                        self.DOC_LIB,
                        file_name
                    ),
                    data=fp
                )
                json_body = json.loads(response.text)
                return '{}{}'.format(self.__share_point_site, json_body['d']['ServerRelativeUrl']) 
            except Exception as err: 
                print(str(err))

class Teams:
    def __init__(self):
        """
        Constructor
        """
        self.__sharepoint_svc = None

    def connect_to_share_point(self, share_point_site: str, site_name: str, user_name: str, password: str):
        """
        Connect to the specified SharePoint site.
        """
        self.__sharepoint_svc = SharePointService(
            share_point_site=share_point_site,
            site_name=site_name,
            user_name=user_name,
            password=password
        )

    def send(self, channel: str, text: str, file: str=''):
        """
        Send the specified file to the Teams TakeMe Pay channel.
        """
        teams = pymsteams.connectorcard(channel)
        teams.text(text)
        if file != '' and self.__sharepoint_svc is not None:
            file_url = self.__sharepoint_svc.upload(file)
            teams.addLinkButton('ファイルを閲覧する', file_url)
        teams.send()
