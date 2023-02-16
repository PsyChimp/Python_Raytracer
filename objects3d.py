import math3d
import math
EPSILON=0.00001
class Ray(object):
    def __init__(self,origin,direction):
        self.mOrigin=origin
        self.mDirection=direction.normalized()
    def getPoint(self,t):
        """return a point that is "t" units along the ray"""
        if isinstance(t,int) or isinstance(t,float):
            point=self.mOrigin+t*self.mDirection
            return point
    def draw(self,pygamesurface,drawBall,lineWidth,lineColor,lineSement):
        """draws the ray object on a pygame display. drawBall allows to draw a circle at origin. lineSement is the "length" of our seemingly infinite ray"""

        point=self.mOrigin+lineSement*self.mDirection
        
        pygame.draw.line(pygamesurface,lineColor,(int(self.mOrigin[0]),int(self.mOrigin[1])),(int(point[0]),int(point[1])),lineWidth)
        if drawBall==True:
            pygame.draw.circle(pygamesurface,(250,0,0),(int(self.mOrigin[0]),int(self.mOrigin[1])),10,0)
        else:
            pass
    def getDistanceToPoint(self,point):
        q=point-self.mOrigin
        qPara=((self.mDirection.dot(q))/self.mDirection.magnitude())*self.mDirection
        distance=qPara-q
        return distance.magnitude()

class Camera(object):
    def __init__(self,pos,coi,up,fov,near,surface):
        self.camPos=pos
        self.coiPos=coi
        self.up=up.normalized()
        self.fov=fov
        self.near=near
        self.surface=surface
        self.aspectRatio=self.surface.get_width()/self.surface.get_height()
        self.zAxis=(self.coiPos-self.camPos).normalized()
        self.xAxis=(self.up.cross(self.zAxis)).normalized()
        self.yAxis=(self.zAxis.cross(self.xAxis)).normalized()
        self.vph=2*near*(math.tan(math.radians(self.fov/2)))
        self.vpw=self.aspectRatio*self.vph
        a=self.near*self.zAxis
        b=(self.vph/2)*self.yAxis
        c=-1*(self.vpw/2)*self.xAxis
        self.vpo=self.camPos+a+b+c
    def __str__(self):
        a=(self.camPos)
        b=(self.coiPos)
        c=(self.up)
        d=(self.xAxis)
        e=(self.yAxis)
        f=(self.zAxis)
        g=((str(self.surface.get_width()))+" x "+str((self.surface.get_height()))+" pixels")
        h=(self.aspectRatio)
        i=(str(float(self.fov))+" degrees")
        j=(str(float(self.near))+" world units")
        k=(str(self.vpw)+" x "+str(self.vph)+" world units")
        l=(self.vpo)
        string="\n"+str(a)+"\n"+str(b)+"\n"+str(c)+"\n"+str(d)+"\n"+str(e)+"\n"+str(f)+"\n"+str(g)+"\n"+str(h)+"\n"+str(i)+"\n"+str(j)+"\n"+str(k)+"\n"+str(l)+"\n"
        return string
    def getPixelPos(self,ix,iy):
        w=self.surface.get_width()
        h=self.surface.get_height()
        s=((ix)/(w-1))*self.vpw
        t=((iy)/(h-1))*self.vph
        d=s*self.xAxis
        e=-1*t*self.yAxis
        pixPos=self.vpo+d+e
        return pixPos

class Plane(object):
    def __init__(self,normal,distance,ambient,diffuse,specular,hardness):
        """creates a 3D Plane object. Takes a normal, distance, and color. Normal and color are Vector3s."""
        self.mNormal=normal.normalized()
        self.mDistance=distance
        self.mAmbient=ambient.clamp(0,1)
        self.mDiffuse=diffuse.clamp(0,1)
        self.mSpecular=specular.clamp(0,1)
        self.mHardness=hardness
    def rayIntersection(self,ray):
        if self.mNormal.dot(ray.mDirection)==0:
            return None
        else:
            t=(self.mDistance-ray.mOrigin.dot(self.mNormal))/(self.mNormal.dot(ray.mDirection))
            if t<0:
                return None
            return t
