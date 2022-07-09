#include<bits/stdc++.h>
#include<unistd.h>
#include<sys/types.h>
#include <fstream>
#include <iostream>
#include<sys/wait.h>

using namespace std;
int ctr=0;
void dfs(int i,int p,int viss[],vector<int> vecc[],int parr[])
{
    viss[i]=1;
    parr[i]=1;
    for(int j=0;j<vecc[i].size();j++)
    {
        int a1=vecc[i][j];
        if(viss[a1]==0)
        {
            dfs(a1,i,viss,vecc,parr);
        }
        else if(parr[a1]>0)
        {
            ctr=1;
            parr[i]=0;
            return;
        }
    }
    parr[i]=0;
    return;
}
signed main()
{
    ctr=0;
    int n=6;
    
    vector<int> vecc[n+2];
    int viss[n+2];
    int parr[n+2];
    for(int i=0;i<=n;i++)
    {
        viss[i]=0;
        parr[i]=0;
    }
    //open a file to perform read operation using file object
    ifstream fin;
    fin.open("tpoint.txt");
    //newfile.open("tpoint.txt",ios::in); //open a file to perform read operation using file object
   if (fin.is_open())
   { //checking whether the file is open
      string tp;
      while(getline(fin, tp))
      { //read data from file object and put it into string.
         cout << tp << "\n"; //print the data of the string
         int a1=tp[0]-'0';
         int a2=tp[2]-'0';
         vecc[a1].push_back(a2);
         
      }
      fin.close(); //close the file object.
   }
    for(int i=0;i<=n;i++)
    {
        if(viss[i]==0)
        {
            dfs(i,i,viss,vecc,parr);
        }
    }
    if(ctr>0)
    {
        // Write in tpoint.txt
        ofstream fout;
        fout.open("deads.txt");
        fout<<"Yes it is in deadlock\n";
    }
    else
    {
        ofstream fout;
        fout.open("deads.txt");
        fout<<"No it is not in deadlock\n";
    }
    return 0;
}
