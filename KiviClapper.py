import atexit
import datetime
import threading


import time

import bpy
import pygame
from bpy.types import Operator
from bpy.types import Panel
import winsound

bl_info = {
    "name": "KIVI Clapperboard",
    "description": "A virtual clapperboard to help you sync video time and blender timeline",
    "author": "Kip",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "View3D",
    "warning": "",
    "support": "COMMUNITY",
    "doc_url": "",
    "category": "3D View"
}

thread = None
kill_thread = False
flash_now = False


def threadLoop():
    def updateScreen(bg, textColor):
        screen.fill(bg)
        text_surface = font.render("KIVI Clapperboard", True, textColor)
        screen.blit(text_surface, (10, 10))
        updateTime()
        pygame.display.flip()

    dot = 0

    def updateTime():
        nonlocal dot
        match dot:
            case 0:
                add = "◓"
                dot += 1
            case 1:
                add = "◑"
                dot += 1
            case 2:
                add = "◒"
                dot += 1
            case 3:
                add = "◐"
                dot = 0

        text_surface = font_clock.render(str(datetime.datetime.now().strftime("%m/%d  %H:%M:%S.%f")[:-5]), True,
                                         (255, 255, 255), (0, 0, 0))
        w, h = pygame.display.get_surface().get_size()
        text_rect = text_surface.get_rect(center=(w / 2, h / 2))
        screen.blit(text_surface, text_rect)

        blip_text = blip_font.render(add, True, (255, 255, 255), (0, 0, 0))
        screen.blit(blip_text, text_surface.get_rect(center=(w / 2 + 480, h / 2)))

    def flash():
        updateScreen((255, 255, 255), (0, 0, 0))
        # Clap
        winsound.Beep(1000, 50)
        # time.sleep(0.05)
        updateScreen((0, 0, 0), (255, 255, 255))

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((800, 500), pygame.RESIZABLE, 32)
    pygame.display.set_caption("Clapperboard")
    clock = pygame.time.Clock()
    pygame.font.init()
    font = pygame.font.SysFont('MicrogrammaDOT-BolExt', 20)
    font_clock = pygame.font.SysFont('MicrogrammaDOT-BolExt', 40)
    blip_font = pygame.font.SysFont("Segoe UI Emoji", 40)

    global flash_now
    while True:
        if kill_thread:
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                kill()
        keys = pygame.key.get_pressed()
        if flash_now:
            flash()
            flash_now = False

        updateScreen((0, 0, 0), (255, 255, 255))

        time.sleep(0.05)


def kill():
    global kill_thread
    kill_thread = True


def startThread():
    global thread, kill_thread
    if thread is not None:
        thread.join()
    kill_thread = False
    thread = threading.Thread(target=threadLoop)
    thread.start()
    atexit.register(kill)
    # threadLoop()


class ClapperboardFlash(Operator):
    """Flash the KIVI Clapperboard"""
    bl_idname = "kivi.clapperboard_flash"
    bl_label = "KIVI Clapperboard Flash"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT" and context.scene.ClapperboardSettings.working

    def execute(self, context):
        settings = context.scene.ClapperboardSettings
        if not settings.working:
            return {'FINISHED'}

        global flash_now
        flash_now = True

        area = context.area
        old_type = area.type
        area.type = 'DOPESHEET_EDITOR'
        bpy.ops.marker.add()
        area.type = old_type

        return {'FINISHED'}


class ToggleClapperboard(Operator):
    """Start KIVI Clapperboard"""
    bl_idname = "kivi.clapperboard_toggle"
    bl_label = "KIVI Clapperboard Toggle"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        settings = context.scene.ClapperboardSettings
        settings.working
        if settings.working:
            # Stop clapper thread
            settings.working = False
            kill()
        else:
            # Start clapper thread
            settings.working = True
            startThread()

        return {'FINISHED'}


class ClapperboardSidebar(Panel):
    """Display test button"""
    bl_label = "KIVI"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "KIVI"

    def draw(self, context):
        col = self.layout.column(align=True)
        settings = context.scene.ClapperboardSettings

        label = 'Stop Clapperboard' if settings.working else 'Start Clapperboard'
        prop = col.operator(ToggleClapperboard.bl_idname, text=label)

        if settings.working:
            col.label(text="Clapperboard Running...")
            col.operator(ClapperboardFlash.bl_idname, text="FLASH")
        else:
            col.label(text="Clapperboard Not Running")


# class that serves as container for all of this addon's data
class ClapperboardSettings(bpy.types.PropertyGroup):
    working: bpy.props.BoolProperty(name='working', default=False)


classes = [
    ToggleClapperboard,
    ClapperboardSidebar,
    ClapperboardFlash,
    ClapperboardSettings
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.ClapperboardSettings = bpy.props.PointerProperty(type=ClapperboardSettings)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
