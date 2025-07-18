import sys

import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
gi.require_version('GimpUi', '3.0')
from gi.repository import GimpUi
from gi.repository import GLib
from gi.repository import GObject
class pyastro_big_gaussian_blur(Gimp.PlugIn):
    def do_query_procedures(self):
        return [ "pyastro-big-gaussian-blur" ]

    def do_set_i18n (self, name):
        return False

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(self, name,
                                            Gimp.PDBProcType.PLUGIN,
                                            self.run, None)

        procedure.set_image_types("RGB*")

        procedure.set_menu_label("PyAstro Big Gaussian Blur")
        procedure.add_menu_path('<Image>/Py-Astro/Image Tools/')

        procedure.set_documentation("Big gaussian blur",
                                    "Big gaussian blur",
                                    name)
        procedure.set_attribution("TM", "TM", "2025")

        procedure.add_double_argument('radius',
                                    'Radius', 'Gaussian blur radius (pixels)',
                                       25.0, 100.0, 25.0,
                                      GObject.ParamFlags.READWRITE | GObject.ParamFlags.CONSTRUCT)
        return procedure
    def run(self, procedure, run_mode, image, drawables, config, run_data):
        if run_mode == Gimp.RunMode.INTERACTIVE:
            GimpUi.init("pyastro_big_gaussian_blur")
            Gimp.context_push()
            dialog=GimpUi.ProcedureDialog.new(procedure=procedure, config=config)
            widget = dialog.get_widget("radius", GimpUi.SpinScale)
            box = dialog.fill(None)

            if not dialog.run():
                dialog.destroy()
                return procedure.new_return_values(Gimp.PDBStatusType.CANCEL, None)
            else:
                dialog.destroy()
            image.undo_group_start()
            filter = Gimp.DrawableFilter.new(drawables[0], 'gegl:gaussian-blur')
            gconf = filter.get_config()
            gconf.set_property('std-dev-x', config.get_property("radius"))
            gconf.set_property('std-dev-y', config.get_property("radius"))
            drawables[0].merge_filter(filter)
            image.undo_group_end()
            Gimp.context_pop()
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, None)
Gimp.main(pyastro_big_gaussian_blur.__gtype__, sys.argv)

