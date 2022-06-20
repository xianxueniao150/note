## Frame的基础结构
```sh
+-----------------------------------------------+
|                 Length (24)                   |
+---------------+---------------+---------------+
|   Type (8)    |   Flags (8)   |
+-+-------------+---------------+-------------------------------+
|R|                 Stream Identifier (31)                      |
+=+=============================================================+
|                   Frame Payload (0...)                      ...
+--------------------------------------------------------------+
```

- Length: 表示Frame Payload的大小，是一个24-bit的整型，表明Frame Payload的大小不应该超过2^24-1字节，但其实payload默认的大小是不超过2^14字节，可以通过SETTING Frame来设置SETTINGS_MAX_FRAME_SIZE修改允许的Payload大小。
- Type: 表示Frame的类型,目前定义了0-9共10种类型。
- Flags: 为一些特定类型的Frame预留的标志位，比如Header, Data, Setting, Ping等，都会用到。
- R: 1-bit的保留位，目前没用，值必须为0
- Stream Identifier: Steam的id标识，表明id的范围只能为0到2^31-1之间，其中0用来传输控制信息，比如Setting, Ping；客户端发起的Stream id 必须为奇数，服务端发起的Stream id必须为偶数；并且每次建立新Stream的时候，id必须比上一次的建立的Stream的id大；当在一个连接里，如果无限建立Stream，最后id大于2^31时，必须从新建立TCP连接，来发送请求。如果是服务端的Stream id超过上限，需要对客户端发送一个GOWAY的Frame来强制客户端重新发起连接。如果是客户端的Stream id超过上限，客户端会新建一条连接。


DATA Frame
DATA Frame(type=0x0)，用来传输可变长度的二进制流，这部分最主要的用途就是用来传递之前HTTP/1中的Request或Response的Body部分。
DATA Frame 的 Payload格式如下：
 +---------------+
 |Pad Length? (8)|
 +---------------+-----------------------------------------------+
 |                            Data (*)                         ...
 +---------------------------------------------------------------+
 |                           Padding (*)                       ...
 +---------------------------------------------------------------+


DATA字段比较好解释，就是要传输的数据内容，那么Pad Length和Padding是干什么用的？HTTP/2在设计的时候就更多的考虑了数据的安全性，所以默认使用HTTPS，除此之外，协议本身也对传输的数据做了一些安全考虑，填充就是其中一个。填充可以模糊帧的大小，使攻击者更难通过帧的数量来猜测传输内容的长度，减少破解的可能性。
DATA帧使用到了Flag字段，其中最重要的是一个END_STREAM (0x1)Flag，这个标志用来表示Data Frame的传输是否结束，当该标志位为1时，表示Stream的传输结束，发起Stream的一方会进入half-closed(local)或者closed状态。END_STREAM在Header帧中也有用到，含义一样，不再单独说明。

HEADERS Frame
HEADERS Frame(type=0x1)用于开启一个Stream，当然也用于传输正常HTTP请求中的Header信息。
 +---------------+
 |Pad Length? (8)|
 +-+-------------+-----------------------------------------------+
 |E|                 Stream Dependency? (31)                     |
 +-+-------------+-----------------------------------------------+
 |  Weight? (8)  |
 +-+-------------+-----------------------------------------------+
 |                   Header Block Fragment (*)                 ...
 +---------------------------------------------------------------+
 |                           Padding (*)                       ...
 +---------------------------------------------------------------+


HEADERS的结构比较简单，Header Block Fragment字段用于存储正常的Http Header头信息，E、Stream Dependency、Weight字段都是用于权重控制。由于HTTP/2是支持多路复用，也就是多个流同时进行传输，那么这个时候哪个流更重要，应该优先传输哪个，就需要用这些字段来进行控制了。


PRIORITY Frame(type=0x2)用于指定Stream的优先级

RST_STREAM Frame(type=0x3)用于立即终止Stream


