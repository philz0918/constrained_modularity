import sys

if len(sys.argv) < 3:
    print("Usage: python glue.py file1 file2 ...")
else:
    filenames = sys.argv[1:]
    for i in range(0,len(filenames)):
        file = open(filenames[i],"r")
        for line in file:
            print(line, end=' ')
        file.close()
        if i != len(filenames)-1:
            print("-2, []")