class Sphere(object):
    def __init__(self,center,radius,ambient,diffuse,specular,hardness):
        """creates a 3D Sphere object. Takes a center position, a radius, and a color(Vector)"""
        self.mCenter=center
        self.mRadius=radius
        self.mRadiusSquared=radius**2

        self.mAmbient=ambient.clamp(0,1)
        self.mDiffuse=diffuse.clamp(0,1)
        self.mSpecular=specular.clamp(0,1)
        self.mHardness=hardness
    def rayIntersection(self,ray):
        q=self.mCenter-ray.mOrigin
        paraDist=q.dot(ray.mDirection.normalized())
        if paraDist<0:
            return None
        perpDistSq=((q.magnitudeSquared()-paraDist**2))
        if perpDistSq>self.mRadiusSquared:
            return None
        offset=((self.mRadiusSquared-perpDistSq))**(1/2)
        t=paraDist-offset
        if t<0:
            return None
        return t
class AABB(object):
    def __init__(self,point1,point2,ambient,diffuse,specular,hardness):
        
        if point1[0]<=point2[0]:
            x=point1[0]
            x2=point2[0]
        else:
            x=point2[0]
            x2=point1[0]

        if point1[1]<=point2[1]:
            y=point1[1]
            y2=point2[1]
        else:
            y=point2[1]
            y2=point1[1]

        if point1[2]<=point2[2]:
            z=point1[2]
            z2=point2[2]
        else:
            z=point2[2]
            z2=point1[2]
        self.mMinPoint=math3d.VectorN(x,y,z)
        self.mMaxPoint=math3d.VectorN(x2,y2,z2)

        self.mAmbient=ambient.clamp(0,1)
        self.mDiffuse=diffuse.clamp(0,1)
        self.mSpecular=specular.clamp(0,1)
        self.mHardness=hardness
        u=math3d.VectorN(0,1,0)
        d=math3d.VectorN(0,-1,0)
        r=math3d.VectorN(1,0,0)
        l=math3d.VectorN(-1,0,0)
        b=math3d.VectorN(0,0,1)
        f=math3d.VectorN(0,0,-1)
        self.mFaces=[]
        self.mFaces.append((Plane(u,self.mMaxPoint.dot(u),self.mAmbient,self.mDiffuse,self.mSpecular,self.mHardness)))
        self.mFaces.append((Plane(d,self.mMinPoint.dot(d),self.mAmbient,self.mDiffuse,self.mSpecular,self.mHardness)))
        self.mFaces.append((Plane(r,self.mMaxPoint.dot(r),self.mAmbient,self.mDiffuse,self.mSpecular,self.mHardness)))
        self.mFaces.append((Plane(l,self.mMinPoint.dot(l),self.mAmbient,self.mDiffuse,self.mSpecular,self.mHardness)))
        self.mFaces.append((Plane(b,self.mMaxPoint.dot(b),self.mAmbient,self.mDiffuse,self.mSpecular,self.mHardness)))
        self.mFaces.append((Plane(f,self.mMinPoint.dot(f),self.mAmbient,self.mDiffuse,self.mSpecular,self.mHardness)))
    def rayIntersection(self,ray):
        values=[]
        for obj in self.mFaces:
            if obj.mNormal.dot(ray.mDirection)==0:
                continue
            else:
                t=(obj.mDistance-ray.mOrigin.dot(obj.mNormal))/(obj.mNormal.dot(ray.mDirection))
            if t<0:
                continue
            else:
                point=ray.getPoint(t)
                
                if self.mMinPoint[0]<=point[0]+EPSILON and point[0]<=self.mMaxPoint[0]+EPSILON:
                    if self.mMinPoint[1]<=point[1]+EPSILON and point[1]<=self.mMaxPoint[1]+EPSILON:
                        if self.mMinPoint[2]<=point[2]+EPSILON and point[2]<=self.mMaxPoint[2]+EPSILON:
                            values.append(t)
                
        if len(values)>0:
            return min(values)
        else:
            return None
class Triangle(object):
    def __init__(self,point1,point2,point3,ambient,diffuse,specular,hardness):
        self.mP1=point1
        self.mP2=point2
        self.mP3=point3
        self.mAmbient=ambient
        self.mDiffuse=diffuse
        self.mSpecular=specular
        self.mHardness=hardness
        self.mNormal=((point2-point1).cross(point3-point1)).normalized()
        self.mPlane=(Plane(self.mNormal,(-1*self.mNormal.dot(self.mP1)),ambient,diffuse,specular,hardness))
    def rayIntersection(self,ray):
        t=self.mPlane.rayIntersection(ray)
        if t!=None:
            point=ray.getPoint(t)
            u=self.mP2-self.mP1
            v=self.mP3-self.mP1
