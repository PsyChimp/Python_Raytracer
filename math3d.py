#Brandon Hofmann
#ETGG 1803.01
#2/17/2016
import math
class VectorN(object):
    def __init__(self,*other_args):
        self.__mData=[]
        for value in other_args:
            self.__mData.append(float(value))
        self.__mDim=len(self.__mData)
    def __str__(self):
        string="<Vector"+str(len(self.__mData))+": "
        for i in range(len(self.__mData)):
            if i==len(self.__mData)-1:
                string+=(str(float(self.__mData[i])))
            else:
                string+=(str(float(self.__mData[i]))+", ")
                
        string+=">"
        return string
    def __len__(self):
        return self.__mDim
    def __getitem__(self,index):
        return self.__mData[index]
    def __setitem__(self,index,value):
        self.__mData[index]=float(value)
        
    def copy(self):
        """returns a vector that is a copy of self"""
        c=VectorN()
        for x in range(0,len(self.__mData)):
            c.__mData.append(0)    
        for i in range(0,len(self.__mData)):
            c.__mData[i]=self.__mData[i]
        return c
    def __eq__(self,rhs):
        """checks if two vectors are equal and returns result"""
        if isinstance(rhs,VectorN)==True and len(self.__mData)==len(rhs.__mData):
            for i in range(len(rhs.__mData)):
                if (self.__mData[i])!=(rhs.__mData[i]):
                 return False

            return True
        return False
    def int(self):
        """returns a tuple of the vector data of self as an integer"""
        tup=[]
        for x in self.__mData:
            x=int(x)
            tup.append(x)
        t=tuple(tup)
        return t
    def __add__(self,rhs):
        """adds two vectors together"""
        if isinstance(rhs,VectorN)==True and len(self.__mData)==len(rhs.__mData):
            newvector=VectorN()
            for x in range(0,len(self.__mData)):
                newvector.__mData.append(0)
            
            for i in range(0,len(self.__mData)):
                newvector.__mData[i]=self.__mData[i]+rhs.__mData[i]
            return newvector
        raise ValueError("You can only add another Vector"+str(len(self.__mData))+" to this Vector"+str(len(self.__mData))+"."+" (you passed "+"'"+str(rhs)+"'"+")") 
    def __sub__(self,rhs):
        """subtract one vector from another"""
        if isinstance(rhs,VectorN)==True and len(self.__mData)==len(rhs.__mData):
            newvector=VectorN()
            for x in range(0,len(self.__mData)):
                newvector.__mData.append(0)
            
            for i in range(0,len(self.__mData)):
                newvector.__mData[i]=self.__mData[i]-rhs.__mData[i]
            return newvector
        raise ValueError("You can only subtract another Vector"+str(len(self.__mData))+" from this Vector"+str(len(self.__mData))+"."+" (you passed "+"'"+str(rhs)+"'"+")")
    def __mul__(self,rhs):
        """multiplies a vector by a number, or a matrix"""
        if isinstance(rhs,int)==True:
            newvector=VectorN()
            for x in range(0,len(self.__mData)):
                newvector.__mData.append(0)
            
            for i in range(0,len(self.__mData)):
                newvector.__mData[i]=self.__mData[i]*rhs
            return newvector
        if isinstance(rhs,float)==True:
            newvector=VectorN()
            for x in range(0,len(self.__mData)):
                newvector.__mData.append(0)
            
            for i in range(0,len(self.__mData)):
                newvector.__mData[i]=self.__mData[i]*rhs
            return newvector
        if isinstance(rhs,MatrixN)==True:
            newValues=[]
            i=0
            for vector in (rhs.transpose()).vectors:
                newValues.append(vector.dot(self))
            return VectorN(*newValues)
                
                        
        raise ValueError("You can only multiply Vector"+str(len(self.__mData))+" and a scalar, or matrix. \n\tYou attempted to multiply by \'"+str(rhs)+"\'.")
    def __rmul__(self,lhs):
        if isinstance(lhs,int)==True:
            newvector=VectorN()
            for x in range(0,len(self.__mData)):
                newvector.__mData.append(0)
            
            for i in range(0,len(self.__mData)):
                newvector.__mData[i]=self.__mData[i]*lhs
            return newvector
        if isinstance(lhs,float)==True:
            newvector=VectorN()
            for x in range(0,len(self.__mData)):
                newvector.__mData.append(0)
            
            for i in range(0,len(self.__mData)):
                newvector.__mData[i]=self.__mData[i]*lhs
            return newvector

        raise ValueError("You can only multiply Vector"+str(len(self.__mData))+" and a scalar. \n\tYou attempted to multiply by \'"+str(lhs)+"\'.")
    def __truediv__(self,rhs):
        """divides a vector by a number"""
        if isinstance(rhs,int)==True:
            newvector=VectorN()
            for x in range(0,len(self.__mData)):
                newvector.__mData.append(0)
            
            for i in range(0,len(self.__mData)):
                newvector.__mData[i]=self.__mData[i]/rhs
            return newvector
        if isinstance(rhs,float)==True:
            newvector=VectorN()
            for x in range(0,len(self.__mData)):
                newvector.__mData.append(0)
            
            for i in range(0,len(self.__mData)):
                newvector.__mData[i]=self.__mData[i]/rhs

            return newvector
        raise ValueError("You can only divide Vector"+str(len(self.__mData))+" by a scalar. \n\tYou attempted to divide by \'"+str(rhs)+"\'.")
    def __neg__(self):
        """returns a negative vector of self
        i.e. multiplies vector by -1"""
        newvector=VectorN()
        for x in range(0,len(self.__mData)):
            newvector.__mData.append(0)
            
        for i in range(0,len(self.__mData)):
            newvector.__mData[i]=self.__mData[i]*-1
        return newvector
    def magnitude(self):
        """returns magnitude of vector self, using pythagorean theorem"""
        magnitude=0
        for i in range(0,len(self.__mData)):
            magnitude+=self.__mData[i]**2
        magnitude**=1/2
        return magnitude
    def magnitudeSquared(self):
        """retruns magnitude squared of vector"""
        magnitude_squared=0
        for i in range(0,len(self.__mData)):
            magnitude_squared+=self.__mData[i]**2
        return magnitude_squared
    def normalized(self):
        """returns a normalized version of vector self
        i.e. transforms vector into a vector with the same direction, but magnitude of 1.0"""
        if(self.magnitude() == 0):
            return self
        newvector=VectorN()
        for x in range(0,len(self.__mData)):
            newvector.__mData.append(0)
        for i in range(0,len(self.__mData)):
            newvector.__mData[i]=self.__mData[i]/self.magnitude()
        return newvector
    def isZero(self):
        """checks if vector self has zeroes for any data and returns result"""
        for i in range(0,len(self.__mData)):
            if self.__mData[i]==0:
                return True
        return False
    def dot(self,rhs):
        """provides the dotproduct of two vectors"""
        if isinstance(rhs,VectorN) and len(self.__mData)==len(rhs.__mData):
            dotproduct=0
            for i in range(0,len(rhs.__mData)):
                dotproduct+=self.__mData[i]*rhs.__mData[i]
        return dotproduct
    def cross(self,rhs):
        """provides the crossproduct of two vectors (must be 3-Dimensional)"""
        if isinstance(rhs,VectorN) and len(self.__mData)==3 and len(rhs.__mData)==3:
            d1=(self.__mData[1]*rhs.__mData[2]-self.__mData[2]*rhs.__mData[1])
            d2=(self.__mData[2]*rhs.__mData[0]-self.__mData[0]*rhs.__mData[2])
            d3=(self.__mData[0]*rhs.__mData[1]-self.__mData[1]*rhs.__mData[0])
            crossproduct=VectorN(d1,d2,d3)
            return crossproduct
    def pairwise_mult(self,rhs):
        """provides the pairwise multiplication of two vectors"""
        if isinstance(self,VectorN):
            if isinstance(rhs,VectorN):
                if len(self)==len(rhs):
                    result=[]
                    for i in range(0,3):
                        result.append(self[i]*rhs[i])
                    return VectorN(*result)
                else:
                    raise ValueError("You can only use Pairwise with two Vectors with an equal number of dimensions")
        else:
            raise ValueError("Pairwise only accepts two Vectors with an equal number of dimensions")
    def clamp(self,low_scalar,high_scalar):
        """Returns a Vector with 'clamped' dimensions. (Adjusts dimensions to be between the two scalars.)"""
        if isinstance(self,VectorN):
            new_values=[]
            for value in self:
                if value<low_scalar:
                    value=low_scalar
                    new_value.append(value)
                if value>high_scalar:
                    value=high_scalar
                    new_values.append(value)
                else:
                    new_values.append(value)
            return VectorN(*new_values)
        else:
            raise ValueError("You can only use the clamp function on a VectorN")

