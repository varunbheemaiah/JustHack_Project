#include<iostream>
using namespace std;

class student
{
    int usn;
    char name[50];
public:
    int age;
    void read()
    {
        cout<<"Enter name: ";
        cin>>name;
        cout<<"Enter USN: ";
        cin>>usn;
        cout<<"Enter age: ";
        cin>>age;
    }
    void display()
    {
        cout<<"USN       :     "<<usn<<endl;
        cout<<"Name      :     "<<name<<endl;
        cout<<"Age       :     "<<age<<endl;
    }
};

class UGStudent:public student
{
    int sem;
    float fees,stipend;
public:
    void ugread()
    {
        read();
        cout<<"Enter Semester: ";
        cin>>sem;
        cout<<"Enter fees :";
        cin>>fees;
        cout<<"Enter Stipend: ";
        cin>>stipend;
    }
    void ugdisplay()
    {
        display();
        cout<<"Semester  :     "<<sem<<endl;
        cout<<"Fees      :     "<<fees<<endl;
        cout<<"Stipend   :     "<<stipend<<endl;
    }
    friend void ugavg(UGStudent,int);
};

class PGStudent:public student
{
    int sem;
    float fees,stipend;
public:
    void pgread()
    {
        read();
        cout<<"Enter Semester: ";
        cin>>sem;
        cout<<"Enter fees :";
        cin>>fees;
        cout<<"Enter Stipend: ";
        cin>>stipend;
    }
    void pgdisplay()
    {
        display();
        cout<<"Semester  :     "<<sem<<endl;
        cout<<"Fees      :     "<<fees<<endl;
        cout<<"Stipend   :     "<<stipend<<endl;
    }
    friend void pgavg(PGStudent,int);
};

void pgavg(PGStudent P[], int n)
{
    float avg; int sum=0;
    for(int i=0;i<n;i++)
    {
        sum+=P[i].age;
    }
    avg = float(sum)/n;
    cout<<"PG Average is : "<<avg<<endl;
}

void ugavg(UGStudent P[], int n)
{
    float avg; int sum=0;
    for(int i=0;i<n;i++)
    {
        sum+=P[i].age;
    }
    avg = float(sum)/n;
    cout<<"UG Average is : "<<avg<<endl;
}

int main()
{
    UGStudent U[100];
    PGStudent P[100];
    int m,n;
    cout<<"Enter the number of UG Students :";
    cin>>m;
    for(int i=0;i<m;i++)
        U[i].ugread();
    cout<<"Enter the number of PG Students :";
    cin>>n;
    for(int i=0;i<n;i++)
        P[i].pgread();
    cout<<"\nUG Students :\n";
    for(int i=0;i<m;i++)
        U[i].ugdisplay();
    cout<<"\nPG Students :\n";
    for(int i=0;i<n;i++)
        P[i].pgdisplay();
    ugavg(U,m);
    pgavg(P,n);
    return 0;
}

