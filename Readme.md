20180418<br />
這是radare2的練習,radare2是專門用來做逆向工程的工具
<br />首先在我們的project裡頭有個C source code,程式碼如下
<br />
#include<stdio.h><br />
#include<stdlib.h><br />
int main()<br />
{<br />
    &emsp;&emsp;int i;<br />
    &emsp;&emsp;printf("please input number:");<br />
    &emsp;&emsp;scanf("%d",&i);<br />
    &emsp;&emsp;if(i%2==0)<br />
      &emsp;&emsp;&emsp;&emsp;puts("even");<br />
    &emsp;&emsp;else<br />
      &emsp;&emsp;&emsp;&emsp;puts("odd");<br />


return 0;<br />
}<br />
這是一個判斷奇偶數的code,在Linux commamd line 執行的情況如下
<br />
<img src="https://github.com/parkmftsai/Radare2_Exercise/blob/master/image/picture1.png" align=left/>
<br />
接著我們使用Python 寫一個腳本(testradare2.py),透過radare2套件r2pipe針對執行檔test.out進行逆向工程<br />

其中我們可以用r2.cmd("pd @sym.main")這段語法看test.out主程式區(main)的組合語言
<br />
<img src="https://github.com/parkmftsai/Radare2_Exercise/blob/master/image/picture2.png" align=left/>
<br />
我們可以觀察出以下這段組合語言語法
<br />
        ,=< 0x0040068a      750c           jne 0x400698<br />
        |   0x0040068c      bf5c074000     mov edi, str.even           ; testc.c:9       puts("even"); ; 0x40075c ; "even"<br />
        |   0x00400691      e85afeffff     call sym.imp.puts<br />
       ,==< 0x00400696      eb0a           jmp 0x4006a2<br />
       |`-> 0x00400698      bf61074000     mov edi, 0x400761           ; testc.c:11       puts("odd");<br />
       |    0x0040069d      e84efeffff     call sym.imp.puts<br />

其中jne(jump not equal)意義為當不符合條件時會跳到一個位址（address）<br />
這段語法為上述語法<br />
if(i%2==0)  <br />
     &emsp;&emsp;puts("even"); <br />
      
else <br />
     &emsp;&emsp;puts("odd");
      <br />
在判斷時的組合語言表示方式<br />

再來我們可以透過r2pipe更改其組合語言語法,首先先進入要修改的區塊,使用以下語法<br />
r2.cmd("s 0x0040068a")<br />

0x0040068a是jne 0x400698所在的記憶體區塊,我們的接下來的動作是將jne改成jmp,<br />
但是要注意,不論是哪個語言,其指令都有一個獨特的機器碼,我們首先要作的是查詢jne 以及jmp的機器碼<br />
,這裡使用rasm2這個工具進行反編譯,用來查詢jne以及jmp的機器碼,以下function提供此功能<br />

def radare2_Decompile_Tool(str,flag):<br />
    &emsp;&emsp;cpu_Structure = "x86"<br />
    &emsp;&emsp;cpu_Register_bit = "64"<br />
    &emsp;&emsp;if(flag == 1):<br />
        &emsp;&emsp;&emsp;&emsp;return r2.syscmd("rasm2 -a " + cpu_Structure + " -b " + cpu_Register_bit + " -d " + str)<br />
    &emsp;&emsp;if (flag == 2):<br />
        &emsp;&emsp;&emsp;&emsp;return r2.syscmd("rasm2 -a " + cpu_Structure + " -b " + cpu_Register_bit + " " + str)<br />

經過查詢jne機器碼為75,jmp為eb<br />
最後開始修改機器語言,使用以下語法<br />
r2.cmd("wx eb")<br />
我們在使用r2.cmd("pd @sym.main")看個組合語言,可以發現<br />
<img src="https://github.com/parkmftsai/Radare2_Exercise/blob/master/image/picture3.png" align=left/><br />
同樣,我們可以觀察出以下這段組合語言語法<br />
        ,=< 0x0040068a      eb0c           jmp 0x400698<br />
        |   0x0040068c      bf5c074000     mov edi, str.even           ; testc.c:9       puts("even"); ; 0x40075c ; "even"<br />
        |   0x00400691      e85afeffff     call sym.imp.puts<br />
       ,==< 0x00400696      eb0a           jmp 0x4006a2<br />
       |`-> 0x00400698      bf61074000     mov edi, 0x400761           ; testc.c:11       puts("odd");<br />
       |    0x0040069d      e84efeffff     call sym.imp.puts<br />

接著再重新執行test.out,此時不管輸入任何數字,只會輸出odd<br />
<img src="https://github.com/parkmftsai/Radare2_Exercise/blob/master/image/picture4.png" align=left/><br />