class MatrixN(object):
    def __init__(self,numRows,numCol,numbers=None):
        self.Rows=numRows
        self.Col=numCol
        if numbers==None:
            self.numbers=[]
            
            for i in range(0,self.Rows*self.Col):
                self.numbers.append(0)
        else:
            self.numbers=list(numbers)
        self.vectors=[]
        if len(self.numbers)!=self.Rows*self.Col:
            raise ValueError("You must pass exactly "+str(self.Rows*self.Col)+" to populate this "+str(self.Rows)+"x"+str(self.Col)+" Matrix.")
        for x in range(self.Rows):
            temp=self.numbers[x*self.Col:self.Col+x*self.Col]
            for item in temp:
                if isinstance(item,float)==False:
                    if isinstance(item,str)==True:
                        item=float(item)
                    else:
                        continue
            
            tempVec=VectorN(*temp)
            self.vectors.append(tempVec)

        self.sStrPrecision=None

    def __str__(self):
        for vector in self.vectors:
            if vector is self.vectors[0]:
                line=(("\n")+("/"))
                for value in vector:
                    if value is vector[-1]:
                        if self.sStrPrecision!=None:
                            line+=str(round(value,self.sStrPrecision))+("\ \n")
                        else:
                            line+=str(value)+("\ \n")
                    else:
                        if self.sStrPrecision!=None:
                            line+=str(round(value,self.sStrPrecision))+("  ")
                        else:
                            line+=str(value)+("  ")
                
                string=line
                
            elif vector is self.vectors[-1]:
                line=('\\')
                for value in vector:
                    if value is vector[-1]:
                        if self.sStrPrecision!=None:
                            line+=str(round(value,self.sStrPrecision))+("/")
                        else:
                            line+=str(value)+("/")
                    else:
                        if self.sStrPrecision!=None:
                            line+=str(round(value,self.sStrPrecision))+("  ")
                        else:
                            line+=str(value)+("  ")
                string+=line
            else:
                line=("|")
                for value in vector:
                    if value is vector[-1]:
                        if self.sStrPrecision!=None:
                            line+=str(round(value,self.sStrPrecision))+("| \n")
                        else:
                            line+=str(value)+("| \n")
                    else:
                        if self.sStrPrecision!=None:
                            line+=str(round(value,self.sStrPrecision))+("  ")
                        else:
                            line+=str(value)+("  ")
                string+=line
        
        return string+("\n")
    def __getitem__(self,index):
        index=tuple(index)
        for vector in self.vectors:
            if vector is self.vectors[index[0]]:
                return vector[index[1]]
    def __setitem__(self,index,value):
        index=tuple(index)
        for vector in self.vectors:
            if vector is self.vectors[index[0]]:
                vector[index[1]]=float(value)
    def copy(self):
        """creates a copy of self, and return it"""
        x=MatrixN(self.Rows,self.Col,self.numbers)
        return x
    def getRow(self,index):
        """returns a specific row, as a vector"""
        for vector in self.vectors:
            if vector is self.vectors[index]:
                return vector
            else:
                raise IndexError("No such Row exists")
    def getCol(self,index):
        """returns a specific column, as a vector"""
        x=self.transpose()
        for vector in x.vectors:
            if vector is self.vectors[index]:
                return vector
            else:
                raise IndexError("No such Column exists")
    def setRow(self,index,newVector):
        """allows you to set a specific row"""
        for vector in self.vectors:
            if vector is self.vectors[index]:
                if len(vector)==len(newVector):
                    self.vectors[index]=newVector
                else:
                    raise ValueError("newVector must have a VectorN of size "+str(len(vector)))
    def setColumn(self,index,newVector):
        """allows you to set a specific column"""
        x=0
        for vector in self.vectors:
            for value in vector:
                if value is vector[index]:
                    value=newVector[x]
                    self.vectors[x][index]=value
                    x+=1
    def transpose(self):
        """'tilts' the matrix i.e., converts the rows into columns and columns into rows"""
        a=self.Col
        b=self.Rows
        c=[]
        for i in range(0,self.Col):
            for vector in self.vectors:
                c.append(vector[i])
        x=MatrixN(a,b,(c))
        return x
    def __mul__(self,rhs):
        if isinstance(rhs,int)==True or isinstance(rhs,float)==True:
            a=self.Rows
            b=self.Col
            c=[]
            d=0
            for vector in self.vectors:
                c.append(vector*rhs)

            x=self.copy()
            x.vectors=c
            return x
        if isinstance(rhs,VectorN)==True:
            newValues=[]
            for vector in self.vectors:
                newValues.append(vector.dot(rhs))
            
            newVector=VectorN(*newValues)
            return newVector
        if isinstance(rhs,MatrixN)==True:
            if self.Col==rhs.Rows:
                new_values=[]
                t_mat=rhs.transpose()
                for vector in self.vectors:
                    for vector2 in t_mat.vectors:
                        new_values.append(vector.dot(vector2))
                
                result=MatrixN(self.Rows,rhs.Col,(new_values))
                return result
        else:
            raise ValueError("you can only multiply this matrix with an integer, float, or vector")
    def __rmul__(self,lhs):
        if isinstance(lhs,int)==True or isinstance(lhs,float)==True:
            a=self.Rows
            b=self.Col
            c=[]
            d=0
            for vector in self.vectors:
                c.append(vector*lhs)
            x=self.copy()
            x.vectors=c
            return x
        else:
            raise ValueError("you can only multiply this matrix with an integer, float, or vector")

