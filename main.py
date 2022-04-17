# MINI PROJECT 2

from pymongo import MongoClient 
import re

port = input("port no: ")
myclient = MongoClient("mongodb://localhost:{}/".format(port)) 
db = myclient["291db"]

def intersection(lst1, lst2):
    # took reference from the web for this function
    """
    Function that is used to find the "intersection" of two lists.
    Parameters:
    - lst1 of type 'list'
    - lst2 of type 'list'
    """
    finalList = [value for value in lst1 if value in lst2]
    return finalList

def search_title():
    """
    Function that is used to search for titles of movies.
    This function is the first task of PHASE 2.
    """
    
    number_of_keywords = 'almer karthik shreya'
    
    while type(number_of_keywords) != int:
        try:
            number_of_keywords = int(input("How many keywords do you want to enter? "))
        except:
            pass
    print("\n\n")
    print("-----------------------------------------------------------")       
    keywords = []
    for i in range (number_of_keywords):
        input_string = "Keyword {}: ".format(i+1)
        new_word = input(input_string)
        keywords.append(new_word)
    print(keywords)
    title_coll = db["title_basics"]
    # SEARCHING FROM HERE MONGODB
    
    sum = 0
    count = 1
    for i in range(len(keywords)):
        results = title_coll.find({'primaryTitle': {'$regex': keywords[i], "$options": 'i'}})
        
        for result in results:  
            print("\nRESULT {}:".format(count))
            count+=1
           
            for key, value in result.items():
                print(key, ' : ', value)
    
    for i in range(len(keywords)):
        results = title_coll.find({'startYear': {'$regex': keywords[i]}})

        for result in results:  
            print("\nRESULT {}:".format(count))
            count+=1
           
            for key, value in result.items():
                print(key, ' : ', value)

    # The user should be able to select a title to see the rating, 
    # the number of votes, the names of cast/crew members and their characters (if any).
    
    
    print("-----------------------------------------------------------")
    print("\n\n")
    movie_option = input("Enter a movie title: ")
    movie_option = movie_option.title()
    results = title_coll.find({'primaryTitle': {'$regex': movie_option}})
    
    

    result_dict = {}

    for st in results:
        if st["primaryTitle"] == movie_option:
            result_dict[st["primaryTitle"]] = st["tconst"]
          
    tconst = result_dict[movie_option]
    print("You have selected the movie ", movie_option, " with tconst value = ", tconst,".")


    title_ratings_coll = db["title_ratings"]

    new_results = title_ratings_coll.find({'tconst': {'$regex': tconst}})
    new_results_dict = {}
    for st in new_results:
        if st["tconst"] == tconst:
            new_results_dict["averageRating"] = st["averageRating"]
            new_results_dict["numVotes"] = st["numVotes"]
    print("-----------------------------------------------------------")
    print("Average Rating: ",new_results_dict["averageRating"])
    print("Votes: ",new_results_dict["numVotes"])
    print("-----------------------------------------------------------")
   # the names of cast/crew members and their characters (if any)
   
    title_principals_coll = db["title_principals"]
    results = title_principals_coll.find({"tconst": tconst})
    nconstsINtconstDICT = {}

    for result in results:
        nconstsINtconstDICT[result["nconst"]] = result["characters"]

   
    print('\n')
    print(".....Cast/ Crew members and their characters (if any):.....")
    for nconst in nconstsINtconstDICT:
        name_basics_coll = db["name_basics"]
        results = name_basics_coll.find({"nconst": nconst})
        for r in results:
                if nconstsINtconstDICT[nconst] == ['\\N']:
                    print("Name:", r["primaryName"],    "|| Character played: N/A")
                else: 
                    char_played = [nconstsINtconstDICT[nconst][0]]
                    l = char_played[0][2:]
                    print("Name:", r["primaryName"],    "|| Character played:", l[:-2])
    print("\n")

    print("-----------------------------------------------------------")

