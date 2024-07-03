---
categories:
- 技术
- 大数据
date: '2019-07-15 11:06:57+08:00'
tags:
- train
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180831191146955.png
title: 1-快学Scala
---
为数据中台新人进行培训，培训内容scala
<!--more-->
[toc]

## 1. Scala是什么？
Scala(Scalable Language)是一种多范式的编程语言，其设计的初衷是要集成面向对象编程和函数式编程的各种特性。
Scala运行于Java平台(java虚拟机上)，并兼容现有的Java程序。
面向对象(将对象当作参数传来传去) + 面向函数(方法，可以将函数当作参数传来传去)

#### 特点
- 优雅简洁：这是框架设计师第一个要考虑的问题，框架的用户是应用开发程序员，API是否优雅直接影响用户体验，Scala程序员曾报告说与Java比起来代码行数可以减少到1/10。

- 速度快：Scala语言表达能力强，一行代码抵得上Java多行，开发速度快；Scala是静态编译的，所以和JRuby,Groovy比起来速度会快很多。

- 与spark关系紧密：天然的分布式理念，Spark的开发代码就是scala语言，相对于其他语言，scala支持的组件全面，pyspark就没有GraphX的集成。


## 2. scala能为我们做什么？
- 大数据分析：Spark的原生语言是Scala，因此入门Scala是学习Spark的第一步。
- web应用：基于scala的特性，可以替换一些java代码，更简洁，更快速。
- 中间件开发：kafka等中间件也是由scala和java编写。

## 3. 快速入门
### 1. 开发环境准备
1. java环境（版本1.8.0_171）
2. scala二进制包下载地址（版本2.11.8）：http://distfiles.macports.org/scala2.11/
3. 安装包解压，配置环境变量
4. 开发工具使用idea，需要安装插件
5. maven

### 2. 相关介绍
#### 1. 第一个程序
```scala
object HelloWorld {
  def main(args: Array[String]): Unit = {
    println( "Hello World!" )
  }
}
```
###### 注意：
- 跟java语法块后面必须加";"是不一样的，scala语句末尾的分号通常是可写可不写的。
- ":"是类型表达式分隔符，后面是推断的或者指定类型。
- Scala将行的结尾视为表达式的结尾，除非它可以推断表达式继续到下一行。
- Scala程序处理从主方法开始，这是每个Scala程序的一个强制性部分。
- main方法未标记为静态，main方法是对自动实例化的单例对象的实例方法。
- main没有返回类型。实际上有Unit，这是类似于void，但它是由编译器推断。
- 我们可以通过在参数后面加一个冒号和类型来显式地指定返回类型：
- Scala使用def关键字告诉编译器这是一个方法。
- 在Scala中没有访问级别修改器。
- Scala未指定公用修饰符，因为默认访问级别为public。
- object是scala的单例对象

#### 2. 相关概念
##### 1. Scala变量
在Scala中，有三种方法可以定义变量：val，var和lazy(延迟加载) val。
Scala允许您在声明它时决定变量是否是不可变的（只读）
- val
使用关键字val声明不可变变量，相当于java中的final。
- var
现在让我们声明一个可变变量。

- lazy val
延迟val变量计算一次，第一次访问变量。

###### 注意：
val定义的变量的时候必须赋值
- `val age:Int` ❌
- `val age = 18` ✅ 可以不声明类型，scala的类型推断会根据值来自动推断
- `val age:Int = 18` ✅

var变量可以使用默认初始化,既用下划线对变量赋值,不同的初始值不一样
- `var age = _` ❌ 使用_必须定义初始类型
- `var age:Int = _` ✅ 初始化值为0
- `var name:String = _` ✅ 初始化值为null
##### 2. 代码块、注释、字符串插值
```scala
object CodeBlock {
  //  方法和变量也可以在用大括号{}表示的代码块中定义。
  val name = {
    "Lily"
  }
  val age = 18
  val province, city = "北京"

  /*
  代码块的结果是在代码块中计算的最后一行，如以下示例所示。
  变量定义也可以是代码块。
  */
  var sex = {
    val flag = Random.nextInt(2)
    if (flag == 1) "男" else "女"
  }
  
  //  字符串插值是一种将字符串中的值与变量组合的机制。
  def introduction() = println(s"Hello,I`m $name, sex is $sex ,from $province,$city 市 ")

  def main(args: Array[String]): Unit = {
    introduction()
  }
}

