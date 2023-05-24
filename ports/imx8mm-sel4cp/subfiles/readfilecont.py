from metadata.breadcrumbs import breadcrumbs
from metadata.nav import nav
from metadata.page_title import page_title
from phew.template import render_template, template_exists
from phew.server import handle_request_cb, content_type_map, Request

from phew.stream import Writer, Reader

import continuation


def make_breadcrumbs(page_name):
    # We assume that the page exists
    pages = page_name.split("/")
    crumbs = []
    if len(pages) == 0 or page_name == "index":
        return b""
    else:
        crumbs = breadcrumbs[pages[0]][pages[1]]

    res = b'<div class="row"><ol class="breadcrumb">'
    for item in crumbs:
        res += b'<li><a href="' + item["url"] + b'">' + item["name"] + b"</a></li>"
    res += b"</ol></div>"
    return res


def render_nav(page_name):
    res = b""
    group = page_name.split("/")[0]

    for item in nav:
        activeGroup = b"active" if item["url"].decode()[1:].startswith(group) else b""
        if page_name == "index":
            activeGroup = b"active" if item["url"] == b"/" else b""

        # res += b'<li><a href="' + item['url'] + b'">' + item['name'] + b'</a></li>'
        if item["children"] and item["children"] != []:
            res += (
                b'<li class="dropdown '
                + activeGroup
                + b'"><a class="dropdown-toggle" data-toggle="dropdown" href="'
                + item["url"]
                + b'">'
                + item["name"]
                + b' <span class="caret"></span></a>'
            )
            res += b'<ul class="dropdown-menu">'
            for child in item["children"]:
                activePage = (
                    b"active"
                    if child["url"].decode()[1:].startswith(page_name)
                    else b""
                )
                res += (
                    b'<li class="'
                    + activePage
                    + b'"><a href="'
                    + child["url"]
                    + b'">'
                    + child["name"]
                    + b"</a></li>"
                )
            res += b"</ul></li>"
        else:
            res += (
                b'<li class="'
                + activeGroup
                + b'"><a href="'
                + item["url"]
                + b'">'
                + item["name"]
                + b"</a></li>"
            )
    return res


def build_page(pagePath, pageContent, addBreadcrumbs=True):
    logoImage = b"logo-text-white.svg"
    logoAlt = b"seL4"
    if pagePath.startswith(b"foundation/summit"):
        logoImage = b"sel4-summit-logo.svg"
        logoAlt = b"seL4 summit logo"
    elif pagePath.startswith(b"foundation"):
        logoImage = b"sel4-foundation-logo.svg"
        logoAlt = b"seL4 foundation logo"

    navigation = render_nav(pagePath)
    breadcrumbs = make_breadcrumbs(pagePath) if addBreadcrumbs else b""
    title = page_title[pagePath]
    content = b"".join(
        [
            b
            for b in render_template(
                "sel4header.html",
                navigation=navigation,
                breadcrumbs=breadcrumbs,
                title=title,
                pageContent=pageContent,
                logoImage=logoImage,
                logoAlt=logoAlt,
            )
        ]
    )
    return content


privateData = continuation.loadprivatedata()
page_cont = continuation.loaddata()
pageReq = privateData["page_req"]

contentType = content_type_map[privateData["pagePath"].split(".")[-1]] if not pageReq else "text/html"
if (pageReq):
    page_cont = build_page(privateData["pagePath"], page_cont, privateData["addBreadcrumbs"])

handle_request_cb(Writer(), Request(privateData['method'], privateData['uri'], privateData['protocol']), (page_cont, 200, contentType))