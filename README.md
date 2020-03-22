# t-state
Linux服务器状态监控工具

## 显示项目含义
- Recv-Q : 网络接收队列,表示收到的数据已经在本地接收缓冲，但是还有多少没有被进程取走，recv(); 如果接收队列Recv-Q一直处于阻塞状态，可能是遭受了拒绝服务 denial-of-service 攻击。
- Send-Q : 对方没有收到的数据或者说没有Ack的,还是本地缓冲区. 如果发送队列Send-Q不能很快的清零，可能是有应用向外发送数据包过快，或者是对方接收数据包不够快。这两个值通常应该为0，如果不为0可能是有问题的。packets在两个队列里都不应该有堆积状态。可接受短暂的非0情况。从步骤一的结果中可以看到22端口对应的链路的 send-Q中堆积了大量的数据包 ,可以判定是发送数据给目的地址的时候出现了阻塞的问题，导致了包堆积在本地缓存中，不能成功发出去。

## TCP 状态
- LISTEN 首先服务端需要打开一个socket进行监听，状态为LISTEN
- SYN_SENT 客户端通过应用程序调用connect进行active open.于是客户端tcp发送一个SYN以请求建立一个连接.之后状态置为SYN_SENT
- SYN_RECV 服务端应发出ACK确认客户端的 SYN,同时自己向客户端发送一个SYN. 之后状态置为SYN_RECV
- ESTABLISHED 代表一个打开的连接，双方可以进行或已经在数据交互了
- FIN_WAIT1 主动关闭(active close)端应用程序调用close，于是其TCP发出FIN请求主动关闭连接，之后进入FIN_WAIT1状态
- CLOSE_WAIT 被动关闭(passive close)端TCP接到FIN后，就发出ACK以回应FIN请求(它的接收也作为文件结束符传递给上层应用程序),并进入CLOSE_WAIT
- FIN_WAIT2 主动关闭端接到ACK后，就进入了 FIN-WAIT-2 
- LAST_ACK 被动关闭端一段时间后，接收到文件结束符的应用程 序将调用CLOSE关闭连接。这导致它的TCP也发送一个 FIN,等待对方的ACK.就进入了LAST-ACK
- TIME_WAIT 在主动关闭端接收到FIN后，TCP 就发送ACK包，并进入TIME-WAIT状态
- CLOSING Both sockets are shut down but we still don’t have all our data sent. 等待远程TCP对连接中断的确认
- CLOSED 被动关闭端在接受到ACK包后，就进入了closed的状态。连接结束