```

##### 3. Scala数据类型
Scala中的数据数据类型构成了Float和Double类型以及诸如Byte，Short，Int，Long和Char等整数数据类型。

##### 下表显示Scala的数值数据类型。
常用的引用数据结构|描述
-|-
Array|定长数组： 有序，可变类型，长度不可变。
ArrayBuffer|不定长数组：有序，可变类型，长度可以扩展。
List|列表：有序，不可变类型。
Set|集合：无序，不可变类型。
Map|映射：无序，不可变类型。
Tuple|元组：有序，不可变类型，可以存放不同数据类型元素。
Option|选项：表示有可能包含值的容器，也可能不包含值。
Iterator|迭代器：不属于容器，但是提供了遍历容器的方法。

|常用的基本数据类型|描述|
|-|-|
Byte|从-128到127范围内的整数
Short|从-32768到32767范围内的整数
Int|从-2147483648到2147483647范围内的整数
Long|从-9223372036854775808到9223372036854775807范围内的整数
Float|最大正有限浮点是3.4028235 * 1038，最小正有限非零浮点是1.40 * 10-45
Double|最大正有限双是1.7976931348623157 * 10308，最小正有限非零双是4.9 * 10-324

Scala可以按顺序自动将数字从一种类型转换为另一种类型。
Byte->Short->Int->Long->Float->Double.
`val x: Byte = 30` 
`val y: Short = x` 

##### 4. 整数常量
整数常量可以用十进制，十六进制或八进制表示。

|类型|格式|例子|
|-|-|-|
Decimal|0或非零数字后跟零或多个数字（0-9）|0, 1, 321
Hexadecimal|0x后跟一个或多个十六进制数字（0-9，A-F，a-f）|0xFF, 0x1a3b
Octal|0后跟一个或多个八进制数字（0-7）a|013, 077
##### 5. 布尔常量
布尔常量是true和false。
```scala
scala> !false
res5: Boolean = true
```
##### 6. 字符常量
字符常量是可打印的Unicode字符或转义序列，写在单引号之间。
```scala
scala> "\u0041"
res4: String = A
scala> "\t"
res6: String = "        "
```
有效的转义序列如下表所示。

|序列|含义|
-|-
\b|退格(BS)
\t|水平制表(HT)
\n|换行(LT)
\f|换页(FF)
\r|回车(CR)...
\"|双引号(“)
\"|单引号(“)
\\|反斜杠(\)
Unicode值介于0和255之间的字符可以由八进制转义表示，即反斜杠（\）后跟最多三个八进制字符的序列。

##### 7. 元组常量
Scala库包括用于将N个项分组的TupleN类（例如，Tuple2），以及括号内的项的逗号分隔列表的文字语法。
对于1到22之间的N，有单独的TupleN类。
例如，val tup =（“Hi”，2014）定义了一个Tuple2实例，其中第一个元素推断String，第二个元素Int推断。

```scala
scala> val t = ("Hello", 1, 2.3)
t: (String, Int, Double) = (Hello,1,2.3)

scala> println( "Print the whole tuple: " + t )
Print the whole tuple: (Hello,1,2.3)

scala> println( "Print the first item:  " + t._1 )
Print the first item:  Hello

scala> println( "Print the second item: " + t._2 )
Print the second item: 1

scala> println( "Print the third item:  " + t._3 )
Print the third item:  2.3

scala> val (t1, t2, t3) = ("World",  "!", 0x22)
t1: String = World
t2: String = !
t3: Int = 34

scala> println( t1 + ", " + t2 + ", " + t3 )
World, !, 34

scala> val (t4, t5, t6) = Tuple3("World",  "!", 0x22)
t4: String = World
t5: String = !
t6: Int = 34

