# KMK fw code (simplified for me and YOU)
# Microcontroller = Seeed XIAO RP2040

# bring our friends in
# the regular friends
import board
import busio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.macros import Press, Release, Tap, Macros
# Knob thingy 
from kmk.modules.encoder import EncoderHandler
# Media ctrls for knob
from kmk.extensions.media_keys import MediaKeys
# OLED Pt 2
from kmk.extensions.display.ssd1306 import SSD1306
from kmk.extensions.display import Display, TextEntry, ImageEntry
# lights
from kmk.extensions.RGB import RGB, AnimationsModes
# the BRAIN
keyboard = KMKKeyboard()

# lets bring our friend named macros
macros = Macros()
keyboard.modules.append(macros)

# lets bring the media friend
keyboard.extensions.append(MediaKeys())

# Bring the knob friend
encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)

# define OLED pins
i2c_bus = busio.I2C(scl=board.GP7, sda=board.GP6)

# Driver
driver = SSD1306(
    i2c=i2c_bus
)

# Display Config
display = Display(
    display=driver
)

# display the text
display.entries = [
    TextEntry(text="Hello!", x=0, y=0)
]

# define our pins for the knob
encoder_handler.pins = ((board.A1, board.A0, None, False),)
# A1 = Vol Up. A0 = Vol Down.

rgb = RGB(
    pixel_pin=board.GP0,
    num_pixel=3,
    hue_default=0,
    animation_mode=AnimationsModes.STATIC,
    sat_default=0,
)
keyboard.extensions.append(rgb)

# define the PINS
# GP1 - GP4 = regular keyboard buttons (SW1-SW4)
# GP28 = Knob button (SW5)
PINS = [board.GP1, board.GP2, board.GP4, board.GP3, board.GP28]

# Tell the brain we arent using a key matrix
keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)

# THE MAIN THING (keymaps)
keyboard.keymap = [
    # SW1: Purr
    KC.MACRO("meoww"),
    # SW2: Open LM Studio
    KC.Macro(
        Tap(KC.LGUI),
        KC.MACRO("LM Studio"),
        Tap(KC.ENTER)
    ),
    # SW3: Open Slack
    KC.Macro(
        Tap(KC.LGUI), # Click Start menu
        KC.MACRO("Slack"), # Type out Slack
        Tap(KC.ENTER) # Click Enter
    ),
    # SW4: Open VMWare Workstation
    KC.Macro(
        Tap(KC.LGUI),
        KC.MACRO("VMware Workstation Pro"),
        Tap(KC.ENTER)
    ),
    # SW5: Mute (Knob)
    KC.MUTE,
]

# Media controls with Knob
encoder_handler.map = [
    ((KC.VOLD, KC.VOLU),) # turn knob left, volume DOWN. turn right, volume UP
]

# GO GO GO!
if __name__ == '__main__':
    keyboard.go()
