---
categories:
- 技术
- 前端
date: 2018-07-11 15:18:38+08:00
tags:
- react
thumbnailImage: //www.azheimage.top/markdown-img-paste-20180725100954649.png
title: react学习
---
React 是一个用于构建用户界面的 JAVASCRIPT 库。
React主要用于构建UI，很多人认为 React 是 MVC 中的 V（视图）。
React 起源于 Facebook 的内部项目，用来架设 Instagram 的网站，并于 2013 年 5 月开源。
React 拥有较高的性能，代码逻辑非常简单，越来越多的人已开始关注和使用它。
<!--more-->
## React Logo：
图标跟atom有点像😄
![react Logo](https://www.azheimage.top/markdown-img-paste-20180711143141965.png)

* ## React 特点：
##### 1. 声明式设计 −React采用声明范式，可以轻松描述应用。
##### 2. 高效 −React通过对DOM的模拟，最大限度地减少与DOM的交互。
##### 3. 灵活 −React可以与已知的库或框架很好地配合。
##### 4. JSX − JSX 是 JavaScript 语法的扩展。React 开发不一定使用 JSX ，但我们建议使用它。
##### 5. 组件 − 通过 React 构建组件，使得代码更加容易得到复用，能够很好的应用在大项目的开发中。
##### 6. 单向响应的数据流 − React 实现了单向响应的数据流，从而减少了重复代码，这也是它为什么比传统数据绑定更简单。

* ## 搭建react开发环境：
##### 1. 安装官方脚手架：
> `npm install -g create-react-app`
> ![](https://www.azheimage.top/markdown-img-paste-20180711143829630.png)
##### 2. 创建工程
> `create-react-app my-app`
>![](https://www.azheimage.top/markdown-img-paste-20180711144312387.png)
##### 3. 进入工程目录，启动
> `cd my-app`
> `npm start`
> ![](https://www.azheimage.top/markdown-img-paste-20180711144442932.png)
##### 4. 启动之后，浏览器会自动打开`http://localhost:3000/`
> ![](https://www.azheimage.top/markdown-img-paste-20180711144621644.png)

* ## JSX基本语法
##### 1. XML基本语法
  定义标签时，只允许被一个标签包裹，标签一定要闭合
```html
const List=()=>(
  <div>
    <Title>this is title</Title>
    <ul>
      <li>list item</li>
      <li>list item</li>
      <li>list item</li>
    </ul>
  </div>
);
```
#### 2. 元素类型
* 小写字母对应DOM元素
* 大写首字母对应组件元素自然
* 注释使用js注释方法
#### 3. 元素属性
* class属性改为className
* for属性改为htmlFor
* Boolean属性：省略Boolean属性值会导致JSX认为默认为true
#### 4. JavaScript属性表达式
属性值要使用表达式，只要{}替换“”即可`<input type="text" value={val ? val:""/}`
#### 5. HTML转义
* react会将所有要显示到DOM的字符串转义，防止XSS。
* 后台传过来的数据带页面标签是的是不能直接转移的，具体转义的写法如下：
```
var content='<strong>content</strong>';
React.render(
  <div dangerouslySetInnerHTML={{__html:content}}</div>,document.body
);
```
#### 6. ReactDOM.render
* 作用：描画dom
* 参数1：dom对象
* 参数2：注入点
```
ReactDOM.render(
  <div>Hello World!</div>,
  document.querySelect("#wrapper")
);
```
#### 7. 组件的声明（ES5）：
```
var Hello=React.createClass({
  render:function(){
    return(
      <div>Hello World!</div>
      )
  }
  });
```
#### 8. 组件的声明（ES6）
```
class Hello extends React.Compoent{
  render(){
    return(
      <div>Hello World!</div>
      )
  }
};
```
