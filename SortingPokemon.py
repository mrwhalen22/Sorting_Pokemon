# Pokemon Sorting Assignment 1
# BY: Matthew Whalen

from cProfile import label
import sys
import os
from typing import Tuple
from matplotlib import pyplot as plt


def insertion_sort(data) -> int:
    count = 0
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while((j >= 0 and data[j][1] > key[1]) or (data[j][1] == key[1] and data[j][0] > key[0])):
            data[j+1] = data[j]
            j-=1
            count += 1
        data[j+1] = key
    return count

def merge_sort(data) -> int:
    count = 0
    if(len(data) > 1):
        mid = len(data)//2
        L = data[:mid]
        R = data[mid:]
  
        count += merge_sort(L)
        count += merge_sort(R)
  
        i = j = k = 0
  
        while(i < len(L) and j < len(R)):
            count+=1
            if((L[i][1] < R[j][1]) or (L[i][1] == R[j][1] and L[i][0] < R[j][0])):
                data[k] = L[i]
                i += 1
            else:
                data[k] = R[j]
                j += 1
            k += 1

        while(i < len(L)):
            count+=1
            data[k] = L[i]
            i += 1
            k += 1
  
        while(j < len(R)):
            count+=1
            data[k] = R[j]
            j += 1
            k += 1
    return count

def partition(data, begin, end) -> Tuple[int, int]:
    count = 0
    j = begin-1
    pivot = data[end]
    
    for i in range(begin, end):
        if((data[i][1] < pivot[1]) or ((data[i][1] == pivot[1]) and  (data[i][0] < pivot[0]))):
            count+=1
            j+=1
            data[i], data[j] = data[j], data[i]
    data[j+1], data[end] = data[end], data[j+1]
    return j+1, count

def quick_sort(data, begin, end) -> int:
    count = 0
    if( begin < end):
        result = partition(data, begin, end)
        div = result[0]
        count += result[1]
        count += quick_sort(data, begin, div-1)
        count += quick_sort(data, div+1, end)
    return count

def isSorted(data) -> bool:
    for i in range(len(data)-1):
        if(data[i][1] > data[i+1][1]):
            print(data[i], data[i+1])
            return False
        elif(data[i][1] == data[i+1][1] and data[i][0] > data[i+1][0]):
            print(data[i], data[i+1])
            return False
    return True

def main() -> int:
    #CHECK FOR ARGUMENTS
    options = sys.argv
    if(len(options) >= 2):
        if(options[1].upper() != "MERGE" and options[1].upper() != "INSERTION" and options[1].upper() != "QUICK"):
            print("Usage: " + sys.argv[0] + " <Sort Type>(Merge, Insertion, Quick)")
            return 0

    #INIT VARS AND PARSE CSV FILENAMES    
    pokemon_data = {}
    sort_counts = {}
    csv_files = list(filter(lambda x: ".csv" in x, os.listdir("./"))) 
    
    # READ IN CSV FILE DATA
    for filename in csv_files:
        file = open(filename, "r")
        data = file.readlines()
        data.pop(0)
        for i in range(len(data)):
            data[i] = data[i].rstrip("\n")
            data[i] = data[i].split(",")
            data[i][1] = int(data[i][1])
        pokemon_data[filename] = data
        file.close()
                     
    #SORT ALL DATA LISTS
    if(len(options) == 1):
        # INSERTION SORT BY DEFAULT
        print("Sorting with Insertion Sort. Please give an option for other sorting methods.")
        for file in csv_files:
            sort_counts[file] = insertion_sort(pokemon_data[file])
            if(isSorted(pokemon_data[file])): print(file + ": SUCCESS")
            else: print(file + ": FAILURE")
    elif(options[1].upper() == "INSERTION"):
        # USE INSERTION SORT
        print("Sorting with Insertion Sort.")
        for file in csv_files:
            sort_counts[file] = insertion_sort(pokemon_data[file])
            if(isSorted(pokemon_data[file])): print(file + ": SUCCESS")
            else: print(file + ": FAILURE")
    elif(options[1].upper() == "MERGE"):
        # USE MERGE SORT
        print("Sorting using Merge Sort.")
        for file in csv_files:
            sort_counts[file] = merge_sort(pokemon_data[file])
            if(isSorted(pokemon_data[file])): print(file + ": SUCCESS")
            else: print(file  + ": FAILURE")
    elif(options[1].upper() == "QUICK"):
        # USE QUICK SORT
        print("Sorting using Quick Sort.")
        for file in csv_files:
            sort_counts[file] = quick_sort(pokemon_data[file], 0, len(pokemon_data[file])-1)
            if(isSorted(pokemon_data[file])): print(file + ": SUCCESS")
            else: print(file + ": FAILURE")
    else:
        print("ERROR")
        return -1  

        

    #EXPORT COUNT DATA
    output = open(options[1][0].upper() + "SortCounts.txt","w")
    for file in csv_files:
        output.writelines(("INSERTION" if len(options) < 2 else options[1].upper()) + " SORT " + file + ": number of values = " + str(len(pokemon_data[file])) + ", comparison count = " + str(sort_counts[file]) + "\n")
        #print(("INSERTION" if len(options) < 2 else options[1].upper()) + " SORT " + file + " comparison count: " + str(sort_counts[file]))
    
    print("Data exported to text file.")

    pxRa=[]
    pyRa=[]
    pxRe=[]
    pyRe=[]
    pxS=[]
    pyS=[]
    i = 0
    for file in csv_files:
        if(i < 3):
            pxRa.append(len(pokemon_data[file]))
            pyRa.append(sort_counts[file])
            
        elif(i < 6):
            pxRe.append(len(pokemon_data[file]))
            pyRe.append(sort_counts[file])
        else:
            pxS.append(len(pokemon_data[file]))
            pyS.append(sort_counts[file])
        i+=1
    plt.plot(pxRa,pyRa, label = "Random")
    plt.plot(pxRe,pyRe, label = "Reverse")
    plt.plot(pxS,pyS, label = "Sorted")

    plt.legend()
    plt.xlabel("Number of Values")
    plt.ylabel("Number of Comparisons Made")
    plt.title("Sort Comparisons - " + options[1].upper())

    print("Displaying Graph.")
    plt.show()



    return 1

if __name__ == "__main__":
    sys.exit(main())
