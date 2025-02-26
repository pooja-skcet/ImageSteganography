# Importing necessary libraries
from tkinter import *  # For creating GUI components
from tkinter import ttk  # For themed GUI widgets
import tkinter.filedialog  # For file dialog operations
from PIL import ImageTk  # For handling images in Tkinter
from PIL import Image  # For image processing
from tkinter import messagebox  # For displaying message boxes
from io import BytesIO  # For handling binary data
import os  # For interacting with the operating system

class Stegno:
    """
    Stegno class handles the image steganography operations, including encoding (hiding)
    and decoding (retrieving) hidden messages within images using a GUI built with Tkinter.
    """

    # ASCII art for decoration in the GUI
    art = '''¯\_(ツ)_/¯'''
    art2 = '''
@(\/)
(\/)-{}-)@
@(={}=)/\)(\/)
(\/(/\)@| (-{}-)
(={}=)@(\/)@(/\)@
(/\)\(={}=)/(\/)
@(\/)\(/\)/(={}=)
(-{}-)""""@/(/\)
|:   |
/::'   \\
/:::     \\
|::'       |
|::        |
\::.       /
':______.'
`""""""`'''
    
    # Variable to store the size of the output image after encoding
    output_image_size = 0

    def main(self, root):
        """
        Initializes the main window of the application with Encode and Decode options.
        
        Parameters:
        root (Tk): The main window instance of Tkinter.
        """
        root.title('ImageSteganography')  # Setting the window title
        root.geometry('500x600')  # Setting the window size
        root.resizable(width=False, height=False)  # Disabling window resizing
        f = Frame(root)  # Creating a frame to hold widgets

        # Creating and configuring the title label
        title = Label(f, text='Image Steganography')
        title.config(font=('courier', 33))
        title.grid(pady=10)  # Positioning the title with padding

        # Creating and configuring the Encode button
        b_encode = Button(f, text="Encode", command=lambda: self.frame1_encode(f), padx=14)
        b_encode.config(font=('courier', 14))
        
        # Creating and configuring the Decode button
        b_decode = Button(f, text="Decode", padx=14, command=lambda: self.frame1_decode(f))
        b_decode.config(font=('courier', 14))
        b_decode.grid(pady=12)  # Positioning the Decode button with padding

        # Creating and configuring ASCII art labels
        ascii_art = Label(f, text=self.art)
        ascii_art.config(font=('courier', 60))
        
        ascii_art2 = Label(f, text=self.art2)
        ascii_art2.config(font=('courier', 12, 'bold'))

        # Configuring grid weights to manage layout
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # Positioning all widgets in the grid
        f.grid()
        title.grid(row=1)
        b_encode.grid(row=2)
        b_decode.grid(row=3)
        ascii_art.grid(row=4, pady=10)
        ascii_art2.grid(row=5, pady=5)

    def home(self, frame):
        """
        Returns to the main window from any other frame.
        
        Parameters:
        frame (Frame): The current frame to be destroyed.
        """
        frame.destroy()  # Destroying the current frame
        self.main(root)  # Re-initializing the main window

    def frame1_decode(self, f):
        """
        Sets up the Decode frame where users can select an image to decode.
        
        Parameters:
        f (Frame): The current frame to be destroyed.
        """
        f.destroy()  # Destroying the current frame
        d_f2 = Frame(root)  # Creating a new frame for decoding

        # Adding decorative label
        label_art = Label(d_f2, text='٩(^‿^)۶')
        label_art.config(font=('courier', 90))
        label_art.grid(row=1, pady=50)

        # Label prompting user to select an image with hidden text
        l1 = Label(d_f2, text='Select Image with Hidden text:')
        l1.config(font=('courier', 18))
        l1.grid()

        # Button to open file dialog for selecting the image
        bws_button = Button(d_f2, text='Select', command=lambda: self.frame2_decode(d_f2))
        bws_button.config(font=('courier', 18))
        bws_button.grid()

        # Cancel button to return to the main window
        back_button = Button(d_f2, text='Cancel', command=lambda: Stegno.home(self, d_f2))
        back_button.config(font=('courier', 18))
        back_button.grid(pady=15)
        back_button.grid()

        d_f2.grid()  # Displaying the decode frame

    def frame2_decode(self, d_f2):
        """
        Handles the decoding process by allowing the user to select an image and retrieve hidden data.
        
        Parameters:
        d_f2 (Frame): The decode frame to be destroyed after processing.
        """
        d_f3 = Frame(root)  # Creating a new frame to display decoding results

        # Opening file dialog to select an image
        myfile = tkinter.filedialog.askopenfilename(
            filetypes=(
                [('png', '*.png'),
                 ('jpeg', '*.jpeg'),
                 ('jpg', '*.jpg'),
                 ('All Files', '*.*')]
            )
        )

        if not myfile:
            # Display error message if no file is selected
            messagebox.showerror("Error", "You have selected nothing!")
        else:
            # Opening and resizing the selected image
            myimg = Image.open(myfile, 'r')
            myimage = myimg.resize((300, 200))
            img = ImageTk.PhotoImage(myimage)

            # Displaying the selected image in the GUI
            l4 = Label(d_f3, text='Selected Image :')
            l4.config(font=('courier', 18))
            l4.grid()
            panel = Label(d_f3, image=img)
            panel.image = img  # Keeping a reference to prevent garbage collection
            panel.grid()

            # Decoding the hidden data from the image
            hidden_data = self.decode(myimg)

            # Displaying the hidden data in a disabled text area
            l2 = Label(d_f3, text='Hidden data is :')
            l2.config(font=('courier', 18))
            l2.grid(pady=10)
            text_area = Text(d_f3, width=50, height=10)
            text_area.insert(INSERT, hidden_data)
            text_area.configure(state='disabled')  # Making the text area read-only
            text_area.grid()

            # Cancel button to return to the main window
            back_button = Button(d_f3, text='Cancel', command=lambda: self.page3(d_f3))
            back_button.config(font=('courier', 11))
            back_button.grid(pady=15)
            back_button.grid()

            # Button to show additional information about the images
            show_info = Button(d_f3, text='More Info', command=self.info)
            show_info.config(font=('courier', 11))
            show_info.grid()

            d_f3.grid(row=1)  # Displaying the decoding results frame
            d_f2.destroy()  # Destroying the previous decode frame

    def decode(self, image):
        """
        Decodes the hidden message from the image using Least Significant Bit (LSB) steganography.
        
        Parameters:
        image (PIL.Image): The image from which to decode the hidden message.
        
        Returns:
        str: The decoded hidden message.
        """
        data = ''  # Variable to store the decoded message
        imgdata = iter(image.getdata())  # Creating an iterator for image pixels

        while True:
            try:
                # Extracting 9 pixels (27 color values) at a time
                pixels = [value for value in imgdata.__next__()[:3] +
                          imgdata.__next__()[:3] +
                          imgdata.__next__()[:3]]
            except StopIteration:
                # If no more pixels are available, exit the loop
                break

            binstr = ''  # Binary string to store bits

            # Extracting the first 8 color values to retrieve the hidden character
            for i in pixels[:8]:
                if i % 2 == 0:
                    binstr += '0'
                else:
                    binstr += '1'

            # Converting the binary string to the corresponding ASCII character
            data += chr(int(binstr, 2))

            # Checking the last bit to determine if the message has ended
            if pixels[-1] % 2 != 0:
                return data  # Returning the decoded message

    def frame1_encode(self, f):
        """
        Sets up the Encode frame where users can select an image to hide a message.
        
        Parameters:
        f (Frame): The current frame to be destroyed.
        """
        f.destroy()  # Destroying the current frame
        f2 = Frame(root)  # Creating a new frame for encoding

        # Adding decorative label
        label_art = Label(f2, text='\'\(°Ω°)/\'')
        label_art.config(font=('courier', 70))
        label_art.grid(row=1, pady=50)

        # Label prompting user to select an image for encoding
        l1 = Label(f2, text='Select the Image in which \nyou want to hide text :')
        l1.config(font=('courier', 18))
        l1.grid()

        # Button to open file dialog for selecting the image
        bws_button = Button(f2, text='Select', command=lambda: self.frame2_encode(f2))
        bws_button.config(font=('courier', 18))
        bws_button.grid()

        # Cancel button to return to the main window
        back_button = Button(f2, text='Cancel', command=lambda: Stegno.home(self, f2))
        back_button.config(font=('courier', 18))
        back_button.grid(pady=15)
        back_button.grid()

        f2.grid()  # Displaying the encode frame

    def frame2_encode(self, f2):
        """
        Handles the encoding process by allowing the user to select an image and enter a message to hide.
        
        Parameters:
        f2 (Frame): The encode frame to be destroyed after processing.
        """
        ep = Frame(root)  # Creating a new frame to display encoding options

        # Opening file dialog to select an image
        myfile = tkinter.filedialog.askopenfilename(
            filetypes=(
                [('png', '*.png'),
                 ('jpeg', '*.jpeg'),
                 ('jpg', '*.jpg'),
                 ('All Files', '*.*')]
            )
        )

        if not myfile:
            # Display error message if no file is selected
            messagebox.showerror("Error", "You have selected nothing!")
        else:
            # Opening and resizing the selected image
            myimg = Image.open(myfile)
            myimage = myimg.resize((300, 200))
            img = ImageTk.PhotoImage(myimage)

            # Displaying the selected image in the GUI
            l3 = Label(ep, text='Selected Image')
            l3.config(font=('courier', 18))
            l3.grid()
            panel = Label(ep, image=img)
            panel.image = img  # Keeping a reference to prevent garbage collection
            self.output_image_size = os.stat(myfile)  # Getting the original image size
            self.o_image_w, self.o_image_h = myimg.size  # Getting original image dimensions
            panel.grid()

            # Label prompting user to enter the message to hide
            l2 = Label(ep, text='Enter the message')
            l2.config(font=('courier', 18))
            l2.grid(pady=15)

            # Text area for entering the message
            text_area = Text(ep, width=50, height=10)
            text_area.grid()

            # Cancel button to return to the main window
            encode_button = Button(ep, text='Cancel', command=lambda: Stegno.home(self, ep))
            encode_button.config(font=('courier', 11))

            # Getting the entered message from the text area
            data = text_area.get("1.0", "end-1c")

            # Encode button to perform the encoding and return to main window
            back_button = Button(
                ep,
                text='Encode',
                command=lambda: [self.enc_fun(text_area, myimg), Stegno.home(self, ep)]
            )
            back_button.config(font=('courier', 11))
            back_button.grid(pady=15)

            # Positioning the Cancel button
            encode_button.grid()

            ep.grid(row=1)  # Displaying the encoding options frame
            f2.destroy()  # Destroying the previous encode frame

    def info(self):
        """
        Displays information about the original and decoded images.
        """
        try:
            # Formatting the information string with image sizes and dimensions
            info_str = (
                'Original Image:-\n'
                f'Size of original image: {self.output_image_size.st_size / 1000000} MB\n'
                f'Width: {self.o_image_w}\n'
                f'Height: {self.o_image_h}\n\n'
                'Decoded Image:-\n'
                f'Size of decoded image: {self.d_image_size / 1000000} MB\n'
                f'Width: {self.d_image_w}\n'
                f'Height: {self.d_image_h}'
            )
            # Displaying the information in a message box
            messagebox.showinfo('Info', info_str)
        except:
            # Displaying error message if information retrieval fails
            messagebox.showinfo('Info', 'Unable to get the information')

    def genData(self, data):
        """
        Converts the input text data into a list of binary strings.
        
        Parameters:
        data (str): The text message to be hidden.
        
        Returns:
        list: A list of 8-bit binary representations of each character.
        """
        newd = []  # List to store binary data

        for i in data:
            # Converting each character to its 8-bit binary representation
            newd.append(format(ord(i), '08b'))
        return newd

    def modPix(self, pix, data):
        """
        Modifies the pixels of the image to embed the binary data.
        
        Parameters:
        pix (iterator): Iterator over the image's pixel data.
        data (str): The binary data to embed.
        
        Yields:
        tuple: Modified pixel values.
        """
        datalist = self.genData(data)  # Generating binary data list from text
        lendata = len(datalist)  # Length of the data list
        imdata = iter(pix)  # Creating an iterator for pixel data

        for i in range(lendata):
            # Extracting 9 color values (3 pixels) at a time
            try:
                pix = [value for value in imdata.__next__()[:3] +
                       imdata.__next__()[:3] +
                       imdata.__next__()[:3]]
            except StopIteration:
                # If no more pixels are available, exit the generator
                break

            # Modifying the first 8 color values based on the binary data
            for j in range(0, 8):
                if (datalist[i][j] == '0') and (pix[j] % 2 != 0):
                    # If the bit is '0' and pixel value is odd, make it even
                    pix[j] -= 1

                elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                    # If the bit is '1' and pixel value is even, make it odd
                    pix[j] -= 1

            # Modifying the 9th color value to indicate the end of the message
            if (i == lendata - 1):
                # If it's the last byte of data, set the last pixel's LSB to 1
                if (pix[-1] % 2 == 0):
                    pix[-1] -= 1
            else:
                # Otherwise, set the last pixel's LSB to 0
                if (pix[-1] % 2 != 0):
                    pix[-1] -= 1

            pix = tuple(pix)  # Converting the list back to a tuple

            # Yielding the modified pixels in chunks of three (RGB)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]

    def encode_enc(self, newimg, data):
        """
        Encodes the data into the image by modifying its pixels.
        
        Parameters:
        newimg (PIL.Image): The image to encode data into.
        data (str): The text message to hide.
        """
        w = newimg.size[0]  # Width of the image
        (x, y) = (0, 0)  # Starting coordinates

        for pixel in self.modPix(newimg.getdata(), data):
            # Putting the modified pixels back into the image
            newimg.putpixel((x, y), pixel)
            if (x == w - 1):
                # Move to the next row if the end of the current row is reached
                x = 0
                y += 1
            else:
                # Move to the next column
                x += 1

    def enc_fun(self, text_area, myimg):
        """
        Handles the encoding process: retrieves the message, encodes it into the image,
        and saves the new image with the hidden text.
        
        Parameters:
        text_area (Text): The text area widget containing the message.
        myimg (PIL.Image): The original image to encode the message into.
        """
        data = text_area.get("1.0", "end-1c")  # Getting the entered message
        if (len(data) == 0):
            # Alert if no message is entered
            messagebox.showinfo("Alert", "Kindly enter text in TextBox")
        else:
            newimg = myimg.copy()  # Creating a copy of the original image
            self.encode_enc(newimg, data)  # Encoding the message into the image

            # Preparing to save the new image
            my_file = BytesIO()
            temp = os.path.splitext(os.path.basename(myimg.filename))[0]  # Extracting the base name

            # Opening a save dialog for the user to choose where to save the encoded image
            newimg.save(tkinter.filedialog.asksaveasfilename(
                initialfile=temp,
                filetypes=([('png', '*.png')]),
                defaultextension=".png"
            ))

            self.d_image_size = my_file.tell()  # Getting the size of the new image
            self.d_image_w, self.d_image_h = newimg.size  # Getting dimensions of the new image

            # Displaying a success message
            messagebox.showinfo(
                "Success",
                "Encoding Successful\nFile is saved as Image_with_hiddentext.png in the same directory"
            )

    def page3(self, frame):
        """
        Returns to the main window from the current frame.
        
        Parameters:
        frame (Frame): The current frame to be destroyed.
        """
        frame.destroy()  # Destroying the current frame
        self.main(root)  # Re-initializing the main window

# Initializing the Tkinter root window
root = Tk()

# Creating an instance of the Stegno class and initializing the main window
o = Stegno()
o.main(root)

# Starting the Tkinter event loop to run the application
root.mainloop()
