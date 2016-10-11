def test_vtk():
    import vtk
    import Tkinter
    import os
    try:
        from vtkTkRenderWidget import vktTkRenderWidget
    except:
        from vtk.tk.vtkTkRenderWidget import vtkTkRenderWidget

    print "vtk is installed in", os.path.dirname(vtk.__file__)
    print "vtk version", vtk.vtkVersion().GetVTKVersion()

    # Create a sphere source, mapper, and actor
    sphere = vtk.vtkSphereSource()

    sphereMapper = vtk.vtkPolyDataMapper()
    sphereMapper.SetInputConnection(sphere.GetOutputPort())
    sphereMapper.GlobalImmediateModeRenderingOn()
    sphereActor = vtk.vtkLODActor()
    sphereActor.SetMapper(sphereMapper)

    # Create a scaled text actor. 
    # Set the text, font, justification, and properties (bold, italics,
    # etc.).
    textActor = vtk.vtkTextActor()
    textActor.ScaledTextOn()
    textActor.SetDisplayPosition(90, 50)
    textActor.SetInput("Hello VTK!")

    # Set coordinates to match the old vtkScaledTextActor default value
    textActor.GetPosition2Coordinate().SetCoordinateSystemToNormalizedViewport()
    textActor.GetPosition2Coordinate().SetValue(0.6, 0.1)

    tprop = textActor.GetTextProperty()
    tprop.SetFontSize(24)
    tprop.SetFontFamilyToArial()
    tprop.SetJustificationToCentered()
    tprop.BoldOn()
    tprop.ItalicOn()
    tprop.ShadowOn()
    tprop.SetColor(0, 0, 1)

    # Create the Renderer, RenderWindow, RenderWindowInteractor
    master = Tkinter.Tk()
    master.withdraw()
    root = Tkinter.Toplevel(master)
    root.title("Hello VTK!")
    def close(event=None):
        root.withdraw()
    root.bind("<KeyPress-q>", close)
    frame = Tkinter.Frame(root, relief='sunken', bd=2)
    frame.pack(side='top', fill='both', expand=1)
    tkw = vtkTkRenderWidget(frame, width=320, height=240)
    tkw.pack(expand='true', fill='both')
    
    ren = vtk.vtkRenderer()
    renwin = tkw.GetRenderWindow()
    renwin.AddRenderer(ren)

    # Add the actors to the renderer; set the background and size; zoom
    # in; and render.
    ren.AddActor2D(textActor)
    ren.AddActor(sphereActor)

    ren.SetBackground(1, 1, 1)
    ren.ResetCamera()
    ren.GetActiveCamera().Zoom(1.5)

    root.update()
    renwin.Render()

    wait()
test_vtk()