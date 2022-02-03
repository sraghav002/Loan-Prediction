from tkinter import font
from tkinter.tix import COLUMN
import numpy as np
import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt
df = pd.read_csv(r'C:\Python36\train.csv')
# The loan ID was of no use so we are dropping it. 
df=df.drop(['Loan_ID'],axis=1)
# Dropping rows which has no data of gender as male or female.
df1=df[~df.Gender.isna()]
df1=df1[~df1.Married.isna()]
# for 3+ dependents we are assuming it to be 4.
df1.loc[df1.Dependents=='3+','Dependents']=4
# filling the null dependents value with median of the available values.
df1.Dependents=df1.Dependents.fillna(df1.Dependents.median())
# removing rows which does not contain information of employment.
df1=df1[~df1.Self_Employed.isna()]
# filling the unavailable loan term with round of average of available. 
p=round(sum(df1[~df1.Loan_Amount_Term.isna()]['Loan_Amount_Term'])/df1.Loan_Amount_Term.count())
df1.Loan_Amount_Term=df1.Loan_Amount_Term.fillna(p)
# filling the unavailable loan amount with average of available.
k=sum(df1[~df1.LoanAmount.isna()]['LoanAmount'])/df1.LoanAmount.count()
df1.LoanAmount=df1.LoanAmount.fillna(k)
# filling the unavailable credit history with median of available. 
df1.Credit_History=df1.Credit_History.fillna(df1.Credit_History.median())
# renaming yes and no with relevant names  
df1['Married'].replace({'Yes':'Married','No':'Not_Married'},inplace = True)
df1['Self_Employed'].replace({'Yes':'Self_Employed','No':'Not_self_employed'},inplace=True)
df1['Loan_Status'].replace({'Y':'1','N':'0'},inplace=True)
df1.rename(columns={'Married':'marital_status','Self_Employed':'job'},inplace=True)
# Hot encoding
d1=pd.get_dummies(df1.marital_status)
d2=pd.get_dummies(df1.job)
d3=pd.get_dummies(df1.Education)
d4=pd.get_dummies(df1.Gender)
d5=pd.get_dummies(df1.Property_Area)
m=pd.concat([df1,d1,d2,d3,d4,d5],axis='columns')
# dropping unnecessary parameters after hot encoding
m=m.drop(['marital_status','job','Education','Gender','Property_Area'],axis='columns')
X = m.drop(['Loan_Status'],axis=1)
y=m['Loan_Status']

# importing relavent Files
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
x1=X
y1=y
#converting object to integers as machine learing is good with integers
x1.Dependents=x1.Dependents.astype(int)
x1.ApplicantIncome=x1.ApplicantIncome.astype(int)
x1.CoapplicantIncome=x1.CoapplicantIncome.astype(int)
x1.LoanAmount=x1.LoanAmount.astype(int)
x1.Loan_Amount_Term=x1.Loan_Amount_Term.astype(int)
LMT_max=max(x1.Loan_Amount_Term)
LA_max=max(x1.LoanAmount)
CAI_max=max(x1.CoapplicantIncome)
AI_max=max(x1.ApplicantIncome)
D_max=max(x1.Dependents)
# Making the range between 0 to 1 for better performance
x1.Loan_Amount_Term=x1.Loan_Amount_Term/max(x1.Loan_Amount_Term)
x1.LoanAmount=x1.LoanAmount/max(x1.LoanAmount)
x1.CoapplicantIncome=x1.CoapplicantIncome/max(x1.CoapplicantIncome)
x1.ApplicantIncome=x1.ApplicantIncome/max(x1.ApplicantIncome)
x1.Dependents=x1.Dependents/max(x1.Dependents)
#dividing the data into test and train dataset
x1_train,x1_test,y1_train,y1_test = train_test_split(x1,y1,test_size=0.1,random_state=3)
m2=LogisticRegression() #model for classification
m2.fit(x1_train,y1_train)
back="Sea Green"
foregroun="White"

# function that predicts whether the loan is safe or not
def get_result():
    if gender_selected.get()=="Select Gender" or married_selected.get()=="Marital Status" or dependent_no.get()=="" or education.get()=="Education" or employment.get()=="Employment" or applicant_income_number.get()=="" or coapplicant_income.get()=="" or loan_amount.get()=="" or loan_term.get()=="" or credit_string.get()=="select credit" or property_selectd.get()=="Location":
        messagebox.showinfo("Error","Please select all attributes")
        return
    print(gender_selected.get())
    male=0
    female=0
    married=0
    unmarried=0
    graduate=0
    not_graduate=0
    self_employed=0
    not_self_employed=0
    urban=0
    rural=0
    semi_urban=0
    
    if gender_selected.get()=="Male" :
        male=1
        female=0
        
    else :
        male=0
        female=1
    if married_selected.get()=="Married":
        married=1
        unmarried=0
    else :
        married=0
        unmarried=1
    if education.get()=="Graduate":
        graduate=1
        not_graduate=0
    else :
        graduate=0
        not_graduate=1
    if employment.get()=="Self Employed":
        self_employed=1
        not_self_employed=0
    else :
        self_employed=0
        not_self_employed=1
    if property_selectd.get()=="Urban":
        urban=1
        semi_urban=0
        rural=0
    if property_selectd.get()=="SemiUrban":
        urban=0
        semi_urban=1
        rural=0
    if property_selectd.get()=="Rural":
        urban=0
        semi_urban=0
        rural=1
    print(int(dependent_no.get()),applicant_income_number.get(),coapplicant_income.get(),loan_amount.get(),loan_term.get(),credit_string.get(),married,unmarried,not_self_employed,self_employed,graduate,not_graduate,female,male,rural,urban ,semi_urban)
    
    result=m2.predict([[(int(dependent_no.get())/D_max),(int(applicant_income_number.get())/AI_max),(int(coapplicant_income.get())/CAI_max),(int(loan_amount.get())/LA_max),(int(loan_term.get())/LMT_max),int(credit_string.get()),int(married),int(unmarried),int(not_self_employed),int(self_employed),int(graduate),int(not_graduate),int(female),int(male),int(rural),int(semi_urban),int(urban)]])
    result_label_safe=Label(root,fg="Green",bg=back,font=("Times","30","bold"))
    result_label_safe.place(x=500,y=440)
    result_label_unsafe=Label(root,fg="Red",bg=back,font=("Times","30","bold"))
    result_label_unsafe.place(x=500,y=440)
    if int(result[0])==1:
        result_label_unsafe.config(text="")
        result_label_safe.config(text="Safe Loan")
    else:
       
        result_label_safe.config(text="")
        result_label_unsafe.config(text="Unsafe Loan")
        
    return
    