def search_title2():
    printedList = []
    
    number_of_keywords = 'almer karthik shreya'
    
    while type(number_of_keywords) != int:
        try:
            number_of_keywords = int(input("How many keywords do you want to enter? "))
        except:
            pass
    print("\n\n")        
    keywords = []
    for i in range (number_of_keywords):
        input_string = "Keyword {}: ".format(i+1)
        new_word = input(input_string)
        keywords.append(new_word)
    #print(keywords)

    alphaTitles = []
    

    for k in keywords:
        try:
            x = int(k)
        except ValueError:
            alphaTitles.append(k)

    intsForYear = list(set(keywords) - set(alphaTitles))
    print(alphaTitles)
    print(intsForYear)
    title_coll = db["title_basics"]
    # SEARCHING FROM HERE MONGODB
    printedany = False
    sum = 0
    count = 1
    for i in range(len(keywords)):
        results = title_coll.find({'primaryTitle': {'$regex': keywords[i], "$options": 'i'}})
        
        for result in results:  
            
            
            yes = True
            # check result matching all keywords
            for alphakeyword in keywords:
                if alphakeyword.lower() not in result["primaryTitle"].lower():
                    yes = False

            # check result matching all keywords
            if yes == True and result["tconst"] not in printedList:
                print("\nRESULT {}:".format(count))
                count+=1
                for key, value in result.items():
                    print(key, ' : ', value)
                    printedany = True
                    printedList.append(result["tconst"])
    
    for i in range(len(intsForYear)):
        results = title_coll.find({'startYear': {'$regex': intsForYear[i]}})

        for result in results:  
            print("\nRESULT {}:".format(count))
            printedany = True
           
            for key, value in result.items():
                print(key, ' : ', value)
                count+=1

    # The user should be able to select a title to see the rating, 
    # the number of votes, the names of cast/crew members and their characters (if any).
   
    print("\n\n")
    if printedany == False:
        print("No results!!")
    elif printedany == True:
        movie_option = input("Enter a movie title: ")
        movie_option = movie_option.title()
        results = title_coll.find({'primaryTitle': {'$regex': movie_option}})
        
        #print(results)

        result_dict = {}

        for st in results:
            if st["primaryTitle"] == movie_option:
                result_dict[st["primaryTitle"]] = st["tconst"]
            
        tconst = result_dict[movie_option]
        print("You have selected the movie ", movie_option, " with tconst value = ", tconst,".")

        title_ratings_coll = db["title_ratings"]

        new_results = title_ratings_coll.find({'tconst': {'$regex': tconst}})
        new_results_dict = {}
        for st in new_results:
            if st["tconst"] == tconst:
                new_results_dict["averageRating"] = st["averageRating"]
                new_results_dict["numVotes"] = st["numVotes"]

        print(new_results_dict)
        print("Average Rating: ", new_results_dict['averageRating'])
        print("Number of Votes: ", new_results_dict['numVotes'] )

    # TODO: the names of cast/crew members and their characters (if any)
    # displaying everything other than ^^

    # cast crew members below:

        title_principals_coll = db["title_principals"]
        results = title_principals_coll.find({"tconst": tconst})
        nconstsINtconstDICT = {}

        for result in results:
            nconstsINtconstDICT[result["nconst"]] = result["characters"]

        #print(nconstsINtconstDICT)
        print('\n')
        print(".....Cast/ Crew members and their characters (if any):.....")
        for nconst in nconstsINtconstDICT:
            name_basics_coll = db["name_basics"]
            results = name_basics_coll.find({"nconst": nconst})
            for r in results:
                if nconstsINtconstDICT[nconst] == ['\\N']:
                    print("Name:", r["primaryName"],    "|| Character played: N/A")
                else: 
                    char_played = [nconstsINtconstDICT[nconst][0]]
                    l = char_played[0][2:]
                    print("Name:", r["primaryName"],    "|| Character played:", l[:-2])
        print("\n")
    

   
