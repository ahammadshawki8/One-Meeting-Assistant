# All imports 
import mm_backend as mm
import kivy
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.screenmanager import NoTransition
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.base import runTouchApp
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image


# Setting up few things
Config.set('graphics', 'height', 680)
Config.set('graphics', 'width', 380)
Config.set('graphics', 'resizable', 0)
Config.write()

    
# GetStarted class
class GetStarted(Screen):
    def go_to_MainPanel(self):
        sm.add_widget(MainPanel(name="MainPanel"))
        sm.transition = SlideTransition(direction = "left")
        sm.current = "MainPanel"
        

# MainPanel class
class MainPanel(Screen):
    def go_to_website(self):
        mm.go_to_website()

    def go_to_AddPanel(self):
        sm.add_widget(AddPanel(name="AddPanel"))
        sm.transition = SlideTransition(direction = "left")
        sm.current = "AddPanel"

    def go_to_SearchPanel(self):
        sm.add_widget(SearchPanel(name="SearchPanel"))
        sm.transition = SlideTransition(direction = "left")
        sm.current = "SearchPanel"

    def go_to_Docs(self):
        mm.go_to_readme()


# AddPanel Class
class AddPanel(Screen):
    def go_to_website(self):
        mm.go_to_website()

    def go_to_AddMeeting(self, category):
        sm.add_widget(AddMeeting(category, name="AddMeeting"))
        sm.transition = SlideTransition(direction = "left")
        sm.current = "AddMeeting"

    def go_back(self):
        for screen in sm.screens:
            if screen.name == "AddPanel":
                sm.screens.remove(screen)
        sm.transition = SlideTransition(direction = "right")
        sm.current = "MainPanel"

# AddMeeting Class
class AddMeeting(Screen):
    def __init__(self, category, **kwargs):
        super().__init__(**kwargs)
        self.category = category
        
        self.info_grid = GridLayout()
        self.info_grid.cols = 2
        self.info_grid.size_hint = 0.9, 0.4
        self.info_grid.pos_hint = {"x": 0.05, "top": 0.65}
        self.time_label = Button(text = "Meeting Time:", font_size = 14, color = (1,1,1,1), background_color = (0/255, 153/255, 204/255, 1))
        self.info_grid.add_widget(self.time_label)
        if self.category == "daily":
            self.time_value = TextInput(text="HH:MM", multiline = False)
        elif self.category == "weekly":
            self.time_value = TextInput(text="WWW, HH:MM", multiline = False)
        else:
            self.time_value = TextInput(text="YYYY-MM-DD, HH:MM", multiline = False)
        self.info_grid.add_widget(self.time_value)
        self.meeting_id_label = Button(text = "Meeting ID:", font_size = 14, color = (1,1,1,1), background_color = (0/255, 153/255, 204/255, 1))
        self.info_grid.add_widget(self.meeting_id_label)
        self.meeting_id_value = TextInput(multiline = False)
        self.info_grid.add_widget(self.meeting_id_value)
        self.passcode_label = Button(text = "Passcode:", font_size = 14, color = (1,1,1,1), background_color = (0/255, 153/255, 204/255, 1))
        self.info_grid.add_widget(self.passcode_label)
        self.passcode_value = TextInput(multiline = False, password = True)
        self.info_grid.add_widget(self.passcode_value)
        self.organizer_label = Button(text = "Organizer:", font_size = 14, color = (1,1,1,1), background_color = (0/255, 153/255, 204/255, 1))
        self.info_grid.add_widget(self.organizer_label)
        self.organizer_value = TextInput(multiline = False)
        self.info_grid.add_widget(self.organizer_value)
        self.subject_label = Button(text = "Meeting Subject:", font_size = 14, color = (1,1,1,1), background_color = (0/255, 153/255, 204/255, 1))
        self.info_grid.add_widget(self.subject_label)
        self.subject_value = TextInput(multiline = False)
        self.info_grid.add_widget(self.subject_value)
        self.meeting_link_label = Button(text = "Browsable Link:", font_size = 14, color = (1,1,1,1), background_color = (0/255, 153/255, 204/255, 1))
        self.info_grid.add_widget(self.meeting_link_label)
        self.meeting_link_value = TextInput(multiline = False)
        self.info_grid.add_widget(self.meeting_link_value)

        self.add_widget(self.info_grid)
        self.submit_button = Button(text = "Add Meeting", italic = True, font_size = 18, color = (1,1,1,1), background_color = (0/255, 153/255, 204/255, 1))
        self.submit_button.size_hint = 0.4, 0.06
        self.submit_button.pos_hint = {"x":0.3,"top": 0.2}
        self.add_widget(self.submit_button)
        self.submit_button.bind(on_release = lambda x: self.write_to_json())

    def write_to_json(self):
        self.category = self.category
        self.meeting_id = self.meeting_id_value.text
        self.passcode = self.passcode_value.text
        self.organizer = self.organizer_value.text
        self.subject = self.subject_value.text
        self.meeting_link = self.meeting_link_value.text
        self.meeting_time = self.time_value.text

        try:
            mm.add_meeting(self.category, self.meeting_id, self.passcode, self.meeting_link, self.organizer, self.subject, self.meeting_time)
        except:
            show_AddMeetingPop()
        
        self.meeting_id_value.text = ""
        self.passcode_value.text = ""
        self.organizer_value.text = ""
        self.subject_value.text = ""
        self.meeting_link_value.text = ""
        if self.category == "daily":
            self.time_value.text = "HH:MM"
        elif self.category == "weekly":
            self.time_value.text = "WWW, HH:MM"
        else:
            self.time_value.text = "YYYY-MM-DD, HH:MM"


    def go_to_website(self):
        mm.go_to_website()

    def go_back(self):
        for screen in sm.screens:
            if screen.name == "AddMeeting":
                sm.screens.remove(screen)
        sm.transition = SlideTransition(direction = "right")
        sm.current = "AddPanel"

