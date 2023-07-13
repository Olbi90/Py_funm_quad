from userinterface.mainwindow.mainwindow import MainWindow
from userinterface.mainwindow.loadingscreen import LoadingScreen

loading_screen = LoadingScreen()
root = MainWindow()
loading_screen.quit()
root.mainloop()          