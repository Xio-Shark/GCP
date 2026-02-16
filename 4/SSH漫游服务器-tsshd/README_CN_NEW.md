# tsshd - 支持漫游连接迁移的 tssh UDP 服务器

trzsz-ssh (tssh) 配合 tsshd 支持间歇性连接，允许漫游，可用于蜂窝数据连接、不稳定 Wi-Fi 等高延迟链路。

它旨在提供与 openssh 的完全兼容性，镜像其所有功能，同时提供 openssh 客户端中没有的额外有用功能：

- 当客户端休眠后唤醒，或暂时失去连接时，保持会话存活。
- 允许客户端"漫游"并更改 IP 地址，在任意网络间切换，同时保持连接。

## 对比

tsshd 灵感来自 [mosh](https://github.com/mobile-shell/mosh)，`tsshd` 的工作方式类似 `mosh-server`，而 `tssh --udp` 的工作方式类似 `mosh`。

| 功能 | mosh (mosh-server) | tssh (tsshd) |
|------|-------------------|--------------|
| 低延迟 | ? | ✅ [KCP](https://github.com/xtaci/kcp-go) |
| 保持连接 | ✅ | ✅ |
| 客户端漫游 | ✅ | ✅ |
| 本地回显和行编辑 | ✅ | 不计划支持 |
| 多平台/Windows | [mosh#293](https://github.com/mobile-shell/mosh/issues/293) | ✅ |
| SSH X11 转发 | [mosh#41](https://github.com/mobile-shell/mosh/issues/41) | ✅ |
| SSH Agent 转发 | [mosh#120](https://github.com/mobile-shell/mosh/issues/120) | ✅ |
| SSH 端口转发 | [mosh#337](https://github.com/mobile-shell/mosh/issues/337) | ✅ |
| 输出滚动缓冲 | [mosh#122](https://github.com/mobile-shell/mosh/issues/122) | ✅ |
| OSC52 序列 | [mosh#637](https://github.com/mobile-shell/mosh/issues/637) | ✅ |
| ProxyJump | [mosh#970](https://github.com/mobile-shell/mosh/issues/970) | ✅ |
| tmux -CC 集成 | [mosh#1078](https://github.com/mobile-shell/mosh/issues/1078) | ✅ |

tssh 和 tsshd 的工作方式与 ssh 完全相同，不计划支持本地回显和行编辑，也不会有 mosh 的问题。

## 使用方法

1. 在客户端（本地机器）安装 [tssh](https://github.com/trzsz/trzsz-ssh?tab=readme-ov-file#installation)。
2. 在服务器（远程主机）安装 [tsshd](https://github.com/trzsz/tsshd?tab=readme-ov-file#installation)。
3. 使用 `tssh --udp xxx` 登录（延迟敏感用户可指定 `--kcp` 选项）。或在 `~/.ssh/config` 中配置如下以省略 `--udp` 或 `--kcp` 选项：

```
Host xxx
    #!! UdpMode Yes/QUIC/KCP
```

## 工作原理

- `tssh` 在客户端扮演 `ssh` 的角色，`tsshd` 在服务器端扮演 `sshd` 的角色。
- `tssh` 首先作为 ssh 客户端正常登录服务器，然后在服务器上运行新的 `tsshd` 进程。
- `tsshd` 进程监听 61001 到 61999 之间的随机 UDP 端口（可通过 `TsshdPort` 自定义），并通过 ssh 通道将其端口号和一些密钥发送回 `tssh` 进程。然后关闭 ssh 连接，`tssh` 进程通过 UDP 与 `tsshd` 进程通信。

## 重连机制

```
┌───────────────────────┐                ┌───────────────────────┐
│                       │                │                       │
│    tssh (process)     │                │    tsshd (process)    │
│                       │                │                       │
│ ┌───────────────────┐ │                │ ┌───────────────────┐ │
│ │                   │ │                │ │                   │ │
│ │  KCP/QUIC Client  │ │                │ │  KCP/QUIC Server  │ │
│ │                   │ │                │ │                   │ │
│ └───────┬───▲───────┘ │                │ └───────┬───▲───────┘ │
│         │   │         │                │         │   │         │
│         │   │         │                │         │   │         │
│ ┌───────▼───┴───────┐ │                │ ┌───────▼───┴───────┐ │
│ │                   ├─┼────────────────┼─►                   │ │
│ │   Client  Proxy   │ │                │ │   Server  Proxy   │ │
│ │                   ◄─┼────────────────┼─┤                   │ │
│ └───────────────────┘ │                │ └───────────────────┘ │
└───────────────────────┘                └───────────────────────┘
```

- 客户端 `KCP/QUIC Client` 和 `Client Proxy` 在同一台机器上且在同一进程中，它们之间的连接不会被中断。
- 服务器 `KCP/QUIC Server` 和 `Server Proxy` 在同一台机器上且在同一进程中，它们之间的连接不会被中断。
- 如果客户端一段时间内没有收到服务器的心跳，可能是因为网络变化导致原连接中断。此时，`Client Proxy` 将重新建立到 `Server Proxy` 的连接，认证成功后通过新连接进行通信。从 `KCP/QUIC Client` 和 `KCP/QUIC Server` 的角度看，连接从未中断。

## 安全性

- `KCP/QUIC Server` 仅监听 localhost 127.0.0.1，且只接受一个连接。一旦同一进程中的 `Server Proxy` 成功连接，所有其他连接将被拒绝。
- `Client Proxy` 仅监听 localhost 127.0.0.1，且只接受一个连接。一旦同一进程中的 `KCP/QUIC Client` 成功连接，所有其他连接将被拒绝。
- `Server Proxy` 仅转发来自唯一且已认证的 `Client Proxy` 的数据包。
- 所有认证消息使用 AES-GCM-256 算法加密，密钥由服务器随机生成并通过 SSH 隧道发送给客户端。

## 配置

```
Host xxx
    #!! UdpMode Yes
    #!! TsshdPort 61001-61999
    #!! TsshdPath ~/go/bin/tsshd
    #!! UdpAliveTimeout 86400
    #!! UdpHeartbeatTimeout 3
    #!! UdpReconnectTimeout 15
    #!! ShowNotificationOnTop yes
    #!! ShowFullNotifications yes
    #!! UdpProxyMode UDP
```

- `UdpMode`：`No`（默认，tssh 在 TCP 模式下工作）、`Yes`（默认协议：QUIC）、`QUIC`（更快速度）、`KCP`（更低延迟）。
- `TsshdPort`：指定 tsshd 监听的端口范围，默认 [61001, 61999]。
- `TsshdPath`：指定服务器上 tsshd 二进制文件的路径。
- `UdpAliveTimeout`：断开超过此秒数后，tssh 和 tsshd 都将退出。默认 86400 秒。
- `UdpHeartbeatTimeout`：断开超过此秒数后，tssh 将尝试重新连接。默认 3 秒。
- `UdpReconnectTimeout`：断开超过此秒数后，tssh 将显示连接丢失通知。默认 15 秒。

## 安装

### 使用 apt 在 Ubuntu 安装

```sh
sudo apt update && sudo apt install software-properties-common
sudo add-apt-repository ppa:trzsz/ppa && sudo apt update
sudo apt install tsshd
```

### 使用 Go 安装（需要 Go 1.25 或更高版本）

```sh
go install github.com/trzsz/tsshd/cmd/tsshd@latest
```

二进制文件通常位于 ~/go/bin/（Windows 上为 C:\Users\your_name\go\bin\）。

### 从源码构建

```sh
git clone --depth 1 https://github.com/trzsz/tsshd.git
cd tsshd
make
sudo make install
```

## 联系方式

欢迎邮件联系作者 <lonnywong@qq.com>，或创建 [issue](https://github.com/trzsz/tsshd/issues)。欢迎加入 QQ 群：318578930。
