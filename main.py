# kivy specific modules 
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import  NoTransition , ScreenManager 
from kivy.core.text import LabelBase
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty , NumericProperty , ObjectProperty
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.clock import Clock
# kivymd components modules 
from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.icon_definitions import md_icons
from kivymd.font_definitions import theme_font_styles
from kivymd.uix.list import ThreeLineAvatarListItem , ImageLeftWidget , OneLineAvatarIconListItem 
from kivymd.uix.list import IconLeftWidget
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDIconButton
from kivymd.uix.button import MDFlatButton

# other modules 
import os , re , random , smtplib , json , requests 
from functools import partial
from email.message import EmailMessage
# imports form local 
from credentials.envar import Envar
from encryptions import Encrypter
from google_auth import initialize_google, login_google, logout_google
# -----------------screemanager---------------
class WindowManager(ScreenManager):
    def androidBackClick(self , window , key , *args):
        # if someone press escape button or back on android so  change the screen accordangly 
        if key == 27:
            if self.current == "RegisterScreen":
                self.current = "LoginScreen"
            else:
                self.current = "PostsScreen"
            
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = NoTransition()
        Window.bind(on_keyboard = self.androidBackClick)



# global classes or functions
def sendMail(email, subject,content):
    try:
        # creating a session 
        session = smtplib.SMTP("smtp.gmail.com", 587)
        # start TLS security 
        session.starttls()
        # Authentication
        session.login("ZeroTwoApplication@gmail.com", "Aanchal911@gmail.com")
        # creating a message 
        message = EmailMessage()
        # adding content to message 
        message.set_content(content)
        # adding subject,From and To to message
        message["Subject"] = subject
        message["From"] = "ZeroTwoApplication@gmail.com"
        message["To"] = email
        # sending the mail 
        session.send_message(message)
        # termination the session 
        session.quit()
        return True
    except:
        return False


def checkMail(email):
    # Make a regular expression
    # for validating an Email
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return True
 
    else:
        return False
# -----------------Otp button class ----------------
class OtpButton(MDFlatButton):
    count = NumericProperty(30)
    def reverseText(self , animation , watch):
            self.count = 30
            self.text = "Get OTP"
            # making button color blue 
            self.theme_text_color = "Custom"
            self.text_color= [135/255,206/255,235/255,1]
    def start(self):
        Animation.cancel_all(self)
        self.anima = Animation(count = 0, duration = self.count)
        self.anima.bind(on_complete = self.reverseText)
        self.anima.start(self)
    def on_count(self , instance , value):
        currentCount = str(int(round(value , 1)))
        self.text =f"Resend in {currentCount}s" 

# front page short blog details class Note : Short class
class BlogDetails(ThreeLineAvatarListItem):
    imageSource = StringProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        leftImage = ImageLeftWidget(source = self.imageSource)
        self.add_widget(leftImage)
#---------------------- tab class for main section Note: short class-------------------------
class Tab(ScrollView, MDTabsBase):
    pass

#---------------------- nav_label class for top navigation left drawer Note: short class-------------------------
class NavLabel(OneLineAvatarIconListItem):
    icon = StringProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        left_icon = IconLeftWidget(icon = self.icon)
        self.add_widget(left_icon)
        
