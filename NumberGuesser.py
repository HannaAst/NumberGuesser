from tkinter import *
from PIL import Image, ImageDraw, ImageTk
from tensorflow.keras.models import load_model
import numpy as np

class GuessN(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.brush_size = 10
        self.brush_color = 'white'
        self.canvas_size=300
        self.canvas_backg = 'black'
        self.setUI()
        self.setmodel()

    def setmodel(self):
        self.model = load_model('models/cnn_v1.hdf5')

    
    def drawLine(self, event):
        self.canv.create_oval(event.x - self.brush_size,
                              event.y - self.brush_size,
                              event.x + self.brush_size,
                              event.y + self.brush_size,
                              fill = self.brush_color, 
                              outline = self.brush_color)
        self.draw.ellipse([(event.x - self.brush_size,
                            event.y - self.brush_size),
                           (event.x + self.brush_size,
                            event.y + self.brush_size)],
                          fill = self.brush_color,
                          outline = self.brush_color)

    
    def guess(self, event = None):
        x = np.expand_dims(np.array(self.image.resize((28,28)))/255., axis=0)
        res = self.model.predict(x, verbose=0)
        self.number['text'] = 'The number: %d'%np.argmax(res)
        self.number.config(font = ("Courier", 12))
        self.number.pack()
        # self.btn_guess["state"] = DISABLED

    
    def clean(self, event = None):
        self.canv.delete('all')
        self.draw.rectangle([0, 0, self.canvas_size, self.canvas_size], 
                            fill = self.canvas_backg)
        self.number['text'] = ''
        # self.btn_guess["state"] = NORMAL

    
    def insImage(self, event = None):
        self.imgage = ImageTk.PhotoImage(self.image.resize((28,28))\
                                .resize((self.canvas_size, self.canvas_size)))
    
        self.canv.delete('all')
        self.canv.create_image(0,0, anchor = 'nw', image = self.imgage)

    
    def setUI(self):
        self.parent.title("Number Guesser")
        self.pack(fill = BOTH, expand = 1)

        self.lbl = Label(self, text = 'Draw a number:', pady = 10)
        self.lbl.config(font = ("Courier", 12))
        self.lbl.pack()
        
        self.canv = Canvas(self, 
                           width = self.canvas_size, 
                           height = self.canvas_size, 
                           background = self.canvas_backg)
        self.canv.pack()

        self.image = Image.new('L', 
                              (self.canvas_size, self.canvas_size), 
                              self.canvas_backg)
        self.draw = ImageDraw.Draw(self.image)

        self.canv.bind("<B1-Motion>", self.drawLine)
        self.canv.bind("<Leave>", self.insImage)

        self.btn_clean = Button(self, text = "Clean", command = self.clean)
        self.btn_clean.pack(pady = 5)
        
        self.btn_guess = Button(self, text = "Guess", command = self.guess)
        self.btn_guess.pack(pady = 5)
        
        self.number = Label(self)
        


def main():
    root = Tk()
    root.geometry("500x450+%d+%d" % 
                  (root.winfo_screenwidth()/3, root.winfo_screenheight()/5))
    app = GuessN(root)
    root.mainloop()


if __name__ == "__main__":
    main()