# Add Meeting PopUp
class AddMeetingPop(FloatLayout):
    pass

def show_AddMeetingPop():
    show = AddMeetingPop()
    popup_window = Popup(title = "ADD MEETING ERROR", content = show, size_hint = (0.9, 0.2))
    popup_window.open()
    

# SearchPanel class
class SearchPanel(Screen):
    def go_to_website(self):
        mm.go_to_website()

    def go_to_AllMeeting(self):
        sm.add_widget(AllMeeting(name="AllMeeting"))
        sm.transition = SlideTransition(direction = "left")
        sm.current = "AllMeeting"

    def go_to_UpcomingMeeting(self):
        sm.add_widget(UpcomingMeeting(name="UpcomingMeeting"))
        sm.transition = SlideTransition(direction = "left")
        sm.current = "UpcomingMeeting"

    def go_to_PastMeeting(self):
        sm.add_widget(PastMeeting(name="PastMeeting"))
        sm.transition = SlideTransition(direction = "left")
        sm.current = "PastMeeting"

    def go_back(self):
        for screen in sm.screens:
            if screen.name == "SearchPanel":
                sm.screens.remove(screen)
        sm.transition = SlideTransition(direction = "right")
        sm.current = "MainPanel"


# All Meeting class
class AllMeeting(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.info_grid = GridLayout()
        self.info_grid.cols = 2
        self.info_grid.size_hint = 0.9, 0.4
        self.info_grid.pos_hint = {"x": 0.05, "top": 0.615}
        self.organizer_query_label = Button(text = "Organizer:", font_size = 14, color = (1,1,1,1), background_color = (0/255, 153/255, 204/255, 1))
        self.info_grid.add_widget(self.organizer_query_label)
        self.organizer_query_value = TextInput(multiline = False)
        self.info_grid.add_widget(self.organizer_query_value)
        self.subject_query_label = Button(text = "Subject:", font_size = 14, color = (1,1,1,1), background_color = (0/255, 153/255, 204/255, 1))
        self.info_grid.add_widget(self.subject_query_label)
        self.subject_query_value = TextInput(multiline = False)
        self.info_grid.add_widget(self.subject_query_value)
        self.weekday_query_label = Button(text = "Weekday:", font_size = 14, color = (1,1,1,1), background_color = (0/255, 153/255, 204/255, 1))
        self.info_grid.add_widget(self.weekday_query_label)
        self.weekday_query_value = TextInput(multiline = False)
        self.info_grid.add_widget(self.weekday_query_value)
        self.date_query_label = Button(text = "Date:", font_size = 14, color = (1,1,1,1), background_color = (0/255, 153/255, 204/255, 1))
        self.info_grid.add_widget(self.date_query_label)
        self.date_query_value = TextInput(text= "YYYY-MM-DD", multiline = False)
        self.info_grid.add_widget(self.date_query_value)
        self.add_widget(self.info_grid)

        self.submit_button = Button(text = "Show Meeting", italic = True, font_size = 18, color = (1,1,1,1), background_color = (0/255, 153/255, 204/255, 1))
        self.submit_button.size_hint = 0.4, 0.06
        self.submit_button.pos_hint = {"x":0.3,"top": 0.17}
        self.add_widget(self.submit_button)
        self.submit_button.bind(on_release = lambda x: self.show_all_meeting())


    def show_all_meeting(self):
        self.organizer_query = "all" if self.organizer_query_value.text.strip() == "" else self.organizer_query_value.text.strip()
        self.subject_query = "all" if self.subject_query_value.text.strip() == "" else self.subject_query_value.text.strip()
        self.weekday_query = "all" if self.weekday_query_value.text.strip() == "" else self.weekday_query_value.text.strip()
        self.date_query = "all" if (self.date_query_value.text.strip() == "") or (self.date_query_value.text.strip() == "YYYY-MM-DD") else self.date_query_value.text.strip()
        
        try:
            queries = {"organizer":self.organizer_query, "subject":self.subject_query, "weekday":self.weekday_query, "date":self.date_query}
            info= mm.show_all_meetings(queries)
            sm.add_widget(MeetingDisplayer("AllMeeting", info, name="MeetingDisplayer"))
            sm.transition = SlideTransition(direction = "left")
            sm.current = "MeetingDisplayer"
            
        except:
            show_AllMeetingPop()

        self.organizer_query_value.text = ""
        self.subject_query_value.text = ""
        self.weekday_query_value.text = ""
        self.date_query_value.text = "YYYY-MM-DD"


    def go_to_website(self):
        mm.go_to_website()

    def go_back(self):
        for screen in sm.screens:
            if screen.name == "AllMeeting":
                sm.screens.remove(screen)
        sm.transition = SlideTransition(direction = "right")
        sm.current = "SearchPanel"

# Add Meeting PopUp
class AllMeetingPop(FloatLayout):
    pass

def show_AllMeetingPop():
    show = AllMeetingPop()
    popup_window = Popup(title = "SHOW ALL MEETING ERROR", content = show, size_hint = (0.9, 0.2))
    popup_window.open()


# Upcoming Meeting class
class UpcomingMeeting(Screen):
    def go_to_website(self):
        mm.go_to_website()

    def go_back(self):
        for screen in sm.screens:
            if screen.name == "UpcomingMeeting":
                sm.screens.remove(screen)
        sm.transition = SlideTransition(direction = "right")
        sm.current = "SearchPanel"


# Past Meeting class
class PastMeeting(Screen):
    def go_to_website(self):
        mm.go_to_website()

    def go_back(self):
        for screen in sm.screens:
            if screen.name == "PastMeeting":
                sm.screens.remove(screen)
        sm.transition = SlideTransition(direction = "right")
        sm.current = "SearchPanel"


# Meeting Displayer Class
class MeetingDisplayer(Screen):
    def __init__(self,back,info,**kwargs):
        super().__init__(**kwargs)
        self.back = back
        self.info = info

        self.headings = []
        for meeting in self.info:
            meeting_subject = meeting["meeting_subject"]
            meeting_organizer = meeting["meeting_organizer"]
            time = meeting["time"]
            heading = f"{meeting_subject} | {meeting_organizer} | {time}"
            self.headings.append(heading)
        
        self.scroller = ScrollView()
        self.scroller.pos_hint = {"x": 0.1, "top": 0.75}
        self.scroller.size_hint = (0.8, 0.63)
        
        self.info_grid = GridLayout()
        self.info_grid.cols = 1
        if len(self.headings) > 20:
            self.info_grid.size_hint = 1, 2
        elif len(self.headings) > 10:
            self.info_grid.size_hint = 1, 1.4
        elif len(self.headings) > 5: 
            self.info_grid.size_hint = 1, 0.8
        else:
            self.info_grid.size_hint = 1, 0.35
        

        for heading in self.headings:
            self.meet_topic = Button(text = heading, font_size = 15, color = (1,1,1,1), background_color = (0/255, 153/255, 204/255, 1))
            self.info_grid.add_widget(self.meet_topic)
            self.meet_topic.bind(on_release = lambda x: self.explain(heading))
        self.scroller.add_widget(self.info_grid)

        self.footer = Image(
            source= 'resources/footer.png',
            size_hint = (0.98, 0.8),
            pos_hint= {"x": 0.01, "top": .135},
            size_hint_y=None, 
            height=100
        )
        self.add_widget(self.scroller)
        self.add_widget(self.footer)

    def explain(self, heading):
        subject, organizer, time = heading.split(" | ")
        for meeting in self.info:
            if meeting["meeting_subject"] == subject and meeting["meeting_organizer"] == organizer and meeting["time"] == time:
                sm.add_widget(MeetingInformation(meeting, name="MeetingInformation"))
                sm.transition = SlideTransition(direction = "left")
                sm.current = "MeetingInformation"

    def go_to_website(self):
        mm.go_to_website()

    def go_back(self):
        for screen in sm.screens:
            if screen.name == "MeetingDisplayer":
                sm.screens.remove(screen)
        sm.transition = SlideTransition(direction = "right")
        sm.current = self.back
        

# Meeting Information class
class MeetingInformation(Screen):
    def __init__(self, meeting, **kwargs):
        super().__init__(**kwargs)
        self.meeting = meeting

        self.info_grid = GridLayout()
        self.info_grid.cols = 2
        self.info_grid.size_hint = 0.9, 0.4
        self.info_grid.pos_hint = {"x": 0.05, "top": 0.67}
        self.category_label = Button(text = "Category:", font_size = 14, color = (1,1,1,1), background_color = (0/255, 153/255, 204/255, 1))
        self.info_grid.add_widget(self.category_label)
        self.category_value = Label(text = meeting["category"], font_size = 14, color = (0,0,0,1))
        self.info_grid.add_widget(self.category_value)
        self.time_label = Button(text = "Time:", font_size = 14, color = (1,1,1,1), background_color = (0/255, 153/255, 204/255, 1))
        self.info_grid.add_widget(self.time_label)
        self.time_value = Label(text = meeting["time"], font_size = 14, color = (0,0,0,1))
        self.info_grid.add_widget(self.time_value)
        self.subject_label = Button(text = "Subject:", font_size = 14, color = (1,1,1,1), background_color = (0/255, 153/255, 204/255, 1))
        self.info_grid.add_widget(self.subject_label)
        self.subject_value = Label(text = meeting["meeting_subject"], font_size = 14, color = (0,0,0,1))
        self.info_grid.add_widget(self.subject_value)
        self.organizer_label = Button(text = "Organizer:", font_size = 14, color = (1,1,1,1), background_color = (0/255, 153/255, 204/255, 1))
        self.info_grid.add_widget(self.organizer_label)
        self.organizer_value = Label(text = meeting["meeting_organizer"], font_size = 14, color = (0,0,0,1))
        self.info_grid.add_widget(self.organizer_value)
        self.meeting_id_label = Button(text = "Meeting ID:", font_size = 14, color = (1,1,1,1), background_color = (0/255, 153/255, 204/255, 1))
        self.info_grid.add_widget(self.meeting_id_label)
        self.meeting_id_value = Label(text = str(meeting["meeting_id"]), font_size = 14, color = (0,0,0,1))
        self.info_grid.add_widget(self.meeting_id_value)
        self.passcode_label = Button(text = str("Meeting Passcode:"), font_size = 14, color = (1,1,1,1), background_color = (0/255, 153/255, 204/255, 1))
        self.info_grid.add_widget(self.passcode_label)
        self.passcode_value = Label(text = meeting["passcode"], font_size = 14, color = (0,0,0,1))
        self.info_grid.add_widget(self.passcode_value)
        self.activation_status_label = Button(text = "Activation Status:", font_size = 14, color = (1,1,1,1), background_color = (0/255, 153/255, 204/255, 1))
        self.info_grid.add_widget(self.activation_status_label)
        self.activation_status_value = Label(text = str(meeting["active"]), font_size = 14, color = (0,0,0,1))
        self.info_grid.add_widget(self.activation_status_value)
        self.add_widget(self.info_grid)

        self.activision_button = Button(text = "DEACTIVATE MEETING", underline = True, font_size = 12, color = (0/255, 153/255, 204/255, 1), background_color = (1,1,1,0))
        self.activision_button.size_hint = 0.4, 0.06
        self.activision_button.pos_hint = {"x":0.3,"top": 0.23}
        self.add_widget(self.activision_button)
        self.activision_button.bind(on_release = lambda x: self.activision_function())

        self.join_button = Button(text = "JOIN MEETING", italic = True, font_size = 18, color = (1,1,1,1), background_color = (0/255, 153/255, 204/255, 1))
        self.join_button.size_hint = 0.4, 0.06
        self.join_button.pos_hint = {"x":0.3,"top": 0.17}
        self.add_widget(self.join_button)
        self.join_button.bind(on_release = lambda x: self.join_meeting())

    def activision_function(self):
        if self.activation_status_value.text == "True":
            mm.deactivate_meeting(self.organizer_value.text, self.subject_value.text, self.time_value.text)
            self.activation_status_value.text = "False"
            self.activision_button.text = "ACTIVATE MEETING"
        else:
            mm.activate_meeting(self.organizer_value.text, self.subject_value.text, self.time_value.text)
            self.activation_status_value.text = "True"
            self.activision_button.text = "DEACTIVATE MEETING"

    def join_meeting(self):
        try:
            mm.join_meeting(self.meeting["meeting_link"])
        except:
            show_ErrorLinkPop()

    def go_to_website(self):
        mm.go_to_website()

    def go_back(self):
        for screen in sm.screens:
            if screen.name == "MeetingInformation":
                sm.screens.remove(screen)
        sm.transition = SlideTransition(direction = "right")
        sm.current = "MeetingDisplayer"

# Error Link PopUp
class ErrorLinkPop(FloatLayout):
    pass

def show_ErrorLinkPop():
    show = ErrorLinkPop()
    popup_window = Popup(title = "MEETING LINK ERROR", content = show, size_hint = (0.9, 0.2))
    popup_window.open()







# Some tasks before the running the file
kv = Builder.load_file("mm_frontend.kv")
sm = ScreenManager(transition = SlideTransition())
screens = [
    GetStarted(name="GetStarted")
    ]

for screen in screens:
    sm.add_widget(screen)
sm.current = "GetStarted"


# main class
class MMApp(App):
    def build(self):
        Window.clearcolor = (0.85,0.85,0.85,1)
        return sm


# Running the entire file
if __name__ == "__main__":
    MMApp().run()