#---------------------------- App class ------------------------------------
class ZeroTwoApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    # global class variables 
    otp = ""
    email = ""
    # Setions from the data base 
    Sections = {"facts":"head-lightbulb" , "science projects":"test-tube" , "wild life":"panda", "funny":"star-face", "history":"history", "tech":"language-java" , "space" :"space-station", "news":"newspaper"}
    def getdata(self , instance):
        return f"your section is {instance.title}"
    def build(self):
        # ---------------------------------icon setting -------------------
        self.icon = "static/logo.jpeg"
        #------------------------------coustom font -------------------------
        # requstring new font name inside kivy label base 
        LabelBase.register(name="helvetica" , fn_regular="static/Helveticamazing.ttf")
        # adding that font name inside kivymd
        theme_font_styles.append('helvetica')
        # changing font default settings 
        self.theme_cls.font_styles["helvetica"] = [
            "helvetica",
            16,
            False,
            0.15,
        ]
        # setting theeme default color 
        self.theme_cls.set_colors(
            "Brown", "A700", "50", "800", "Teal", "600", "100", "800"
        )
        # adding theme style to dark 
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file("main.kv")

    def on_start(self):
        # Adding main sections 
        for section ,icon in self.Sections.items():
            self.root.current_screen.ids.tabs.add_widget(Tab(icon=icon , title=section))
        # adding labels to Navigation drawer 
        # this is for sharing application 
        self.root.current_screen.ids.nav_drawer_list.add_widget(NavLabel(text = "Share Zero2",icon = "share-variant-outline" , on_release = self.shareApp))
        # this is settings label 
        self.root.current_screen.ids.nav_drawer_list.add_widget(NavLabel(text = "Settings",icon = "cog" , on_release = self.settings))
        # this is logic for login logout state 
        if os.path.exists("credentials/user.id"):
            # if user is loged in 
            self.root.current_screen.ids.nav_drawer_list.add_widget(NavLabel(text = "Logout",icon = "logout" , on_release = self.logoutUser))
            # if user id is correct 
            ValidityStatus , user_id = self.ValidUserID()
            print(ValidityStatus , user_id)
            if ValidityStatus == True:
                # trying to add user name and his email address to navigation drawer 
                try:
                    # getting user id 
                    self.root.current_screen.ids.nav_name.text = str(user_id)
                except:
                    pass
            # id user id is  not correct 
            else:
                Snackbar(
                    text = f"Your Login credentials are not right. Try logout",
                    duration = 1,
                    snackbar_x=dp(10),
                    snackbar_y=dp(10),
                    size_hint_x=.8,
                    pos_hint = {"center_x":.5},
                    radius = [10],
                    buttons = [
                        MDIconButton(
                            icon = "exclamation-thick",
                            
                        )
                    ]
                ).open()

        else:
            self.root.current_screen.ids.nav_drawer_list.add_widget(NavLabel(text = "Login",icon = "login" , on_release = partial(self.changeRootScreen , "LoginScreen")))


            
    def postItem(self,instance_tab, image , *args):
        instance_tab.ids.postslist.add_widget(BlogDetails(
                imageSource = str("./movies/"+image),
                text= "Title of the post",
                secondary_text= "TV-MA | 30 Comedy,Horrer,News",
                tertiary_text= "More details about movies " ,
                on_press = self.moreBlogDetails
            ))
    def on_tab_switch(
        self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):
        '''
        Called when switching tabs.

        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        '''
        # get the tab icon.
        count_icon = instance_tab.icon
        # print it on shell/bash.
        # adding movies acording to section
        for count , image in enumerate(os.listdir("./movies")):
            delay_time = count/2
            Clock.schedule_once(partial(self.postItem ,instance_tab,image),delay_time)
        
        print(f"Welcome to {count_icon}' tab'")
    def moreBlogDetails(self, instance):
        print(instance.text)
    def menu(self):
        print("yes you are in menu")
    # this is for checking that user id in user.id file is correct or not 
    def ValidUserID(self):
        try:
            with open("credentials/user.id", "r") as cred_file:
                id = Encrypter.decryptText(cred_file.read())
                # trying to make user_id to integer 
                user_id = int(id)
                # if user id is correct so checking its exextance in database 
                print("JUFFLER check ID existance in database ")
                ValidityStatus = True
                return ValidityStatus, user_id
        except:
            ValidityStatus = False
            user_id = None
            return ValidityStatus , user_id
        
    def changeRootScreen(self , screenName  , *args):
        self.root.current = screenName
    def isValidMail(self , textField, optButton):
        # if email is wrong 
        if not checkMail(textField.text):
            textField.error = True
            textField.helper_text = "not a valid Email ID"
            # making opt button red 
            optButton.theme_text_color = "Custom"
            optButton.text_color= [1,0,0,.8]
        else:
            textField.error = False
            textField.helper_text = "Email ID is required"
            # make opt button blue 
            optButton.theme_text_color = "Custom"
            optButton.text_color= [135/255,206/255,235/255,1]
    # this is logic to send otp 
    def sendOtp(self , emailAddress  ,mail_subject  ,msg_content, *args):
            # if mail got send so display tost of success 
            if sendMail(emailAddress,mail_subject,msg_content):
                Snackbar(
                    text = f"Successfully sent to your Email ID {emailAddress}",
                    duration = 1,
                    snackbar_x=dp(10),
                    snackbar_y=dp(10),
                    size_hint_x=.8,
                    pos_hint = {"center_x":.5},
                    radius = [10],
                    buttons = [
                        MDIconButton(
                            icon = "robot-happy-outline",
                            
                        )
                    ]
                ).open()
            else:
                # if email not send 
                Snackbar(
                    text = f"Can't sent to your Email ID {emailAddress} , Check Internet connection",
                    duration = 1,
                    snackbar_x=dp(10),
                    snackbar_y=dp(10),
                    size_hint_x=.8,
                    pos_hint = {"center_x":.5},
                    radius = [10],
                    buttons = [
                        MDIconButton(
                            icon = "exclamation-thick",
                            
                        )
                    ]
                ).open()

        

    def makeOtp(self, otpButton, textField ):
        # if email is empty 
        if textField.text.replace(" ", "") == "" or textField.error:
            # making text red 
            otpButton.theme_text_color = "Custom"
            otpButton.text_color= [1,0,0,.8]
            Snackbar(
                text = "Email ID is not valid" ,
                duration = .5,
                snackbar_x=dp(10),
                snackbar_y=dp(10),
                size_hint_x=.8,
                pos_hint = {"center_x":.5},
                radius = [10],
                buttons = [
                    MDIconButton(
                        icon = "information",
                        
                    )
                ]
                ).open()
        # if email ID is not empty  
        else:
            # getting email address 
            emailAddress = textField.text
            # changing btn color to green 
            otpButton.theme_text_color = "Custom"
            otpButton.text_color= [75/255,181/255,67/255,1]
            # start countdown for Resend opt 
            OtpButton.start(otpButton)
              # sending an otp if "Get Otp" in text of button
            if str(otpButton.text).lower().replace(" ", "") == "getotp":
                # making a random otp and save both otp and email to global variables 
                self.otp = random.randint(1000 , 9999)
                self.email = emailAddress
                # making subject to sending mail 
                mail_subject = "OTP Verification"
                # making mail to send 
                msg_content = f"Welcome to ZeroTwoApplication. To join our services, we need you to quick verify your email adress. Use the code to complete sign up on ZeroTwo.\nVerification Code: {self.otp}\nDo not forward and share this code to anyone.\nSincerely,\nTeamZeroTwo"
                # calling sendOtp function 
                Clock.schedule_once(partial(self.sendOtp, self.email , mail_subject , msg_content) , 1.5)
            else:
                # msg to show in tost alert 
                secondsLeft =str(otpButton.text).split("in")[1]
                mssg = f"Wait for {secondsLeft} and Try again !"
                Snackbar(
                    text = mssg,
                    duration = .5,
                    snackbar_x=dp(10),
                    snackbar_y=dp(10),
                    size_hint_x=.8,
                    pos_hint = {"center_x":.5},
                    radius = [10],
                    buttons = [
                        MDIconButton(
                            icon = "information",
                            
                        )
                    ]
                ).open()

    # checking if otp is valid 4 digit alpha numeric character or not 
    def checkOtp(self, instance):
        if not instance.text.isnumeric():
            instance.helper_text = "OTP must in digit"
            instance.error = True
        elif len(instance.text) > 4:
            instance.helper_text = "OTP must of 4 digit"
        elif len(instance.text) == 4:
            instance.focus = False
            instance.error = False
        else:
            instance.helper_text = "OTP is required"
            instance.error = False
    def shareApp(self, instance):
        print(instance)
    # -------------------main functions for application pages ----------------------------
    def settings(self , *args):
        print("I am settings")
    def registerUserThroughGoogleAuth(self):
        # callback functions for initilixe_google function
        def register_succed(name , email , photo_url):
            print(name , email , photo_url)
            # Clock.schedule_once(partial(self.createNewUser, name , email ,photo_url),1)
        def register_error():
             # msg to show in tost alert of error while registring
            Snackbar(
                text = "Register Failed check your Internet connection",
                duration = .5,
                snackbar_x=dp(10),
                snackbar_y=dp(10),
                size_hint_x=.8,
                pos_hint = {"center_x":.5},
                radius = [10],
                buttons = [
                    MDIconButton(
                        icon = "exclamation-thick",
                        
                    )
                ]
            ).open()
        # opening json client file 
        with open("credentials/client.json" , "r") as f:
            credentials = json.load(f)
        # getting data from client.json file 
        client_id = credentials["installed"]["client_id"]
        client_secret = credentials["installed"]["client_secret"]
        # initialize google
        initialize_google(register_succed , register_error ,client_id=client_id , client_secret=client_secret)
        # making login request 
        login_google()
    # this is for mannual register 
    def registerUser(self , pageInstance):
        emailField = pageInstance.ids.textField
        optField = pageInstance.ids.otpField
        fullName = pageInstance.ids.nameField
        # if Fullname ,textField or otp are empty so generate error
        if optField.text.replace(" ","") == "":
            optField.error = True
            optField.focus = True
        if emailField.text.replace(" ","") == "":
            emailField.error = True
            emailField.focus = True
        if fullName.text.replace(" ","") == "":
            fullName.error = True
            fullName.focus = True
        # handling errors 
        if optField.error:
            optField.focus = True
        if emailField.error:
            emailField.focus = True
        if fullName.error:
            fullName.focus = True
        else:
            # checking is opt correct 
            # initilizing user otp  
            userOtp = 0
            # trying to assign user OTP 
            try:
                userOtp = int(optField.text)
            except:
                pass
            if self.otp == userOtp and self.email == emailField.text:
                # creating new user | Note : it return true if user get created
                created_responce = self.createNewUser(fullName.text , emailField.text)
                # resetting all fields if user get created succfully
                if created_responce == True:
                    # resetting all text fields 
                    fullName.text = "***"
                    emailField.text = "***"
                    optField.text = "***"
                else:
                    pass
            else:
                optField.error = True
                optField.focus = True
                optField.helper_text = "OTP is incorrect"
    def useless(self):
        '''this function is useless because googleauth logout needs callback'''
    def createNewUser(self , name , email , photo_url = None , *args):
        try:
            # -----------------checking if user already exists ------------------
            req = requests.get(f"{Envar.base_api}/is_exists",
                            params={"key": Envar.auth_key, "email": email})
            # if the request is not SUCCESSed so showing error msg to user
            if req.status_code != 200:
                Snackbar(
                    text=f"Internal server error, Tell this to owner",
                    duration=1,
                    snackbar_x=dp(10),
                    snackbar_y=dp(10),
                    size_hint_x=.8,
                    pos_hint={"center_x": .5},
                    radius=[10],
                    buttons=[
                        MDIconButton(
                            icon="exclamation-thick",

                        )
                    ]
                ).open()
            # if request get SUCCESSed
            else:
                # getting responce from api {is_exists}
                responce = req.json()
                # if key was wrong
                if responce["key_error"]:
                    Snackbar(
                        text=f"Internal server error, Tell this to owner",
                        duration=1,
                        snackbar_x=dp(10),
                        snackbar_y=dp(10),
                        size_hint_x=.8,
                        pos_hint={"center_x": .5},
                        radius=[10],
                        buttons=[
                            MDIconButton(icon="exclamation-thick",)
                        ]
                    ).open()
                # if key was right
                else:
                    if responce["existance"] == True:
                        Snackbar(
                            text=f"Account already exists with this gmail Try other gmail",
                            duration=1,
                            snackbar_x=dp(10),
                            snackbar_y=dp(10),
                            size_hint_x=.8,
                            pos_hint={"center_x": .5},
                            radius=[10],
                            buttons=[
                                MDIconButton(icon="exclamation-thick",)
                            ]
                        ).open()
                    # is user doesn't exists so create new one
                    else:
                        
                        # create user request
                        creat_user_req = requests.post(f"{Envar.base_api}/create_user", params={
                                                    "key": Envar.auth_key}, json={"name":  name, "mail": email})
                        
                        # if request not get SUCCESSed
                        if creat_user_req.status_code != 200:
                            Snackbar(
                                text=f"Internal server error, Tell this to owner",
                                duration=1,
                                snackbar_x=dp(10),
                                snackbar_y=dp(10),
                                size_hint_x=.8,
                                pos_hint={"center_x": .5},
                                radius=[10],
                                buttons=[
                                    MDIconButton(icon="exclamation-thick",)
                                ]
                            ).open()
                        # if request get SUCCESSed
                        else:
                            create_request_responce = creat_user_req.json()
                            if create_request_responce["key_error"]:
                                Snackbar(
                                    text=f"Internal server error, Can't create user",
                                    duration=1,
                                    snackbar_x=dp(10),
                                    snackbar_y=dp(10),
                                    size_hint_x=.8,
                                    pos_hint={"center_x": .5},
                                    radius=[10],
                                    buttons=[
                                        MDIconButton(icon="exclamation-thick",)
                                    ]
                                ).open()
                            # checking is user is added or not
                            else:
                                # if user is added successfully
                                if create_request_responce["user_added"] == True or create_request_responce["status"] == True:
                                    Snackbar(
                                        text=f"Successfully created account with {email} email",
                                        duration=1,
                                        snackbar_x=dp(10),
                                        snackbar_y=dp(10),
                                        size_hint_x=.8,
                                        pos_hint={"center_x": .5},
                                        radius=[10],
                                        buttons=[
                                            MDIconButton(icon="sticker-check-outline",)
                                        ]
                                    ).open()
                                    self.loginUser(create_request_responce["id"])
                                    return True
                                # is user not added
                                else:
                                    Snackbar(
                                        text=f"Something wrong happened Try again later..",
                                        duration=1,
                                        snackbar_x=dp(10),
                                        snackbar_y=dp(10),
                                        size_hint_x=.8,
                                        pos_hint={"center_x": .5},
                                        radius=[10],
                                        buttons=[
                                            MDIconButton(icon="exclamation-thick",)
                                        ]
                                    ).open()
        except:
            Snackbar(
                text=f"Registration Failed Please check your Internet-connection ",
                duration=1,
                snackbar_x=dp(10),
                snackbar_y=dp(10),
                size_hint_x=.8,
                pos_hint={"center_x": .5},
                radius=[10],
                buttons=[
                    MDIconButton(icon="exclamation-thick",)
                ]
            ).open()
    def logoutUser(self , *args):
        try:
            # removing login file 
            os.remove("credentials/user.id")
            # getting navDrawerList
            navDrawerList = self.root.current_screen.ids.nav_drawer_list 
            # removing login button by iterating all labels in nav_drawer_list
            for child in navDrawerList.children:
                labelName = str(child.text)
                if labelName.lower().replace(" " ,"") == "logout":
                    navDrawerList.remove_widget(child)
                else:
                    pass
            # adding logout button 
            navDrawerList.add_widget(NavLabel(text = "Login" ,icon = "login" , on_release = partial(self.changeRootScreen , "LoginScreen")))
            Snackbar(
                text=f"Loged out successfully",
                duration=1,
                snackbar_x=dp(10),
                snackbar_y=dp(10),
                size_hint_x=.8,
                pos_hint={"center_x": .5},
                radius=[10],
                buttons=[
                    MDIconButton(icon="exclamation-thick",)
                ]
            ).open()
        except:
            Snackbar(
                text=f"Can't logout due to some technical issue",
                duration=1,
                snackbar_x=dp(10),
                snackbar_y=dp(10),
                size_hint_x=.8,
                pos_hint={"center_x": .5},
                radius=[10],
                buttons=[
                    MDIconButton(icon="exclamation-thick",)
                ]
            ).open()

        # this is login after creating new user account 
    def loginUser(self , id):
        # adding user id to current user device for next time login 
        with open("credentials/user.id" , "w") as user_id:
            # writting  id to file 
            user_id.write(Encrypter.encryptText(str(id)))
        # changing to home screen 
        self.changeRootScreen("PostsScreen")
        try:
            # getting navDrawerList
            navDrawerList = self.root.current_screen.ids.nav_drawer_list 
            # removing login button by iterating all labels in nav_drawer_list
            for child in navDrawerList.children:
                labelName = str(child.text)
                if labelName.lower().replace(" " ,"") == "login":
                    navDrawerList.remove_widget(child)
                else:
                    pass
            # adding logout button 
            navDrawerList.add_widget(NavLabel(text = "Logout" ,icon = "logout" , on_release = self.logoutUser))
        except:
            Snackbar(
                text=f"Check your Internet-connection ",
                duration=1,
                snackbar_x=dp(10),
                snackbar_y=dp(10),
                size_hint_x=.8,
                pos_hint={"center_x": .5},
                radius=[10],
                buttons=[
                    MDIconButton(icon="exclamation-thick",)
                ]
            ).open()


    def loginWithGoogleAuth(self):
        # callback functions for initilixe_google function
        def login_succed(name , email , photo_url):
            Clock.schedule_once(partial(self.loginCheck, email),1)  
        def login_error():
             # msg to show in tost alert of error while registring
            Snackbar(
                text = "Login Failed check your Internet connection",
                duration = .5,
                snackbar_x=dp(10),
                snackbar_y=dp(10),
                size_hint_x=.8,
                pos_hint = {"center_x":.5},
                radius = [10],
                buttons = [
                    MDIconButton(
                        icon = "exclamation-thick",
                        
                    )
                ]
            ).open()
        # opening json client file 
        with open("credentials/client.json" , "r") as f:
            credentials = json.load(f)
        # getting data from client.json file 
        client_id = credentials["installed"]["client_id"]
        client_secret = credentials["installed"]["client_secret"]
        # initialize google
        initialize_google(login_succed , login_error ,client_id=client_id , client_secret=client_secret)
        # making login request 
        login_google()
        
    # functionf or login page 
    def login(self , pageInstance): 
        emailField = pageInstance.ids.textField
        optField = pageInstance.ids.otpField
        # if textField or otp are empty so generate error
        if optField.text.replace(" ","") == "":
            optField.error = True
            optField.focus = True
        if emailField.text.replace(" ","") == "":
            emailField.error = True
            emailField.focus = True
        # handling errors 
        if optField.error:
            optField.focus = True
        if emailField.error:
            emailField.focus = True
        else:
            # checking is opt correct 
            # initilizing user otp  
            userOtp = 0
            # trying to assign user OTP 
            try:
                userOtp = int(optField.text)
            except:
                pass
            if self.otp == userOtp and self.email == emailField.text:
                loginStatus = self.loginCheck(emailField.text)
                if loginStatus == True:
                     # resetting all text fields 
                    emailField.text = "***"
                    optField.text = "***"
            else:
                optField.error = True
                optField.focus = True
                optField.helper_text = "OTP is incorrect"
    def loginCheck(self,email,*args):
        # try exception for internet confirmation 
        try:
            # -----------------checking if user already exists ------------------
            req = requests.get(f"{Envar.base_api}/is_exists",
                            params={"key": Envar.auth_key, "email": email})
            # if the request is not SUCCESSed so showing error msg to user
            if req.status_code != 200:
                Snackbar(
                    text=f"Internal server error, Tell this to owner",
                    duration=1,
                    snackbar_x=dp(10),
                    snackbar_y=dp(10),
                    size_hint_x=.8,
                    pos_hint={"center_x": .5},
                    radius=[10],
                    buttons=[
                        MDIconButton(
                            icon="exclamation-thick",

                        )
                    ]
                ).open()
            # if request get SUCCESSed
            else:
                # getting responce from api {is_exists}
                responce = req.json()
                # if key was wrong
                if responce["key_error"]:
                    self.root.current_screen.add_widget(Snackbar(
                        text=f"Internal server error, Tell this to owner",
                        duration=1,
                        snackbar_x=dp(10),
                        snackbar_y=dp(10),
                        size_hint_x=.8,
                        pos_hint={"center_x": .5},
                        radius=[10],
                        buttons=[
                            MDIconButton(icon="exclamation-thick",)
                        ]
                    ).open())
                # if key was right
                else:
                    if responce["existance"] == True:
                        id = responce["id"]
                        Snackbar(
                            text = "Login successed ",
                            duration = .5,
                            snackbar_x=dp(10),
                            snackbar_y=dp(10),
                            size_hint_x=.8,
                            pos_hint = {"center_x":.5},
                            radius = [10],
                            buttons = [
                                MDIconButton(
                                    icon = "sticker-check-outline",
                                    
                                )
                            ]
                        ).open()
                        # calling loginUser function to create login file
                        self.loginUser(id)
                        return True
                    else:
                            Snackbar(
                            text = "Login Failed User doesn't exists Please create new account",
                            duration = .5,
                            snackbar_x=dp(10),
                            snackbar_y=dp(10),
                            size_hint_x=.8,
                            pos_hint = {"center_x":.5},
                            radius = [10],
                            buttons = [
                                MDIconButton(
                                    icon = "exclamation-thick",
                                    
                                )
                            ]
                        ).open()
                    
        except:
            Snackbar(
                text = "Login Failed check your Internet connection",
                duration = .5,
                snackbar_x=dp(10),
                snackbar_y=dp(10),
                size_hint_x=.8,
                pos_hint = {"center_x":.5},
                radius = [10],
                buttons = [
                    MDIconButton(
                        icon = "exclamation-thick",
                        
                    )
                ]
            ).open()

                

            
            





        

if __name__ == "__main__":
    ZeroTwoApp().run()
