from tkinter import *
from tkinter.ttk import *
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk, ImageDraw, ImageFont
from fonts import FONTS
import os

# get current directory
current_dir = os.path.dirname(__file__)


# ----------------------------------------FUNCTIONS----------------------------------------

def open_file():
    global img_width, img_height, image
    image_path = askopenfilename(title="Select An Image", filetypes=[('Images', '*.jpg *.jpeg *.png *.webp *.gif')])
    if image_path:
        img_width, img_height = Image.open(image_path).size
        # Update User Interface with values based on new Image
        width_position.config(to=img_width)
        height_position.config(to=img_height)
        width_label.configure(text="Width: ")
        height_label.configure(text="Height: ")
        current_width.set(int(img_width / 2))
        current_height.set(int(img_height / 2))
        # Correct the ratio of uploaded image
        image = Image.open(image_path)
        # this shows how the image will be upload in the frame,we need to adjust the height and the width
        img_width = int(img_width * (750 / img_height))
        image = image.resize((img_width, 750))
        # Update Displayed Image
        uploaded_image = ImageTk.PhotoImage(image)
        label.configure(image=uploaded_image)
        label.image = uploaded_image
        apply_watermark()
    else:
        remove_files()
        quit()


def remove_files():
    os.remove("blank_image.png")  # To remove file
    if os.path.exists("new_img_with_watermark.png"):  # To check whether a particular path exists
        os.remove("new_img_with_watermark.png")
    if os.path.exists("temp_image.png"):
        os.remove("temp_image.png")


def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb


def change_text_color():
    colors = askcolor(title="Watermark Color Chooser")
    global text_color
    text_color = colors[0]  # colors[0] is RGB value
    color_selection.configure(bg=colors[1])  # colors[1] is hex value, this creates the selected


#    color in the color selection canvas
def height_slider_moved(event):
    height_label.configure(text=f"Height: {1 * (current_height.get() - 1 / 2 * img_height)}")


def width_slider_moved(event):
    width_label.configure(text=f"Width: {current_width.get() - 1 / 2 * img_width}")


def apply_watermark():
    watermark_image = image.convert('RGBA')
    my_font = ImageFont.truetype(f"/Library/Fonts/{font_var.get()}", current_font_size.get())

    # Blank image for text
    blank_image_dims = (round(4 * watermark_image.width),
                        round(4 * watermark_image.height))
    text_image = Image.new('RGBA', blank_image_dims, (255, 255, 255, 0))
    my_watermark = ImageDraw.Draw(text_image)

    # Create RGBA tuple from color choice and opacity value
    opacity_tuple = ((round(current_opacity.get() * 2.55)),)
    rgba_text_color = text_color + opacity_tuple

    # Setup Watermark
    center_of_image = (round(text_image.width / 2), round(text_image.height / 2))
    my_watermark.text(center_of_image,
                      watermark_input.get(),
                      font=my_font,
                      fill=rgba_text_color
                      )
    # Trim text image to just text to rotate around the center of text
    text_box_size = text_image.getbbox()
    text_image = text_image.crop(text_box_size)
    text_image = text_image.rotate(current_tilt.get(),
                                   center=(text_image.width / 2, text_image.height / 2),
                                   expand=True)
    # Create new image to paste text to because cannot alpha_composite two different sized images
    d = Image.new('RGBA', watermark_image.size, (255, 255, 255, 0))
    text_position = ((int(current_width.get() - text_image.width / 2),
                      int(current_height.get() - text_image.height / 2)))
    Image.Image.paste(d, text_image, text_position)
    # Combine image with text and save image
    combined = Image.alpha_composite(watermark_image, d).convert('RGB')
    combined.save((os.path.join(current_dir, "new_img_with_watermark.png")),
                  format='PNG')  # To concat current directory
    watermark_image.close()
    # Apply changes to screen
    updated_image = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, "new_img_with_watermark.png")))
    label.configure(image=updated_image)
    label.image = updated_image


def another_watermark():
    global image
    # to open the saved watermarked image and save it
    temporary_img = Image.open(os.path.join(current_dir, "new_img_with_watermark.png"))
    # temporary_img.save((os.path.join(current_dir, "temp_image.png")))
    # to  apply new watermark and save that image as a temporary one
    # temporary_img = Image.open(os.path.join(current_dir, "temp_image.png"))
    apply_watermark()
    temporary_img.save((os.path.join(current_dir, "temp_image.png")))
    temporary_img.close()


def logo_watermark():
    global watermark_image
    watermark_image = image.convert('RGBA')
    watermark_image_path = askopenfilename(title="Select Your Logo",
                                           filetypes=[('Images', '*.jpg *.jpeg *.png *.webp *.gif')])
    watermark = Image.open(watermark_image_path)
    watermark.thumbnail((200, 300))
    logo_position = ((int(current_width.get() - watermark.width / 2),
                      int(current_height.get() - watermark.height / 2)))
    watermark_image.paste(watermark, logo_position)
    watermark_image.show()
    watermark_image.save((os.path.join(current_dir, "new_img_with_watermark.png")))


def save_new_image():
    new_image = Image.open(os.path.join(current_dir, "new_img_with_watermark.png"))
    file = asksaveasfilename(title="Save Image", filetypes=[("png files", "*.png")])
    if file:
        new_image.save(file)
    new_image.close()


def enter_pressed(event):
    apply_watermark()


