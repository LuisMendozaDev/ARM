from tkinter import tix

class View(object):
    def __init__(self, root):
        self.root = root
        self.makeCheckList()

    def makeCheckList(self):
        self.cl = tix.CheckList(self.root, browsecmd=self.selectItem, width=400, height=300)
        self.cl.pack()
        
        # Set background color to light gray
        self.cl.hlist.config(bg="#f0f0f0")

        # First checklist
        self.cl.hlist.add("CL1", text="checklist1")
        self.cl.setstatus("CL1", "off")

        for i in range(1, 5):
            item_name = f"CL1.Item{i}"
            self.cl.hlist.add(item_name, text=f"subitem{i}")
            self.cl.setstatus(item_name, "off")

        # Second checklist
        self.cl.hlist.add("CL2", text="checklist2")
        self.cl.setstatus("CL2", "off")

        for i in range(1, 5):
            item_name = f"CL2.Item{i}"
            self.cl.hlist.add(item_name, text=f"subitem{i}")
            self.cl.setstatus(item_name, "off")

        # Add more checklists and items as needed

        self.cl.autosetmode()

    def selectItem(self, item):
        print(item, self.cl.getstatus(item))

def main():
    root = tix.Tk()
    view = View(root)
    root.update()
    root.mainloop()

if __name__ == '__main__':
    main()