from view import *

class RDImageManager(ImageManager):

    def __init__(self):
        pass

    def initialise(self):
        if ImageManager.initialised is False:
            super().initialise()
            print("Initialising {0}".format(__class__))
            self.load_skins()
            self.load_sprite_sheets()

    def load_skins(self):

        new_skin_name = ImageManager.DEFAULT_SKIN
        new_skin = (new_skin_name, {

            "NSEW": "roomC-NSEW.png",
            "NSE_": "roomC-NSE_.png",
            "_SEW": "roomC-_SEW.png",
            "NS_W": "roomC-NS_W.png",
            "N_EW": "roomC-N_EW.png",
            "NS__": "roomB-NS__.png",
            "_SE_": "roomC-_SE_.png",
            "_S_W": "roomC-_S_W.png",
            "N_E_": "roomC-N_E_.png",
            "__EW": "roomB-__EW.png",
            "N___": "roomC-N___.png",
            "_S__": "roomC-_S__.png",
            "___W": "roomC-___W.png",
            "__E_": "roomC-__E_.png",
            "_S_W": "roomC-_S_W.png",
            "N__W": "roomC-N__W.png",

        })

        ImageManager.skins[new_skin_name] = new_skin

    def load_sprite_sheets(self):

        sheet_file_name = "token.png"
        for i in range(0, 5):
            self.sprite_sheets["token{0}.png".format(i)] = (sheet_file_name, (i * 8, 0, 8, 8))
