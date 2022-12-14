import glfw
import OpenGL.GL as gl

import imgui
from imgui.integrations.glfw import GlfwRenderer
from tkinter import filedialog
from tkinter import *
from testwindow import show_test_window


def CenterText(data):
    window_width = imgui.get_window_width()
    text_size = imgui.calc_text_size(data).x

    imgui.set_cursor_pos_x((window_width - text_size) * 0.5)
    imgui.text(data)


def main():
    text_file_extension = ['*.cs']
    ftypes = [
        ('Dump File', text_file_extension)
    ]
    file_name = ""
    function_name = ""
    class_name = ""
    edit1 = ""
    edit2 = ""
    i = 0
    imgui.create_context()
    window = impl_glfw_init()
    impl = GlfwRenderer(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()

        imgui.new_frame()

        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):

                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", 'Cmd+Q', False, True
                )

                if clicked_quit:
                    exit(1)

                imgui.end_menu()
            imgui.end_main_menu_bar()

        imgui.set_next_window_size(1280, 720)
        imgui.set_next_window_position(0, 18)
        imgui.begin("Offset Finder", True, flags=imgui.WINDOW_NO_TITLE_BAR)
        imgui.begin_child("##c1", 1260, -620, border=True)
        imgui.columns(3, '##1', border=False)
        imgui.set_column_width(0, 120.0)
        imgui.set_column_width(1, imgui.get_window_width() * 0.80)
        imgui.text("File: ")
        imgui.next_column()
        imgui.push_item_width(imgui.get_window_width() * 50.0)
        filechanged, file_name = imgui.input_text(
            '##',
            file_name,
            256,
            flags=imgui.INPUT_TEXT_READ_ONLY
        )
        imgui.pop_item_width()
        imgui.next_column()
        if imgui.button("Select File"):
            Tk.filename = filedialog.askopenfilename(
                initialdir="/", title="Select File", filetypes=ftypes)
            file_name = Tk.filename
        imgui.next_column()
        imgui.text("Class Name: ")
        imgui.next_column()
        imgui.push_item_width(imgui.get_window_width() * 50.0)
        classnamechanged, class_name = imgui.input_text(
            '##a',
            class_name,
            256
        )
        imgui.pop_item_width()
        imgui.next_column()
        imgui.text("")
        imgui.next_column()
        imgui.text("Function Name: ")
        imgui.next_column()
        imgui.push_item_width(imgui.get_window_width() * 50.0)
        fnnamechanged, function_name = imgui.input_text(
            '##b',
            function_name,
            256
        )
        imgui.pop_item_width()
        imgui.next_column()
        imgui.text("")
        imgui.end_child()
        imgui.button("Find Offset", width=1260.0)
        imgui.spacing()
        imgui.spacing()
        CenterText("Result")
        imgui.spacing()
        imgui.spacing()
        if imgui.begin_table("Test Table", 3):
            for i in range(15):
                imgui.table_next_column()
                imgui.text(f"Item {i}")
        imgui.end_table()
        imgui.end()

        show_test_window()

        gl.glClearColor(1., 1., 1., 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()


def impl_glfw_init():
    width, height = 1280, 720
    window_name = "Offset Finder"

    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(
        int(width), int(height), window_name, None, None
    )
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        exit(1)

    return window


if __name__ == "__main__":
    main()
