import tkinter as tk
from tkinter import filedialog

from PIL import Image, ImageTk

# logic module for image transformation
from image_transformation import image_to_dithering, image_to_sketch, quantize_img


app = tk.Tk()  # beginning of interface
app.title("Image Transformer")  # setting title of app
app.geometry("350x350+500+200")  # window size & positioning from left and top
app.configure(bg="#856ff8", bd=0, highlightthickness=0, relief="ridge")

label = tk.Label(
    app, text="ImageTransFormer", height=3, bg="#856ff8", font=("Arial", 22)
).pack(side="top")  # pack is used to show the object in the app


# display function
def display(img_path, cv2_img_arr):
    # print(cv2_img_arr)
    newWindow = tk.Toplevel(app)
    newWindow.title("Result")
    newWindow.geometry("600x400+500+200")
    pane = tk.Frame(newWindow)
    pane.pack(fill=tk.BOTH, expand=True)

    # Create a photoimage object of the image in the path
    image1 = Image.open(img_path)
    image2 = Image.fromarray(cv2_img_arr)

    aspect_ratio = image1.width / image1.height
    image1 = image1.resize((300, int(300 / aspect_ratio)))
    image2 = image2.resize((300, int(300 / aspect_ratio)))

    input_img = ImageTk.PhotoImage(image1)
    out_img = ImageTk.PhotoImage(image2)

    # Constructing the first frame, frame1
    b1 = tk.LabelFrame(pane)
    inp_label = tk.Label(b1, text="Input image")
    inp_label.pack()
    image_label = tk.Label(b1, image=input_img)
    image_label.image = input_img
    image_label.pack()
    b1.pack(side="left", fill=tk.BOTH, expand=tk.TRUE)

    # Constructing the second frame, frame2
    b2 = tk.LabelFrame(pane)
    out_label = tk.Label(b2, text="Output image")
    out_label.pack()

    output_image_label = tk.Label(b2, image=out_img)
    output_image_label.image = out_img
    output_image_label.pack()
    b2.pack(side="right", fill=tk.BOTH, expand=tk.TRUE)


# button function
def upload_file():
    f_types = [
        ("Jpeg Files", "*.jpeg"),
        ("Jpg Files", "*.jpg"),
        ("PNG Files", "*.png"),
    ]  # type of files to select
    filename = filedialog.askopenfilename(filetypes=f_types)
    if filename:
        filename = filename[0]
        uploadBtn_text.set("Image uploaded")

        quanBtn_text = tk.StringVar()
        quanBtn = tk.Button(
            app,
            textvariable=quanBtn_text,
            command=lambda: display(filename, quantize_img(filename, 3)),
            font="Raleway",
            bg="black",
            fg="white",
            width=15,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        quanBtn_text.set("Image Quantization")
        quanBtn.pack()

        dethBtn_text = tk.StringVar()
        dethBtn = tk.Button(
            app,
            textvariable=dethBtn_text,
            command=lambda: display(filename, image_to_dithering(filename)),
            font="Raleway",
            bg="black",
            fg="white",
            width=15,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        dethBtn_text.set("Image Dethering")
        dethBtn.pack()

        sketchBtn_text = tk.StringVar()
        sketchBtn = tk.Button(
            app,
            textvariable=sketchBtn_text,
            command=lambda: display(filename, image_to_sketch(filename)),
            font="Raleway",
            bg="black",
            fg="white",
            width=15,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        sketchBtn_text.set("Image Sketch")
        sketchBtn.pack()


def disable_btn():
    upBtn["state"] = "disabled"
    upload_file()


# Upload button
uploadBtn_text = tk.StringVar()
upBtn = tk.Button(
    app,
    textvariable=uploadBtn_text,
    command=disable_btn,
    font="Raleway",
    bg="black",
    fg="white",
    width=15,
    bd=0,
    highlightthickness=0,
    relief="ridge",
)
uploadBtn_text.set("Upload image")
upBtn.pack()

app.mainloop()  # ending of interface