class Polymesh(object):
    def __init__(self,obj_fname,offset,scale_factor,ambient,diffuse,specular,hardness):
        self.mVList=[]
        self.mFList=[]
        self.FAreaSq=[]
        self.mAmbient=ambient
        self.mDiffuse=diffuse
        self.mSpecular=specular
        self.mHardness=hardness
        self.mPos=offset
        self.mSFactor=scale_factor
        self.mAABB=self.loadMesh(obj_fname, offset, scale_factor)
    def triangleArea(self, a, b, c):
        v = a - b
        w = c - a
        result = v.cross(w)
        return result.magnitude()
    def loadMesh(self,fname,offset,scale_factor):
        self.mPos=offset
        self.mSFactor=scale_factor
        self.mVList=[]
        self.mFList=[]
        self.mFArea = []
        self.mFNorm = []
        self.mFDVal = []
        minPt = None
        maxPt = None

        fp=open(fname,"r")
        for line in fp:
            elem = line.strip().split(" ")
            if elem[0] == "v":
                v = math3d.VectorN(elem[1], elem[2], elem[3]) * scale_factor + offset
                if minPt == None:
                    minPt = v.copy()
                    maxPt = v.copy()
                else:
                    if v[0] < minPt[0]:         minPt[0] = v[0]
                    if v[1] < minPt[1]:         minPt[1] = v[1]
                    if v[2] < minPt[2]:         minPt[2] = v[2]
                    if v[0] > maxPt[0]:         maxPt[0] = v[0]
                    if v[1] > maxPt[1]:         maxPt[1] = v[1]
                    if v[2] > maxPt[2]:         maxPt[2] = v[2]
                self.mVList.append(v)
            elif elem[0] == "f":
                if len(elem) != 4:
                    raise ValueError("Sorry -- I can only currently handle meshes with all triangles :-(")
                indicies = (int(elem[1]) - 1, int(elem[2]) - 1, int(elem[3]) - 1)
                va = self.mVList[indicies[0]]
                vb = self.mVList[indicies[1]]
                vc = self.mVList[indicies[2]]
                self.mFList.append(indicies)
                self.mFArea.append(self.triangleArea(va, vb, vc))
                self.mFNorm.append((va - vc).cross(vb - vc).normalized())
                self.mFDVal.append(va.dot(self.mFNorm[-1]))
        fp.close()

        return AABB(minPt, maxPt, self.mAmbient,self.mDiffuse,self.mSpecular,self.mHardness)
    def rayIntersection(self,R):
        minT=None
        normal=None
        if self.mAABB.rayIntersection(R)==None:
            return None
        for i in range(len(self.mFList)):
            # Don't consider back-faces
            if self.mFNorm[i].dot(R.mDirection) >= 0:
                continue
            # See where the ray hits the plane (if at all)
            p = Plane(self.mFNorm[i], self.mFDVal[i], self.mAmbient,self.mDiffuse,self.mSpecular,self.mHardness)
            result = p.rayIntersection(R)
            if result != None:
                hitPt = R.getPoint(result)
                # Calculate the barycentric coordinates of this hitPoint within the face
                ba = self.triangleArea(hitPt, self.mVList[self.mFList[i][1]], self.mVList[self.mFList[i][2]])
                bb = self.triangleArea(hitPt, self.mVList[self.mFList[i][0]], self.mVList[self.mFList[i][2]])
                bc = self.triangleArea(hitPt, self.mVList[self.mFList[i][0]], self.mVList[self.mFList[i][1]])
                if self.mFArea[i] - EPSILON <= ba + bb + bc <= self.mFArea[i] + EPSILON:
                    # See if this hit is closer than previous hits
                    if minT == None or result < minT:
                        minT = result
                        normal=self.mFNorm[i]
        if minT==None:
            return None
        else:
            return minT,normal

class Light(object):
    def __init__(self,position,diffuse,specular):
        self.pos=position
        self.mDiffuse=diffuse.clamp(0,1)
        self.mSpecular=specular.clamp(0,1)
