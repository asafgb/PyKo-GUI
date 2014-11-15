#!/usr/bin/env python
# makes it possible to run the file as a script invoking the interpreter implicitly, e.g. in a CGI context.

__author__ = "Daniel Koifman, Alexander Putilin"
__copyright__ = "Copyright 2014, Daniel Koifman, Alexander Putilin"
__credits__ = ["Daniel Koifman, Alexander Putilin"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Daniel Koifman"
__email__ = "primeless42@gmail.com"
__status__ = "Development"


# Written by Daniel Koifman(A.K.A HeliosHype) and Alexander Putilin
# You are allowed to freely use, edit, modify and distribute this software, just make sure to give proper credit :)
# Also, if you want to contribute to the code, fork it. Once you're done, send in a pull request.
# Github: https://github.com/Koifman/PyKo-GUI
# Please make sure do properly document your contribution!


from Tkinter import *
from tkFileDialog import *
from ttk import *
from bs4 import BeautifulSoup
from threading import Thread
from tkMessageBox import *
import requests, pafy, os


class Application(Frame):
    def __init__(self, master=None):
        self.killDownload = False
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def setFlag(self):
        self.killDownload = True


    def progressCallback(self, totalBytes, bytesDownloaded, ratio, rate, eta):
        self.progress.config(maximum=totalBytes, value=bytesDownloaded)
        self.label3.config(text="Download rate: %.0f KBPS     ETA: %.0f Seconds" % (rate, eta))
        if totalBytes == bytesDownloaded:
            self.label3.config(text="Download finished successfully!")

        if self.killDownload:
            self.progress.config(value=0)
            self.label3.config(text="Download aborted!")
            self.label4.config(text="You can still download another song.")
            self.killDownload = False
            raise Exception("Aborted Download")

    def downloadSong(self, soup_url):
        link_to_download = ""
        # stream_url = ""
        source_code2 = requests.get(soup_url, verify=False) # Need a way to include youtube's certificate
        plain_text2 = source_code2.text
        soup2 = BeautifulSoup(plain_text2)
        selected_item = self.lb.get(ACTIVE)
        for title in soup2.findAll('a', {'title': selected_item}):
            link_to_download = "http://www.youtube.com" + title.get("href")
            # stream_url = title.get("href").split("=")[1]

        video = pafy.new(link_to_download)
        # stream = pafy.new(stream_url)
        best = video.getbest(preftype="mp4")
        best.download(quiet=True, filepath=self.pathName, callback=self.progressCallback)


    def filedialog(self):
        getUser = os.getenv('USERNAME')
        #Need to change this line to support Linux
        self.pathName = askdirectory(initialdir="C:\\Users\\" + getUser + "\\Desktop", title="Where do you want to save the song?")
        self.v.set(self.pathName)

    def begin_query(self, s1, s2, list):
        if s1 == "" and s2 == "":
            showerror("Error", "Can't query an empty string!")
        else:
            rsn = s1.replace(" ", "+")
            ran = s2.replace(" ", "+")
            self.url = "https://www.youtube.com/results?search_query=%s+%s" % (rsn, ran)
            self.slist = list
            source_code = requests.get(self.url, verify=False) # Need a way to include youtube's certificate
            plain_text = source_code.text
            self.soup = BeautifulSoup(plain_text)
            for SongTitle in self.soup.findAll('a', {'class': 'yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink     spf-link '}):
                self.slist.append(SongTitle.string)


            self.main()

    def createWidgets(self):
        label1 = Label(text="Name of song: ").place(x=60, y=7)
        label2 = Label(text="Name of artist: ").place(x=60, y=38)
        self.label3 = Label(text="")
        self.label3.place(x=120, y=350)
        self.label4 = Label(text="")
        self.label4.place(x=120, y=370)

        entry1 = Entry(width=20)
        entry1.place(x=180, y=6.5)

        entry2 = Entry(width=20)
        entry2.place(x=180, y=37.5)

        self.v = StringVar()
        self.entry3 = Entry(width=40, textvariable=self.v, state='readonly')
        self.entry3.place(y=280, x=60)

        songs_list = []
        b1 = Button(text="Search", command=lambda: self.begin_query(entry1.get(), entry2.get(), songs_list))
        b1.place(x=330, y=5)

        b2 = Button(text="Save as...", command=self.filedialog)
        b2.place(y=277.5, x=310)

        b3 = Button(text="Download", command=lambda: Thread(target=self.downloadSong, args=(self.url,)).start())
        b3.place(y=35, x=330)

        b4 = Button(text="Kill Download", command=self.setFlag)
        b4.place(y=70, x=327)

        self.lb = Listbox(width=50)
        self.lb.place(x=60, y=100)

        self.scrollbar = Scrollbar(root)
        self.scrollbar.place(x=365, y=100, height=165)

        self.lb.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lb.yview)

        self.progress = Progressbar(orient="horizontal", length=330, mode="determinate")
        self.progress.place(y=320, x=60)

    def main(self):
        for item in self.slist:
            self.lb.insert(END, item)




root = Tk()
root.iconbitmap('icon.ico')
root.title("PyKo GUI")
root.geometry("450x450+500+300")
root.resizable(0, 0)
app = Application(master=root)
app.mainloop()
