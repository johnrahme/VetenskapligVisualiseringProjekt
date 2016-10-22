import ReadPointsCSV
import vtk
import math
import Tkinter
#from Tkint import  app_tk
#------------------------Start KeyBoard interface------------------------------

class KeyboardInterface(object):
    global size, min_strength
    def __init__(self):
        self.screenshot_counter = 0
        self.day_in_sec = 86400
        self.day_counter = 0        
        self.render_window = None
        self.window2image_filter = None
        self.png_writer = None   
        self.new_strength = vtk.vtkFloatArray()
        self.new_strength.Resize(size)
    def keypress(self, obj, event):
        key = obj.GetKeySym()
        
        if key == "9":
            self.render_window.Render()
            self.window2image_filter.Modified()
            screenshot_filename = ("screenshot%02d.png" %
                                   (self.screenshot_counter))
            self.png_writer.SetFileName(screenshot_filename)
            self.png_writer.Write()
            print("Saved %s" % (screenshot_filename))
            self.screenshot_counter += 1
			
            
        elif key == "Up":
            self.day_counter += 1
            print self.day_counter
            print math.floor((max_time-min_time)/self.day_in_sec) #Last day of data
            if self.day_counter < math.floor((max_time-min_time)/self.day_in_sec):
                threshold_filter.ThresholdBetween(min_time+(self.day_counter-1)*self.day_in_sec,min_time+self.day_counter*self.day_in_sec)	
                threshold_filter.Update()
            else:
                self.day_counter = math.floor((max_time-min_time)/self.day_in_sec)
            self.render_window.Render()
        elif key == "Down":
            self.day_counter -= 1
            print self.day_counter
            if self.day_counter > 0:
                threshold_filter.ThresholdBetween(min_time+(self.day_counter-1)*self.day_in_sec,min_time+self.day_counter*self.day_in_sec)	
                threshold_filter.Update()
            else:
                self.day_counter = 0
            self.render_window.Render()
            
        #Sort out values less than 7 in magnitude
        elif key == "Left":      
            print("left")
            for index in range(size):
                if strength.GetValue(index) < 4:
                    self.new_strength.SetValue(index,0) 
                else:
                    self.new_strength.SetValue(index,strength.GetValue(index))
            self.new_strength.SetName("new_strength")               
            points_polydata.GetPointData().AddArray(self.new_strength)
            points_polydata.GetPointData().SetActiveScalars("new_strength")
            threshold_filter.SetInputData(points_polydata)
            threshold_filter.Update()
            self.render_window.Render()
            
            
        #Sort out values larger than 5 in magnitude           
        elif key == "Right":     
            print("Right")
            for index in range(size):
                if strength.GetValue(index) > 1.5:
                    self.new_strength.SetValue(index,0) 
                else:
                    self.new_strength.SetValue(index,strength.GetValue(index))
            self.new_strength.SetName("new_strength")  
            points_polydata.GetPointData().AddArray(self.new_strength)             
            points_polydata.GetPointData().SetActiveScalars("new_strength")
            threshold_filter.SetInputData(points_polydata)
            threshold_filter.Update()
            self.render_window.Render()
            
        #Redraw all data no matter what magnitude
        elif key == "1":      
            print("1")
            points_polydata.GetPointData().AddArray(strength) 
            points_polydata.GetPointData().SetActiveScalars("strength")
            threshold_filter.SetInputData(points_polydata)
            threshold_filter.Update()
            self.render_window.Render()

#--------------------------End KeyBoard interface------------------------------

#--------------------------GUI start-------------------------------------------

class app_tk(Tkinter.Tk):
    global min_time, max_time, min_strenght, max_strength, size
    
    def __init__(self, parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.running = None
        self.day_in_sec = 86400
        self.day_counter = 0  
        self.initialize()    
        self.new_strength = vtk.vtkFloatArray()
        self.new_strength.Resize(size)
        
    def initialize(self):
        self.grid()
        
        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self, textvariable=self.entryVariable)
