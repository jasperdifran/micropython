from metadata.breadcrumbs import breadcrumbs
from metadata.nav import nav
from metadata.page_title import page_title
from phew.template import render_template, template_exists
from phew.server import handle_request_cb

from phew.stream import Writer, Reader

import continuation


def make_breadcrumbs(page_name):
    # We assume that the page exists
    pages = page_name.split("/")
    crumbs = []
    if len(pages) == 0:
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


def build_page(page_name, page_content, addBreadcrumbs=True):
    logo_image = b"logo-text-white.svg"
    logo_alt = b"seL4"
    if page_name.startswith(b"foundation/summit"):
        logo_image = b"sel4-summit-logo.svg"
        logo_alt = b"seL4 summit logo"
    elif page_name.startswith(b"foundation"):
        logo_image = b"sel4-foundation-logo.svg"
        logo_alt = b"seL4 foundation logo"

    navigation = render_nav(page_name)
    breadcrumbs = make_breadcrumbs(page_name) if addBreadcrumbs else b""
    title = page_title[page_name]
    content = b"".join(
        [
            b
            for b in render_template(
                "sel4header.html",
                navigation=navigation,
                breadcrumbs=breadcrumbs,
                title=title,
                page_content=page_content,
                logo_image=logo_image,
                logo_alt=logo_alt,
            )
        ]
    )
    return content


req = continuation.loadprivatedata()
print("Got request", req["page_req"])
print("Got request", req["start_time"])
print("Got request", req["uri"])
print("got request", req["method"])
page_cont = continuation.loaddata()
cont_len = len(page_cont)
# print("Last 3", page_cont[-3:])
# for i in range(10):
#     if (page_cont[cont_len - 1 - i] == 0):
#         print("Last char is null")
#         page_cont = page_cont[:-1]


# if (page_cont[cont_len - 1] == 0):
#     print("Last char is null")
#     page_cont = page_cont[:-1]

# print("last 3", page_cont[-3:])

print("Got page content len", len(page_cont))
finished_page = build_page("index", page_cont, False)
print("Got page content len", len(finished_page))

handle_request_cb(None, Writer(), req, (finished_page, 200, "text/html"))

# print("Got page content btyes", page_cont)
# print("Got page content", page_cont.decode())

# print(build_page(req["uri"] if req["uri"] != "/" else "index", page_cont, False).decode())