def search_genres():
    """
    Function that searches for genres of movies. The result is sorted based on the average 
    rating with the highest rating on top.
    This function is the second task of PHASE 2.
    """
    title_basics_coll = db["title_basics"]

    genre= input("Enter a genre: ")

    regx = re.compile(genre, re.IGNORECASE)
    vote= int(input("Enter a minimum vote count: "))


    tconst_genres=[]
    result1 = title_basics_coll.find({"genres":regx})
    for result2 in result1:
       
        tconst_genres.append(result2['tconst'])

    tconst=[]
    title_ratings_coll = db["title_ratings"]
    
    result3= title_ratings_coll.find({"$expr" : {"$gte" : [{"$toInt" :"$numVotes"} , vote]}})
    
    for result4 in result3:
       
        tconst.append(result4['tconst'])

    new_list = intersection(tconst,tconst_genres)
  
    sortingDict = {}
    print("-----------------------------------------------------------")
    title_basics_coll = db["title_basics"]
    titleDict = {}
    for i in range (len(new_list)):
        oneresult = title_basics_coll.find({"tconst": new_list[i] })
        for newresult in oneresult: 
            sortingDict[newresult["tconst"]] = newresult["originalTitle"]
            titleDict[newresult["tconst"]] = newresult["primaryTitle"]


    title_ratings_coll = db["title_ratings"]
    for i in range (len(new_list)):
        oneresult = title_ratings_coll.find({"tconst": new_list[i] })
        for newnewresult in oneresult:  
            sortingDict[newnewresult["tconst"]] = newnewresult["averageRating"]
    

    for key in sortingDict:
        sortingDict[key] = float(sortingDict[key])

    finalDict = sorted(sortingDict.items(), key=lambda x: x[1], reverse=True)
    
    count = 1
    for tconst in finalDict:
        print(count,'.', titleDict[tconst[0]],",",finalDict[count-1][1])
        count+=1
      
    print("-----------------------------------------------------------\n")


def search_mp():
    """
    The function searches for cast/crew members and displays all professions of the member and for each title the member 
    had a job, the primary title, the job and character (if any).
    This function is the third task of PHASE 2.
    """
    mp_name_input = input("cast/crew member name: ")
    mp_name = mp_name_input.title()

    name_basics_coll = db["name_basics"]
    newresults = name_basics_coll.find({"primaryName": mp_name })
    print("Professions")
    print("----------------")
    count = 1
    nconstsLIST = []
    for newresult in newresults:
        
        nconstsLIST.append(newresult["nconst"])
        for ele in newresult["primaryProfession"]:
            print(count, ". ", ele)
            count+=1
    print("\nnconsts are: ", nconstsLIST)
    print("\n")
   
    ## PRINTED PROFESSIONS
    
    for i in range (len(nconstsLIST)):
        count = 1
        title_principals_coll = db["title_principals"]
        newestresults = title_principals_coll.find({"nconst": nconstsLIST[i] })

        nonNullDataSetsDICT = {}
        for result in newestresults:
            
            if result["characters"][0][0] == '[':
                nonNullDataSetsDICT[result["tconst"]]=result["characters"]
            if result["job"][0][0].isalpha() is True:
                nonNullDataSetsDICT[result["tconst"]]=result["job"]

        
        for ele in nonNullDataSetsDICT:
            movie_tconst = ele
            title_basics_coll = db["title_basics"]
            eresult = title_basics_coll.find({"tconst": movie_tconst })
            for elem in eresult:
                pTitle = elem["primaryTitle"]
                
            print(count,". ",movie_tconst,'||',pTitle,'||',nonNullDataSetsDICT[ele][0])
            count += 1
    print("------------------------------------------------\n\n")