# ---------------------------------------GUI------------------------------------------------
window = Tk()
window.title("Watermark App")
window.resizable(False, False)

# GUI Style
style = Style(window)
style.configure('Wide.TButton', width=30, padding=5)

# Image frame
image_frame = Frame(window)  # this creates the frame for the image on the window.
image_frame.pack(side=LEFT, padx=10, pady=10)

# image display,this creates a new blank image
blank_image = Image.new('RGB', (500, 500), "black")
# this line creates the path for the blank image to get saved
blank_image_path = os.path.join(current_dir, 'a_blank_image.png')
# saves blank image
blank_image.save(blank_image_path)

# open the blank image
open_blank_image = ImageTk.PhotoImage(Image.open(blank_image_path))

# this label makes the blank image appear on the window
label = Label(image_frame, image=open_blank_image)
label.grid(column=0, row=0)

# edit frame- this will help to edit the frame while creating widgets
edit_frame = Frame(window, height=500)
edit_frame.pack(padx=10, pady=10)

# upload image file button
upload_button = Button(edit_frame, text="Upload your Image", command=open_file,
                       style="Wide.TButton")
upload_button.grid(column=1, row=0, columnspan=2)

# watermark text
watermark_text_label = Label(edit_frame, text="Watermark Text: ")
watermark_text_label.grid(column=0, row=1)
# this entry is for watermark input
watermark_input = Entry(edit_frame, width=22)
watermark_input.grid(column=1, row=1)

# watermark font
font_label = Label(edit_frame, text="Font: ", width=12)
font_label.grid(column=0, row=2)
font_var = StringVar()
drop_menu = OptionMenu(edit_frame, font_var, FONTS[3], *FONTS)  # FONTS[3] selects from font index 3
drop_menu.grid(column=1, row=2)

# Watermark Font Size
current_font_size = IntVar(value=30)
font_size_label = Label(edit_frame, text="Font size: ", width=12)
font_size_label.grid(column=0, row=3)
font_size = Spinbox(edit_frame,
                    from_=8,
                    to=250,
                    wrap=True,
                    textvariable=current_font_size, )
font_size.grid(column=1, row=3)

# Watermark Opacity
current_opacity = IntVar(value=100)
opacity_label = Label(edit_frame, text="Opacity", width=12)
opacity_label.grid(column=0, row=4)
opacity_spinbox = Spinbox(edit_frame,
                          from_=0,
                          to=100,
                          textvariable=current_opacity,
                          wrap=False,  # Boolean value. If True, increment and decrement
                          # buttons will cycle from the to value to the from
                          # value or the from value to the to value, respectively.
                          )
opacity_spinbox.grid(column=1, row=4)
# Watermark Color
text_color = (0, 0, 0)
color_selection = Canvas(edit_frame,
                         bg=rgb_to_hex(text_color),
                         width=110,
                         height=15)
color_selection.grid(column=0, row=5)
color_button = Button(edit_frame,
                      text="Change Color",
                      command=change_text_color,
                      style="Color.TButton",
                      width=18)
color_button.grid(column=1, row=5, columnspan=1)

# Watermark Height
img_width, img_height = 500, 500
height_label = Label(edit_frame, text="Height: ", width=12, anchor="w")
height_label.grid(column=0, row=6)
current_height = IntVar(value=int(img_height / 2))
height_position = Scale(edit_frame,
                        from_=0,
                        to=img_height,
                        variable=current_height,
                        orient=VERTICAL,
                        command=height_slider_moved)
height_position.grid(column=1, row=6)
# Watermark Width
width_label = Label(edit_frame, text="Width: ", width=12)
width_label.grid(column=0, row=7)
current_width = IntVar(value=int(img_height / 2))
width_position = Scale(edit_frame,
                       from_=0,
                       to=img_width,
                       variable=current_width,
                       orient=HORIZONTAL,
                       command=width_slider_moved)
width_position.grid(column=1, row=7)

# Watermark Angle
current_tilt = IntVar(value=0)
tilt_label = Label(edit_frame, text="Tilt: ", width=12)
tilt_label.grid(column=0, row=8)
tilt_spinbox = Spinbox(edit_frame,
                       from_=0,
                       to=359,
                       wrap=True,
                       textvariable=current_tilt,
                       )
tilt_spinbox.grid(column=1, row=8)
# Apply/Update Button
confirm_button = Button(edit_frame,
                        text="Apply Watermark",
                        command=apply_watermark,
                        style="Wide.TButton")
confirm_button.grid(column=1, row=9, columnspan=2)
# Button to save current watermark and add another
another_wm_button = Button(edit_frame,
                           text="Add Another Watermark",
                           command=another_watermark,
                           style="Wide.TButton")
another_wm_button.grid(column=1, row=10, columnspan=2)

# Watermark-logo button
add_logo = Button(edit_frame,
                  text="Logo Watermark",
                  command=logo_watermark,
                  style="Wide.TButton")
add_logo.grid(column=1, row=11, columnspan=2)

# Save Button
save_button = Button(edit_frame,
                     text="Save",
                     command=save_new_image,
                     style="Wide.TButton")
save_button.grid(column=1, row=12, columnspan=2)

# Bind Enter key to apply watermark
window.bind('<Return>', enter_pressed)

# On App start hide window, open file, and open window back up
window.withdraw()
open_file()
window.deiconify()

if __name__ == '__main__':
    window.mainloop()
    remove_files()
