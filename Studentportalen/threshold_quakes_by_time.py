import ReadPointsCSV
import vtk

#------------------------Start KeyBoard interface------------------------------

class KeyboardInterface(object):
    global size, strength, min_strength
    def __init__(self):
        self.screenshot_counter = 0
        self.day_in_sec = 86400
        self.day_counter = 0        
        self.render_window = None
        self.window2image_filter = None
        self.png_writer = None
        self.new_strength = strength   
        
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
            threshold_filter.ThresholdBetween(min_time+(self.day_counter-1)*self.day_in_sec,min_time+self.day_counter*self.day_in_sec)	
            threshold_filter.Update()
            self.render_window.Render()
        elif key == "Down":
            self.day_counter -= 1
            print self.day_counter
            threshold_filter.ThresholdBetween(min_time+(self.day_counter-1)*self.day_in_sec,min_time+self.day_counter*self.day_in_sec)	
            threshold_filter.Update()
            self.render_window.Render()
        elif key == "Left":      
            self.new_strength = strength
            for index in range(size):
                #print 'strength = ' , self.new_strength[index]
                if self.new_strength.GetValue(index) < 7:
                    self.new_strength.SetValue(index,0) 
            self.new_strength.SetName("new_strength")               
            points_polydata.GetPointData().SetActiveScalars("new_strength")
            threshold_filter.Update()
            self.render_window.Render()
            
        elif key == "Right":      
            self.new_strength = strength
            for index in range(size):
                #print 'strength = ' , self.new_strength[index]
                if self.new_strength.GetValue(index) > 5:
                    self.new_strength.SetValue(index,0) 
            self.new_strength.SetName("new_strength")               
            points_polydata.GetPointData().SetActiveScalars("new_strength")
            threshold_filter.Update()
            self.render_window.Render()
            
        elif key == "1":      
            self.new_strength = strength
            self.new_strength.SetName("new_strength")               
            points_polydata.GetPointData().SetActiveScalars("new_strength")
            threshold_filter.Update()
            self.render_window.Render()

#--------------------------End KeyBoard interface------------------------------

#-----------------------Start Create quake glyphs------------------------------

# Load the earthquake data
points, strength, time_, = ReadPointsCSV.readPoints("Quake_data.txt")
min_strength, max_strength = strength.GetRange()
min_time, max_time = time_.GetRange()  # in seconds
size = strength.GetSize()
print(size)
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

#----------------------------Background stuff (not working atm) START--------------------------------
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

#----------------------------Background stuff END-------------------------------------

#-------------------------Start ColorTransfer function------------------------- 

ColorTrans = vtk.vtkColorTransferFunction()
ColorTrans.SetColorSpaceToRGB()
ColorTrans.AddRGBPoint(min_strength, 1, 0, 0)
ColorTrans.AddRGBPoint((max_strength-min_strength)/2,1, 1, 1)
ColorTrans.AddRGBPoint(max_strength, 0, 0, 1)

#---------------------------End ColorTransfer function------------------------- 

sphere = vtk.vtkSphereSource()

glyph = vtk.vtkGlyph3D()
glyph.SetInputConnection(threshold_filter.GetOutputPort())
glyph.SetSourceConnection(sphere.GetOutputPort())

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

#-------------------------End Outline------------------------------------------

#------------------------Start Renderer----------------------------------------
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.1, 0.1, 0.1)
renderer.AddActor(outline_actor)
renderer.AddActor(glyph_actor)

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
interactor.Start()


#--------------------------End Renderer----------------------------------------