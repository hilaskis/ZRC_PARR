import wx
import wx.lib.newevent
import threading
import time
import logging

UpdateSysInfoEvent, EVT_UPDATE_SYSINFO = wx.lib.newevent.NewEvent()

class SysInfoForm(wx.Panel):
    """ Base form class for System Info controls that
        creates a bunch of conrols and handlers for callbacks.
        Doing the layout of the controls is the responsibility
        of subclasses (by means of doLayout() method """

    def __init__(self, *args, **kwargs):
        super(SysInfoForm, self).__init__(*args, **kwargs)
        self.altitude = 0
        self.bearing = 0
        self.frequency = 0
        self.create_controls()
        self.bind_events()
        self.do_layout()
        self.SetBackgroundColour('#FFFFD6')

    def create_controls(self):
        """ Create all controls necessary for the form """
        self.title_label = wx.StaticText(parent=self, label='SYSTEM INFO', style=wx.ALIGN_TOP)
        self.altitude_label = wx.StaticText(parent=self, label='Altitude:')
        self.altitude_value = wx.StaticText(parent=self, label='meters')
        self.heading_label = wx.StaticText(parent=self, label='Current Heading:')
        self.heading_value = wx.StaticText(parent=self, label='degrees')
        self.frequency_label = wx.StaticText(parent=self, label='Scan Frequency:')
        self.frequency_value = wx.StaticText(parent=self, label='MHz')

    def bind_events(self):
        """ Bind events for the control """
        self.Bind(EVT_UPDATE_SYSINFO, self.update_labels)

    def do_layout(self):
        """ Layout the controls that were created by createControls().
            Form.doLayout will raise NotImplementedError because it
            is the responsibility of subclasses to layout the controls """
        raise NotImplementedError

    def set_title_font(self, font):
        self.title_label.SetFont(font)

    def update_labels(self):
        self.altitude_value.SetLabel(str(self.altitude) + ' meters')
        self.heading_value.SetLabel(str(self.bearing) + ' degrees')
        self.frequency_value.SetLabel(str(self.frequency) + ' MHz')


class SystemInfoCtrl(SysInfoForm):
    def __init__(self, *args, **kwargs):
        super(SystemInfoCtrl, self).__init__(*args, **kwargs)
        update_thread = threading.Thread(target=self.tick_event)
        update_thread.setDaemon(True)
        update_thread.start()

    def do_layout(self):
        """ Define the layout of the controls """
        # Top level box sizer for control
        top_sizer = wx.BoxSizer(wx.VERTICAL)
        top_sizer.Add(self.title_label, 0, wx.TOP | wx.LEFT, border=20)

        control_grid = wx.GridSizer(rows=3, cols=2, vgap=5, hgap=5)
        flags = wx.EXPAND | wx.ALL
        control_grid.AddMany([
            (self.altitude_label, 0, flags),
            (self.altitude_value, 0, flags),
            (self.heading_label, 0, flags),
            (self.heading_value, 0, flags),
            (self.frequency_label, 0, flags),
            (self.frequency_value, 0, flags)])
        top_sizer.Add(control_grid, 0, wx.ALL | wx.EXPAND, border=20)
        self.SetSizerAndFit(top_sizer)

    def tick_event(self):
        while True:
            wx.CallAfter(self.update_labels)
            time.sleep(0.3)


class DetectionSettingsForm(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(DetectionSettingsForm, self).__init__(*args, **kwargs)
        self.settings = {'frequency': 0, 'gain': 1, 'snr': 1}
        self.create_controls()
        self.bind_events()
        self.do_layout()
        self.SetBackgroundColour('#C2D1B2')

    def create_controls(self):
        self.title_label = wx.StaticText(parent=self, label='DETECTION SETTINGS', style=wx.ALIGN_TOP)
        self.frequency_label = wx.StaticText(parent=self, label='Set Frequency (MHz):')
        self.frequency_input = wx.TextCtrl(parent=self)
        self.gain_label = wx.StaticText(parent=self, label='Set Gain (dB):')
        self.gain_input = wx.TextCtrl(parent=self)
        self.snr_label = wx.StaticText(parent=self, label='Set SNR:')
        self.snr_input = wx.StaticText(parent=self)
        self.submit_button = wx.Button(parent=self, id=wx.ID_ANY, label="Submit")

    def bind_events(self):
        self.submit_button.Bind(wx.EVT_BUTTON, self.set_settings)

    def do_layout(self):
        raise NotImplementedError

    def set_title_font(self, font):
        self.title_label.SetFont(font)

    def set_settings(self):
        try:
            freq = float(self.frequency_input.GetValue())
            gain = float(self.gain_input.GetValue())
            snr = float(self.snr_input.GetValue())
        except ValueError as ex:
            print 'Failed to convert a setting to float.\n$s' % ex.message

        self.settings['frequency'] = freq
        self.settings['gain'] = gain
        self.settings['snr'] = snr


class DetectionSettingsCtrl(DetectionSettingsForm):
    def __init__(self, *args, **kwargs):
        super(DetectionSettingsCtrl, self).__init__(*args, **kwargs)

    def do_layout(self):
        # top level container
        top_sizer = wx.BoxSizer(wx.VERTICAL)
        top_sizer.Add(item=self.title_label, proportion=0, flag=wx.TOP | wx.LEFT, border=20)
        # grid holding input controls and their labels
        input_grid = wx.GridSizer(rows=3, cols=2, vgap=5, hgap=5)
        input_grid.AddMany(items=[self.frequency_label, self.frequency_input,
                                  self.gain_label, self.gain_input,
                                  self.snr_label, self.snr_input])
        # outer container holding input and submit button
        input_container = wx.GridSizer(rows=1, cols=2, vgap=5, hgap=5)
        input_container.AddMany(items=[input_grid, self.submit_button])
        top_sizer.Add(item=input_container)
