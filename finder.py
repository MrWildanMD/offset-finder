import dearpygui.dearpygui as imgui
from tkinter import *
from tkinter import filedialog
import re

global_class_line = 0
global_class_end_line = 0
global_function_line = 0

def is_match(regex, text):
    pattern = re.compile(regex)
    return pattern.search(text) is not None

def string_before(value, b):
    pos_b = value.find(b)
    if pos_b == -1:
        return ""
    return value[0:pos_b]


def string_after(value, a):
    pos_a = value.rfind(a)
    if pos_a == -1:
        return ""
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= len(value):
        return ""
    return value[adjusted_pos_a:]


def string_between(value, a, b):
    pos_a = value.find(a)
    if pos_a == -1:
        return ""
    pos_b = value.rfind(b)
    if pos_b == -1:
        return ""
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= pos_b:
        return ""
    return value[adjusted_pos_a:pos_b]


def get_class_line(file, classname: str):
    with open(file, 'r', encoding="utf-8") as cl:
        for l_no, line in enumerate(cl):
            if f"public class {classname.lower()}" in line.lower():
                return l_no


def get_class_end_line(file, classline):
    with open(file, 'r', encoding='utf-8') as cel:
        lines_num = []
        lines_text = []
        for i, line in enumerate(cel):
            if i >= classline:
                lines_num.append(i)
                lines_text.append(line.strip())
                for j, line in enumerate(lines_text):
                    if "Namespace" in lines_text[j]:
                        return lines_num[j - 1]


def get_methods_line(file, classline, class_end_line):
    with open(file, 'r', encoding='utf-8') as methodlen:
        for l_no, line in enumerate(methodlen):
            if l_no >= classline and l_no <= class_end_line:
                if "Methods" in line:
                    return l_no

def get_function_in_class_offset(file, function_name: str, methods_line, class_end_line):
    with open(file, 'r', encoding='utf-8') as fnco:
        class_method = []
        method_lines = []
        for i, line in enumerate(fnco):
            if i in range(methods_line, class_end_line):
                class_method.append(line.strip())
                method_lines.append(i)
            elif i > class_end_line:
                break

        for j in range(len(class_method)):
            if function_name.lower() in class_method[j].lower():
                offset_line = class_method[j - 1]
                return string_between(offset_line, "Offset: ", " VA:")


def get_function_in_class_rva(file, function_name: str, methods_line, class_end_line):
    with open(file, 'r', encoding='utf-8') as fnco:
        class_method = []
        method_lines = []
        for i, line in enumerate(fnco):
            if i in range(methods_line, class_end_line):
                class_method.append(line.strip())
                method_lines.append(i)
            elif i > class_end_line:
                break

        for j in range(len(class_method)):
            if function_name.lower() in class_method[j].lower():
                offset_line = class_method[j - 1]
                return string_between(offset_line, "RVA: ", " Offset:")


def quit():
    imgui.destroy_context()


def select_file():
    text_file_extension = ['*.cs']
    ftypes = [
        ('Dump File', text_file_extension)
    ]
    Tk.filename = filedialog.askopenfilename(
        initialdir="/", title="Select File", filetypes=ftypes)
    imgui.set_value(item="inpath", value=Tk.filename)


def classname_text_input_controller(sender, data):
    pass


def functionname_text_input_controller(sender, data):
    pass


def find_offset_button_controller(sender, data):
    # imgui.set_value("tableresult", value=[["classcolumn"]["Halo"]])
    # print(get_class_end_line(imgui.get_value("inpath"), get_class_line(
    #     imgui.get_value("inpath"), imgui.get_value('classname'))))
    # print(get_function_in_class_offset(imgui.get_value("inpath"), imgui.get_value(
    #     "functionname"), get_class_line(imgui.get_value("inpath"), imgui.get_value("classname")), get_class_end_line(imgui.get_value("inpath"), get_class_line(
    #         imgui.get_value("inpath"), imgui.get_value("classname")))))
    # print(get_methods_line(imgui.get_value("inpath"), get_class_line(
    #     imgui.get_value("inpath"), imgui.get_value("classname")), get_class_end_line(imgui.get_value("inpath"), get_class_line(
    #         imgui.get_value("inpath"), imgui.get_value("classname")))))
    # print(get_class_line(imgui.get_value("inpath"), imgui.get_value("classname")))
    global_class_line = get_class_line(
        imgui.get_value("inpath"), imgui.get_value("classname"))
    global_class_end_line = get_class_end_line(
        imgui.get_value("inpath"), global_class_line)
    global_methods_line = get_methods_line(imgui.get_value("inpath"), global_class_line, global_class_end_line)
    with imgui.table_row(parent="tableresult"):
        imgui.add_text(imgui.get_value("classname"))
        imgui.add_text(imgui.get_value("functionname"))
        imgui.add_text(get_function_in_class_offset(imgui.get_value("inpath"), imgui.get_value("functionname"), global_methods_line, global_class_end_line))
        imgui.add_text(get_function_in_class_rva(imgui.get_value("inpath"), imgui.get_value("functionname"), global_methods_line, global_class_end_line))
    print(get_function_in_class_offset(imgui.get_value("inpath"), imgui.get_value("functionname"), global_methods_line, global_class_end_line))


def result_table_controller(sender, data):
    pass


imgui.create_context()
imgui.create_viewport(title="Offset Finder", max_width=1280,
                      max_height=800, resizable=False)
imgui.setup_dearpygui()

# global imgui var