scala> println( t4 + ", " + t5 + ", " + t6 )
World, !, 34
```

##### 8. 函数常量
(i:Int，s:String)=> s + i 是Function2类型的函数文本[Int，String，String]（返回String）。
你甚至可以使用常量语法作为类型声明。
以下声明是等效的：
val f1: (Int,String) => String       = (i, s) => s+i 
val f2: Function2[Int,String,String] = (i, s) => s+i 

##### 9. Any、Null、null、Nothing、None、Nil、Unit理解
![](https://www.azheimage.top/markdown-img-paste-20190711202315983.png)
![](https://www.azheimage.top/markdown-img-paste-20190711202214682.png)

###### 1. Any
在scala中，Any类是所有类的超类。Any有两个子类：AnyVal和AnyRef
AnyVal是所有值类的基类。
AnyRef是所有引用类型的基类,除了值类型，所有类型都继承自AnyRef。
###### 2. Null
Null是所有AnyRef的子类，是所有继承了Object的类的子类，所以Null可以赋值给所有的引用类型(AnyRef)，不能赋值给值类型(AnyVal)，这个java的语义是相同的。null是Null的唯一对象。
>val x = null         // x: Null
val y: String = null // y: String = null
val z: Int = null    // error: type mismatch
val u: Unit = null   // u: Unit = ()

###### 3. Nothing
Nothing是所有类的子类，是一个类。Nothing没有对象，但是可以用来定义类型。
Nothing的用处是什么呢？
- 用于标记不正常的停止或者中断
- 一个空的collection
>scala> def foo = throw new RuntimeException
foo: Nothing
scala> val l:List[Int] = List[Nothing]()
l: List[Int] = List()

###### 4. None
这是Option的一个子类，没有值的时候，使用None。如果有值可以引用，就使用Some来包含这个值。Some也是Option的子类。
>scala> val m = Map("a"->1,"b"->2)
m: scala.collection.immutable.Map[String,Int] = Map(a -> 1, b -> 2)
scala> m.get("a")
res37: Option[Int] = Some(1)
scala> m.get("a").get
res38: Int = 1
scala> m.get("c")
res39: Option[Int] = None
scala> m.get("c").get
java.util.NoSuchElementException: None.get
  at scala.None$.get(Option.scala:347)
  at scala.None$.get(Option.scala:345)
  ... 32 elided
scala> m.get("c").isEmpty
res41: Boolean = true

###### 4. Nil
Nil是空List
>scala> Nil
res44: scala.collection.immutable.Nil.type = List()

###### 5. Unit
表示无值，和其他语言中void等同。用作不返回任何结果的方法的结果类型。Unit只有一个实例值，写成()。

##### 10. 输入输出
输出：println,print,printf
输入：scala.io.StdIn
写文件：java.io.PrintWriter
读文件：scala.io.Source

##### 11. 选择结构
Scala的选择结构主要通过if语句以及match语句实现。
match 语句相当于多分支结构，可以使用模式匹配。

##### 12. 循环结构
Scala循环结构主要是 for循环和while循环,此外还可以使用for推导式。

##### 13. 异常捕获
异常捕获的语句是 try...catch...finally...
此外还可以用throw抛出异常。
```scala
object ExceptionDemo {
  def main(args: Array[String]) {
    try {
      val f = new FileReader("input.txt")
    } catch {
      case ex: FileNotFoundException => {
        println("Missing file exception")
      }
      case ex: IOException => {
        println("IO Exception")
      }
    } finally {
      println("Exiting finally...")
    }
  }
}

