# -*- coding: utf-8 -*-
import sys
import glfw
import OpenGL.GL as gl
import cv2

import imgui
from imgui.integrations.glfw import GlfwRenderer

def main():

    print('python version  :', sys.version)
    print('GLFW version   :', glfw.__version__)
    print('imgui version  :', imgui.__version__)
    print('OpenCV version :', cv2.__version__)

    imgui.create_context()
    window = impl_glfw_init()
    impl = GlfwRenderer(window)

    img_scale = 1.0
    img_texture, img_w, img_h = load_image("box.jpg")

    while not glfw.window_should_close(window):
        glfw.wait_events()
        glfw.poll_events()
        impl.process_inputs()

        imgui.new_frame()

        ### Menu Bar
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):

                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", 'Cmd+Q', False, True
                )

                if clicked_quit:
                    exit(1)

                imgui.end_menu()
            imgui.end_main_menu_bar()

        ### Config Window
        imgui.begin("Config", True)
        ret, img_scale=imgui.slider_float('img_scale', img_scale, 0.1, 4.0, '%.1f', 1.0)
        imgui.end()

        ### Image Window
        imgui.begin("Image display")
        imgui.image(img_texture, int(img_w*img_scale), int(img_h*img_scale), border_color=(1, 0, 0, 1))
        imgui.end()

        ### OpenGL / Background
        gl.glClearColor(0.4, 0.4, 0.4, 1) # gray background
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        ### Render
        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()


def impl_glfw_init():
    width, height = 1280, 720
    window_name = "ImGui/GLFW3 Open-CV example"

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

def load_image(IMAGE):
    img = cv2.imread(IMAGE) # read
    img_gl = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # convert color
    height, width = img.shape[:2] # get shape

    # テクスチャ・オブジェクトを生成する。
    texture = gl.glGenTextures(1)

    # テクスチャユニット１以上を使用する場合に使用。テクスチャユニット0に切り替える
    gl.glActiveTexture(gl.GL_TEXTURE0)

    # テクスチャをバインド。指定した名前のテクスチャを有効にする。
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)

    # テクスチャの拡大/縮小オプション
    gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)

    # 画像（テクスチャ）がメモリにどのように格納されているかを OpenGL に伝える
    gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)

    # メモリ上の２次元画像をテクスチャに割り当てる。
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, width, height, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, img_gl)

    # Show versions
    """
    print('OpenGL version :', gl.glGetString(gl.GL_VERSION))
    print('Vendor :', gl.glGetString(gl.GL_VENDOR))
    print('GPU :', gl.glGetString(gl.GL_RENDERER))
    """

    return texture, width, height

if __name__ == "__main__":
    main()
