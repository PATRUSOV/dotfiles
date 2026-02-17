import os
import sys
from .config import MONITORS_CONFIGURATIONS

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
HYPRLAND_MONITORS_CFG_PATH = os.path.expanduser("~/.config/hypr/configs/monitors.conf")


def main():
    print("Доступные команды: configs, set, exit\n")

    while True:
        inp = input("command: ").strip()
        print()

        match inp:
            case "configs":
                for i, conf in enumerate(MONITORS_CONFIGURATIONS):
                    print(f"{i}: {conf.name}\n")

            case "set":
                index_str = input("index: ").strip()
                try:
                    index = int(index_str)
                    conf = MONITORS_CONFIGURATIONS[index]
                except (ValueError, IndexError):
                    print("Неверный индекс конфигурации!\n")
                    continue

                try:
                    os.makedirs(
                        os.path.dirname(HYPRLAND_MONITORS_CFG_PATH), exist_ok=True
                    )
                    with open(
                        HYPRLAND_MONITORS_CFG_PATH, "w", encoding="utf-8"
                    ) as cfg_file:
                        cfg_file.write(str(conf))
                    print(f"Конфигурация '{conf.name}' успешно сохранена!\n")
                except OSError as e:
                    print(f"Ошибка при записи файла: {e}\n")

            case "exit":
                print("Выход из программы.")
                break

            case _:
                print("Неизвестная команда. Используйте: configs, set, exit\n")


if __name__ == "__main__":
    main()
