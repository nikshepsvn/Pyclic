#importing necassary dependencies
import urllib.request, json, requests

#wrapper function that calls all the necassary functions to generate object of valid and invalid menus
def getValidAndInvalidMenus(url, challengeid=1): #defaulting challegeid to be 1
    objOfValidAndInvalidMenus = {} #initializing object
    objOfValidAndInvalidMenus["valid_menus"] = [] #initializing valid_menus array in object as empty
    objOfValidAndInvalidMenus["invalid_menus"] = [] #initializing invalid_menus array in object as empty
    data = getAllMenuData(url, challengeid) #getting all json menu data
    listOfRootMenus = getListOfRootMenus(data) #getting list of 'roots', ie. challenges without any parents
    for num in listOfRootMenus:
        childrenOfCurrentNum = getAllChildMembers(data, num) #getting all children of that root
        if(classifyIfMenuIsValidOrNot(num, childrenOfCurrentNum)): #if children of the root doesn't have the root itself then it is not cyclic and hence valid
            objOfValidAndInvalidMenus["valid_menus"].append({"root_id": num, "children": childrenOfCurrentNum})
        else: #if children contain root itself then invalid
            objOfValidAndInvalidMenus["invalid_menus"].append({"root_id": num, "children": childrenOfCurrentNum})

    return objOfValidAndInvalidMenus

#function gets all json data from all pages of specified challenege
def getAllMenuData(url, challengeid):
    count = 1;
    menudata = []
    while(1):
        result = requests.get(url, {'id':challengeid, 'page':count})
        if result.status_code is not 200:
            print ('Failed to GET data, exiting.')
            exit(1)
        menudata += result.json()["menus"]
        pageNumber = int(result.json()["pagination"]["total"]/result.json()["pagination"]["per_page"]) #calculates the number of pages
        if(count == pageNumber): #breaks the loop when we pull all the data we need
            break;
        count += 1
    return menudata

#function gets list of roots, ie. id's without any parents
def getListOfRootMenus (data):
    parentMenus = []
    for ele in data:
        if(ele.get('parent_id')):
            continue;
        else:
            currentEleID = ele.get('id');
            parentMenus.append(currentEleID)

    return parentMenus

#gets children of given num
def getChildren(data, num):
    listOfChildren = []
    listOfChildrensChildren = []

    for ele in data:
        if(ele.get('id') == num):
            listOfChildren += (ele.get('child_ids'))

    return listOfChildren

#gets all children of given num
def getAllChildMembers(data,num):
    count = 0
    childrenOfNum = getChildren(data, num)
    for child in childrenOfNum:
        childrenOfNum += (getChildren(data,child))
        if(len((getChildren(data,child)))>=1):
            count += 1
        if num in (getChildren(data,child)) or count is 4:
            break;

    return sorted(childrenOfNum, key=int)

#returns true if menu is valid, else returns false
def classifyIfMenuIsValidOrNot(num, childrenOfCurrentNum):
    if num in childrenOfCurrentNum:
        return False
    else:
        return True

if __name__ == "__main__":
    url = "https://backend-challenge-summer-2018.herokuapp.com/challenges.json"

    print("Challenge 1")
    print(getValidAndInvalidMenus(url, 1))
    print()
    print("Challenge 2")
    print(getValidAndInvalidMenus(url, 2))
