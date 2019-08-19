from GutGuiModules.utility import *
import numpy as np


class AbsorptionSpec:
    def __init__(self, absorption_spec_frame, listener):
        self.root = absorption_spec_frame

        # Listener
        self.listener = listener

        self.specs = (False, True, False)
        self.spec_number = 1

        self.x_vals = np.arange(500, 1000, 5)
        self.absorption_spec = []

        self.local_maximum_title = None
        self.local_maximum_text = None
        self.local_maximum_value = None
        self.local_minimum_title = None
        self.local_minimum_text = None
        self.local_minimum_value = None

        self.x_upper_scale_text = None
        self.y_upper_scale_text = None
        self.x_lower_scale_text = None
        self.y_lower_scale_text = None
        self.x_upper_scale_input = None
        self.y_upper_scale_input = None
        self.x_lower_scale_input = None
        self.y_lower_scale_input = None
        self.x_upper_scale_value = None
        self.y_upper_scale_value = None
        self.x_lower_scale_value = None
        self.y_lower_scale_value = None

        self.save_label = None
        self.save_checkbox = None
        self.save_checkbox_value = IntVar()
        self.save_wo_scale_label = None
        self.save_wo_scale_checkbox = None
        self.save_wo_scale_checkbox_value = IntVar()
        self.save_as_excel_label = None
        self.save_as_excel_checkbox = None
        self.save_as_excel_checkbox_value = IntVar()

        self.interactive_absorption_spec_graph = None
        self.axes = None
        self.interactive_absorption_spec = None

        self.upper_text = None
        self.upper_input = None
        self.upper_value = 995
        self.lower_text = None
        self.lower_input = None
        self.lower_value = 500

        self.drop_down_var = StringVar()
        self.choices = ['1. Reflectance - Original',
                        '2. Reflectance - Original without Negative Values',
                        '3. Reflectance - Normalised',
                        '4. Reflectance - Normalised without Negative Values',
                        '5. Absorbance - Original',
                        '6. Absorbance - Original without Negative Values',
                        '7. Absorbance - Normalised',
                        '8. Absorbance - Normalised without Negative Values']

        self.reset_button = None
        self.info_label = None
        self._init_widgets()

    def update_absorption_spec(self, absorption_spec_data):
        self.absorption_spec = absorption_spec_data
        self._calc_extrema()
        self._calc_high_low()
        self._build_scale()
        self._build_interactive_absorption_spec()

    # Helper
    def _init_widgets(self):
        self._build_scale()
        self._build_save()
        self._build_save_wo_scale()
        self._build_save_as_excel()
        self._build_info_label()
        self._build_reset_button()
        self._build_drop_down()
        self._build_interactive_absorption_spec()
        self._build_extrema()

    def _build_save(self):
        self.save_label = make_label(self.root, "Save", row=8, column=0, inner_padx=10, inner_pady=5, outer_padx=15,
                                     outer_pady=(0, 15))
        self.save_checkbox = make_checkbox(self.root, "", row=8, column=0, var=self.save_checkbox_value, sticky=NE,
                                           inner_padx=0, inner_pady=0, outer_padx=(0, 13))
        self.save_checkbox.deselect()
        self.save_checkbox.bind('<Button-1>', self.__update_save_with_scale_check_status)

    def _build_save_wo_scale(self):
        self.save_wo_scale_label = make_label(self.root, "Save W/O Scale", row=8, column=1, inner_padx=10, inner_pady=5,
                                              outer_padx=(5, 16), outer_pady=(0, 15), columnspan=1)
        self.save_wo_scale_checkbox = make_checkbox(self.root, "", row=8, column=1,
                                                    var=self.save_wo_scale_checkbox_value, sticky=NE, inner_padx=0,
                                                    inner_pady=0, outer_padx=(0, 25))
        self.save_wo_scale_checkbox.deselect()
        self.save_wo_scale_checkbox.bind('<Button-1>', self.__update_save_wo_scale_check_status)

    def _build_save_as_excel(self):
        self.save_as_excel_label = make_label(self.root, "Save as CSV", row=8, column=2, inner_padx=10, inner_pady=5,
                                              outer_padx=(5, 15), outer_pady=(0, 15))
        self.save_as_excel_checkbox = make_checkbox(self.root, "", row=8, column=2,
                                                    var=self.save_as_excel_checkbox_value, sticky=NE, inner_padx=0,
                                                    inner_pady=0, outer_padx=(0, 7))
        self.save_as_excel_checkbox.deselect()
        self.save_as_excel_checkbox.bind('<Button-1>', self.__update_save_as_excel_check_status)

    def _build_reset_button(self):
        self.reset_button = make_button(self.root, "Reset", row=8, column=3, command=self.__reset, inner_padx=10,
                                        inner_pady=5, outer_padx=15, outer_pady=(0, 10), columnspan=2)

    def _build_drop_down(self):
        self.drop_down_var.set(self.choices[0])
        self.drop_down_menu = OptionMenu(self.root, self.drop_down_var, *self.choices, command=self.__update_data)
        self.drop_down_menu.configure(highlightthickness=0, width=6, anchor='w', padx=15)
        self.drop_down_menu.grid(column=1, row=0, columnspan=1, padx=(80, 0))

    def _build_extrema(self):
        self.local_maximum_text = make_text(self.root, content="Local Max: " + str(self.local_maximum_value),
                                            bg=tkcolour_from_rgb(BACKGROUND), column=0, row=1, width=25, columnspan=2,
                                            pady=(0, 5), padx=5, state=NORMAL)

        self.local_minimum_text = make_text(self.root, content="Local Min: " + str(self.local_minimum_value),
                                            bg=tkcolour_from_rgb(BACKGROUND), column=2, row=1, width=25, columnspan=2,
                                            pady=(0, 5), padx=(0, 5), state=NORMAL)

    def _build_scale(self):
        # lower
        self.lower_text = make_text(self.root, content="Lower: ", bg=tkcolour_from_rgb(BACKGROUND), column=3, row=2,
                                    width=7, columnspan=1, pady=(0, 10))
        self.lower_input = make_entry(self.root, row=2, column=4, width=5, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.lower_input.bind('<Return>', self.__update_upper_lower)
        self.lower_input.insert(END, str(self.lower_value))

        # upper
        self.upper_text = make_text(self.root, content="Upper: ", bg=tkcolour_from_rgb(BACKGROUND), column=3, row=3,
                                    width=7, columnspan=1, pady=(0, 10))
        self.upper_input = make_entry(self.root, row=3, column=4, width=5, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.upper_input.bind('<Return>', self.__update_upper_lower)
        self.upper_input.insert(END, str(self.upper_value))

        # x lower
        self.x_lower_scale_text = make_text(self.root, content="Min x: ", bg=tkcolour_from_rgb(BACKGROUND), column=3,
                                            row=4, width=7, columnspan=1, pady=(0, 10))
        self.x_lower_scale_input = make_entry(self.root, row=4, column=4, width=5, pady=(0, 10), padx=(0, 15),
                                              columnspan=1)
        self.x_lower_scale_input.bind('<Return>', self.__update_scales)
        self.x_lower_scale_input.insert(END, str(self.x_lower_scale_value))

        # x upper
        self.x_upper_scale_text = make_text(self.root, content="Max x: ", bg=tkcolour_from_rgb(BACKGROUND),
                                            column=3, row=5, width=7, columnspan=1, pady=(0, 10))
        self.x_upper_scale_input = make_entry(self.root, row=5, column=4, width=5, pady=(0, 10), padx=(0, 15),
                                              columnspan=1)
        self.x_upper_scale_input.bind('<Return>', self.__update_scales)
        self.x_upper_scale_input.insert(END, str(self.x_upper_scale_value))

        # y lower
        self.y_lower_scale_text = make_text(self.root, content="Min y: ", bg=tkcolour_from_rgb(BACKGROUND), column=3,
                                            row=6, width=7, columnspan=1, pady=(0, 10))
        self.y_lower_scale_input = make_entry(self.root, row=6, column=4, width=5, pady=(0, 10), padx=(0, 15),
                                              columnspan=1)
        self.y_lower_scale_input.bind('<Return>', self.__update_scales)
        self.y_lower_scale_input.insert(END, str(self.y_lower_scale_value))

        # y upper
        self.y_upper_scale_text = make_text(self.root, content="Max y: ", bg=tkcolour_from_rgb(BACKGROUND), column=3,
                                            row=7, width=7, columnspan=1, pady=(0, 10))
        self.y_upper_scale_input = make_entry(self.root, row=7, column=4, width=5, pady=(0, 10), padx=(0, 15),
                                              columnspan=1)
        self.y_upper_scale_input.bind('<Return>', self.__update_scales)
        self.y_upper_scale_input.insert(END, str(self.y_upper_scale_value))

    def _build_info_label(self):
        self.info_label = make_label_button(self.root, text='Optical Spectrum', command=self.__info, width=13)
        self.info_label.grid(columnspan=2, padx=(15, 120))

    def _build_interactive_absorption_spec(self):
        # create canvas
        self.interactive_absorption_spec_graph = Figure(figsize=(3.5, 2))
        self.axes = self.interactive_absorption_spec_graph.add_subplot(111)
        self.interactive_absorption_spec_graph.patch.set_facecolor(rgb_to_rgba(BACKGROUND))
        # plot absorption spec
        if len(self.absorption_spec) != 0:
            self.axes.plot(self.x_vals, self.absorption_spec, '-', lw=0.5)
            self.axes.grid(linestyle=':', linewidth=0.5)
        # set axes
        self.interactive_absorption_spec_graph.set_tight_layout(True)
        self.axes.set_xlim(left=self.x_lower_scale_value, right=self.x_upper_scale_value)
        self.axes.set_ylim(bottom=self.y_lower_scale_value, top=self.y_upper_scale_value)
        # commas and non-scientific notation
        self.axes.ticklabel_format(style='plain')
        self.axes.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(self._format_axis))
        self.axes.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(self._format_axis))
        # draw figure
        self.interactive_absorption_spec = FigureCanvasTkAgg(self.interactive_absorption_spec_graph, master=self.root)
        self.interactive_absorption_spec.draw()
        self.interactive_absorption_spec.get_tk_widget().grid(column=0, row=2, columnspan=3, rowspan=6, ipady=5,
                                                              ipadx=0)
        self.interactive_absorption_spec.get_tk_widget().bind('<Button-2>', self.__pop_up_image)

    def _format_axis(self, x, p):
        if x % 1 == 0:
            return format(int(x), ',')
        else:
            return format(round(x, 2))

    def _calc_high_low(self):
        self.x_lower_scale_value = np.ma.min(self.x_vals)
        self.x_upper_scale_value = np.ma.max(self.x_vals)
        self.y_lower_scale_value = round(np.ma.min(self.absorption_spec), 3)
        self.y_upper_scale_value = round(np.ma.max(self.absorption_spec), 3)

    def _calc_extrema(self):
        abs_spec_list = list(self.absorption_spec)
        abs_range = abs_spec_list[int((self.lower_value - 500) / 5):int((self.upper_value - 500) / 5)]
        maximum = np.ma.max(abs_range)
        maximum_x = abs_spec_list.index(maximum) * 5 + 500
        self.local_maximum_value = (maximum_x, round(maximum, 3))
        minimum = np.ma.min(abs_range)
        minimum_x = abs_spec_list.index(minimum) * 5 + 500
        self.local_minimum_value = (minimum_x, round(minimum, 3))
        self._build_extrema()

    # Commands (Callbacks)
    def __reset(self):
        self._calc_extrema()
        self._calc_high_low()
        self._build_scale()
        self._build_interactive_absorption_spec()

    def __info(self):
        info = self.listener.get_abspec_info()
        title = "Optical Spectrum Information"
        make_info(title=title, info=info)

    def __update_upper_lower(self, event):
        self.upper_value = int(self.upper_input.get())
        self.lower_value = int(self.lower_input.get())
        self._calc_extrema()

    def __update_scales(self, event):
        self.x_upper_scale_value = float(self.x_upper_scale_input.get())
        self.y_upper_scale_value = float(self.y_upper_scale_input.get())
        self.x_lower_scale_value = float(self.x_lower_scale_input.get())
        self.y_lower_scale_value = float(self.y_lower_scale_input.get())
        self._build_interactive_absorption_spec()

    def __update_data(self, event):
        choice = self.drop_down_var.get()[:2]
        if choice == '1.':
            self.specs = (False, True, False)
        elif choice == '2.':
            self.specs = (False, True, True)
        elif choice == '3.':
            self.specs = (False, False, False)
        elif choice == '4.':
            self.specs = (False, False, True)
        elif choice == '5.':
            self.specs = (True, True, False)
        elif choice == '6.':
            self.specs = (True, True, True)
        elif choice == '7.':
            self.specs = (True, False, False)
        elif choice == '8.':
            self.specs = (True, False, True)
        self.spec_number = choice[0]
        self.listener.update_abs_specs(self.specs)

    def __update_save_with_scale_check_status(self, event):
        value = not bool(self.save_checkbox_value.get())
        self.listener.update_saved(ABSORPTION_SPEC_IMAGE, value)

    def __update_save_wo_scale_check_status(self, event):
        value = not bool(self.save_wo_scale_checkbox_value.get())
        self.listener.update_saved(ABSORPTION_SPEC_IMAGE_WO_SCALE, value)

    def __update_save_as_excel_check_status(self, event):
        value = not bool(self.save_as_excel_checkbox_value.get())
        self.listener.update_saved(ABSORPTION_SPEC_EXCEL, value)

    def __pop_up_image(self, event):
        make_popup_image(self.interactive_absorption_spec_graph)
