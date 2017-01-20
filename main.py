
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.modalview import ModalView
from kivy.uix.relativelayout import RelativeLayout
from settings_json import settings_json

from Widgets import ReceiverParams
from Widgets import StatusWidget



class MainWidget(GridLayout):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)

    def exit(self):
        App.get_running_app().stop()

    def on_start_settings_press(self, *args):
        view = ModalView(size_hint=(None, None), size=(400,400))
        view.open()




class MainApp(App):
    def build(self):
        self.use_kivy_settings = False
        self.settings_cls = SettingsWithSidebar
        return MainWidget()

    def build_config(self, config):
        config.setdefaults('communication', {
            'telemetry_device': '/dev/ttyUSB0',
            'telemetry_baud': 57600
        })

    def build_settings(self, settings):
        settings.add_json_panel('PARR Settings',
                                self.config,
                                data=settings_json)

if __name__ == '__main__':
    MainApp().run()