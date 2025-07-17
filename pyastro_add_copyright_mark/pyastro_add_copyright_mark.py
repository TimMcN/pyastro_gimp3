
import sys

import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
gi.require_version('GimpUi', '3.0')
from gi.repository import GimpUi
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Gio

class pyastro_add_copyright_mark(Gimp.PlugIn):
    def do_query_procedures(self):
        return [ "pyastro-add-copyright-mark" ]

    def do_set_i18n (self, name):
        return False

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(self, name,
                                            Gimp.PDBProcType.PLUGIN,
                                            self.run, None)

        procedure.set_image_types("*")

        procedure.set_menu_label("PyAstro Add Copyright Mark")
        procedure.add_menu_path('<Image>/Py-Astro/misc')

        procedure.set_documentation("Add Copyright Mark",
                                    "Add Copyright Mark",
                                    name)
        procedure.set_attribution("TM", "TM", "2025")
        procedure.add_file_argument("file", "Select File", "Select A file for copyright", Gimp.FileChooserAction.OPEN,
                                    False, None, GObject.ParamFlags.READWRITE)
        return procedure
    def run(self, procedure, run_mode, image, drawables, config, run_data):
        Gimp.context_push()
        GimpUi.init("pyastro_add_copyright_mark")
        image.undo_group_start()    
        dialog=GimpUi.ProcedureDialog(procedure=procedure, config=config)
        dialog.fill(None)

        if not dialog.run():
            dialog.destroy()
        else:
            procedure.new_return_values(Gimp.PDBStatusType.CANCEL,GLib.Error())
        Gimp.progress_init("Loading copyright image file")
        fileobj = config.get_property("file")
        try:
            fl =Gimp.get_pdb().lookup_procedure("gimp-file-load")
            flc = fl.create_config()
            flc.set_property("run-mode", Gimp.RunMode.NONINTERACTIVE)
            flc.set_property("file", fileobj)
            r = fl.run(flc)
            cimg = r.index(1)

        except Exception as e:
            Gimp.message("Error loading copyright image:" + str(e))
            Gimp.progress_end()
        Gimp.progress_end()

        mode=0
        scl = image.get_height()/2000.0
        sx = scl*cimg.get_width()
        sy = scl*cimg.get_height()
        mx = -(image.get_width()-sx-sy) /2
        my = -(image.get_height() -2 * sy) /2
        Gimp.progress_init("Adding Copyright Image")

        cimg.get_layers()[0].set_mode(mode)
        Gimp.edit_copy([cimg.get_layers()[0]])
        Gimp.edit_paste(image.get_layers()[0], True)
        l1 = image.get_layers()[0]
        l1.set_mode(mode)
        l1.scale(sx,sy, True)
        l1.transform_translate(mx,my)
        Gimp.floating_sel_to_layer(l1)
        image.merge_down(l1, Gimp.MergeType.EXPAND_AS_NECESSARY)
        Gimp.progress_end()
        image.undo_group_end()
        Gimp.context_pop()
        
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())
Gimp.main(pyastro_add_copyright_mark.__gtype__, sys.argv)