# GUI
from tkinter import *
root = Tk()
root.geometry("840x600")

ft=("Times","13","bold")
root.config(bg=back)

title = Label(root,text="Loan Predictor",fg=foregroun, font=("Times", "24", "bold"),bg=back)
title.pack()

gender=Label(root,text="Gender",font=ft,fg=foregroun,bg=back)
gender.place(x=50,y=70)

option=["Male","Female"]
gender_selected=StringVar()
gender_selected.set("Select Gender")
gender_drop=OptionMenu(root,gender_selected,*option)
gender_drop.place(x=220,y=70)

marital_status=Label(root,text="Marital Status",font=ft,fg=foregroun,bg=back)
marital_status.place(x=50,y=120)
married_options=["Married","Unmarried"]
married_selected=StringVar()
married_selected.set("Marital Status")
marital_drop=OptionMenu(root,married_selected,*married_options)
marital_drop.place(x=220,y=120)

dependents=Label(root,text="Dependents",font=ft,fg=foregroun,bg=back)
dependents.place(x=50,y=170)
dependent_no=StringVar()
dependent_entry=Entry(root,textvariable=dependent_no)
dependent_entry.place(x=220,y=170)

education_label=Label(root,text="Education",font=ft,fg=foregroun,bg=back)
education_label.place(x=50,y=220)
education=StringVar()
education.set("Education")
eduaction_options=["Graduate","Not Graduate"]
education_drop=OptionMenu(root,education,*eduaction_options)
education_drop.place(x=220,y=220)

employment_label=Label(root,text="Employment",font=ft,fg=foregroun,bg=back)
employment_label.place(x=50,y=270)
employment=StringVar()
employment.set("Employment")
employment_option=["Self Employed","Not self Employed"]
employment_drop=OptionMenu(root,employment,*employment_option)
employment_drop.place(x=220,y=270)

applicant_income=Label(root,text="Applicant Income",font=ft,fg=foregroun,bg=back)
applicant_income.place(x=50,y=330)
applicant_income_number=StringVar()
income_entry=Entry(root,textvariable=applicant_income_number)
income_entry.place(x=220,y=330)

coapplicant_income=Label(root,text="Coapplicant Income",font=ft,fg=foregroun,bg=back)
coapplicant_income.place(x=390,y=270)
coapplicant_income=StringVar()
coapplicant_income_entry=Entry(root,textvariable=coapplicant_income)
coapplicant_income_entry.place(x=560,y=270)

loan_amount_label=Label(root,text="Loan Amount",font=ft,fg=foregroun,bg=back)
loan_amount_label.place(x=390,y=220)
loan_amount=StringVar()
loan_amount_entry=Entry(root,textvariable=loan_amount)
loan_amount_entry.place(x=560,y=220)

loan_term_label=Label(root,text="Loan period",font=ft,fg=foregroun,bg=back)
loan_term_label.place(x=390,y=170)
loan_term=StringVar()
loan_term_entry=Entry(root,textvariable=loan_term)
loan_term_entry.place(x=560,y=170)

credit_label=Label(root,text="Credit History",font=ft,fg=foregroun,bg=back)
credit_label.place(x=390,y=70)
credit_option=["1","0"]
credit_string=StringVar()
credit_string.set("select credit")
credit_drop=OptionMenu(root,credit_string,*credit_option)
credit_drop.place(x=560,y=70)

property_label=Label(root,text="Property",font=ft,fg=foregroun,bg=back)
property_label.place(x=390,y=120)
property_option=["Urban","SemiUrban","Rural"]
property_selectd=StringVar()
property_selectd.set("Location")
property_drop=OptionMenu(root,property_selectd,*property_option)
property_drop.place(x=560,y=120)

result_button=Button(root,text="Get Result",command=get_result,font=("Times","20","bold"),fg="Green")
result_button.place(x=330,y=440)

Disclamer1=Label(root,text="Note : The Applicant income and Coapplicant income is monthly income of the applicant and Coapplicant in $. ",font=("Times","11"),fg="White",bg=back)
Disclamer1.place(x=50,y=510)
Disclamer2=Label(root,text="          The Loan Amount is in multiple of thousand $ if 150,000 is loan enter 150",font=("Times","11"),fg="White",bg=back)
Disclamer2.place(x=50,y=530)
Disclamer3=Label(root,text="          The Loan term is time period in months",font=("Times","11"),fg="White",bg=back)
Disclamer3.place(x=50,y=550)
root.mainloop()