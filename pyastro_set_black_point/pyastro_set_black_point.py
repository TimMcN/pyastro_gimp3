import sys
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
from gi.repository import Gegl
gi.require_version('GimpUi', '3.0')
from gi.repository import GimpUi
from gi.repository import GLib
from gi.repository import GObject
class pyastro_set_black_point(Gimp.PlugIn):
    def do_query_procedures(self):
        return [ "pyastro-set-black-point" ]

    def do_set_i18n (self, name):
        return False

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(self, name,
                                            Gimp.PDBProcType.PLUGIN,
                                            self.run, None)

        procedure.set_image_types("RGB*")

        procedure.set_menu_label("PyAstro Auto Set Black Point")
        procedure.add_menu_path('<Image>/Py-Astro/Colour Tools/')

        procedure.set_documentation("Set the image black point automatically",
                                    "Set the image black point automatically",
                                    name)
        procedure.set_attribution("TM", "TM", "2025")

         
        return procedure
    def run(self, procedure, run_mode, image, drawables, config, run_data):
        GimpUi.init("Set Black Point")
        image.undo_group_start()

        bpp = drawables[0].get_bpp()
        if bpp > 8:
            Gimp.message("Error too many bytes per pixel")
            return procedure.new_return_values(Gimp.PDBStatusType.EXECUTION_ERROR)
        suc,avg_red, sig_red, median, pixels, kount, per_red = drawables[0].histogram(1, 0.0, 1.0)
        suc,avg_grn, sig_grn, median, pixels, kount, per_grn = drawables[0].histogram(2, 0.0, 1.0)
        suc,avg_blu, sig_blu, median, pixels, kount, per_blu = drawables[0].histogram(2, 0.0, 1.0)

        if avg_red < sig_red or avg_grn < sig_grn or avg_blu < sig_blu:
            Gimp.Message("Black point reset, not practical for this image")
            return procedure.new_return_values(Gimp.PDBStatusType.CALLING_ERROR)
        
        if bpp <=4:
            avg_red /= 255.0
            avg_grn /= 255.0
            avg_blu /= 255.0
            sig_red /= 255.0
            sig_grn /= 255.0
            sig_blu /= 255.0

        ddr = max(0.0, avg_red - sig_red)
        ddg = max(0.0, avg_grn - sig_grn)
        ddb = max(0.0, avg_blu- sig_blu)

        new_layer = Gimp.Layer.new(image,"Mask...", drawables[0].get_width(), drawables[0].get_height(), drawables[0].type(), drawables[0].get_opacity(), 0)
        image.insert_layer(new_layer, None, -1)
        Gimp.context_set_default_colors()
        new_layer.edit_fill(Gimp.FillType.BACKGROUND)
        new_layer.levels(1, 0.0, 1.0, True, 1.0, 0.0, ddr, True)
        new_layer.levels(2, 0.0, 1.0, True, 1.0, 0.0, ddg, True)
        new_layer.levels(3, 0.0, 1.0, True, 1.0, 0.0, ddb, True)

        new_layer.set_mode(Gimp.LayerMode.SUBTRACT)
        image.merge_down(new_layer, 0)

        Gimp.context_pop()
        image.undo_group_end()
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, None)
Gimp.main(pyastro_set_black_point.__gtype__, sys.argv)

