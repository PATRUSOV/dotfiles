from .struct import HyprlandMonitor, HyprlandMonitorsConfiguration

MONITORS_CONFIGURATIONS = [
    HyprlandMonitorsConfiguration(
        name="only DP-1",
        monitors=[
            HyprlandMonitor("DP-1", "1920x1080", 60, "0x0", 1),
            HyprlandMonitor.make_disabled("eDP-1"),
        ],
    ),
    HyprlandMonitorsConfiguration(
        name="only eDP-1",
        monitors=[
            HyprlandMonitor("DP-1", "1920x1080", 60, "0x0", 1),
            HyprlandMonitor.make_disabled("eDP-1"),
        ],
    ),
]
