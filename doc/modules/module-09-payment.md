# 模块9：支付系统 💳

> 微信支付接入

## 支付场景

| 场景 | 说明 |
|------|------|
| 会员升级 | 审核通过后支付，激活全部功能 |
| 空间预约 | 预约锁定后支付 |
| 未来拓展 | 其他付费服务 |

## 技术实现

- 微信支付JSAPI（小程序内支付）
- 统一支付单号管理
- 支付结果异步通知处理

## 相关API

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/payments/membership | 会员升级支付 |
| POST | /api/payments/space-booking | 空间预约支付 |
| GET | /api/payments/{id} | 查询支付状态 |
| POST | /api/payments/notify | 微信支付回调 |
