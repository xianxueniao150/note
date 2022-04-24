HTTP报文分为请求报文和响应报文两种

## 请求报文
HTTP请求报文由请求行（request line）、请求头部（header）、空行和请求数据四个部分组成。使用 CRLF 分隔

```sh
GET / HTTP/1.1
Host: developer.mozilla.org
Accept-Language: fr
```

```sh
POST /contact_form.php HTTP/1.1
Host: developer.mozilla.org
Content-Length: 64
Content-Type: application/x-www-form-urlencoded

name=Joe%20User&request=Send%20me%20one%20of%20your%20catalogue
```

1. 请求行
	- 请求方法
	- 请求目标 (request target)，格式因不同的 HTTP 方法而异。它可以是：
		- 一个绝对路径，末尾跟上一个 ' ? ' 和查询字符串。这是最常见的形式，称为 原始形式 (origin form)，被 GET，POST，HEAD 和 OPTIONS 方法所使用。
			POST / HTTP/1.1
			GET /background.png HTTP/1.0
			HEAD /test.html?query=alibaba HTTP/1.1
			OPTIONS /anypage.html HTTP/1.0
		- 一个完整的URL，被称为 绝对形式 (absolute form)，主要在使用 GET 方法连接到代理时使用。
			GET http://developer.mozilla.org/en-US/docs/Web/HTTP/Messages HTTP/1.1
		- 由域名和可选端口(以':'为前缀）组成的 URL 的 authority component，称为 authority form。 仅在使用 CONNECT 建立 HTTP 隧道时才使用。
			CONNECT developer.mozilla.org:80 HTTP/1.1
		- 星号形式 (asterisk form)，一个简单的星号('*')，配合 OPTIONS 方法使用，代表整个服务器。
			OPTIONS * HTTP/1.1
	- 使用的 HTTP 协议版本
2. 请求头部
3. 空行，请求头部后面的空行是必须的即使第四部分的请求数据为空，也必须有空行。
4. 最后一块是可选数据块，包含更多数据，主要被 POST 方法所使用。

## 响应报文
HTTP响应也由四个部分组成，分别是：状态行、消息报头、空行和响应正文。

```sh
HTTP/1.1 200 OK
Date: Sat, 09 Oct 2010 14:28:02 GMT
Server: Apache
Last-Modified: Tue, 01 Dec 2009 20:18:22 GMT
ETag: "51142bc1-7449-479b075b2891b"
Accept-Ranges: bytes
Content-Length: 29769
Content-Type: text/html

<!DOCTYPE html... (这里是 29769 字节的网页HTML源代码)
```

1. 状态行，包括使用的 HTTP 协议版本，状态码和一个状态描述（可读描述文本）。
2. 接下来每一行都表示一个 HTTP 首部，与客户端请求的头部块类似
3. 空行，消息报头后面的空行是必须的。
4. 响应正文，包含了响应的数据 （如果有的话）。

请求资源已被永久移动的网页响应：
```sh
HTTP/1.1 301 Moved Permanently
Server: Apache/2.2.3 (Red Hat)
Content-Type: text/html; charset=iso-8859-1
Date: Sat, 09 Oct 2010 14:30:24 GMT
Location: https://developer.mozilla.org/ (目标资源的新地址, 服务器期望用户代理去访问它)
Keep-Alive: timeout=15, max=98
Accept-Ranges: bytes
Via: Moz-Cache-zlb05
Connection: Keep-Alive
X-Cache-Info: caching
X-Cache-Info: caching
Content-Length: 325 (如果用户代理无法转到新地址，就显示一个默认页面)

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>301 Moved Permanently</title>
</head><body>
<h1>Moved Permanently</h1>
<p>The document has moved <a href="https://developer.mozilla.org/">here</a>.</p>
<hr>
<address>Apache/2.2.3 (Red Hat) Server at developer.mozilla.org Port 80</address>
</body></html>
```



?
