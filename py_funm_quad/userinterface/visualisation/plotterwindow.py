import sys
import tkinter as tk
import tkinter.ttk as ttk

import numpy as np
import matplotlib as matp
import matplotlib.pyplot as plt

from userinterface.visualisation.database import Database

# https://stackoverflow.com/questions/4971269/how-to-pick-a-new-color-for-each-plotted-line-within-a-figure-in-matplotlib
# was used as help for the lines 521-529 to create multiple colors

class PlotterWindow(tk.Toplevel):
    """ With PlotterWindow you can create plots from your Database. """

    def __init__(self, master, database:Database):
        """ Plotterwindow with the opportunity to plot data from one solving,
        compare two solvings or print general parameters from all solvings.
        """

        tk.Toplevel.__init__(self, master)
        # Window
        self.focus()
        if sys.platform == 'win32':
            self.style = ttk.Style(self)
            self.style.theme_use('vista')
        # Window size and middle of the screen   
        self.title('Plot Settings')
        window_width = str(int(self.winfo_screenwidth()/2))
        window_height = str(int(self.winfo_screenheight()/2))
        self.geometry(#window_width + 'x' + window_height 
            '+' + str(int(self.winfo_screenwidth()/2)
            - int(int(window_width)/2))
            + '+' + str(int(self.winfo_screenheight()/2)
            - int(int(window_height)/2)))
        self.resizable(True,True)

        # Database
        self.database = database
        # Variables
        self.__var_plot_number = tk.StringVar(self, value='one')
        self.__var_database_length = int(self.database.index.max())
        self.__var_step = int(self.database.at[0,'Cycles'])
        self.__var_plot_step = tk.IntVar(self, value=self.__var_step)
        self.__var_plot_step_one = tk.IntVar(self, value=self.__var_step)
        self.__var_plot_step_two = tk.IntVar(self, value=self.__var_step)

        # FRAMES
        # Mainframe 
        self.frame_main = tk.LabelFrame(self, relief='groove', text='Settings')
        self.frame_main.grid(
            row=0, column=0, padx=(5,5), pady=(5,5), sticky=tk.NSEW)        
        # Plotcategories
        self.frame_plotnumber = tk.LabelFrame(
            self.frame_main, relief='groove', text='How many plots?')
        self.frame_plotnumber.grid(
            row=0, column=0, padx=(5,5), pady=(5,5), sticky=tk.NSEW)
        # Frame one plot
        self.frame_one_plotdetails = tk.LabelFrame(
            self.frame_main, relief='groove', text='One plot')
        self.frame_one_plotdetails.grid(
            row=0, column=1, padx=(5,5), pady=(5,5), sticky=tk.NSEW)
        # Frame two plot
        self.frame_two_plotdetails = tk.LabelFrame(
            self.frame_main, relief='groove', text='Two plots')
        self.frame_two_plotdetails.grid(
            row=0, column=1, padx=(5,5), pady=(5,5), sticky=tk.NSEW)
        self.frame_two_plotdetails.grid_remove()
        # Frame all plot
        self.frame_all_plotdetails = tk.LabelFrame(
            self.frame_main, relief='groove', text='All plot')
        self.frame_all_plotdetails.grid(
            row=0, column=1, padx=(5,5), pady=(5,5), sticky=tk.NSEW)
        self.frame_all_plotdetails.grid_remove()

        # Radiobuttons
        self.radio_one_plot = ttk.Radiobutton(
            self.frame_plotnumber, text='One plot',
            variable=self.__var_plot_number, value='one',
            command= self.__radio_function)
        self.radio_one_plot.grid(
            row=0, column=0, padx=(5,5), pady=(5,5), ipadx=5, ipady=5,
            sticky=tk.W)
        self.radio_one_plot.invoke()
        self.radio_two_plot = ttk.Radiobutton(
            self.frame_plotnumber, text='Two plots', 
            variable=self.__var_plot_number, value='two', 
            command= self.__radio_function)
        self.radio_two_plot.grid(
            row=1, column=0, padx=(5,5), pady=(5,5), 
            ipadx=5, ipady=5, sticky=tk.W)
        self.radio_all_plot = ttk.Radiobutton(
            self.frame_plotnumber, text='General plot', 
            variable=self.__var_plot_number, value='all', 
            command= self.__radio_function)
        self.radio_all_plot.grid(
            row=2, column=0, padx=(5,5), pady=(5,5), ipadx=5, ipady=5,
            sticky=tk.W)

        # One Plot Layout
        one_plot_details = list(['Eigenvalues','Time','Error_norms'])
        self.__var_plot_index = tk.IntVar(self, 0)       
        # Create a dictionary for looping the checkboxes
        self.__var_one_plotdetails = dict(
            zip(one_plot_details,one_plot_details))
        # Create Checkboxes for the Attributes to plot
        for value in self.__var_one_plotdetails:
            self.__var_one_plotdetails[value] = tk.StringVar(self, value='0')
            self.plt_details = ttk.Checkbutton(
                self.frame_one_plotdetails, text=str(value), 
                variable=self.__var_one_plotdetails[value], 
                onvalue=value, offvalue='0')
            self.plt_details.grid(padx=5, pady=5, sticky=tk.W)
        # Label
        self.label_database_index = ttk.Label(
            self.frame_one_plotdetails, 
            text=self.database.at[self.__var_plot_index.get(),'Name'])
        self.label_database_index.grid(padx=(5,5), pady=(5,5), sticky=tk.NSEW)
        # Scale Index
        self.scale_index = tk.Scale(
            self.frame_one_plotdetails, label='Solver to plot', 
            orient='horizontal', from_=0, to=self.__var_database_length, 
            showvalue=1, variable=self.__var_plot_index, 
            command= lambda arg1=self.__var_plot_index.get(), 
            arg2=self.label_database_index: self.__show_index_name(arg1,arg2))
        self.scale_index.grid(padx=(5,5), pady=(5,5), ipadx=5, ipady=5,
            sticky=tk.W)
        # Scale Restart Step
        self.scale_step = tk.Scale(
            self.frame_one_plotdetails, label='Restart Cycle', 
            orient='horizontal', from_=1, to=self.__var_step, 
            showvalue=1, variable=self.__var_plot_step)
        self.scale_step.grid(padx=(5,5), pady=(5,5), ipadx=5, ipady=5,
            sticky=tk.W)
        # Buttons
        self.button_plot = ttk.Button(
            self.frame_one_plotdetails, text='Plot Data', 
            command= self.__plot_one_plot)
        self.button_plot.grid(padx=(5,5), pady=(5,5), sticky=tk.NSEW)

        # Two Plot Layout
        two_plot_details = list(['Eigenvalues','Time', 'Error_norms'])
        self.__var_plot_index_one = tk.IntVar(self, 0)
        self.__var_plot_index_two = tk.IntVar(self, 0)
        # Create a dictionary for looping the checkboxes
        self.__var_two_plotdetails = dict(
            zip(two_plot_details,two_plot_details))
        # Create Checkboxes for the Attributes to plot
        for value in self.__var_two_plotdetails:
            self.__var_two_plotdetails[value] = tk.StringVar(self, value='0')
            self.plt_details = ttk.Checkbutton(
                self.frame_two_plotdetails, text=str(value), 
                variable=self.__var_two_plotdetails[value], 
                onvalue=value, offvalue='0')
            self.plt_details.grid(padx=5, pady=5, sticky=tk.W)
        # Label plot one
        self.label_database_index_one = ttk.Label(
            self.frame_two_plotdetails, 
            text=self.database.at[self.__var_plot_index_one.get(),'Name'])
        self.label_database_index_one.grid(
            padx=(5,5), pady=(5,5), sticky=tk.NSEW)
        # Scale plot one
        self.scale_index = tk.Scale(
            self.frame_two_plotdetails, label='Solver to plot', 
            orient='horizontal', from_=0, to=self.__var_database_length, 
            showvalue=1, variable=self.__var_plot_index_one, 
            command= lambda arg1=self.__var_plot_index_one.get(), 
            arg2=self.label_database_index_one: self.__show_index_name(arg1, arg2))
        self.scale_index.grid(padx=(5,5), pady=(5,5), ipadx=5, ipady=5,
            sticky=tk.W)
        # Scale plot Restart Step
        self.scale_step_one = tk.Scale(
            self.frame_two_plotdetails, label='Restart Cycle', 
            orient='horizontal', from_=1, to=self.__var_step, 
            showvalue=1, variable=self.__var_plot_step_one)
        self.scale_step_one.grid(padx=(5,5), pady=(5,5), ipadx=5, ipady=5,
            sticky=tk.W)
        # Label plot two
        self.label_database_index_two = ttk.Label(
            self.frame_two_plotdetails, 
            text=self.database.at[self.__var_plot_index_two.get(),'Name'])
        self.label_database_index_two.grid(
            padx=(5,5), pady=(5,5), sticky=tk.NSEW)
        # Scale plot two
        self.scale_index = tk.Scale(
            self.frame_two_plotdetails, label='Solver to plot', 
            orient='horizontal', from_=0, to=self.__var_database_length, 
            showvalue=1, variable=self.__var_plot_index_two, 
            command= lambda arg1=self.__var_plot_index_two.get(), 
            arg2=self.label_database_index_two: self.__show_index_name(arg1,arg2))
        self.scale_index.grid(padx=(5,5), pady=(5,5), ipadx=5, ipady=5,
            sticky=tk.W)
        # Scale plot Restart Step
        self.scale_step_two = tk.Scale(
            self.frame_two_plotdetails, label='Restart Cycle', 
            orient='horizontal', from_=1, to=self.__var_step, 
            showvalue=1, variable=self.__var_plot_step_two)
        self.scale_step_two.grid(padx=(5,5), pady=(5,5), ipadx=5, ipady=5,
            sticky=tk.W)
        # Buttons
        self.button_plot_two = ttk.Button(self.frame_two_plotdetails, 
                                     text='Plot Data', 
                                     command= self.__plot_two_plot)
        self.button_plot_two.grid(padx=(5,5), pady=(5,5), sticky=tk.NSEW)

        # General Plot Layout
        all_plot_details = list(['Time', 'Error_norms'])
        # Create a dictionary for looping the checkboxes
        self.__var_all_plotdetails = dict(
            zip(all_plot_details,all_plot_details))
        # Create Checkboxes for the Attributes to plot
        for value in self.__var_all_plotdetails:
            self.__var_all_plotdetails[value] = tk.StringVar(self, value='0')
            self.plt_details = ttk.Checkbutton(
                self.frame_all_plotdetails, text=str(value), 
                variable=self.__var_all_plotdetails[value], 
                onvalue=value, offvalue='0')
            self.plt_details.grid(padx=5, pady=5, sticky=tk.W)
        # Buttons
        self.button_plot_all = ttk.Button(self.frame_all_plotdetails, 
                                     text='Plot Data', 
                                     command= self.__plot_all_plot)
        self.button_plot_all.grid(padx=(5,5), pady=(5,5), sticky=tk.NSEW)

    # Radiobuttons
    def __radio_function(self):
        """ Choose wich type of plot you want to use. """

        value = self.__var_plot_number.get()
        if value == 'one':
            self.frame_one_plotdetails.grid()
            self.frame_two_plotdetails.grid_remove()
            self.frame_all_plotdetails.grid_remove()
        elif value == 'two':
            self.frame_one_plotdetails.grid_remove()
            self.frame_two_plotdetails.grid()
            self.frame_all_plotdetails.grid_remove()
        elif value == 'all':
            self.frame_one_plotdetails.grid_remove()
            self.frame_two_plotdetails.grid_remove()
            self.frame_all_plotdetails.grid()

    # Scale
    def __show_index_name(self, value, label):
        """ Change the label text, to let the user know 
        wich solving is selected. 
        """

        label.config(text= self.database.at[int(value),'Name'])
        self.__var_step = int(self.database.at[int(value),'Cycles'])
        if label == self.label_database_index:
            self.scale_step.config(to=self.__var_step)
        if label == self.label_database_index_one:
            self.scale_step_one.config(to=self.__var_step)
        if label == self.label_database_index_two:
            self.scale_step_two.config(to=self.__var_step)

    def __load_string_to_array(self, index, what):
        """ Because of the actual circumstances the Error_norms and Eigenvalues
        are stored es lists in the Dataframe. This function is a workaround to
        read them in and transform them into a numpy array."""

        data = self.database.at[index,what]
        new_data = data.replace('[','')
        new_data = new_data.replace(']','')
        new_data = new_data.replace('(','')
        new_data = new_data.replace(')','')
        new_data = new_data.replace(' ', '')
        data_list = new_data.split(',')
        new_array = np.array(data_list)
        
        return new_array

    def __plot_one_plot(self):
        """ Plot for one solving. 
        Actual supported Time, Eigenvalues and Error Norms.
        """

        plt.close('Eigenvalues')
        index = self.__var_plot_index.get()
        cycle = self.__var_plot_step.get()
        eigenval = self.__var_one_plotdetails['Eigenvalues'].get()
        time = self.__var_one_plotdetails['Time'].get()
        error_norms = self.__var_one_plotdetails['Error_norms'].get()
        new_shape_1 = int(self.database.at[index,'Length'])
        new_shape_2 = int(self.database.at[index,'Cycles'])

        if eigenval != '0':
            plt.close('Eigenvalues')
            if type(self.database.at[index,'Eigenvalues']) == str:
                new_array = self.__load_string_to_array(index, 'Eigenvalues')
                new_array.shape = (new_shape_1,new_shape_2)
                new_array = new_array.astype(np.complex64)
            else:
                new_array = self.database.at[index,'Eigenvalues']
                new_array = np.array(new_array)
                new_array.shape = (new_shape_1,new_shape_2)
                new_array = new_array.astype(np.complex64)

            ax = plt.figure().add_subplot(projection='3d')
            ax.scatter(new_array[cycle-1,:].real, 
                       new_array[cycle-1,:].imag, zs=0, zdir='y', 
                       label=('Eigenvalues in {}. Cycle'.format(cycle)))
            ax.legend()
            ax.set_xlabel('Real')
            ax.set_zlabel('Imag')

        if time != '0':
            plt.close('Time')
            
            tcomplete = float(self.database.at[index,'Time_complete'])
            tarnoldi = float(self.database.at[index,'Time_arnoldi'])
            tmxa = float(self.database.at[index,'Time_mult_A'])
            tscalar = float(self.database.at[index,'Time_scalar'])
            tquadrature = float(self.database.at[index,'Time_quadrature'])
            tapproxf = float(self.database.at[index,'Time_approx_f'])

            x_overview = np.array(['Overview', 'Arnoldi'])
            list_overview = list(
                ['Complete','Arnoldi','Quadratur','Approximation'])
            y_overview = np.array([tcomplete,tarnoldi,tquadrature,tapproxf])
            list_arnoldi = list(['Arnoldi','Mult. A', 'Scalar'])
            y_arnoldi = np.array([tarnoldi,tmxa,tscalar])
            fig, axe = plt.subplots(num='Time')
            x_axe = np.arange(len(x_overview))
            for i in range(len(y_overview)):
                axe.bar(x_axe[0] + 0.2*i, y_overview[i], width=0.2, 
                        label=list_overview[i])
            for i in range(len(y_arnoldi)):
                axe.bar(x_axe[1] + 0.2*i, y_arnoldi[i], width=0.2, 
                        label=list_arnoldi[i])
            fig.suptitle('Runtime')
            axe.set_xticks(x_axe,x_overview)
            axe.set_ylabel('Time in sec.')
            axe.legend()

        if error_norms != '0':
            plt.close('Error Norms')
            if self.database.at[index,'Error_norms'] == 'No exact solution given':
                fig, axe = plt.subplots(num='Error Norms')
                x_axe = np.array([0,1])
                y_axe = np.array([1,0])
                axe.plot(x_axe, y_axe, '-r')
                axe.plot(y_axe, y_axe, '-r')
            else:
                if type(self.database.at[index,'Error_norms']) == str:
                    new_ev_array = self.__load_string_to_array(index, 'Error_norms')
                    new_ev_array = new_ev_array.astype(np.float64)
                else:
                    new_ev_array = self.database.at[index,'Error_norms'][0]

                new_ev_array = np.around(new_ev_array,4)
                fig, axe = plt.subplots(num='Error Norms')
                x_axe = np.arange(0,len(new_ev_array),1)
                axe.plot(x_axe, new_ev_array, 'o-r', label=self.database.at[index,'Name'])
                axe.set_title('Error Norms')
                axe.set_xlabel('Restart Cycle')
                axe.grid()
                axe.legend()
        
        plt.draw()
        plt.show()

    def __plot_two_plot(self):
        """ Plot for two solvings. 
        Actual supported Time, Eigenvalues and Error Norms.
        """
        index_one = self.__var_plot_index_one.get()
        index_two = self.__var_plot_index_two.get()
        cycle_one = self.__var_plot_step_one.get()
        cycle_two = self.__var_plot_step_two.get()

        eigenval = self.__var_two_plotdetails['Eigenvalues'].get()
        time = self.__var_two_plotdetails['Time'].get()
        error_norms = self.__var_two_plotdetails['Error_norms'].get()
        new_shape_one_1 = int(self.database.at[index_one,'Length'])
        new_shape_one_2 = int(self.database.at[index_one,'Cycles'])
        new_shape_two_1 = int(self.database.at[index_two,'Length'])
        new_shape_two_2 = int(self.database.at[index_two,'Cycles'])
        if eigenval != '0':
            plt.close('Eigenvalues')
            if type(self.database.at[index_one,'Eigenvalues']) == str:
                # Plot one
                new_array_one = self.__load_string_to_array(index_one, 'Eigenvalues')
                new_array_one.shape = (new_shape_one_1,new_shape_one_2)
                new_array_one = new_array_one.astype(np.complex64)
            else:
                new_array = self.database.at[index_one,'Eigenvalues']
                new_array_one = np.array(new_array)
                new_array_one.shape = (new_shape_one_1,new_shape_one_2)
                new_array_one = new_array_one.astype(np.complex64)
            
            # Plot two
            if type(self.database.at[index_two,'Eigenvalues']) == str:
                new_array_two = self.__load_string_to_array(index_two, 'Eigenvalues')
                new_array_two.shape = (new_shape_two_1,new_shape_two_2)
                new_array_two = new_array_two.astype(np.complex64)
            else:
                new_array = self.database.at[index_two,'Eigenvalues']
                new_array_two = np.array(new_array)
                new_array_two.shape = (new_shape_two_1,new_shape_two_2)
                new_array_two = new_array_two.astype(np.complex64)
            
            ax = plt.figure().add_subplot(projection='3d')
            ax.scatter(new_array_one[cycle_one-1,:].real, new_array_one[cycle_one-1,:].imag, 
                       zs=0, zdir='y', label=self.database.at[index_one,'Name'])
            ax.scatter(new_array_two[cycle_two-1,:].real, new_array_two[cycle_two-1,:].imag, 
                       zs=0, zdir='y', label=self.database.at[index_two,'Name'])
            
            ax.set_xlabel('Real')
            ax.set_zlabel('Imag')
            ax.legend()

        if time != '0':
            plt.close('Time')
            # Plot One
            tcomplete = float(self.database.at[index_one,'Time_complete'])
            tarnoldi = float(self.database.at[index_one,'Time_arnoldi'])
            tmxa = float(self.database.at[index_one,'Time_mult_A'])
            tscalar = float(self.database.at[index_one,'Time_scalar'])
            tquadrature = float(self.database.at[index_one,'Time_quadrature'])
            tapproxf = float(self.database.at[index_one,'Time_approx_f'])

            x_overview = np.array(['Overview', 'Arnoldi'])
            list_overview = list(
                ['Complete','Arnoldi','Quadratur','Approximation'])
            y_overview = np.array([tcomplete,tarnoldi,tquadrature,tapproxf])
            list_arnoldi = list(['Arnoldi','Mult. A', 'Scalar'])
            y_arnoldi = np.array([tarnoldi,tmxa,tscalar])
            fig, (axe_one, axe_two) = plt.subplots(
                1,2, sharey=True, num='Time')
            fig.suptitle('Time to Solve')
            x_axe = np.arange(len(x_overview))

            for i in range(len(y_overview)):
                axe_one.bar(x_axe[0] + 0.2*i, y_overview[i], width=0.2, 
                            label=list_overview[i])
            for i in range(len(y_arnoldi)):
                axe_one.bar(x_axe[1] + 0.2*i, y_arnoldi[i], width=0.2, 
                            label=list_arnoldi[i])
            axe_one.set_xticks(x_axe,x_overview)
            axe_one.set_ylabel('Time in sec.')
            axe_one.set_title(self.database.at[index_one,'Name'])
            axe_one.legend()

            # Plot two
            tcomplete = float(self.database.at[index_two,'Time_complete'])
            tarnoldi = float(self.database.at[index_two,'Time_arnoldi'])
            tmxa = float(self.database.at[index_two,'Time_mult_A'])
            tscalar = float(self.database.at[index_two,'Time_scalar'])
            tquadrature = float(self.database.at[index_two,'Time_quadrature'])
            tapproxf = float(self.database.at[index_two,'Time_approx_f'])

            x_overview = np.array(['Overview', 'Arnoldi'])
            list_overview = list(
                ['Complete','Arnoldi','Quadratur','Approximation'])
            y_overview = np.array([tcomplete,tarnoldi,tquadrature,tapproxf])
            list_arnoldi = list(['Arnoldi','Mult. A', 'Scalar'])
            y_arnoldi = np.array([tarnoldi,tmxa,tscalar])

            for i in range(len(y_overview)):
                axe_two.bar(x_axe[0] + 0.2*i, y_overview[i], width=0.2, 
                            label=list_overview[i])
            for i in range(len(y_arnoldi)):
                axe_two.bar(x_axe[1] + 0.2*i, y_arnoldi[i], width=0.2, 
                            label=list_arnoldi[i])
            axe_two.set_xticks(x_axe,x_overview, rotation=45)
            axe_two.set_ylabel('Time in sec.')
            axe_two.set_title(self.database.at[index_two,'Name'])
            axe_two.legend()
        
        if error_norms != '0':
            plt.close('Error Norms')
            fig, axe = plt.subplots(num='Error Norms')
            if self.database.at[index_one,'Error_norms'] != 'No exact solution given':
                if type(self.database.at[index_one,'Error_norms']) == str:
                    new_ev_array_one = self.__load_string_to_array(index_one, 'Error_norms')
                    new_ev_array_one  = new_ev_array_one.astype(np.float64)
                else:
                    new_ev_array_one = self.database.at[index_one,'Error_norms'][0]

                new_ev_array_one = np.around(new_ev_array_one,4)
                x_axe_one = np.arange(0,len(new_ev_array_one),1)
                axe.plot(x_axe_one, new_ev_array_one, 'o-r', 
                     label=self.database.at[index_one, 'Name'])

            if self.database.at[index_two,'Error_norms'] != 'No exact solution given':
                if type(self.database.at[index_two,'Error_norms']) == str:
                    new_ev_array_two = self.__load_string_to_array(index_two, 'Error_norms')
                    new_ev_array_two = new_ev_array_two.astype(np.float64)
                else:
                    new_ev_array_two = self.database.at[index_two,'Error_norms'][0]

                new_ev_array_two = np.around(new_ev_array_two,4)
                x_axe_two = np.arange(0,len(new_ev_array_two),1)
                axe.plot(x_axe_two, new_ev_array_two, '^-g', 
                     label=self.database.at[index_two, 'Name'])        
            
            axe.set_title('Error Norms')
            axe.set_xlabel('Restart Cycle')
            axe.grid()
            axe.legend()

        plt.draw()
        plt.show()

    def __plot_all_plot(self):
        """ Plot for all solvings. 
        Actual supported Time, Eigenvalues and Error Norms.
        """

        time = self.__var_all_plotdetails['Time'].get()
        error_norms = self.__var_all_plotdetails['Error_norms'].get()

        if time != '0':
            plt.close('Time')
            x_axe = self.database['Name'].to_list()
            x_num = np.array(np.arange(0,self.__var_database_length+1,1))
            y_axe = self.database['Time_complete'].to_list()
            fig, axe = plt.subplots(num='Time')
            axe.bar(x_num,y_axe)
            axe.set_ylabel('Time in sec.')
            plt.xticks(x_num,x_axe, rotation = 45)                

        if error_norms != '0':
            plt.close('Error Norms')
            print_error_norms = list()
            for i in range(self.__var_database_length + 1):
                if self.database.at[i,'Error_norms'] != 'No exact solution given':
                    if type(self.database.at[i,'Error_norms']) == str:
                        new_ev_array = self.__load_string_to_array(i,'Error_norms')
                        new_ev_array = new_ev_array.astype(np.float64)
                    else:
                        new_ev_array = self.database.at[i,'Error_norms'][0]
                else:
                    new_ev_array = np.array([0,0])

                new_ev_array = np.around(new_ev_array,4)
                print_error_norms.append(new_ev_array)

            fig, axe = plt.subplots(num='Error Norms')
            colors = matp.cm.get_cmap('rainbow')
            colors = colors(np.linspace(0,1,self.__var_database_length + 1))
            colors = iter(colors)
            for i in range(self.__var_database_length + 1):
                line_color = next(colors)
                x_axe = np.arange(0,len(print_error_norms[i]),1)
                axe.plot(x_axe,print_error_norms[i],color=line_color,
                         label=self.database.at[i,'Name'])
                
            axe.set_title('Error Norms')
            axe.set_xlabel('Restart Cycle')
            axe.grid()
            axe.legend()

        plt.draw()
        plt.show()