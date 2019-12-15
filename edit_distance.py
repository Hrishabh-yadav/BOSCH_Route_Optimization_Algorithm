import os
def editDistDP(str1, str2, m, n): 
    # Create a table to store results of subproblems 
    dp = [[0 for x in range(n+1)] for x in range(m+1)] 
  
    # Fill d[][] in bottom up manner 
    for i in range(m+1): 
        for j in range(n+1): 
  
            # If first string is empty, only option is to 
            # insert all characters of second string 
            if i == 0: 
                dp[i][j] = j    # Min. operations = j 
  
            # If second string is empty, only option is to 
            # remove all characters of second string 
            elif j == 0: 
                dp[i][j] = i    # Min. operations = i 
  
            # If last characters are same, ignore last char 
            # and recur for remaining string 
            elif str1[i-1] == str2[j-1]: 
                dp[i][j] = dp[i-1][j-1] 
  
            # If last character are different, consider all 
            # possibilities and find minimum 
            else: 
                dp[i][j] = 1 + min(dp[i][j-1],        # Insert 
                                   dp[i-1][j],        # Remove 
                                   dp[i-1][j-1])    # Replace 
  
    return dp[m][n]


def binarySearch(arr, x): 
    l = 0
    r = len(arr)
    x=x.lower()
    ed_list=[]
    mined=40
    while (l <= r): 
        m = l + ((r - l) // 2) 
        wx=arr[m].split()
        wx=wx[0].split('+')
        wxx=""
        for i in range(len(wx)):
            wxx=wxx+" "+wx[i]
        wxx.strip()
        arr[m]=wxx
        
        arr[m]=arr[m].lower().strip()
        
        # Check if x is present at mid 
        if (x == arr[m]):
            return m

        #find edit distance
        else:
            edist = editDistDP(x, arr[m], len(x), len(arr[m]))
            if(edist < mined):
                ed_list=[]
                mined=edist
                ed_list.append(m)
            elif(edist == mined):
                ed_list.append(m)
        # If x greater, ignore left half
        if (x > arr[m]):
            l = m + 1
  
        # If x is smaller, ignore right half 
        else:
            r = m - 1
  
    if(mined>4):
        return -1
    else:
        return ed_list


def checkfunction(word):
    
    file=open('bus_stand_names.txt')
    all_lines=file.readlines()
    x=binarySearch(all_lines,word)
    ans = all_lines[x]
    print(word + " : "+ans) 
    return(x)

if __name__ == "__main__":
	file = open("places.txt",'r')
	all_lines = file.readlines()
	for words in all_lines:
	
		ans = checkfunction(words[:len(words) - 10])
		if(isinstance(ans, int)):
		    if(ans==-1):
		        print("Not found")
		    else:
		        print("FOund at ",ans)
		else:
			print("Similar words at indices:")
			print(ans)