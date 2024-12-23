"""
client
======

Convenience functions for working with the Onshape API
"""

from .onshape import Onshape

import os
import random
import string
from urllib import parse
import mimetypes
from typing import Literal


class Client:
    """
    Defines methods for testing the Onshape API. Comes with several methods:

    - Create a document
    - Delete a document
    - Get a list of documents

    Attributes:
        - stack (str, default='https://cad.onshape.com'): Base URL
        - logging (bool, default=True): Turn logging on or off
    """

    def __init__(self, stack="https://cad.onshape.com", logging=True):
        """
        Instantiates a new Onshape client.

        Args:
            - stack (str, default='https://cad.onshape.com'): Base URL
            - logging (bool, default=True): Turn logging on or off
        """

        self._stack = stack
        self._api = Onshape(stack=stack, logging=logging)

    def new_document(self, name="Test Document", owner_type=0, public=False):
        """
        Create a new document.

        Args:
            - name (str, default='Test Document'): The doc name
            - owner_type (int, default=0): 0 for user, 1 for company, 2 for team
            - public (bool, default=False): Whether or not to make doc public

        Returns:
            - requests.Response: Onshape response data
        """

        payload = {"name": name, "ownerType": owner_type, "isPublic": public}

        return self._api.request("post", "/api/documents", body=payload)

    def rename_document(self, did, name):
        """
        Renames the specified document.

        Args:
            - did (str): Document ID
            - name (str): New document name

        Returns:
            - requests.Response: Onshape response data
        """

        payload = {"name": name}

        return self._api.request("post", "/api/documents/" + did, body=payload)

    def del_document(self, did):
        """
        Delete the specified document.

        Args:
            - did (str): Document ID

        Returns:
            - requests.Response: Onshape response data
        """

        return self._api.request("delete", "/api/documents/" + did)

    def get_document(self, did: str):
        """
        Get details for a specified document.

        Args:
            - did (str): Document ID

        Returns:
            - requests.Response: Onshape response data
        """

        return self._api.request("get", "/api/documents/" + did)

    def get_versions(self, did: str):
        """
        Get details for a specified document.

        Args:
            - did (str): Document ID

        Returns:
            - requests.Response: Onshape response data
        """

        return self._api.request("get", f"/api/documents/{did}/versions")

    def get_tabs(
        self, did: str, wv: Literal["workspace", "version", "microversion"], wvmid: str
    ):
        """
        Get details for a specified document.

        Args:
            - did (str): Document ID

        Returns:
            - requests.Response: Onshape response data
        """
        mode = ""

        match wv:
            case "workspace":
                mode = "w"
            case "version":
                mode = "v"
            case "microversion":
                mode = "m"

        return self._api.request(
            "get", f"/api/documents/d/{did}/{mode}/{wvmid}/elements"
        )

    def get_workspaces(self, did: str):
        """
        Get details for a specified document.

        Args:
            - did (str): Document ID

        Returns:
            - requests.Response: Onshape response data
        """

        return self._api.request("get", "/api/documents/" + did + "/workspaces")

    def get_documents(
        self,
        filter: Literal["my", "public"] | Literal[0, 1, 2, 3, 4] = "my",
        q: str = "",
        limit: int = 20,
        offset: int = 0,
    ):
        """
        Get list of documents for current user.

        Returns:
            - requests.Response: Onshape response data
        """
        params = {}
        if q:
            params["q"] = q

        if filter == "public":
            params["filter"] = 4
        elif filter == "my":
            params["filter"] = 0

        else:
            try:
                filter = int(filter)  # type: ignore
                params["filter"] = filter
            except:
                pass

        if offset:
            params["offset"] = offset

        params["limit"] = limit

        return self._api.request("get", "/api/documents", params=params)

    def search_documents(
        self,
        filter: Literal["my", "public"] | Literal[0, 1, 2, 3, 4] = "my",
        q: str = "",
        limit: int = 20,
        offset: int = 0,
    ):
        """
        Get list of documents for current user.

        Returns:
            - requests.Response: Onshape response data
        """
        params = {}
        if filter == "public":
            params["documentFilter"] = 4
        elif filter == "my":
            params["documentFilter"] = 0

        else:
            try:
                filter = int(filter)  # type: ignore
                params["documentFilter"] = filter
            except:
                pass

        params.update(
            {
                "foundIn": "w",
                "limit": limit,
                "offset": offset,
                "ownerId": "",
                "parentId": "ALL",
                "rawQuery": f"_all:{q} type:partstudio" if q else "",
                "sortColumn": "createdAt",
                "sortOrder": "desc",
                "type": "string",
                "when": "latest",
            }
        )

        return self._api.request("post", "/api/documents/search", body=params)

    def documents_id(
        self, filter: Literal["my", "public"] = "my", query: str = "", limit: int = 20
    ) -> list[str]:
        if limit < 0:
            unlimited = True
        else:
            unlimited = False
        response = self.search_documents(
            filter, query, limit if limit < 20 and not unlimited else 20
        ).json()
        result = [doc["id"] for doc in response["items"]]

        if limit > 20 or unlimited:
            limit -= len(result)
            while unlimited or limit > 0:
                params = parse.parse_qs(parse.urlparse(response["next"]).query)
                params = {
                    k: v[0] if v and len(v) == 1 else v for k, v in params.items()
                }

                if params:
                    params["limit"] = limit if limit < 20 and not unlimited else 20
                    params["q"] = query
                    params["filter"] = filter
                    response = self.search_documents(**params).json()  # type: ignore
                    new = [doc["id"] for doc in response["items"]]
                    limit -= len(new)
                    result += new

                else:
                    break

        return result

    def document_links(self, did: str) -> list[str]:
        result: list[str] = []
        workspaces = [ws["id"] for ws in self.get_workspaces(did).json()]

        for ws in workspaces:
            tabs = [t["id"] for t in self.get_tabs(did, "workspace", ws).json()]
            for t in tabs:
                result.append(f"https://cad.onshape.com/documents/{did}/w/{ws}/e/{t}")

        return result

    def create_assembly(self, did, wid, name="My Assembly"):
        """
        Creates a new assembly element in the specified document / workspace.

        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - name (str, default='My Assembly')

        Returns:
            - requests.Response: Onshape response data
        """

        payload = {"name": name}

        return self._api.request(
            "post", "/api/assemblies/d/" + did + "/w/" + wid, body=payload
        )

    def get_features(self, did, wid, eid):
        """
        Gets the feature list for specified document / workspace / part studio.

        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - eid (str): Element ID

        Returns:
            - requests.Response: Onshape response data
        """

        return self._api.request(
            "get", "/api/partstudios/d/" + did + "/w/" + wid + "/e/" + eid + "/features"
        )

    def get_partstudio_tessellatededges(self, did, wid, eid):
        """
        Gets the tessellation of the edges of all parts in a part studio.

        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - eid (str): Element ID

        Returns:
            - requests.Response: Onshape response data
        """

        return self._api.request(
            "get",
            "/api/partstudios/d/"
            + did
            + "/w/"
            + wid
            + "/e/"
            + eid
            + "/tessellatededges",
        )

    def upload_blob(self, did, wid, filepath="./blob.json"):
        """
        Uploads a file to a new blob element in the specified doc.

        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - filepath (str, default='./blob.json'): Blob element location

        Returns:
            - requests.Response: Onshape response data
        """

        chars = string.ascii_letters + string.digits
        boundary_key = "".join(random.choice(chars) for i in range(8))

        mimetype = mimetypes.guess_type(filepath)[0]
        encoded_filename = os.path.basename(filepath)
        file_content_length = str(os.path.getsize(filepath))
        blob = open(filepath)

        req_headers = {
            "Content-Type": 'multipart/form-data; boundary="%s"' % boundary_key
        }

        # build request body
        assert mimetype is not None, "Mimetype can't be None"

        payload = (
            "--"
            + boundary_key
            + '\r\nContent-Disposition: form-data; name="encodedFilename"\r\n\r\n'
            + encoded_filename
            + "\r\n"
        )
        payload += (
            "--"
            + boundary_key
            + '\r\nContent-Disposition: form-data; name="fileContentLength"\r\n\r\n'
            + file_content_length
            + "\r\n"
        )
        payload += (
            "--"
            + boundary_key
            + '\r\nContent-Disposition: form-data; name="file"; filename="'
            + encoded_filename
            + '"\r\n'
        )
        payload += "Content-Type: " + mimetype + "\r\n\r\n"
        payload += blob.read()
        payload += "\r\n--" + boundary_key + "--"

        return self._api.request(
            "post",
            "/api/blobelements/d/" + did + "/w/" + wid,
            headers=req_headers,
            body=payload,
        )

    def part_studio_stl(self, did, wid, eid):
        """
        Exports STL export from a part studio

        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - eid (str): Element ID

        Returns:
            - requests.Response: Onshape response data
        """

        req_headers = {"Accept": "application/vnd.onshape.v1+octet-stream"}
        return self._api.request(
            "get",
            "/api/partstudios/d/" + did + "/w/" + wid + "/e/" + eid + "/stl",
            headers=req_headers,
        )