with imgui.theme() as global_theme:
    with imgui.theme_component(imgui.mvAll):
        imgui.add_theme_color(
            imgui.mvThemeCol_Text, (255, 255, 255, 255), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_TextDisabled,
                              (128, 128, 128), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_WindowBg,
                              (15, 15, 15, 240), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_ChildBg,
                              (0, 0, 0, 0), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_PopupBg,
                              (20, 20, 20, 240), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(
            imgui.mvThemeCol_Border, (110, 110, 128, 128), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_BorderShadow,
                              (0, 0, 0, 0), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_FrameBg,
                              (41, 74, 122, 138), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_FrameBgHovered,
                              (66, 150, 250, 102), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_FrameBgActive,
                              (66, 150, 250, 171), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_TitleBg,
                              (10, 10, 10, 255), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_TitleBgActive,
                              (41, 74, 122, 255), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_TitleBgCollapsed,
                              (0, 0, 0, 130), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_MenuBarBg,
                              (36, 36, 36, 255), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_ScrollbarBg,
                              (5, 5, 5, 135), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_ScrollbarGrab,
                              (79, 79, 79, 255), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_ScrollbarGrabHovered,
                              (105, 105, 105, 255), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_ScrollbarGrabActive,
                              (130, 130, 130, 255), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_CheckMark,
                              (66, 150, 250, 255), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_SliderGrab,
                              (61, 133, 224, 255), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_SliderGrabActive,
                              (66, 150, 250, 255), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(
            imgui.mvThemeCol_Button, (66, 150, 250, 102), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_ButtonHovered,
                              (66, 150, 250, 255), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_ButtonActive,
                              (15, 135, 250, 255), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_Header,
                              (66, 150, 250, 79), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_HeaderHovered,
                              (66, 150, 250, 204), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_HeaderActive,
                              (66, 150, 250, 255), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_Separator,
                              (110, 110, 128, 128), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_SeparatorHovered,
                              (26, 102, 191, 199), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_SeparatorActive,
                              (26, 102, 191, 255), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_ResizeGrip,
                              (66, 150, 250, 51), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_ResizeGripHovered,
                              (66, 150, 250, 171), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_ResizeGripActive,
                              (66, 150, 250, 242), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(
            imgui.mvThemeCol_Tab, (46, 89, 148, 220), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_TabHovered,
                              (66, 150, 250, 204), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_TabActive,
                              (51, 105, 173, 255), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_TabUnfocused,
                              (17, 26, 38, 248), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_TabUnfocusedActive,
                              (35, 67, 108, 255), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_TableHeaderBg,
                              (48, 48, 51, 255), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_TableBorderStrong,
                              (79, 79, 89, 255), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_TableBorderLight,
                              (59, 59, 64, 255), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_TableRowBg,
                              (0, 0, 0, 0), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_TableRowBgAlt,
                              (255, 255, 255, 15), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_TextSelectedBg,
                              (66, 150, 250, 89), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_DragDropTarget,
                              (255, 255, 0, 230), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_NavHighlight,
                              (66, 150, 250, 255), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_NavWindowingHighlight,
                              (255, 255, 255, 179), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_NavWindowingDimBg,
                              (204, 204, 204, 51), category=imgui.mvThemeCat_Core)
        imgui.add_theme_color(imgui.mvThemeCol_ModalWindowDimBg,
                              (204, 204, 204, 89), category=imgui.mvThemeCat_Core)

imgui.bind_theme(global_theme)

with imgui.window(label="Example Window", no_close=True, no_title_bar=True, width=1280, height=800, no_resize=True, no_move=True):
    with imgui.menu_bar():
        with imgui.menu(label="File"):
            imgui.add_menu_item(label="Quit", callback=quit)

    with imgui.child_window(label="##c1", width=imgui.get_viewport_width() - 30, height=-680):
        with imgui.table(header_row=False, policy=imgui.mvTable_SizingFixedFit):
            imgui.add_table_column(label="##A", init_width_or_weight=120.0)
            imgui.add_table_column(
                label="##B", init_width_or_weight=imgui.get_viewport_width() * 0.79)
            imgui.add_table_column()
            with imgui.table_row():
                imgui.add_text("File: ")
                imgui.add_input_text(
                    readonly=True, width=imgui.get_viewport_width() - 100.0, tag="inpath")
                imgui.add_button(label="Select File", callback=select_file)
            with imgui.table_row():
                imgui.add_text("Class Name: ")
                imgui.add_input_text(width=imgui.get_viewport_width(
                ) - 100.0, tag="classname", callback=classname_text_input_controller)
            with imgui.table_row():
                imgui.add_text("Function Name: ")
                imgui.add_input_text(width=imgui.get_viewport_width(
                ) - 100.0, tag="functionname", callback=functionname_text_input_controller)

    imgui.add_button(
        label="Find Offset", callback=find_offset_button_controller, width=1250)
    imgui.add_spacer()
    imgui.add_spacer()
    imgui.add_text("Result")
    with imgui.table(header_row=True, row_background=True, borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True, policy=imgui.mvTable_SizingFixedFit, tag="tableresult", callback=result_table_controller):
        imgui.add_table_column(
            label="Class Name", init_width_or_weight=200.0, tag="classcolumn")
        imgui.add_table_column(label="Function Name",
                               init_width_or_weight=200.0)
        imgui.add_table_column(label="Offset", init_width_or_weight=200.0)
        imgui.add_table_column(label="RVA", init_width_or_weight=200.0)

imgui.show_viewport()
imgui.start_dearpygui()
imgui.destroy_context()
