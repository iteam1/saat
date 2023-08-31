import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class AnnotationTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Annotation Tool")

        self.canvas = tk.Canvas(self.root, cursor="cross")
        self.canvas.pack()

        self.bbox_list = []
        self.current_bbox = None

        self.load_button = tk.Button(self.root, text="Load Image", command=self.load_image)
        self.load_button.pack()

        self.save_button = tk.Button(self.root, text="Save Annotations", command=self.save_annotations)
        self.save_button.pack()

        self.canvas.bind("<Button-1>", self.start_bbox)
        self.canvas.bind("<B1-Motion>", self.draw_bbox)
        self.canvas.bind("<ButtonRelease-1>", self.end_bbox)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.image = Image.open(file_path)
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo)

    def start_bbox(self, event):
        self.bbox_list.append((event.x, event.y))
        self.current_bbox = self.canvas.create_rectangle(event.x, event.y, event.x, event.y, outline="red")

    def draw_bbox(self, event):
        self.canvas.coords(self.current_bbox, self.bbox_list[-1][0], self.bbox_list[-1][1], event.x, event.y)

    def end_bbox(self, event):
        self.bbox_list[-1] = (self.bbox_list[-1][0], self.bbox_list[-1][1], event.x, event.y)
        self.current_bbox = None

    def save_annotations(self):
        annotation_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if annotation_file:
            with open(annotation_file, "w") as f:
                for bbox in self.bbox_list:
                    f.write(f"{bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = AnnotationTool(root)
    root.mainloop()