def add_movie():
    """
    Function that adds a movie to the database. Both the primary title and the original title 
    is set to the provided title, the title type is set to movie and isAdult and endYear 
    are set to Null .
    This function is the fourth task of PHASE 2.
    """
    
    title_basics_coll = db["title_basics"]
    
    valid = True
    
    id = input("ID: ")
    
    latest_result = title_basics_coll.find({"tconst": id })
    
    for result in latest_result:
        
        if result["tconst"] == id:
            valid = False
            
    if valid is True:
        title = input("Title: ")
        startYear = input("Start Year: ")
        runtime = input("Runtime: ")
        list_of_genres = []
        no_of_genres = int(input("number of genres: "))
        for i in range (no_of_genres):
            inputGenre= input("genre {}: ".format(i+1))
            list_of_genres.append(inputGenre)
        back = "\\N"

        mydict = {"tconst": id, "titleType" :"movie",  "primaryTitle": title, "originalTitle": title, "isAdult": back, "startYear": startYear, "endYear": back, "runtimeMinutes": runtime, "genres": list_of_genres}
        
        title_basics_coll = db["title_basics"]
        title_basics_coll.insert_one(mydict)
        print(".................Added Movie Successfully!...............")
        print("\n")
    else:
        print("\n.................Invalid ID................\n")

def add_mp():
    """
    Function that adds a cast/crew member to the database. The user is able to add a row to title_principals by 
    providing a cast/crew member id, a title id, and a category.
    This function is the fifth task of PHASE 2.
    """
    passValue = 0 

    nconst = input("cast/ crew member id: ")

    name_basics_coll = db["name_basics"]

    try:
        nsresults = name_basics_coll.find({"nconst": nconst })
    except TypeError:
        print("Invalid nconst")

    ralist = []
    for nsresult in nsresults:
        ralist.append(nsresult["nconst"])
    try:
        if ralist[0] == nconst:
            print('nconst exists in name_basics')
            passValue += 1
    except IndexError:    
        print("..\nInvalid nconst..\n..")

    tconst = input("title id: ")
    

    title_basics_coll = db["title_basics"]

    try:
        nresults = title_basics_coll.find({"tconst": tconst })
    except TypeError:
        print("Invalid tconst")

    rlist = []
    for nresult in nresults:
        rlist.append(nresult["tconst"])
    
    try:
        if rlist[0] == tconst:
            print('tconst exists in title_basics')
            passValue +=1

    except IndexError:    
        print("..\nInvalid tconst\n..")
    # ORDERING += 1 PART.............
    
    orderingList = []
    title_principals_coll = db["title_principals"]
    results = title_principals_coll.find({"tconst":tconst})
    for result in results:
        orderingList.append(result["ordering"])

    intsList = []

    for ele in orderingList:
        intsList.append(int(ele))

    ordering = int(max(intsList))+1
    print(ordering)


    # INSERTING PART............
    if passValue == 2:
        category = input("category: ")
        mydict = {"tconst": tconst, "nconst" :nconst,  "category": category, "job": "\\N", "ordering": str(ordering)}
        title_principals_coll = db["title_principals"]
        title_principals_coll.insert_one(mydict)
    else:
        print("..\nInvalid data\n..")

def main():
    """
    MAIN FUNCTION. Calls all the functions so that the program performs the required tasks. 
    Also, displays the options to the user.
    """
    option = 0 
    print("Hello! Welcome to the Document Store! Please choose a valid option:")
    
    while option != 'e':
        print("1. Search for titles ")
        print("2. Search for genres ")
        print("3. Search for cast/crew members  ")
        print("4. Add a movie ")
        print("5. Add a cast/crew member ")
        print("e. exit")
        option = input("Select an option (1-5 / e): ")
        if option == '1':
            search_title()
            #search_title2()
        elif option == '2':
            search_genres()
        elif option == '3':
            search_mp()
        elif option == '4':
            add_movie()
        elif option == '5':
            add_mp()
            print("\n")
        elif option == 'e':
            print("\n......Exiting the Document Store. Goodbye!......\n")
            exit()
        else:
            print("\nInvalid option. Please enter a valid option:\n")

main()