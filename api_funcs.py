import base64
import hashlib
from django.http import JsonResponse



def api_url(urlpat):
    """a decorator function to tag function with their param regexp"""
    def decorate(func):
        func.__urlpattern__ = urlpat
        return func
    return decorate


def render_json(result, err):
    """renders out a consistant json responce"""
    status = 200

    if err is None:
        if result is None:
            err = {
                "msg": "Not Implimented",
                "code": 501,
                "source": "API"
            }
            status = 501
    else:
        status = err["code"]

    res = {
        "err": err,
        "result": result
    }

    return JsonResponse(res, status=status)


def authorize(func):
    '''
    if the header looks like 
    "Authorization: Token 4SMPkrseLzXWYxoaDrTrQOzIwmb3IJCrSc40RvKqkpM="
    take the token and authorise a user
    set req.user to the user object
    '''
    def auth_wrapper(req, *args, **kwargs):
        auth_header = req.META.get('Authorization')
        header_parts = auth_header.split(' ')
        if len(header_parts) == 2 and header_parts[0].upper() == 'TOKEN':
            token = header_parts[1]
            # TODO IMPLIMENT

            return func(req, *args, **kwargs)
        else:
            return render_json(
                None, 
                {
                    "msg": "Not Authorized",
                    "code": 403,
                    "source": "Auth"
                }
            )

    return auth_wrapper



@api_url(r"")
@authorize
def getUser(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getUserByName(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getResidentByName(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getResidentByID(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getResidentByRoom(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getResidentPicByName(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getResidentPicByID(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getResidentNotes(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getResidentNote(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getFormTemplateList(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getFormTemplate(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getFormData(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getRequestedForms(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getFormStatus(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getResidenceHalls(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getResidencehallByName(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getZones(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getZonesByhall(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getZone(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getNodesInZone(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getNode(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getIssues(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getIssuesByZone(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getIssue(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getIssueComments(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getIssueComment(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getRoundTemplates(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getRoundTemplate(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getRound(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def getRoundStatus(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def createResidentNote(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def editResidentNote(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def addResident(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def createForm(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def editFormData(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def createFormTemplate(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def editFromTemplate(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def removeFormTemplate(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def createIssue(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def editIssue(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def createIssueComment(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def editIssueComment(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def createRoundData(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def editRoundData(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def searchResidentByArea(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def searchResidentByHall(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def searchResidentByName(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)


@api_url(r"")
@authorize
def searchResidentFull(req):
    """"""
    result = None
    err = None

    # TODO

    return render_json(result, err)

