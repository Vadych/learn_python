import os
import tempfile

class File:
    def __init__(self,filename):
        self.filename=filename

    def write(self,str):
        with open(self.filename,"w") as f:
            f.write(str)

    def __str__(self):
        return self.filename
    def __add__(self, other):
        _, new_filename=tempfile.mkstemp(prefix="1",suffix=".txt")
        with open(self.filename,'r') as f:
            str1=f.read()
        with open(other.filename,'r')as f:
            str2=f.read()
        new_file=File(new_filename)
        new_file.write(str1+str2)
        return new_file
    def __iter__(self):
        with open(self.filename,'r') as f:
            self._str =f.readlines()
            self._index =-1
        return self
    def __next__(self):
        self._index +=1
        if self._index==len(self._str):
            raise StopIteration
        return self._str[self._index]



if __name__ == '__main__':
    f1=File(os.path.join(tempfile.gettempdir(), "1.txt"))
    f2=File(os.path.join(tempfile.gettempdir(), "2.txt"))
    f1.write('файл1 стр1\nфайл1 стр2\nфайл1 стр3')
    f2.write('файл2 стр1\nфайл2 стр2\nфайл2 стр3')
    f3=f1+f2
    print (f3)
    for row in f1:
        print(row)