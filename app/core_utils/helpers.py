# /app/core_utils/helpers.py

from functools import wraps
from django.shortcuts import redirect
from django.conf import settings

def login_required_no_next(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Redirect straight to your login page without appending ?next=
            return redirect(settings.LOGIN_URL)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def is_garden_editor(user):
    """ Helper function to verify user group """
    return user.is_authenticated and user.groups.filter(name='Garden-Editor').exists()

def string2list(string):
    """ Utility: convert list in string form to a list """
    # print('string: ', string)
    temp = string
    temp = temp.replace("[", "")
    temp = temp.replace("'", "")
    temp = temp.replace("]", "")
    temp = temp.split(", ")
    return(temp)

def string_display(string):
    """ Utility: formal string for display """
    temp = string
    temp = temp.replace("[", "")
    temp = temp.replace("'", "")
    temp = temp.replace("]", "")
    return(temp)

def pH_check(target, lower_limit, upper_limit):
    if (target == "Any"):
        hit = True
    elif ((lower_limit == 'tbd') or (upper_limit == 'tbd')):
        hit = False
    elif ((target >= lower_limit) and (target <= upper_limit)):
        hit = True
    else:
        hit = False
    return(hit)

def usda_zone_check(target, lower_limit, upper_limit):
    if target == "Any":
        hit = True
    elif (target.find("a") == 1 or target.find("b")== 1):
        target_adj = "0" + target
    else:
        target_adj = target

    if lower_limit == "tbd":
        lower_limit_adj = "00a"
    elif (lower_limit.find("a") == 1 or lower_limit.find("b")== 1):
        lower_limit_adj = "0" + lower_limit[0:2]
    else:
        lower_limit_adj = lower_limit[0:3]

    if upper_limit == "tbd":
        upper_limit_adj = "99b"
    elif (upper_limit.find("a") == 1 or upper_limit.find("b")== 1):
        upper_limit_adj = "0" + upper_limit[0:2]
    else:
        upper_limit_adj = upper_limit[0:3]

    if (target == "Any"):
        hit = True
    elif (target_adj >= lower_limit_adj) and (target_adj <= upper_limit_adj):
        hit = True
    else:
        hit = False
    return(hit)

def sunset_zone_check(target, range, options):
    zone_list =[]
    if target == "Any":
        hit = True
    elif range == "tbd":
        hit = False
    else:
        # Convert range into a list of single zones or ranges of zones (form of x-y)
        temp_1 = range.strip()
        temp_2 = temp_1.replace(",", "")
        range_adj = temp_2.split()
        # Convert the list into a list of single zones
        for x in range_adj:
            if "-" in x:
                partition = x.partition("-")
                subrange_start = partition[0]
                subrange_end   = partition[2]
                # Search for the subrange starting zone in the complete list of zones
                # Once the subrange starting zone has been found, search for the subrange end zone
                subrange_start_found = False
                for zone in options:
                    if (subrange_start_found == False) and (subrange_start == zone):
                        zone_list.append(zone)
                        subrange_start_found = True
                    elif (subrange_start_found == True) and (subrange_end != zone):
                        zone_list.append(zone)
                    elif (subrange_start_found == True) and (subrange_end == zone):
                        zone_list.append(zone)
                        break
            else:
                zone_list.append(x)
        # Check to determine is target is contained in the list
        if (target in zone_list):
            hit = True
        else:
            hit = False
    return(hit)

def bloom_month_check(target, start, end, options):
    options_2x = options + options
    if (target == "Any"):
        hit = True
    elif (start == "tbd") or (start == "None") or (end == "tbd") or (end == "None"):
        hit = False
    else:
        begin = False
        for option in options_2x:
            if option == start:
                begin = True
                countdown = 12
            if begin == True:
                if target == option:
                    hit = True
                    return(hit)
                else:
                    countdown = countdown - 1
                if option == end or countdown == 0:
                    hit = False
                    return(hit)
    return(hit)

def bloom_month_list(start, end, options):
    options_2x = options + options
    list = []
    if (start == "tbd") or (start == "None") or (end == "tbd") or (end == "None"):
       return(list)
    begin = False
    for option in options_2x:
        if option == start:
            begin = True
        if begin:
            list.append(option)
        if begin and option == end:
            return(list)

def DEBUG_print_request(request):
    """ Utility: print contents of HTTP Request to console """
    print(f"================================================================")  
    print(f"INFO: Print HTTP request")  
    print(f"================================================================")  
    print(f"Request Path:           {request.path}")
    print(f"Request Method:         {request.method}")
    if(request.method == 'GET'):
        print(f"Request GET Parameters: {request.GET}")
    if request.method == 'POST':
        print(f"Request POST Parameters:")
        max_length = 0
        for key in request.POST:
            max_length = max(max_length, len(key))
        for key in request.POST:
            value = request.POST.getlist(key)
            spaces_to_align = max_length - len(key)
            print(f"  Key: {key} {" "*spaces_to_align} Value: {value}")
            # use following print command to also list the type of the value
            # print(f"Key: {key} {" "*spaces_to_align} Value: {value} Type: {type(value)}")
    print(f"================================================================") 
    # For more complex data structures like request.META, use pprint
    # print("Request META data:")
    # pp = pprint.PrettyPrinter(indent=4)
    # print(pp.pformat(request.META))
    # print(f"================================================================")  
    return()