import cv2
import os
import sys
import time
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkinter import *

class VideoConverterApp:
    def __init__(self, master):
        self.filePath = ""
        self.outputFolderPath = ""
        self.outputFormat = StringVar()
        self.outputFormat.set("jpg") 

        self.create_widgets(master)

    def create_widgets(self, master):
        Label(master, text="Video:", width=20).grid(row=0, column=0)
        Button(master, text="Select", command=self.select_video, width=10).grid(row=0, column=1)

        Label(master, text="Output-Folder:", width=20).grid(row=1, column=0)
        Button(master, text="Select", command=self.select_output_folder, width=10).grid(row=1, column=1)

        Label(master, text="Output Format:", width=20).grid(row=2, column=0)
        format_menu = OptionMenu(master, self.outputFormat, "jpg", "png")
        format_menu.grid(row=2, column=1)

        Button(master, text="Start", command=self.convert_video_to_images, width=10).grid(row=3, column=0)

        self.progress = ttk.Progressbar(master, orient=HORIZONTAL, length=100, mode='determinate')
        self.progress.grid(row=3, column=1)

    def select_video(self):
        self.filePath = filedialog.askopenfilename(
            initialdir="C:\\",
            title="Select input-file",
            filetypes=(("input-file", "*.mp4 *.avi *.wmv"), ("all files", "*.*"))
        )
        print("Selected Video: \t" + self.filePath)

    def select_output_folder(self):
        self.outputFolderPath = filedialog.askdirectory(title="Select output folder")
        print("Selected Folder: \t" + self.outputFolderPath)

    def convert_video_to_images(self):
        if not self.filePath:
            messagebox.showwarning("Warning", "Please select a video file.")
            return

        video = cv2.VideoCapture(self.filePath)
        number_of_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        date = time.strftime("%d-%m-%Y")
        local_time = time.strftime("%H-%M-%S")
        timed_output_folder_path = os.path.join(self.outputFolderPath, f"{date}_{local_time}")
        print("Final Output-Folder: \t" + timed_output_folder_path)

        if not os.path.exists(timed_output_folder_path):
            os.makedirs(timed_output_folder_path)

        success, image = video.read()
        i = 0
        success = True
        while success:
            success, image = video.read()
            if success:
                output_extension = self.outputFormat.get()
                output_filename = f"frame{i}.{output_extension}"
                output_path = os.path.join(timed_output_folder_path, output_filename)

                cv2.imwrite(output_path, image)

                self.progress['value'] = int((i / number_of_frames) * 100)
                self.progress.update_idletasks()

                if cv2.waitKey(10) == 27:
                    break
                i += 1
            else:
                sys.exit()

if __name__ == "__main__":
    root = Tk()
    root.title("Video Converter")
    app = VideoConverterApp(root)
    root.mainloop()