#        self.entry.grid(column=3, row=2)
#        self.entry.bind("<Return>", self.OnPressEnter)
#        self.entryVariable.set(u"Enter text here")
        
        self.EndMagnitude = Tkinter.DoubleVar()
        Magmax = Tkinter.Scale(self,label="Maximum magnitude", variable = self.EndMagnitude ,from_=max_strength,to=min_strength,tickinterval=1,resolution=0.1, orient ='vertical')
        Magmax.set(max_strength)
        Magmax.pack()
        Magmax.grid(column=3, row=0)
        
        self.StartMagnitude = Tkinter.DoubleVar() #min_strength
        Magmin = Tkinter.Scale(self,label="Lowest magnitude",variable = self.StartMagnitude, from_=max_strength,to=min_strength,tickinterval=1,resolution=0.1,orient ='vertical')
        Magmin.set(0)
        Magmin.pack()
        Magmin.grid(column=2, row=0)
        
        self.StartTime = Tkinter.DoubleVar() #min_time
        t1 = Tkinter.Scale(self,label="Start time",variable = self.StartTime, from_=0,to=math.floor((max_time-min_time)/self.day_in_sec),tickinterval=50, length=300, orient = 'horizontal')
        t1.set(0)
        t1.pack()
        t1.grid(column=1, row=0)
        
        self.EndTime = Tkinter.DoubleVar() #max_time
        t2 = Tkinter.Scale(self,label="End time",variable = self.EndTime, from_=0,to=math.floor((max_time-min_time)/self.day_in_sec),tickinterval=50, length=300, orient = 'horizontal')
        t2.set(math.floor((max_time-min_time)/self.day_in_sec))
        t2.pack()
        t2.grid(column=1, row=1)
        
        self.Opacity = Tkinter.DoubleVar() #max_time
        t2 = Tkinter.Scale(self,label="Opacity" ,variable = self.Opacity, from_=0,to=100,tickinterval=10, length=200, orient = 'horizontal')
        t2.set(100)
        t2.pack()
        t2.grid(column=1, row=1)
        
        
        button1 = Tkinter.Button(self,text="Update opacity of map in render window", 
                                 command=self.OnMapClick)
        button1.grid(column=1, row=2)

       
        button4 = Tkinter.Button(self,text="Update time in render window", 
                                 command=self.OnTimeClick)
        button4.grid(column=1, row=3)
        
        
        button5 = Tkinter.Button(self,text="Update Magnitude in render window", 
                                 command=self.OnMagnitudeClick)
        button5.grid(column=1, row=4)
    
        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self, textvariable = self.labelVariable, 
                              anchor="w", fg="white", bg="black")
        label.grid(column=3, row=3, columnspan=2, sticky='WE')
        self.labelVariable.set(u"Information")
        
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.resizable(True,True)
        self.update()
        self.geometry(self.geometry())
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
        
    def OnMapClick(self):
        self.labelVariable.set("(Map)")
        self.entry.focus_set()
        self.entry.selection_range(0,Tkinter.END)
        

    
    def OnTimeClick(self):
        self.labelVariable.set(str(self.StartTime.get()) + str(",") + str(self.EndTime.get()) + "(Time in days)")
        self.entry.focus_set()
        self.entry.selection_range(0,Tkinter.END)
        threshold_filter.ThresholdBetween(min_time + (self.StartTime.get()-1)*self.day_in_sec,min_time+self.EndTime.get()*self.day_in_sec)	
        threshold_filter.Update()
        render_window.Render()
        
    
    def OnMagnitudeClick(self):
        #self.labelVariable.set(variablemin, variablemax, "(Magnitude)")
        
        self.labelVariable.set(str(self.StartMagnitude.get()) + str(",") + str(self.EndMagnitude.get()) + "(Magnitude (min,max))")      
        self.entry.focus_set()
        self.entry.selection_range(0,Tkinter.END)
        for index in range(size):
            if (strength.GetValue(index) < self.StartMagnitude.get()) or (strength.GetValue(index) > self.EndMagnitude.get()):
                self.new_strength.SetValue(index,0) 
            else:
                self.new_strength.SetValue(index,strength.GetValue(index))
        self.new_strength.SetName("new_strength")               
        points_polydata.GetPointData().AddArray(self.new_strength)
        points_polydata.GetPointData().SetActiveScalars("new_strength")
        threshold_filter.SetInputData(points_polydata)
        threshold_filter.Update()
        render_window.Render()

    def OnPressEnter(self,event):
        self.labelVariable.set(self.entryVariable.get()+ "(You pressed Enter)")
        #self.entry.focus_set()
        #self.entry.selection_range(0,Tkinter.END)
 
 #--------------------------------GUI end--------------------------------------


#-----------------------Start Create quake glyphs------------------------------

# Load the earthquake data
points, strength, time_, = ReadPointsCSV.readPoints("Quake_data.txt")
min_strength, max_strength = strength.GetRange()
min_time, max_time = time_.GetRange()  # in seconds
size = strength.GetSize()
#print(size)
# Assign unique names to the scalar arrays
strength.SetName("strength")
time_.SetName("time")


points_polydata = vtk.vtkPolyData()
points_polydata.SetPoints(points)
points_polydata.GetPointData().AddArray(strength)
points_polydata.GetPointData().AddArray(time_)
points_polydata.GetPointData().SetActiveScalars("strength")


threshold_filter = vtk.vtkThresholdPoints()
threshold_filter.SetInputData(points_polydata)
threshold_filter.ThresholdBetween(min_time, max_time)
threshold_filter.SetInputArrayToProcess(0, 0, 0, 0, "time")
threshold_filter.Update()


#-------------------------Start ColorTransfer function------------------------- 

