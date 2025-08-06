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
        return [ "pyastro-plugin-name" ]

    def do_set_i18n (self, name):
        return False

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(self, name,
                                            Gimp.PDBProcType.PLUGIN,
                                            self.run, None)

        procedure.set_image_types("RGB*")

        procedure.set_menu_label("PyAstro Menu Name")
        procedure.add_menu_path('<Image>/Py-Astro/plugin-path/')

        procedure.set_documentation("DocuTitle",
                                    "Documentation Long description",
                                    name)
        procedure.set_attribution("TM", "TM", "2025")
         
        return procedure
    def run(self, procedure, run_mode, image, drawables, config, run_data):
        if run_mode == Gimp.RunMode.INTERACTIVE:
            GimpUi.init("title")
            Gimp.context_push()
            backup = drawables[0].copy()
            dialog=GimpUi.ProcedureDialog.new(procedure=procedure, config=config)

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

