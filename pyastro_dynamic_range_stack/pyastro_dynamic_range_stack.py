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
        return [ "pyastro-dynamic-range-stack" ]

    def do_set_i18n (self, name):
        return False

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(self, name,
                                            Gimp.PDBProcType.PLUGIN,
                                            self.run, None)

        procedure.set_image_types("RGB*")

        procedure.set_menu_label("PyAstro Dynamic Range Stack")
        procedure.add_menu_path('<Image>/Py-Astro/Layer Tools/')

        procedure.set_documentation("Apply Lodriguss method to image stack",
                                    "Apply Lodriguss method to a stack of astro images",
                                    name)
        procedure.set_attribution("TM", "TM", "2025")
        procedure.add_int_argument('gwdth',
                                    'Gaussian blur (pixels)', 'Gaussian blur radius (pixels)',
                                       0, 50, 1,
                                      GObject.ParamFlags.READWRITE | GObject.ParamFlags.CONSTRUCT)
        
        procedure.add_boolean_argument("setblk", "Set Black Point", "Set black point in images", False, 
                                       GObject.ParamFlags.READWRITE | GObject.ParamFlags.CONSTRUCT)
        
        return procedure
    def run(self, procedure, run_mode, image, drawables, config, run_data):
        if run_mode == Gimp.RunMode.INTERACTIVE:
            GimpUi.init("pyastro_clip_image_brightness")
            image.undo_group_start()
            Gimp.context_push()

            dialog=GimpUi.ProcedureDialog.new(procedure=procedure, config=config)
            dialog.get_widget("gwdth", GimpUi.SpinScale)
            box = dialog.fill(None)

            if not dialog.run():
                dialog.destroy()
                Gimp.context_pop()
                image.undo_group_end()
                return procedure.new_return_values(Gimp.PDBStatusType.CANCEL, None)
            else:
                dialog.destroy()

            Gimp.context_pop()
            image.undo_group_end()
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, None)
Gimp.main(pyastro_clip_image_brightness.__gtype__, sys.argv)

