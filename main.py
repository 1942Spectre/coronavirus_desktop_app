import gi
from corona import get_df,get_country 
import matplotlib.pyplot as plt
import seaborn as sns


gi.require_version("Gtk" , "3.0")

from gi.repository import Gtk as gtk

class Main:
    def __init__(self):
        glade_file = "corona.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(glade_file)
        self.builder.connect_signals(self)

        self.df = get_df()

        country_names = self.df["Country"].values



        self.total_confirmed = self.builder.get_object("total_confirmed")
        self.new_confirmed = self.builder.get_object("new_confirmed")


        self.total_deaths = self.builder.get_object("total_deaths")
        self.new_deaths = self.builder.get_object("new_deaths")


        self.total_recovered = self.builder.get_object("total_recovered")
        self.new_recovered = self.builder.get_object("new_recovered")

        self.death_rate = self.builder.get_object("death_rate")
        self.recovery_rate = self.builder.get_object("recovery_rate")

        self.combo = self.builder.get_object("combo")

        countries = self.builder.get_object("countries")

        self.date = self.builder.get_object("date")
        self.country_name = self.builder.get_object("country_name")

        self.most_new = self.builder.get_object("most_new")
        self.most_confirmed = self.builder.get_object("most_confirmed")


        for country in country_names:
            countries.append([country])

        

        self.most_confirmed.set_text( str(self.df.sort_values(by = "TotalConfirmed",ascending = False).iloc[0]["Country"]))
        self.most_new.set_text( str(self.df.sort_values(by = "NewConfirmed",ascending = False).iloc[0]["Country"]))


        window = self.builder.get_object("Main")

        window.connect("delete-event",gtk.main_quit)
        window.show()

        #### Button
        button1 = self.builder.get_object("button1")
        
        button1.connect("clicked",self.button_1_click)

        plot_button = self.builder.get_object("plot_button")
        
        plot_button.connect("clicked",self.plot_button_click)


    def button_1_click(self , widget):

        selected_country = self.combo.get_text()
        country_data = get_country(selected_country , df=self.df)

        self.total_confirmed.set_text(str(country_data["TotalConfirmed"].values[0])) 
        self.new_confirmed.set_text(str(country_data["NewConfirmed"].values[0]))


        self.total_deaths.set_text(str(country_data["TotalDeaths"].values[0]))
        self.new_deaths.set_text(str(country_data["NewDeaths"].values[0]))

        self.total_recovered.set_text(str(country_data["TotalRecovered"].values[0]))
        self.new_recovered.set_text(str(country_data["NewRecovered"].values[0]))

        self.recovery_rate.set_text("%" + str(100*country_data["TotalRecovered"].values[0] / country_data["TotalConfirmed"].values[0])[:6])
        self.death_rate.set_text("%" + str(100*country_data["TotalDeaths"].values[0] / country_data["TotalConfirmed"].values[0])[:6])

        self.date.set_text(str(country_data["Date"].values[0]))
        self.country_name.set_text(str(country_data["Country"].values[0]))

    def plot_button_click(self,widget):

        by = self.builder.get_object("by_combo").get_text()
        n = self.builder.get_object("n").get_text()

        print(by)
        print(n)

        ordered_df = self.df.sort_values(by = by , ascending = False)

        ordered_df = ordered_df.head(int(n))

        sns.barplot(x = "Country" , y = by , data = ordered_df)
        plt.show()







if __name__ == "__main__":
    main = Main()
    gtk.main()