SETTINGS Frame
SETTINGS Frame(type=0x4)用来控制客户端和服务端之间通信的一些配置。SETTINGS帧必须在连接开始时由通信双方发送，并且可以在任何其他时间由任一端点在连接的生命周期内发送。SETTINGS帧必须在id为0的stream上进行发送，不能通过其他stream发送；SETTINGS影响的是整个TCP链接，而不是某个stream；在SETTINGS设置出现错误时，必须当做connection error重置整个链接。SETTINGS帧带有Ack的Flag，接收方必须收到ack为0的SETTINGS后，应马上启用SETTING的配置并返回一个Ack为1的SETTINGS帧。

常用的SETTINGS有几类：
SETTINGS_HEADER_TABLE_SIZE (0x1): 控制每个Header帧中的HTTP头信息的大小
SETTINGS_ENABLE_PUSH (0x2): 是否启用服务端推送(Server Push)，默认开启；不管是服务端还是客户端发送了禁用的配置，那么服务端就不应该发送PUSH_PROMISE帧
SETTINGS_MAX_CONCURRENT_STREAMS (0x3): 用来控制多路复用中Stream并发的数量，这个主要是用来限制单个链接对服务端的资源的占用过大，这个值默认是没有限制，如果做一个server服务，那么建议一定要设置这个值，RFC文档中建议不要小于100，那么我们设置100就可以了。

PUSH_PROMISE
PUSH_PROMISE Frame(type=0x5)用于服务端在发送PUSH之前先发送PUSH_PROMISE帧来通知客户端将要发送的PUSH信息。
PUSH_PROMISE中，包含了一个Promised Stream ID，这个是服务端承诺向客户端推送相关数据时使用的Stream ID，Header Block中包含资源链接等相关内容。
客户端收到PUSH_PROMISE后，可以选择接受服务器推送的资源，如果客户端发现本地缓存已经存在，不需要服务端再推送，也可以向对应的Stream ID发送RST_STREAM帧，来阻止服务端发送Push.
PUSH_PROMISE涉及到server push的相关信息。
+---------------+
 |Pad Length? (8)|
 +-+-------------+-----------------------------------------------+
 |R|                  Promised Stream ID (31)                    |
 +-+-----------------------------+-------------------------------+
 |                   Header Block Fragment (*)                 ...
 +---------------------------------------------------------------+
 |                           Padding (*)                       ...
 +---------------------------------------------------------------+


PING Frame
PING Frame(type=0x6) 是用来测量来自发送方的最小往返时间以及确定空闲连接是否仍然起作用的机制。 PING帧可以从任何一方发送。PING帧跟SETTINGS帧非常类似，一个是必须在id为0的stream上发送，另一个就是它也包含一个Ack的Flag，发送方发送ack=0的PING帧，接收方必须响应一个ack=1的PING帧，并且PING帧的响应 应该 优先于任何其他帧。

GOAWAY frame
GOAWAY frame(type=0x7)用于关闭连接，GOAWAY允许端点优雅地停止接受新流，同时仍然完成先前建立的流的处理。
 +-+-------------------------------------------------------------+
 |R|                  Last-Stream-ID (31)                        |
 +-+-------------------------------------------------------------+
 |                      Error Code (32)                          |
 +---------------------------------------------------------------+
 |                  Additional Debug Data (*)                    |
 +---------------------------------------------------------------+

WINDOW_UPDATE frame(type=0x8)用于流控

CONTINUATION frame(type=0x9)用于持续的发送未发送完的HTTP header信息.如果前边是这三个帧(HEADERS, PUSH_PROMISE, or CONTINUATION)，并且未携带END_HEADERS的flag，就可以继续发送CONTINUATION帧。

## Priority
因为一条连接允许多个 streams 在上面发送 frame，那么在一些场景下面，我们还是希望 stream 有优先级，方便对端为不同的请求分配不同的资源。譬如对于一个 Web 站点来说，优先加载重要的资源，而对于一些不那么重要的图片啥的，则使用低的优先级。

我们还可以设置 Stream Dependencies，形成一棵 streams priority tree。假设 Stream A 是 parent，Stream B 和 C 都是它的孩子，B 的 weight 是 4，C 的 weight 是 12，假设现在 A 能分配到所有的资源，那么后面 B 能分配到的资源只有 C 的 1/3。