def Translate(trans_vector,left=True):
    """returns a 4x4 translation matrix, if right-handed system, set 'left' to False"""
    result=(MatrixN(4,4,(1,0,0,0,0,1,0,0,0,0,1,0,trans_vector[0],trans_vector[1],trans_vector[2],1)))
    if left==False:
        return result.transpose()
    else:
        return result
def Scale(scale_vector,left=True):
    """returns a 4x4 scale matrix, if right-handed system, set 'left' to False"""
    result=(MatrixN(4,4,(scale_vector[0],0,0,0,0,scale_vector[1],0,0,0,0,scale_vector[2],0,0,0,0,1)))
    if left==False:
        return result.transpose()
    else:
        return result
def RotX(angle,left=True):
    """returns a 4x4 rotation matrix, if right-handed system, set 'left' to False"""
    result=(MatrixN(4,4,(1,0,0,0,0,math.cos(math.radians(angle)),math.sin(math.radians(angle)),0,0,-1*math.sin(math.radians(angle)),math.cos(math.radians(angle)),0,0,0,0,1)))
    if left==False:
        return result.transpose()
    else:
        return result
def RotY(angle,left=True):
    """returns a 4x4 rotation matrix, if right-handed system, set 'left' to False"""
    result=(MatrixN(4,4,(math.cos(math.radians(angle)),0,-1*math.sin(math.radians(angle)),0,0,1,0,0,math.sin(math.radians(angle)),0,math.cos(math.radians(angle)),0,0,0,0,1)))
    if left==False:
        return result.trasnpose()
    else:
        return result
def RotZ(angle,left=True):
    """returns a 4x4 rotation matrix, if right-handed system, set 'left' to False"""
    result=(MatrixN(4,4,(math.cos(math.radians(angle)),math.sin(math.radians(angle)),0,0,-1*math.sin(math.radians(angle)),math.cos(math.radians(angle)),0,0,0,0,1,0,0,0,0,1)))
    if left==False:
        return result.transpose()
    else:
        return result
def Identity(size):
    stuff=[]
    for i in range(0,size-1):
        stuff.append(1)
        for x in range(0,size):
            stuff.append(0)
    stuff.append(1)
    
    result=MatrixN(size,size,stuff)
    return result
    