ColorTrans = vtk.vtkColorTransferFunction()
ColorTrans.SetColorSpaceToRGB()
ColorTrans.AddRGBPoint(min_strength, 1, 0, 0)
ColorTrans.AddRGBPoint((max_strength-min_strength)/2,1, 1, 1)
ColorTrans.AddRGBPoint(max_strength, 0, 0, 1)

#---------------------------End ColorTransfer function------------------------- 

#-----------------------------Start Create glyphs for quake data---------------
sphere = vtk.vtkSphereSource()

glyph = vtk.vtkGlyph3D()
glyph.SetInputConnection(threshold_filter.GetOutputPort())
glyph.SetSourceConnection(sphere.GetOutputPort())
glyph.ScalingOn()
glyph.SetScaleFactor(5)

glyph_mapper = vtk.vtkPolyDataMapper()
glyph_mapper.SetInputConnection(glyph.GetOutputPort())
glyph_mapper.SetLookupTable(ColorTrans)

glyph_actor = vtk.vtkActor()
glyph_actor.SetMapper(glyph_mapper)

#-----------------------End Create quake glyphs--------------------------------

#-----------------------Start Outline------------------------------------------

outline = vtk.vtkOutlineFilter()
outline.SetInputData(points_polydata)
outline_mapper = vtk.vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())
outline_actor = vtk.vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.SetScale(1)
xmi, xma, ymi, yma, zmi, zma = outline_actor.GetBounds()
print outline_actor.GetBounds()

#-------------------------End Outline------------------------------------------


#----------------------------Background stuff START--------------------------------
jpegfile = "map-italy.jpg"
 
 
# Generate an sphere polydata
image_plane = vtk.vtkPlaneSource()
#sphere.SetThetaResolution(12)
#sphere.SetPhiResolution(12)
 
# Read the image data from a file
reader = vtk.vtkJPEGReader()
reader.SetFileName(jpegfile)
 
# Create texture object
texture = vtk.vtkTexture()

transform = vtk.vtkTransform()
transform.RotateWXYZ(180,0,1,0)
transform.RotateWXYZ(90,0,0,1)

texture.SetTransform(transform)

texture.SetInputConnection(reader.GetOutputPort())
 
# Map texture coordinates
map_to_plane = vtk.vtkTextureMapToPlane()

map_to_plane.SetInputConnection(image_plane.GetOutputPort())
#map_to_sphere.PreventSeamOn()
 
# Create mapper and set the mapped texture as input
mapper = vtk.vtkPolyDataMapper()

mapper.SetInputConnection(map_to_plane.GetOutputPort())
 
# Create actor and set the mapper and the texture
image_actor = vtk.vtkActor()
image_actor.SetMapper(mapper)
image_actor.SetTexture(texture)
scalingFactor = 1200
image_actor.SetOrigin(-xma/2/scalingFactor,-yma/2/scalingFactor,0)
image_actor.SetScale(scalingFactor)
print image_actor.GetBounds()

#----------------------------Background stuff END-------------------------------------

#-----------------------Start ColorBar-----------------------------------------

ColorBar = vtk.vtkScalarBarActor()
ColorBar.SetLookupTable(ColorTrans)
ColorBar.SetOrientationToHorizontal()
ColorBar.SetTitle("Quake magnitude")
ColorBar.SetMaximumWidthInPixels(400)
ColorBar.SetMaximumHeightInPixels(60)
ColorBar.SetTextPosition(200)
ColorBar.SetPosition(0.2 ,0)
ColorBar.SetPosition2(0.7,0.1)

#-----------------------End ColorBar-------------------------------------------

#------------------------Start Renderer----------------------------------------
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.1, 0.1, 0.1)
renderer.AddActor(outline_actor)
renderer.AddActor(glyph_actor)
renderer.AddActor(ColorBar)
renderer.AddActor(image_actor)

# Create a render window
render_window = vtk.vtkRenderWindow()
render_window.SetWindowName("Quake illustration")
render_window.SetSize(500, 500)
render_window.AddRenderer(renderer)

# Create an interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Create a window-to-image filter and a PNG writer that can be used
# to take screenshots
window2image_filter = vtk.vtkWindowToImageFilter()
window2image_filter.SetInput(render_window)
png_writer = vtk.vtkPNGWriter()
png_writer.SetInputConnection(window2image_filter.GetOutputPort())

# Set up the keyboard interface
# Set up the keyboard interface
keyboard_interface = KeyboardInterface()
keyboard_interface.render_window = render_window
keyboard_interface.window2image_filter = window2image_filter
keyboard_interface.png_writer = png_writer

# Connect the keyboard interface to the interactor
interactor.AddObserver("KeyPressEvent", keyboard_interface.keypress)


# Initialize the interactor and start the rendering loop
interactor.Initialize()
render_window.Render()
app = app_tk(None)
app.title('GUI')
while(1):
    app.update()

#,min_time,max_time,min_strength,max_strength

#--------------------------End Renderer----------------------------------------