//Missing file exception
//Exiting finally...
```

##### 13. 函数定义
Scala中的函数可以通过关键字def定义或者使用匿名函数。
此处介绍def定义函数的语法。

def functionName(args list) :[return type] = {
   function body
}
当函数的输出类型可以推断时，可以省去“ :[return type]= “。

##### 14. 匿名函数
Scala中的函数是一等公民，可以像变量一样定义和使用。
和变量一样，函数具有类型和值。

##### 15. 高阶函数
高阶函数即可以传入函数作为其参数的函数。
Scala支持非常强大的函数式编程风格。
map,flatMap,forech,reduce

##### 16. 类、对象、特质
Scala中用关键字class定义普通类,用abstract class定义抽象类，用case class定义样例类, 用object定义单例对象，用trait定义特征。

- case class
case类本来设计用来进行模式匹配，自带apply和unapply方法，实例化时可以不用new关键字。除了做了优化用于模式匹配，其它方面和普通类没有什么区别。
- abstract class
抽象类，它定义了一些方法但没有实现他们。取而代之的是有扩展抽象类的子类定义这些方法，用关键字extends继承。
Scala每个类只能继承一个超类。
abstract class不能创建抽象类的实例
- object
object相当于class的单个实例，类似于Java中的static，通常在里面放一些静态的field和method。 
  
第一次调用object中的方法时，会执行object的constructor，也就是object内部不在method或者代码块中的所有代码，但是object不能定义接受参数的constructor 

- 伴生对象和伴生类
当单例对象和类同名的时候，而且在同一个文件中，互为伴生。
这个时候伴生对象和伴生类可以访问彼此的私有成员。

- trait
Scala每个类只能继承一个超类。
为了实现多继承的功能，在指定一个超类的同时可以指定若干个trait特征进行继承。
抽象类与特质的选择：
1.优先使用特质。一个类扩展多个特质是很方便的，但却只能扩展一个抽象类。
2.如果你需要构造函数参数，使用抽象类。因为抽象类可以定义带参数的构造函数，而特质不行。

### 3. Demo
gitee链接：https://gitee.com/azhegit/ScalaDemo
### 4. 预期任务
#### 1. 用scala编写99乘法表
#### 2. 编写一个算法
##### 输入：
|时间|速度|
-|-
2019-7-12 10:00:00|12
2019-7-12 10:00:10|0
2019-7-12 10:00:20|34
2019-7-12 10:00:30|32
2019-7-12 10:00:40|19
2019-7-12 10:00:50|0
2019-7-12 10:01:00|0
2019-7-12 10:01:10|26
2019-7-12 10:01:20|38
2019-7-12 10:01:30|38
2019-7-12 10:01:40|28
2019-7-12 10:01:50|0
2019-7-12 10:02:00|0
2019-7-12 10:02:10|18
2019-7-12 10:02:20|10
2019-7-12 10:02:30|16
2019-7-12 10:02:40|7
2019-7-12 10:02:50|30
2019-7-12 10:03:00|25
2019-7-12 10:03:10|9
2019-7-12 10:03:20|7
2019-7-12 10:03:30|0
2019-7-12 10:03:40|0
2019-7-12 10:03:50|4
2019-7-12 10:04:00|53
##### 输出：
1. 计算起步速冻为0加速的最高速度的平均速度（橙色线）
2. 计算最高速度到减速到0的平均速度（绿色线）


![](https://www.azheimage.top/markdown-img-paste-20190712162402655.png)

### 5. 学习资料
1. runoob上的Scala 教程:https://www.runoob.com/scala/scala-tutorial.html
2. 官网：https://www.scala-lang.org/
3. 一个比较好的博客：http://hongjiang.info/scala/
4. Twitter Scala School：http://twitter.github.io/scala_school/index.html

### 6. Scala语言的设计哲学
#### 1. 一切皆对象
从整数，字符串，函数，类到各种数据结构，Scala中一切皆为对象，Any是它们的超类。
#### 2. 一切皆表达式
Scala中书写的每条语句都可以看成是一条表达式。
表达式的基本格式是 name:type = {...} 
name是对象标识符，type是它的类型，{}括起来的作用域部分都是它的值。
从变量的定义，函数的定义，判断语句，循环语句到类的定义，都可以看成是这个格式省去某些部分的特例或语法糖等价书写形式。

#### 3. 简洁而富有表现力
同样的功能，Scala的代码量可能不到Java的五分之一。
并且Scala的许多特性设计非常有表现力。
简洁范例：强大的自动类型推断，隐含类型转换，匿名函数，case类，字符串插值器。
表现力范例：集合的&和|运算,函数定义的=>符号,for循环<-的符号，Map的 ->符号，以及生成range的 1 to 100等表达。
#### 4. 函数式编程
函数的特点是操作无副作用，唯一的作用的生成函数值。
把一个函数作用到一些参数上，不会对输入参数造成改变。
为了逼近这个目标，scala设计的默认数据结构绝大部分是不可变的。
并且在一个良好风格的scala程序中，只需要使用val不可变变量而无需使用var可变变量。
显式的for或者while循环是不可取的，让我们用更多的高阶函数吧。

#### 5. 多范式编程
尽管函数式编程是Scala的推荐编程范式，但Scala同时混合了强大的命令式编程的功能。
你可以使用强大的for循环，for推导式，使用可变的变量和数据类型实现命令式编程。
你还可以使用强大的模式匹配，基于模式匹配完成复杂的变换操作，实现模式化编程。

最后，正如同它的名字的蕴意，Scala是一门可以伸缩的语言。通过编写扩展类和对象，或继承各种Trait生成新数据结构，Scala可以很容易地成为某个领域的"专业语言"。新增加的那些特性就好像是Scala语法本身的一部分。

