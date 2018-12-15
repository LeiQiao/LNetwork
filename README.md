# LNetwork

局域网流量监控 （ 基于 Parasite ）

基于电信天翼智能网管，定时统计当前局域网的设备流量

## API
### GET /lnetwork/device

获取所有设备信息，包括设备的名称、 IP、当前流量、日流量、月流量等信息

### PUT /lnetwork/device 

设置设备信息，设置设备的名称、类型及描述

### /lnetwork/summary

获取设备的统计信息：当前流量、日流量、月流量