## flow control
HTTP/2 也支持流控，如果 sender 端发送数据太快，receiver 端可能因为太忙，或者压力太大，或者只想给特定的 stream 分配资源，receiver 端就可能不想处理这些数据。譬如，如果 client 给 server 请求了一个视频，但这时候用户暂停观看了，client 就可能告诉 server 别在发送数据了。

虽然 TCP 也有 flow control，但它仅仅只对一个连接有效果。HTTP/2 在一条连接上面会有多个 streams，有时候，我们仅仅只想对一些 stream 进行控制，所以 HTTP/2 单独提供了流控机制。Flow control 有如下特性：
- Flow control 是单向的。Receiver 可以选择给 stream 或者整个连接设置 window size。
- Flow control 是基于信任的。Receiver 只是会给 sender 建议它的初始连接和 stream 的 flow control window size。
- Flow control 是 hop-by-hop，并不是 end-to-end 的，也就是我们可以用一个中间人来进行 flow control。
这里需要注意，HTTP/2 默认的 window size 是 64 KB。

在 http2 中，每个 http stream 都有自己公示的流量窗口，对于每个 stream 来说，client 和 server 都必须互相告诉对方自己能够处理的窗口大小，stream 中的数据帧大小不得超过能处理的窗口值。

## Stream 状态机
这个状态图从客户端和服务端两方面分别来展示的，大家可以先自己看下，图下方有发送标记的解释：
```sh
                            +--------+
                     send PP |        | recv PP
                    ,--------|  idle  |--------.
                   /         |        |         \
                  v          +--------+          v
           +----------+          |           +----------+
           |          |          | send H /  |          |
    ,------| reserved |          | recv H    | reserved |------.
    |      | (local)  |          |           | (remote) |      |
    |      +----------+          v           +----------+      |
    |          |             +--------+             |          |
    |          |     recv ES |        | send ES     |          |
    |   send H |     ,-------|  open  |-------.     | recv H   |
    |          |    /        |        |        \    |          |
    |          v   v         +--------+         v   v          |
    |      +----------+          |           +----------+      |
    |      |   half   |          |           |   half   |      |
    |      |  closed  |          | send R /  |  closed  |      |
    |      | (remote) |          | recv R    | (local)  |      |
    |      +----------+          |           +----------+      |
    |           |                |                 |           |
    |           | send ES /      |       recv ES / |           |
    |           | send R /       v        send R / |           |
    |           | recv R     +--------+   recv R   |           |
    | send R /  `----------->|        |<-----------'  send R / |
    | recv R                 | closed |               recv R   |
    `----------------------->|        |<----------------------'
                             +--------+
       send:   endpoint sends this frame
       recv:   endpoint receives this frame
       H:  HEADERS frame (with implied CONTINUATIONs)
       PP: PUSH_PROMISE frame (with implied CONTINUATIONs)
       ES: END_STREAM flag
       R:  RST_STREAM frame
```

其中,half closed状态，就是进入Server Push后的状态，有一方，其实就是客户端，进入了半开闭状态，这时候它不能通过这个Stream再发送请求的相关数据，只能接受数据，或者选择结束链接。half closed状态可以由idle状态经过两条路径到达:
服务端发送PUSH_PROMISE后发送Header帧信息，使客户端进入半开闭；
客户端通过Header帧向服务端发送数据，并在Header标记END_STREAM的Flag,表明自己期望结束Stream，不再向服务端发送Header或Data的数据，这个时候服务端还没同意关闭Stream，所以服务端是可以向客户端发送数据的。
这里边比较奇怪的就是reserved和half closed两个状态，看起来没有什么区别，通过一个无关紧要的Header帧来触发状态转换。
其实，在Go语言里，对HTTP/2的Stream State的实现，就是把reserved和half closed当做一个状态给合并了。

那么为什么会有这两个状态呢，其实是出于Stream Concurrency并发的限制，在并发限制里，reserved状态不计入活跃状态，不进行限制。这样能达到的一个效果就是，即使Stream并发数达到限制以后，服务端仍然是能向客户端发送PUSH_PROMISE的，能够一定程度的防止PUSH_PROMISE不能发送而导致的客户端竞争请求。


