import ctypes, math, numpy as np, torch, win32api, dxcam, os, pystyle, time
os.system("title Hyzr Aim")
os.system("cls")
print('\033[?25l', end="")
resx, resy, fov = 1920, 1080, 410 #RES AND FOV
class KeyBdInput(ctypes.Structure): _fields_ = [("wVk", ctypes.c_ushort), ("wScan", ctypes.c_ushort), ("dwFlags", ctypes.c_ulong), ("time", ctypes.c_ulong), ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]
class HardwareInput(ctypes.Structure): _fields_ = [("uMsg", ctypes.c_ulong), ("wParamL", ctypes.c_short), ("wParamH", ctypes.c_ushort)]
class MouseInput(ctypes.Structure): _fields_ = [("dx", ctypes.c_long), ("dy", ctypes.c_long), ("mouseData", ctypes.c_ulong), ("dwFlags", ctypes.c_ulong), ("time", ctypes.c_ulong), ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]
class Input_I(ctypes.Union): _fields_ = [("ki", KeyBdInput), ("mi", MouseInput), ("hi", HardwareInput)]
class Input(ctypes.Structure): _fields_ = [("type", ctypes.c_ulong), ("ii", Input_I)]
class Aimbot:
    extra, ii_, screen = ctypes.c_ulong(0), Input_I(), dxcam.create()
    def __init__(self):
        print("\u001b[30m")
        self.model = torch.hub.load("ultralytics/yolov5", "custom", path="best.pt", force_reload=True)
        xy = 7.0 # PUT UR XY SENS 
        targeting = 100.0 # PUT YOUR TARGETING
        Aimbot.sens_config, self.model.conf = {"xy_sens": xy, "targeting_sens": targeting, "xy_scale": 10/xy, "targeting_scale": 1000/(targeting * xy)}, 0.70 # THIS IS YOUR SENS AND CONFIDENCE VALUES
    def move_crosshair(self, x, y):
        scale = Aimbot.sens_config["xy_scale"] * 0.50 # THIS IS YOUR STRENGTH
        for rel_x, rel_y in Aimbot.interpolate_coordinates_from_center(self, (x, y), scale):
            Aimbot.ii_.mi = MouseInput(rel_x, rel_y, 0, 0x0001, 0, ctypes.pointer(Aimbot.extra))
            ctypes.windll.user32.SendInput(1, ctypes.byref(Input(ctypes.c_ulong(0), Aimbot.ii_)), ctypes.sizeof(Input(ctypes.c_ulong(0), Aimbot.ii_)))
    def interpolate_coordinates_from_center(self, absolute_coordinates, scale):
        diff_x, diff_y = (absolute_coordinates[0] - resx / 2) * scale / 0.7, (absolute_coordinates[1] - resy / 2) * scale / 0.7
        length = int(math.dist((0, 0), (diff_x, diff_y)))
        if length == 0: return
        unit_x, unit_y = (diff_x / length) * 0.7, (diff_y / length) * 0.7
        x = y = sum_x = sum_y = 0
        for k in range(0, length):
            sum_x += x
            sum_y += y
            x, y = round(unit_x * k - sum_x), round(unit_y * k - sum_y)
            yield x, y
    def start(self):
        detection_box = (int( resx / 2 - fov // 2 ), int(resy / 2 - fov // 2), int(resx / 2 + fov // 2), int(resy / 2 + fov // 2))
        Aimbot.screen.start(detection_box, video_mode=True)
        os.system("cls")
        print('''\n\n\n\n               \u001b[35m[\u001b[37m+\u001b[35m] \u001b[32;1mYour subscription will never expire''')
        time.sleep(1)
        os.system("cls")
        print('''\n\n\n\n               \u001b[35m[\u001b[37m+\u001b[35m] \u001b[36mHyzr Cheats''')
        time.sleep(1)
        os.system("cls")
        hyper = r"""
$$\   $$\ $$\     $$\ $$$$$$$\  $$$$$$$$\ $$$$$$$\         $$$$$$\  $$$$$$\ $$\      $$\ 
$$ |  $$ |\$$\   $$  |$$  __$$\ $$  _____|$$  __$$\       $$  __$$\ \_$$  _|$$$\    $$$ |
$$ |  $$ | \$$\ $$  / $$ |  $$ |$$ |      $$ |  $$ |      $$ /  $$ |  $$ |  $$$$\  $$$$ |
$$$$$$$$ |  \$$$$  /  $$$$$$$  |$$$$$\    $$$$$$$  |      $$$$$$$$ |  $$ |  $$\$$\$$ $$ |
$$  __$$ |   \$$  /   $$  ____/ $$  __|   $$  __$$<       $$  __$$ |  $$ |  $$ \$$$  $$ |
$$ |  $$ |    $$ |    $$ |      $$ |      $$ |  $$ |      $$ |  $$ |  $$ |  $$ |\$  /$$ |
$$ |  $$ |    $$ |    $$ |      $$$$$$$$\ $$ |  $$ |      $$ |  $$ |$$$$$$\ $$ | \_/ $$ |
\__|  \__|    \__|    \__|      \________|\__|  \__|      \__|  \__|\______|\__|     \__|

                                                                                         
                                    Github.com/hypr1x        



"""
        pystyle.System.Size(120, 30)
        pystyle.System.Clear()
        pystyle.Write.Print(
            pystyle.Center.Center(hyper),
            pystyle.Colors.purple_to_blue,
            interval=0,
        )
        pystyle.Cursor.HideCursor()
        while True: 
            results = self.model(np.array(Aimbot.screen.get_latest_frame()))
            if len(results.xyxy[0]) != 0:
                least_crosshair_dist = closest_detection = False
                for *box, conf, _ in results.xyxy[0]: 
                    x1y1, x2y2 = [int(x.item()) for x in box[:2]], [int(x.item()) for x in box[2:]]
                    x1, y1, x2, y2, conf = *x1y1, *x2y2, conf.item()
                    relative_head_X, relative_head_Y, own_player = int((x1 + x2) / 2), int((y1 + y2) / 2 - (y2 - y1) / 2.51), x1 < 15 or (x1 < fov / 5 and y2 > fov / 1.2)
                    crosshair_dist = math.dist((relative_head_X, relative_head_Y),(fov / 2, fov / 2)) 
                    if not least_crosshair_dist: least_crosshair_dist = crosshair_dist 
                    if crosshair_dist <= least_crosshair_dist and not own_player: least_crosshair_dist, closest_detection = crosshair_dist, {"x1y1": x1y1, "x2y2": x2y2, "relative_head_X": relative_head_X, "relative_head_Y": relative_head_Y, "conf": conf }
                    if own_player: own_player = False
                if closest_detection and (True if win32api.GetKeyState(0x02) in (-127, -128) else False): Aimbot.move_crosshair(self, closest_detection["relative_head_X"] + detection_box[0], closest_detection["relative_head_Y"] + detection_box[1])
Aimbot().start()