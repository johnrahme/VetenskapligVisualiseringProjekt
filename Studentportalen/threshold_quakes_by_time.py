import ReadPointsCSV
import vtk


# Define a class for the keyboard interface
class KeyboardInterface(object):
    """Keyboard interface.

    Provides a simple keyboard interface for interaction. You may
    extend this interface with keyboard shortcuts for, e.g., moving
    the slice plane(s) or manipulating the streamline seedpoints.

    """

    def __init__(self):
        self.screenshot_counter = 0
        #self.level_depth = 7
        self.render_window = None
        self.window2image_filter = None
        self.png_writer = None
        # Add the extra attributes you need here...

    def keypress(self, obj, event):
        """This function captures keypress events and defines actions for
        keyboard shortcuts."""
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
            threshold_filter.ThresholdBetween((max_time-min_time)/3,(max_time-min_time)/2)
            self.render_window.Render()
          
            
        # elif key == "Down":
            # if self.level_depth > 1:
                # self.level_depth = self.level_depth-1
                # planes.SetExtent(0,W,0,H,self.level_depth,self.level_depth)
                # print(self.level_depth)
                # self.render_window.Render()

# Load the earthquake data
points, strength, time_, = ReadPointsCSV.readPoints("Quake_data.txt")
min_strength, max_strength = strength.GetRange()
min_time, max_time = time_.GetRange()  # in seconds

# Assign unique names to the scalar arrays
strength.SetName("strength")
time_.SetName("time")

# Create a vtkPolyData object from the earthquake data and specify
# that "strength" should be the active scalar array
points_polydata = vtk.vtkPolyData()
points_polydata.SetPoints(points)
points_polydata.GetPointData().AddArray(strength)
points_polydata.GetPointData().AddArray(time_)
points_polydata.GetPointData().SetActiveScalars("strength")

# Threshold the earthquake points to extract all points within a
# specified time interval.
#
# If you do not specify which input array to process, i.e., if you
# comment out the SetInputArrayToProcess() call, the thresholding will
# be performed on the active scalar array ("strength", in this case).
threshold_filter = vtk.vtkThresholdPoints()
threshold_filter.SetInputData(points_polydata)
threshold_filter.ThresholdBetween(min_time, max_time)
threshold_filter.SetInputArrayToProcess(0, 0, 0, 0, "time")
threshold_filter.Update()

# Connect the output of the threshold filter to a vtkGlyph3D filter
# and proceed with the visualization!

ColorTrans = vtk.vtkColorTransferFunction()
ColorTrans.SetColorSpaceToRGB()
ColorTrans.AddRGBPoint(min_strength, 1, 0, 0)
ColorTrans.AddRGBPoint((max_strength-min_strength)/2,1, 1, 1)
ColorTrans.AddRGBPoint(max_strength, 0, 0, 1)

outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(threshold_filter.GetOutputPort())
outline_mapper = vtk.vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())
outline_actor = vtk.vtkActor()
outline_actor.SetMapper(outline_mapper)

sphere = vtk.vtkSphereSource()

glyph = vtk.vtkGlyph3D()
glyph.SetInputConnection(threshold_filter.GetOutputPort())
glyph.SetSourceConnection(sphere.GetOutputPort())

glyph_mapper = vtk.vtkPolyDataMapper()
glyph_mapper.SetInputConnection(glyph.GetOutputPort())
glyph_mapper.SetLookupTable(ColorTrans)

glyph_actor = vtk.vtkActor()
glyph_actor.SetMapper(glyph_mapper)


renderer = vtk.vtkRenderer()
renderer.SetBackground(0, 0, 0)
renderer.AddActor(outline_actor)
renderer.AddActor(glyph_actor)
#renderer.AddActor(tubes_actor)
#renderer.AddActor(legendBar)

# Create a render window
render_window = vtk.vtkRenderWindow()
render_window.SetWindowName("Molecular dynamics")
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