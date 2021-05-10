# Basic source to markdown generator

### **scan2md** tool is a very basic source code to markdown generator.
### The tool scans source file, looks for a special comments and writes
### commands or text to markdown file.
### Special comments starts with /*! and ends with */
### For **Phyton** special comments starts with '''! and ends with '''
### Doxygen is a very powerfull tool. **scan2md** isn't Doxygen.
### **scan2md** use similar Doxygen commands for easy handling.
### The function of commands in **scan2md** can be different as in Doxygen.
### The code type is determined from input file extension.
<br>

## Usage:
---
```
python scan2md <input-file.ext> <output-file.md> 
```
## Commands Usage:
---
- ### Within special comment block, commands starts with @.
- ### Lines without command outputs direct to markdown file with indent.
- ### Lines without command and starts with $ writes direct to markdown file.
- ### You can use any markdown syntax within text (e.g ** to **bold** a text).
- ### Lines with @@ are substitute to @ and writes as text to md file.
- ### **scan2md** use indenting in markdown.
- ### Some commands increase indent of next command (***@class*** for example).
- ### You can decrease or reset indent with @sa command (see ***@sa***).
- ### ***@fn*** (Function) has different command handling.
- ### ***@fn*** The line after comment end are recognized as function declaration.

- ### Example:
```c
/*! @fn calculate sum
    @param op1 operand1      
    @param op2 operand2
    @return sum of op1 and op2      
*/ 
int sum(int op1, int op2)
{
    return op1 + op2;
}
```
### Markdown Output:
<br>
💠Function: calculate sum<br>

```c 
int sum(int op1, int op2)
```
- ▶️Param:  **op1** operand1<br>
- ▶️Param:  **op2** operand2<br>
- ✅Return: sum of op1 and op2<br>

<br>

## Commands:
---
<br>

## ***@brief*** text
text<br>

## ***@--*** (horizontal line)
---

## ***@n*** (new line)

## ***@b*** (break add \<br\>)
<br>

## ***@sa*** \>> (set indent 2)
>>
>>text<br>

## ***@sa*** (set indent 0)
text<br>

## ***@tablehead*** col1,col2,col3,col4
## ***@table*** 34,17, ,**128**
## ***@table*** abc,def,**ghi**
|col1|col2|col3|col4|
|---|---|---|---|
|34|17||**128**|
|abc|def|**ghi**|

## ***@file*** filename 
💾 filename<br>

## ***@copyright*** copyright 
🧾 copyright<br>

## ***@date*** date 
📆 date<br>

## ***@name*** name description
>##  **name** description<br>

## ***@version*** version 
⚙️ version<br>

## ***@author*** name 
✏️ name<br>

## ***@todo*** todo 
❓ todo<br>

## ***@warning*** warning 
⚠️ warning<br>

## ***@emoj*** blush 
:blush:<br>

## ***@mainpage*** filename 
🏠 [Main Page](filename)<br>

## ***@mainpage*** filename text 
🏠 [text](filename)<br>

## ***@link*** filename 
📌 [Link](filename)<br>

## ***@link*** filename text 
📌 [text](filename)<br>

## ***@image*** dolphin.png 
![image](dolphin.png)<br>

## ***@code*** 
```c
#include <stdio.h>
int main()
{
    printf("Hello World\n");
    return 0;
}
```
## ***@code*** python 
```python
import sys
def main():
     print("Hello World")
```

## ***@class*** name description
💎Class: **name** description<br>

## ***@union*** name description
🔳Union: **name** description<br>

## ***@struct*** name description
🔲Struct: **name** description<br>

## ***@interface*** name description
🔑Interface: **name** description<br>

## ***@namespace*** name description
📇Namespace: **name** description<br>

## ***@typedef*** name description
🔨Typedef: **name** description<br>

## ***@def*** name description
🔟Const: **name** description<br>

## ***@enum*** name description
🔢Enum: **name** description<br>

## ***@var*** name description
✳️Variable: **name** description<br>

## ***@global*** name description
🌐Global: **name** description<br>

## ***@static*** description
🌲Static: description

## ***@public*** description
📢Public: description

## ***@private*** description
🔒Private: description

## ***@overload*** description
⏬Overload: description

## ***@virtual*** description
👻Virtual: description

## ***@fn*** description
💠Function: description

## ***@param*** name description
- ▶️Param: **name** description<br>

## ***@return*** description
- ✅Return: description

## ***@return[error]*** description
- ❌Return: description

## ***@throw*** description
- ⛔️Throw: description

