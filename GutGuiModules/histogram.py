from GutGuiModules.utility import *

class Histogram:
    def __init__(self, histogram_frame):
        self.root = histogram_frame
        # self.x_vals = x_vals
        # self.y_vals = y_vals

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

        self.step_size_text = None
        self.step_size_input = None
        self.step_size_value = None

        self.save_label = None
        self.save_checkbox = None
        self.save_checkbox_value = None
        self.save_wo_scale_label = None
        self.save_wo_scale_checkbox = None
        self.save_wo_scale_checkbox_value = None
        self.save_as_excel_label = None
        self.save_as_excel_checkbox = None
        self.save_as_excel_checkbox_value = None

        self.interactive_histogram = None

        self.maximum_text = None
        self.maximum_input = None
        self.minimum_text = None
        self.maximum_input = None
        self.selected_text = None
        self.selected_input = None

        self._init_widgets()

    # Helper
    def _init_widgets(self):
        self._build_scale()
        self._build_step_size()
        self._build_save()
        self._build_save_wo_scale()
        self._build_save_as_excel()
        self._build_interactive_histogram()

    def _build_save(self):
        self.save_label = make_label(self.root, "Save", row=7, column=0, inner_padx=10, inner_pady=5, outer_padx=0, outer_pady=(0, 15))
        self.save_checkbox = make_checkbox(self.root, "", row=7, column=0, var=self.save_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_padx=(0, 12))
        self.save_checkbox.deselect()

    def _build_save_wo_scale(self):
        self.save_wo_scale_label = make_label(self.root, "Save W/O Scale", row=7, column=1, inner_padx=10, inner_pady=5, outer_padx=(0, 16), outer_pady=(0, 15))
        self.save_wo_scale_checkbox = make_checkbox(self.root, "", row=7, column=1, var=self.save_wo_scale_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_padx=(0,12))
        self.save_wo_scale_checkbox.deselect()

    def _build_save_as_excel(self):
        self.save_as_excel_label = make_label(self.root, "Save as Excel", row=7, column=2, inner_padx=10, inner_pady=5, outer_padx=(0, 10), outer_pady=(0, 15))
        self.save_as_excel_checkbox = make_checkbox(self.root, "", row=7, column=2, var=self.save_as_excel_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_padx=(0, 9))
        self.save_as_excel_checkbox.deselect()

    def _build_scale(self):
        # maximum
        self.maximum_text = make_text(self.root, content="Maximum: ", 
            bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=3, row=1, width=9, columnspan=1, pady=(0, 10))
        self.maximum_input = make_entry(self.root, row=1, column=4, width=5, pady=(0, 10), padx=(0, 15), columnspan=1)

        # minimum
        self.minimum_text = make_text(self.root, content="Minimum: ", 
            bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=3, row=2, width=9, columnspan=1, pady=(0, 10))
        self.minimum_input = make_entry(self.root, row=2, column=4, width=5, pady=(0, 10), padx=(0, 15), columnspan=1)

        # selection
        self.selection_text = make_text(self.root, content="Selection: ", 
            bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=3, row=3, width=11, columnspan=1, pady=(0, 10))
        self.selection_input = make_entry(self.root, row=3, column=4, width=5, pady=(0, 10), padx=(0, 15), columnspan=1)

        # x upper
        self.x_upper_scale_text = make_text(self.root, content="x upper scale end: ", bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=3, row=4, width=19, columnspan=1, pady=(0, 10))
        self.x_upper_scale_input = make_entry(self.root, row=4, column=4, width=5, pady=(0, 10), padx=(0, 15), columnspan=1)

        # x lower
        self.x_lower_scale_text = make_text(self.root, content="x lower scale end: ", bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=3, row=5, width=19, columnspan=1, pady=(0, 10))
        self.x_lower_scale_input = make_entry(self.root, row=5, column=4, width=5, pady=(0, 10), padx=(0, 15), columnspan=1)

        # y upper
        self.y_upper_scale_text = make_text(self.root, content="y upper scale end: ", bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=3, row=6, width=19, columnspan=1, pady=(0, 10))
        self.y_upper_scale_input = make_entry(self.root, row=6, column=4, width=5, pady=(0, 10), padx=(0, 15), columnspan=1)

        # y lower
        self.y_lower_scale_text = make_text(self.root, content="y lower scale end: ", bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=3, row=7, width=19, columnspan=1, pady=(0, 15))
        self.y_lower_scale_input = make_entry(self.root, row=7, column=4, width=5, pady=(0, 15), padx=(0, 15), columnspan=1)

    def _build_step_size(self):
        self.step_size_text = make_text(self.root, content="Stepsize: ", 
            bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), column=0, row=1, width=10, columnspan=1, pady=(0, 10))
        self.step_size_input = make_entry(self.root, row=1, column=1, width=28, pady=(0, 10), padx=(0, 20), columnspan=2)

    def _build_interactive_histogram(self):
        self.interactive_histogram = make_text(self.root, content="Interactive Boi", column=0, row=2, width=15, columnspan=3, rowspan=5, pady=(0, 10))

    # Commands (Callbacks)
    def __update_scale_x_upper(self):
        pass

    def __update_scale_y_upper(self):
        pass

    def __update_scale_x_lower(self):
        pass

    def __update_scale_y_lower(self):
        pass

    def __update_save_checked(self):
        pass

    def __update_save_wo_scale_checked(self):
        pass

    def __update_save_as_excel_checked(self):
        pass

    def __update_interactive_histogram(self):
        pass