from tkinter import *
from imdb import IMDb
import datetime
import httplib2
import os
import oauth2client
from oauth2client import client, tools
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery
import mysql.connector

mydb=mysql.connector.connect(host="localhost",user="YOUR USERNAME",passwd="YOUR PASSWORD",database="DATABASE NAME")

mycursor=mydb.cursor()

year=datetime.date.today().year
ia=IMDb();
from tkinter import messagebox


def mess(a,message):
      final_message=""
      for x in range(0,len(message)):
              final_message=final_message+"TV series name:"+a[x]+"<br>Status:"+message[x]+"<br><br>"
      return final_message

def mail(to_email,final):
      SCOPES = 'https://www.googleapis.com/auth/gmail.send'
      CLIENT_SECRET_FILE = 'client_secret.json'
      APPLICATION_NAME = 'Gmail API'

      def get_credentials():
               home_dir = os.path.expanduser('~')
               credential_dir = os.path.join(home_dir, '.credentials')
               if not os.path.exists(credential_dir):
                     os.makedirs(credential_dir)
               credential_path = os.path.join(credential_dir, 'gmail-python-email-send.json')
               store = oauth2client.file.Storage(credential_path)
               credentials = store.get()
               if not credentials or credentials.invalid:
                      flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
                      flow.user_agent = APPLICATION_NAME
                      credentials = tools.run_flow(flow, store)
                      print('Storing credentials to ' + credential_path)
               return credentials

      def SendMessage(sender, to, subject, msgHtml, msgPlain):
               credentials = get_credentials()
               http = credentials.authorize(httplib2.Http())
               service = discovery.build('gmail', 'v1', http=http)
               message1 = CreateMessage(sender, to, subject, msgHtml, msgPlain)
               SendMessageInternal(service, "me", message1)

      def SendMessageInternal(service, user_id, message):
               try:
                    message = (service.users().messages().send(userId=user_id, body=message).execute())
                    print('Message Id: %s' % message['id'])
                    return message
               except errors.HttpError as error:
                    print('An error occurred: %s' % error)

      def CreateMessage(sender, to, subject, msgHtml, msgPlain):
                    msg = MIMEMultipart('alternative')
                    msg['Subject'] = subject
                    msg['From'] = sender
                    msg['To'] = to
                    msg.attach(MIMEText(msgPlain, 'plain'))
                    msg.attach(MIMEText(msgHtml, 'html'))
                    raw = base64.urlsafe_b64encode(bytes(msg))
                    raw = raw.decode()
                    body = {'raw': raw}
                    return body

      def main():
                    to = to_email
                    sender = "YOUR EMAIL ID"
                    subject = "Next Streaming episodes of TV Series"
                    msgHtml = final
                    msgPlain = final
                    SendMessage(sender, to, subject, msgHtml, msgPlain)

      if __name__ == '__main__':
                    main()
def func():
      if(len(value1.get())!=0 and len(value2.get())!=0):
                  messagebox.showinfo("INNOVACCER","E-MAIL WILL BE SENT TO YOU SHORTLY!");
                  root.destroy();
                  sql="INSERT INTO USERS(EMAIL,SERIES)VALUES(%s,%s)"
                  val=(value1.get(),value2.get())
                  mycursor.execute(sql,val)
                  mydb.commit()
                  print("record inserted in MYSQL Database");
                  a=[x.strip() for x in value2.get().split(',')]
                  message=[];
                  for x in a:
                           flag=0;
                           seriesN=ia.get_movie(ia.search_movie(x)[0].movieID);
                           ia.update(seriesN,'episodes');
                           seasonN=max(sorted(seriesN['episodes'].keys()));
                           episodeN=len(seriesN['episodes'][seasonN]);
                           for i in range(1,episodeN+1):
                                   if(flag==0):    
                                            episodeDetails=ia.get_movie(seriesN['episodes'][seasonN][i].movieID);
                                            if(episodeDetails.get('original air date')!=None):
                                                       if(len(episodeDetails.get('original air date'))==4):  
                                                                 if(int(episodeDetails.get('original air date'))>int(year)):
                                                                        message.append("The next season begins in " + episodeDetails.get('original air date'));
                                                                        flag=1;
                                                       elif(len(episodeDetails.get('original air date'))>4):
                                                                 if(int(episodeDetails.get('original air date')[7:])>int(year)):
                                                                        message.append("The episode is streaming on:"+episodeDetails.get('original air date'));
                                                                        flag=1;       
                                            else:
                                                       message.append('no further details about next episode');
                                                       flag=1;
                           if(flag==0):
                                     message.append('The show has finished all its episodes');
                             
                  print(message)
                  final=""
                  final=mess(a,message)
                  mail(value1.get(),final)
      else:
                   messagebox.showinfo("ERROR","ALL THE FIELDS ARE MANDATORY!");






root = Tk()
root.geometry('500x500')
root.title("TV SERIES DETAILS")
root.configure(background='yellow');
label_0 = Label(root, bg="yellow",text="Get Streaming Dates of your Favourite TV Series",width=40,font=("bold", 13))
label_0.place(x=80,y=53)

value2=StringVar();
value1=StringVar();

label_1 = Label(root, bg="yellow",text="Email Address",width=20,font=("bold", 10))
label_1.place(x=80,y=130)

entry_1 = Entry(root,textvariable=value1)
entry_1.place(x=240,y=130)

label_2 = Label(root, bg="yellow",text="TV Series",width=20,font=("bold", 10))
label_2.place(x=68,y=180)

entry_2 = Entry(root,textvariable=value2)
entry_2.place(x=240,y=180)

Button(root, text='Submit',width=20,bg='brown',command=func,fg='white').place(x=180,y=280)





root.mainloop()

