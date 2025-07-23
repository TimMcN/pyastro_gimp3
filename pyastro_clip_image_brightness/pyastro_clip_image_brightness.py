import sys

import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
from gi.repository import Gegl
gi.require_version('GimpUi', '3.0')
from gi.repository import GimpUi
from gi.repository import GLib
from gi.repository import GObject
class pyastro_clip_image_brightness(Gimp.PlugIn):
    def do_query_procedures(self):
        return [ "pyastro-clip-image-brightness" ]

    def do_set_i18n (self, name):
        return False

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(self, name,
                                            Gimp.PDBProcType.PLUGIN,
                                            self.run, None)

        procedure.set_image_types("RGB*")

        procedure.set_menu_label("PyAstro Clip Image Brightness")
        procedure.add_menu_path('<Image>/Py-Astro/Colour Tools/')

        procedure.set_documentation("Clip The Image Brightness",
                                    "Clip the image at a minimum percentage brightness",
                                    name)
        procedure.set_attribution("TM", "TM", "2025")

        procedure.add_double_argument('rclip',
                                    'Red limt', 'Gaussian blur radius (pixels)',
                                       0.0, 100.0, 25.0,
                                      GObject.ParamFlags.READWRITE | GObject.ParamFlags.CONSTRUCT)
        procedure.add_double_argument('gclip',
                                    'Green limt', 'Gaussian blur radius (pixels)',
                                       0.0, 100.0, 25.0,
                                      GObject.ParamFlags.READWRITE | GObject.ParamFlags.CONSTRUCT)
        procedure.add_double_argument('bclip',
                                    'Blue limt', 'Gaussian blur radius (pixels)',
                                       0.0, 100.0, 25.0,
                                      GObject.ParamFlags.READWRITE | GObject.ParamFlags.CONSTRUCT)
        return procedure
    def run(self, procedure, run_mode, image, drawables, config, run_data):
        if run_mode == Gimp.RunMode.INTERACTIVE:
            GimpUi.init("pyastro_clip_image_brightness")
            Gimp.context_push()
            dialog=GimpUi.ProcedureDialog.new(procedure=procedure, config=config)
            dialog.get_widget("rclip", GimpUi.SpinScale)
            dialog.get_widget("gclip", GimpUi.SpinScale)
            dialog.get_widget("bclip", GimpUi.SpinScale)
            
            box = dialog.fill(None)

            if not dialog.run():
                dialog.destroy()
                return procedure.new_return_values(Gimp.PDBStatusType.CANCEL, None)
            else:
                dialog.destroy()
            image.undo_group_start()


            rclip = config.get_property("rclip")
            gclip = config.get_property("gclip")
            bclip = config.get_property("bclip")

            rmax = rclip /100.0
            gmax = gclip /100.0
            bmax = bclip /100.0

            mode_subtract = 8
            width = image.get_width()
            height = image.get_height()
            l1 = Gimp.Layer.copy(drawables[0])
            image.insert_layer(l1, None, -1)
            
            mask = Gimp.Layer.new(image, "Mask...", width, height, l1.type(), l1.get_opacity(), Gimp.LayerMode.NORMAL)
            
            c=Gegl.Color.new("")
            c.set_rgba(rmax,gmax,bmax, 1.0)
            print(f"{rmax} {gmax} {bmax} | {rclip} {bclip} {gclip}")
            print(c.get_rgba())
            print(Gimp.context_set_background(c))
            mask.fill(Gimp.FillType.BACKGROUND)
            image.insert_layer(mask, None, -1)
            image.merge_down(mask, 0)
            image.get_layers()[0].set_mode(Gimp.LayerMode.SUBTRACT)
            image.merge_down(image.get_layers()[0], 0)

            Gimp.context_pop()
            image.undo_group_end()
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, None)
Gimp.main(pyastro_clip_image_brightness.__gtype__, sys.argv)

